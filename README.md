Dynamic SMS Management Web Application
This project is a Full Stack SMS Management System developed as part of a Full Stack Developer Internship Assignment. 
The application provides a dashboard for managing and monitoring SMS traffic across multiple country-operator pairs on a Linux server. 
The system dynamically handles SMS delivery through independent Python programs, ensuring high-priority handling and real-time monitoring with alerts.

Table of Contents:

Project Overview
Features
Tech Stack
Architecture
Installation and Setup
Usage
Project Structure
Contributing
License

Project Overview
The application manages SMS traffic by running multiple Python programs via screen sessions, each handling a specific country-operator pair. The dashboard allows for:

Real-time monitoring of SMS delivery and success rates
Management of program sessions (start/stop/restart)
CRUD operations for country-operator pairs
Automated alerts for critical failures or low success rates
Features
Backend API

Manage screen sessions for individual programs
Retrieve real-time SMS metrics and success rates
Rate limiting to ensure 10 SMS/minute per country
Dynamic CRUD operations for country-operator pairs with prioritization
JWT-based authentication for secure access
Alert notifications via Telegram for critical events
Frontend Dashboard

Real-time display of SMS metrics (charts, tables)
Control over SMS programs (start, stop, restart)
Country-operator management with high-priority flags
Secure login with JWT-based authentication
Database Management

MongoDB for program configurations and dynamic updates
MySQL for SMS metrics and performance trend analysis
Monitoring and Alerts

Prometheus and Grafana for metrics monitoring and visualization
Prometheus AlertManager for critical alerts (success rate drops, program crashes)
Tech Stack
Frontend: ReactJS
Backend: FastAPI
Database: MongoDB, MySQL
Monitoring: Prometheus, Grafana
Authentication: JWT
Containerization (optional): Docker
Messaging: Telegram bot for alerts
Architecture
The application uses a microservices-inspired architecture, with backend APIs to manage SMS programs and a frontend for control and monitoring. Each service communicates through RESTful APIs, and Prometheus monitors system health. Refer to the Architecture Diagram for a high-level view of component interactions.

Installation and Setup
Prerequisites
Python 3.8+
Node.js & npm
MongoDB & MySQL
Prometheus & Grafana (for monitoring)
Docker (optional, for containerization)

Step-by-Step Setup
Clone the Repository
git clone https://github.com/RahamanSD26/sms_management_system
cd repository

Backend Setup

Install Python dependencies:
pip install -r backend/requirements.txt
Configure database connections for MongoDB and MySQL.

Set environment variables (e.g., ACCESS_TOKEN_SECRET, TELEGRAM_BOT_TOKEN).

Run FastAPI server:
uvicorn backend.main:app --reload

Frontend Setup

Navigate to the frontend directory:
cd frontend
Install dependencies and run the development server:
npm install
npm start

Prometheus and Grafana Setup

Configure Prometheus and Grafana to monitor the backend API endpoints.
Import the provided Grafana dashboards for SMS success rates and error tracking.
Usage
Login: Navigate to /login to access the dashboard (JWT-based authentication required).
Dashboard: View SMS metrics in real-time charts and tables.
Program Control: Start, stop, or restart individual SMS programs.
Country-Operator Management: Add, update, or prioritize country-operator pairs dynamically.

Contributing
Contributions are welcome! To contribute, please:

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-name).
Create a pull request.
