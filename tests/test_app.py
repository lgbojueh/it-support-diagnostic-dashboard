from app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/api/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"System Diagnostic Dashboard" in response.data


def test_diagnostics_endpoint():
    client = app.test_client()

    response = client.get("/api/diagnostics")
    data = response.get_json()

    assert response.status_code == 200
    assert "system" in data
    assert "network" in data
    assert "warnings" in data