from unittest.mock import patch

from assistant_server.orchestrator.pipeline import AssistantPipeline
from tests.mocks import create_mock_services


def test_run_llm_returns_response_and_updates_memory() -> None:
    # Arrange
    services = create_mock_services()
    pipeline = AssistantPipeline(**services.model_dump())
    memory = services.memory

    # Act
    result = pipeline.run_llm("hello", session_id=None)

    # Assert
    response = list(result.response_message)
    assert "".join(response) == "mock response message"
    assert result.session_id is not None

    messages = memory.load_chat_history(result.session_id)
    assert messages == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "mock response message"},
    ]


def test_run_pipeline_returns_audio_stream() -> None:
    # Arrange
    services = create_mock_services()
    pipeline = AssistantPipeline(**services.model_dump())

    # Act
    stream, session_id = pipeline.run(b"audio bytes", session_id="session-1")
    chunks = list(stream)

    # Assert
    assert session_id == "session-1"
    assert len(chunks) == 3
    assert all(isinstance(chunk, bytes) for chunk in chunks)
    assert all(chunk for chunk in chunks)


def test_run_llm_updates_activity() -> None:
    # Arrange
    services = create_mock_services()
    orchestrator = AssistantPipeline(**services.model_dump())

    with patch.object(orchestrator, "update_activity") as update:
        # Act
        orchestrator.run_llm("hello")

        # Assert
        update.assert_called_once()
