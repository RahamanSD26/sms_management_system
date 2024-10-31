import os
import subprocess
import multiprocessing
import sys
from collections import defaultdict

from fastapi import APIRouter, HTTPException
import datetime
import time

process_manager_app = APIRouter()


# Dictionary to store session names and their corresponding PIDs
running_sessions = {}

metrics = defaultdict(lambda: {
    "total_sms_sent": 0,
    "successful_sms": 0,
    "failed_sms": 0,
    "rate_limit_exceeded": 0
})

# Dictionary to track SMS send counts for rate limiting per country_operator
rate_limits = defaultdict(lambda: {
    "count": 0,
    "last_reset": datetime.datetime.now()
})


def start_process(session_name, program_name, country_operator):
    program_path = os.path.join("./TestingPrograms", f"{program_name}.py")  # Improved path handling
    if not os.path.exists(program_path):
        raise ValueError(f"Program not found: {program_path}")

    command = ["python", program_path]
    process = multiprocessing.Process(target=run_command, args=(command,))
    running_sessions[session_name] = process
    process.start()
    send_sms(country_operator, f"Test Message for {country_operator}")


def run_command(command):
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())  # Handle stdout output

        for line in iter(process.stderr.readline, b''):
            print(line.decode().strip(), file=sys.stderr)  # Handle stderr output

        process.wait()  # Wait for the process to finish


def kill_process(pid, session_name):
    try:
        process = subprocess.Popen(['kill', str(pid)])
        process.wait()
        if process.returncode == 0:
            print(f"Process with PID {pid} terminated successfully.")
            del running_sessions[session_name]
        else:
            print(f"Error terminating process with PID {pid}.")
    except Exception as e:
        print(f"Error: {str(e)}")


def stop_process(session_name):
    if session_name in running_sessions:
        process = running_sessions[session_name]
        process.terminate()  # Send SIGTERM signal
        process.join()  # Wait for the process to terminate
        print(f"Process {session_name} stopped.")
        return {"status": f"{session_name} stopped successfully with pid= {process.pid}"}
    else:
        print(f"Process {session_name} not found.")
        return {"error": "error occurred"}


def restart_process(session_name):
    if session_name in running_sessions:
        # stop_process(session_name)
        start_process(session_name, *session_name.split("_"))  # Unpack session_name
    else:
        print(f"Process {session_name} not found.")


def check_rate_limit(country_operator):
    now = datetime.datetime.now()

    # Initialize rate limit data if not present
    if country_operator not in rate_limits:
        rate_limits[country_operator] = {"count": 0, "last_reset": now}

    # Check if a minute has passed since last reset
    if now - rate_limits[country_operator]["last_reset"] >= datetime.timedelta(minutes=1):
        # Reset the rate limit count and timestamp
        rate_limits[country_operator]["count"] = 0
        rate_limits[country_operator]["last_reset"] = now

    # If count has reached the limit of 10, block SMS and mark as rate-limited
    if rate_limits[country_operator]["count"] >= 10:
        return False

    # Increment the count if below the rate limit and allow SMS to proceed
    rate_limits[country_operator]["count"] += 1
    return True


def send_sms(country_operator, message):
    # Simulate continuous sending for a period
    for i in range(30):  # Attempt to send SMS multiple times
        # Check if we can send a new SMS based on the rate limit
        if check_rate_limit(country_operator):
            try:
                # Simulate sending the SMS
                success = True  # Change this based on actual sending logic
                print(f"SMS sent: {message}")
                metrics[country_operator]["total_sms_sent"] += 1
                metrics[country_operator]["successful_sms"] += 1
            except Exception as e:
                success = False
                print(f"Error sending SMS: {str(e)}")
                metrics[country_operator]["failed_sms"] += 1
        else:
            metrics[country_operator]["rate_limit_exceeded"] += 1
            print(f"Rate limit exceeded for {country_operator}")

        # Wait for a short duration before attempting to send the next SMS
        time.sleep(2)  # Adjust as needed for testing

    # Wait a minute before checking rate limits again
    print("Waiting for the rate limit to reset...")
    time.sleep(60)  # Simulate waiting for the rate limit to reset


@process_manager_app.post("/start/{session_name}")
async def start_session(session_name: str):
    try:
        parts = session_name.split("_")
        if len(parts) != 2:
            raise ValueError("Invalid session name format")
        program_name, country_operator = parts[:2]
        start_process(session_name, program_name, country_operator)
        return {"status": "started", "session_name": session_name, "pid": running_sessions[session_name].pid}
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@process_manager_app.get("/metrics/{country_operator}")
async def get_metrics(country_operator: str):
    """Retrieve real-time metrics for a specific country/operator."""
    if country_operator not in metrics:
        return {"message": "Country operator not found"}
    return metrics[country_operator]
