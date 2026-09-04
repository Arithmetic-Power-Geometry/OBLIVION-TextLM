from fastapi.testclient import TestClient

from oblivion_textlm.api import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_required_for_metrics():
    client = TestClient(app)
    assert client.get("/metrics").status_code == 401


def test_health_does_not_require_authentication():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "oblivion-textlm"
