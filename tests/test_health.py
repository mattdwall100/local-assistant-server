from fastapi.testclient import TestClient

from assistant_server.main import create_app

from .mocks import create_mock_services


def test_health() -> None:
    client = TestClient(create_app(service_factory=create_mock_services))
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
