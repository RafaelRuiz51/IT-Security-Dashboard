# IT Security Dashboard

A Flask-based internal IT security monitoring portal built to simulate real enterprise security operations.

## Features
- Real-time security alert dashboard
- Brute force detection via log parsing
- Auto-generated help desk tickets from security events
- Active Directory locked account reporting
- User management panel
- Dockerfile included for containerization

## Tech Stack
- Python / Flask
- SQLite
- Bootstrap 5
- Docker

## Screenshots

### Dashboard
![Dashboard](screenshots/Dashboard.png)

### Log Parser Alert
![Log Parser](screenshots/logparseralert.png)

### Tickets
![Tickets](screenshots/ticketsdashboard.png)

## How To Run Locally

```bash
git clone https://github.com/YOURUSERNAME/IT-Security-Dashboard
cd IT-Security-Dashboard
python -m venv venv
venv\Scripts\activate
pip install flask
python app.py
```

Open http://localhost:5000

## How The Log Parser Works

```bash
python log_parser.py
```

Refresh the dashboard to see auto-generated alerts and tickets from parsed logs.

## What I Learned
- Flask routing and Jinja2 templating
- SQLite database design and queries
- Log parsing with regex
- Automated alerting and ticketing logic
- Docker containerization
