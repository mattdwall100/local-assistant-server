import json
from unittest.mock import patch

from ollama import ChatResponse, Message

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
    result = pipeline.run(b"audio bytes", session_id="session-1")
    chunks = list(result.stream)

    # Assert
    assert result.session_id == "session-1"
    assert result.transcript == "mock transcription"
    assert list(result.tool_calls) == []
    assert len(chunks) == 3
    assert all(isinstance(chunk, bytes) for chunk in chunks)
    assert all(chunk for chunk in chunks)


def test_run_pipeline_multiplex_yields_paired_text_and_audio_frames() -> None:
    # Arrange
    services = create_mock_services()
    pipeline = AssistantPipeline(**services.model_dump())

    # Act
    result = pipeline.run(b"audio bytes", session_id="session-1", multiplex=True)
    frames = [json.loads(line) for line in b"".join(result.stream).splitlines() if line.strip()]

    # Assert: one text frame, its audio frames, then a terminating done frame
    types = [frame["type"] for frame in frames]
    assert frames[0] == {"type": "text", "seq": 0, "data": "mock response message"}
    assert types.count("audio") == 3
    assert types[-1] == "done"


def test_remember_llm_stream_yields_sentences_progressively() -> None:
    # Arrange
    services = create_mock_services()
    pipeline = AssistantPipeline(**services.model_dump())

    tokens = ["Hello there. ", "How are ", "you today? ", "Good."]
    consumed: list[str] = []

    def fake_stream(messages: list[dict[str, str]]):
        del messages
        for token in tokens:
            consumed.append(token)
            yield ChatResponse(message=Message(role="assistant", content=token))

    with patch.object(pipeline._llm, "stream_complete", side_effect=fake_stream):
        # Act
        stream = pipeline.remember_llm_stream([{"role": "user", "content": "hi"}], "session-1")
        first_sentence = next(stream)

        # Assert: first sentence yielded after consuming only the first token
        assert first_sentence == "Hello there."
        assert consumed == ["Hello there. "]

        # Assert: remaining text arrives split on sentence boundaries
        assert list(stream) == ["How are you today?", "Good."]


def test_remember_llm_stream_flushes_long_unpunctuated_text() -> None:
    # Arrange
    services = create_mock_services()
    pipeline = AssistantPipeline(**services.model_dump())

    tokens = ["word " * 50, "word " * 50, "word " * 50]  # 250 chars each, no punctuation

    def fake_stream(messages: list[dict[str, str]]):
        del messages
        for token in tokens:
            yield ChatResponse(message=Message(role="assistant", content=token))

    with patch.object(pipeline._llm, "stream_complete", side_effect=fake_stream):
        # Act
        chunks = list(
            pipeline.remember_llm_stream([{"role": "user", "content": "hi"}], "session-1")
        )

    # Assert: safety flush emits chunks instead of buffering the whole run
    assert len(chunks) == 2
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
