from pydantic import BaseModel, ConfigDict

from .memory.store import MemoryStore
from .orchestrator.fallback import FallbackHandler
from .rag.retriever import Retriever
from .services.llm.ollama_client import OllamaClient
from .services.stt.fasterWhisper_client import FasterWhisperSTT
from .services.tts.base import TtsService
from .services.tts.piper_client import PiperTTS
from .tools.base import ToolRegistry


class Services(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stt: FasterWhisperSTT
    llm: OllamaClient
    tts: PiperTTS
    fallback_handler: FallbackHandler
    memory: MemoryStore
    tools: ToolRegistry
    retriever: Retriever


def create_services() -> Services:
    stt_service = FasterWhisperSTT()
    tts_service = PiperTTS()
    llm_service = OllamaClient()

    fallback_handler = FallbackHandler(TtsService(tts_service))
    memory = MemoryStore()
    tools = ToolRegistry()
    retriever = Retriever()

    return Services(
        stt=stt_service,
        llm=llm_service,
        tts=tts_service,
        fallback_handler=fallback_handler,
        tools=tools,
        memory=memory,
        retriever=retriever,
    )
