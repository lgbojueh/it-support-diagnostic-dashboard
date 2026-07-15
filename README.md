# IT Support Diagnostic Dashboard

A full-stack IT support dashboard for monitoring system resources, testing network connectivity, and identifying common technical issues through an interactive web interface.

## Overview

The IT Support Diagnostic Dashboard collects non-sensitive system information and presents it in a clear, responsive dashboard. It helps support technicians quickly review CPU, memory, disk, operating-system, and basic network information.

The project demonstrates Python backend development, REST API design, system diagnostics, frontend development, automated testing, and technical troubleshooting.

## Problem Solved

IT support professionals frequently need to gather system information before diagnosing performance and connectivity issues. Collecting this information manually can be repetitive.

This application provides one dashboard for:

- Monitoring CPU, memory, and disk usage
- Viewing device and operating-system information
- Testing basic internet connectivity
- Identifying resource warnings
- Generating a structured diagnostic summary

## Features

- Interactive system diagnostic dashboard
- CPU usage monitoring
- Memory usage monitoring
- Disk usage and available-space monitoring
- Operating-system and architecture information
- Hostname and local IP information
- Basic internet connectivity testing
- Warning thresholds for elevated resource usage
- Responsive frontend for desktop and mobile devices
- REST API endpoints for system and network information
- Automated backend tests with Pytest
- User-friendly API error responses

## Technology Stack

### Backend

- Python 3.12
- Flask
- psutil
- Python socket and platform modules

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Fetch API
- Responsive design

### Testing

- Pytest
- Flask test client

## Project Structure

```text
it-support-diagnostic-dashboard/
├── .github/
│   └── workflows/
│       └── tests.yml
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── app.py
├── LICENSE
├── pytest.ini
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.12 or newer
- Git
- A modern web browser

### 1. Clone the repository

```bash
git clone https://github.com/lgbojueh/it-support-diagnostic-dashboard.git
cd it-support-diagnostic-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Application

Start the Flask server:

```bash
python app.py
```

Open the interactive dashboard:

```text
http://127.0.0.1:5000
```

Select **Run Diagnostics** to collect and display the current system information.

Stop the server by pressing:

```text
Control + C
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the interactive dashboard |
| GET | `/api/health` | Returns API health and version information |
| GET | `/api/system` | Returns current system resource information |
| GET | `/api/network` | Returns hostname, local IP, and connectivity information |
| GET | `/api/diagnostics` | Returns the complete diagnostic summary |
| GET | Any unknown route | Returns a JSON 404 response |

### Example Health Response

```json
{
  "service": "IT Support Diagnostic Dashboard",
  "status": "healthy",
  "timestamp": "2026-07-15T19:44:45.906Z",
  "version": "1.0.0"
}
```

### Example Diagnostic Response

```json
{
  "generated_at": "2026-07-15T19:44:45.906Z",
  "system": {
    "operating_system": "Darwin",
    "architecture": "x86_64",
    "cpu_usage_percent": 18.4,
    "memory": {
      "total_gb": 16.0,
      "available_gb": 7.5,
      "used_percent": 53.1
    },
    "disk": {
      "total_gb": 460.43,
      "free_gb": 210.25,
      "used_percent": 54.3
    }
  },
  "network": {
    "hostname": "example-computer",
    "local_ip": "192.168.1.10",
    "internet_connected": true
  },
  "warnings": [
    {
      "level": "healthy",
      "message": "No immediate system issues were detected."
    }
  ]
}
```

Values in the response will vary by computer.

## Run the Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The tests verify:

- The health endpoint
- The interactive home page
- The complete diagnostics endpoint

To check test discovery without executing the tests:

```bash
python -m pytest --collect-only -q
```

## Diagnostic Thresholds

The application generates warnings using these thresholds:

| Resource | Warning | Critical |
|---|---:|---:|
| CPU usage | 75% or higher | 90% or higher |
| Memory usage | 75% or higher | 90% or higher |
| Disk usage | 80% or higher | 90% or higher |
| Internet connection | — | Connectivity test fails |

These warnings are intended to support initial troubleshooting. They are not a replacement for professional system monitoring or security software.

## Architecture

The frontend requests diagnostic information from the Flask REST API using the browser Fetch API.

```text
Browser Interface
       |
       | GET /api/diagnostics
       v
Flask REST API
       |
       ├── psutil system metrics
       ├── platform information
       └── socket network checks
       |
       v
JSON Diagnostic Response
       |
       v
Interactive Dashboard
```

## Privacy and Security

- The application does not require user accounts.
- It does not intentionally collect passwords or personal files.
- Diagnostic information is generated when the user runs the application.
- Environment files and generated reports are excluded from Git.
- The application should only be run on systems where the user has authorization.

Do not expose the development server directly to the public internet.

## Deployment Note

When the project runs locally, it reports information about the local computer.

When deployed to a cloud host, it reports information about the hosting server—not the website visitor’s computer. Web browsers do not allow websites to access a visitor’s CPU, memory, or disk information directly for security reasons.

## Challenges and Solutions

### Collecting system information safely

The application uses `psutil`, `platform`, and `socket` to collect useful diagnostic information without reading personal documents or credentials.

### Presenting backend data in the browser

The frontend uses asynchronous Fetch API requests to retrieve JSON from Flask and update the dashboard without reloading the page.

### Handling diagnostic failures

The backend returns structured error responses, while the frontend displays a clear message if diagnostic information cannot be retrieved.

## Future Improvements

- User-selected ping tests
- DNS lookup tools
- TCP port connectivity checks
- Downloadable JSON and text reports
- Diagnostic history
- Log analysis
- Process monitoring
- Configurable alert thresholds
- Additional automated tests
- Docker support
- Production deployment configuration

## Author

**Lyoneh Gbojueh**

- GitHub: [github.com/lgbojueh](https://github.com/lgbojueh)
- LinkedIn: [Lyoneh Gbojueh](https://www.linkedin.com/in/lyoneh-gbojueh-988275255)
- Email: [lyonehgbojueh32@gmail.com](mailto:lyonehgbojueh32@gmail.com)

## License

This project is available under the [MIT License](LICENSE).