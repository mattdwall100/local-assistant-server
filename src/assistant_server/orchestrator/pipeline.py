from dataclasses import dataclass

from assistant_server.memory.store import MemoryStore
from assistant_server.rag.retriever import Retriever
from assistant_server.services.llm.base import LlmService
from assistant_server.tools.registry import ToolRegistry


# Currently handling engine, state, contracts all at once.
# state is everything that persists across turns (tool results, session id, responses etc.)

@dataclass(frozen=True)
class PipelineResult:
    text: str
    session_id: str | None


class AssistantPipeline:
    def __init__(self) -> None:
        self._llm = LlmService()
        self._tools = ToolRegistry()
        self._memory = MemoryStore()
        self._retriever = Retriever()

    def run(self, text: str, session_id: str | None = None) -> PipelineResult:
        # Placeholder orchestration contract for future STT -> tool loop -> TTS flow.
        memory_context = self._memory.load(session_id)
        retrieval_context = self._retriever.retrieve(text)
        tool_schemas = self._tools.schemas()
        response = self._llm.complete(text, memory_context, retrieval_context, tool_schemas)
        llm_text = response.content
        resolved_session = self._memory.save(session_id=session_id, user_text=text, assistant_text=llm_text)
        return PipelineResult(text=llm_text, session_id=resolved_session)

