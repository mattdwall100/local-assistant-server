from assistant_server.api.schemas import FallbackStream
from tests.mocks import create_mock_services


def _raise_failure(*args, **kwargs):
    del args
    del kwargs
    raise Exception("fail")


def test_fallback_handler_returns_audio_stream_for_failure() -> None:
    # Arrange
    services = create_mock_services()
    handler = services["fallback_handler"]

    # Act
    stream = handler.handle("llm", Exception("boom"), session_id="session-1")
    chunks = list(stream)

    # Assert
    assert len(chunks) == 3
    assert all(isinstance(chunk, bytes) for chunk in chunks)


def test_fallback_handler_returns_fallback_text_when_tts_fails(tmp_path) -> None:
    # Arrange
    services = create_mock_services()
    services["tts"].stream_synthesize = _raise_failure
    handler = services["fallback_handler"]
    handler.fallback_path = str(tmp_path)

    # Act
    response = handler.handle("tts", Exception("boom"), session_id="session-2")

    # Assert
    assert isinstance(response, FallbackStream)
    assert response.fallback_text.startswith("Sorry, I'm having trouble getting my words out")
    assert "boom" in response.fallback_text
    assert response.headers["x-session-id"] == "session-2"
    assert response.headers["x-fallback-txt"] == response.fallback_text
