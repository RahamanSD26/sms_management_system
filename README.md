Dynamic SMS Management Web Application

This project is a web-based dashboard to dynamically manage and monitor an SMS system running on a Linux server. It includes a FastAPI backend, a React frontend, and uses MongoDB and data storage. The system is designed to trigger, monitor, and manage SMS messages sent across multiple country-telecom pairs with real-time performance metrics.

## Prerequisites

- Python 3.8+
- FastAPI
- MongoDB

## Setup

### Clone the repository

```bash
git clone git@github.com:RahamanSD26/sms_management_system.git
cd sms_management_system
```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   python init_db.py
   ```

### Frontend Setup

## Running the Application

### Start the Backend

1. Navigate to the backend directory if not already there:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Start the backend API:
   ```bash
   uvicorn main:app --reload
   ```

### Start the Frontend
Just run the app you will be redirect to login page

## Accessing the Application

Access the application at [http://localhost:5173](http://localhost:7000) (or the port specified by Vite).

## Features

- **User Authentication**: Secure login using JWT-based authentication.
- **Real-Time SMS Program Management**: Start, stop, or restart SMS programs and monitor status per country-operator pair.
- **SMS Metrics Visualization**: View real-time metrics and success rates.
- **Monitoring and Alerts**: Integrated with Prometheus and Grafana for monitoring, with alerts for critical events via Telegram.

## Contributing

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on the code of conduct and submission guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

--- 

This README provides clear guidance for setting up, running, and accessing your application, along with listing the core features and prerequisites.
