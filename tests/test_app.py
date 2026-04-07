from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root_returns_system_ready() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "System Ready"}


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
