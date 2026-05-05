from fastapi.testclient import TestClient

from assistant_server.main import create_app
from tests.mocks import create_mock_services


def test_health_endpoint_returns_ok() -> None:
    # Arrange
    client = TestClient(create_app(service_factory=create_mock_services))

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_response_shape() -> None:
    # Arrange
    client = TestClient(create_app(service_factory=create_mock_services))

    # Act
    response = client.post("/chat", json={"text": "hello", "session_id": None})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["text"] == "mock response message"
    assert isinstance(payload["session_id"], str)
    assert payload["session_id"]


def test_transcribe_endpoint_returns_mock_transcription() -> None:
    # Arrange
    client = TestClient(create_app(service_factory=create_mock_services))

    # Act
    response = client.post(
        "/transcribe",
        files={"file": ("audio.wav", b"audio bytes", "audio/wav")},
        data={"session_id": "session-1"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"text": "mock transcription", "session_id": "session-1"}


def test_speak_endpoint_runs_end_to_end() -> None:
    # Arrange
    client = TestClient(create_app(service_factory=create_mock_services))

    # Act
    response = client.post(
        "/speak",
        files={"file": ("audio.wav", b"audio bytes", "audio/wav")},
        data={"session_id": "session-2"},
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["x-session-id"] == "session-2"
    assert response.content
    assert isinstance(response.content, bytes)
