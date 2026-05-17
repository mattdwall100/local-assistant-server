from collections.abc import Callable, Generator, Iterable

from ollama import ChatResponse, Message

from assistant_server.memory.store import MemoryStore
from assistant_server.orchestrator.fallback import FallbackHandler
from assistant_server.rag.retriever import Retriever
from assistant_server.tools.base import ToolRegistry


class MockSttClient:
    def transcribe(self, audio_bytes: bytes) -> str:
        del audio_bytes
        return "mock transcription"


class MockLlmClient:
    def warmup(self) -> None:
        pass

    def complete(
        self,
        messages: list[dict[str, str]],
        tool_list: list[Callable],
    ) -> tuple[str, list[object | None]]:
        del messages
        del tool_list

        return "mock response message", None
    
    def stream_complete(self, messages: list[dict[str, str]]) -> Iterable[str]:
        yield "The "
        yield "cat "
        yield "jumped,"
        yield " over"
        yield " the "
        yield "wall."




class MockTtsClient:
    def synthesize_file(self, text: str, output_path: str = None) -> None:
        del text
        del output_path
        pass  # do nothing, just simulate the interface

    def stream_synthesize(self, text: str) -> Generator[bytes, None, None]:
        # simulate chunked audio (like Piper)
        chunks = [
            b"\x00\x01" * 2000,
            b"\x02\x03" * 2000,
            b"\x04\x05" * 2000,
        ]
        yield from chunks


def create_mock_services():
    stt_service = MockSttClient()
    tts_service = MockTtsClient()
    llm_service = MockLlmClient()

    fallback_handler = FallbackHandler(tts_service)
    memory = MemoryStore()
    tools = ToolRegistry()
    retriever = Retriever()

    return {
        "stt": stt_service,
        "llm": llm_service,
        "tts": tts_service,
        "fallback_handler": fallback_handler,
        "tools": tools,
        "memory": memory,
        "retriever": retriever,
    }
