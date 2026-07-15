from datetime import datetime, timezone
import platform
import socket

import psutil
from flask import Flask, jsonify, render_template


app = Flask(__name__)


def bytes_to_gb(value):
    """Convert bytes to gigabytes."""
    return round(value / (1024 ** 3), 2)


def check_internet_connection():
    """
    Test basic outbound connectivity.

    This does not send user information or make an HTTP request.
    It only attempts to open a short TCP connection.
    """
    try:
        connection = socket.create_connection(
            ("1.1.1.1", 53),
            timeout=2
        )
        connection.close()
        return True
    except OSError:
        return False


def get_local_ip():
    """Attempt to determine the computer's local network address."""
    connection = None

    try:
        connection = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]
    except OSError:
        return "Unavailable"
    finally:
        if connection:
            connection.close()


def get_system_information():
    """Collect non-sensitive system resource information."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "operating_system": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unavailable",
        "python_version": platform.python_version(),
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=0.25),
        "memory": {
            "total_gb": bytes_to_gb(memory.total),
            "available_gb": bytes_to_gb(memory.available),
            "used_percent": memory.percent
        },
        "disk": {
            "total_gb": bytes_to_gb(disk.total),
            "free_gb": bytes_to_gb(disk.free),
            "used_percent": disk.percent
        },
        "boot_time": datetime.fromtimestamp(
            psutil.boot_time(),
            tz=timezone.utc
        ).isoformat()
    }


def get_network_information():
    """Collect basic network diagnostic information."""
    hostname = socket.gethostname()

    return {
        "hostname": hostname,
        "local_ip": get_local_ip(),
        "internet_connected": check_internet_connection()
    }


def create_diagnostic_summary(system_information, network_information):
    """Generate support warnings based on resource thresholds."""
    warnings = []

    cpu_usage = system_information["cpu_usage_percent"]
    memory_usage = system_information["memory"]["used_percent"]
    disk_usage = system_information["disk"]["used_percent"]

    if cpu_usage >= 90:
        warnings.append({
            "level": "critical",
            "message": "CPU usage is critically high."
        })
    elif cpu_usage >= 75:
        warnings.append({
            "level": "warning",
            "message": "CPU usage is elevated."
        })

    if memory_usage >= 90:
        warnings.append({
            "level": "critical",
            "message": "Memory usage is critically high."
        })
    elif memory_usage >= 75:
        warnings.append({
            "level": "warning",
            "message": "Memory usage is elevated."
        })

    if disk_usage >= 90:
        warnings.append({
            "level": "critical",
            "message": "Disk space is critically low."
        })
    elif disk_usage >= 80:
        warnings.append({
            "level": "warning",
            "message": "Available disk space is running low."
        })

    if not network_information["internet_connected"]:
        warnings.append({
            "level": "critical",
            "message": "Internet connectivity test failed."
        })

    if not warnings:
        warnings.append({
            "level": "healthy",
            "message": "No immediate system issues were detected."
        })

    return warnings


@app.get("/")
def home():
    """Serve the interactive frontend."""
    return render_template("index.html")


@app.get("/api/health")
def health():
    """Return API health information."""
    return jsonify({
        "status": "healthy",
        "service": "IT Support Diagnostic Dashboard",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.get("/api/system")
def system():
    """Return current system information."""
    return jsonify(get_system_information())


@app.get("/api/network")
def network():
    """Return current network information."""
    return jsonify(get_network_information())


@app.get("/api/diagnostics")
def diagnostics():
    """Return a complete diagnostic report."""
    system_information = get_system_information()
    network_information = get_network_information()

    return jsonify({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "system": system_information,
        "network": network_information,
        "warnings": create_diagnostic_summary(
            system_information,
            network_information
        )
    })


@app.errorhandler(404)
def not_found(_error):
    return jsonify({
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({
        "error": "An internal server error occurred"
    }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )