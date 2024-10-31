import time


def send_sms():
    print("Sending SMS2...")  # Placeholder for actual SMS sending logic


if __name__ == "__main__":
    try:
        while True:
            send_sms()
            time.sleep(5)  # Wait for 5 seconds before sending the next SMS
    except KeyboardInterrupt:
        print("SMS sending stopped.")

