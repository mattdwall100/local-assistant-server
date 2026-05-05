from fastapi.testclient import TestClient

from assistant_server.main import create_app
from tests.mocks import create_mock_services


def _raise_failure(*args, **kwargs):
    del args
    del kwargs
    raise Exception("fail")


def test_speak_endpoint_returns_fallback_when_stt_fails() -> None:
    # Arrange
    services = create_mock_services()
    services["stt"].transcribe = _raise_failure
    client = TestClient(create_app(service_factory=lambda: services))

    # Act
    response = client.post(
        "/speak",
        files={"file": ("audio.wav", b"audio bytes", "audio/wav")},
        data={"session_id": "session-stt"},
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["x-session-id"] == "session-stt"
    assert response.content


def test_speak_endpoint_returns_fallback_when_llm_fails() -> None:
    # Arrange
    services = create_mock_services()
    services["llm"].complete = _raise_failure
    client = TestClient(create_app(service_factory=lambda: services))

    # Act
    response = client.post(
        "/speak",
        files={"file": ("audio.wav", b"audio bytes", "audio/wav")},
        data={"session_id": "session-llm"},
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["x-session-id"] == "session-llm"
    assert response.content


def test_speak_endpoint_returns_fallback_when_tts_fails() -> None:
    # Arrange
    services = create_mock_services()
    app = create_app(service_factory=lambda: services)
    app.state.orchestrator._tts.stream_synthesize = _raise_failure
    client = TestClient(app)

    # Act
    response = client.post(
        "/speak",
        files={"file": ("audio.wav", b"audio bytes", "audio/wav")},
        data={"session_id": "session-tts"},
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["x-session-id"] == "session-tts"
    assert response.content
