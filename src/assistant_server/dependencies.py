from pydantic import BaseModel, ConfigDict

from .core.config import get_settings
from .memory.store import MemoryStore
from .orchestrator.fallback import FallbackHandler
from .rag.retriever import Retriever
from .services.llm.ollama_client import OllamaClient
from .services.stt.fasterWhisper_client import FasterWhisperSTT
from .services.tts.base import TtsService
from .services.tts.piper_client import PiperTTS
from .tools.base import ToolRegistry

settings = get_settings()


class Services(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stt: FasterWhisperSTT
    llm: OllamaClient
    routing_llm: OllamaClient
    tts: PiperTTS
    fallback_handler: FallbackHandler
    memory: MemoryStore
    tools: ToolRegistry
    retriever: Retriever


def create_services() -> Services:
    stt_service = FasterWhisperSTT()
    tts_service = PiperTTS()
    llm_service = OllamaClient(modelname=settings.modelname)
    routing_llm_service = OllamaClient(modelname=settings.routing_modelname)

    fallback_handler = FallbackHandler(TtsService(tts_service))
    memory = MemoryStore()
    tools = ToolRegistry()
    retriever = Retriever()

    return Services(
        stt=stt_service,
        llm=llm_service,
        routing_llm=routing_llm_service,
        tts=tts_service,
        fallback_handler=fallback_handler,
        tools=tools,
        memory=memory,
        retriever=retriever,
    )
