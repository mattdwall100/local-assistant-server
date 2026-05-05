from .services.llm.ollama_client import OllamaClient
from .services.stt.fasterWhisper_client import FasterWhisperSTT 
from .services.tts.piper_client import PiperTTS
from .orchestrator.fallback import FallbackHandler
from .tools.base import ToolRegistry
from .memory.store import MemoryStore
from .rag.retriever import Retriever

def create_services():
    stt_service = FasterWhisperSTT()
    tts_service = PiperTTS()
    llm_service = OllamaClient()

    fallback_handler = FallbackHandler(tts_service)
    tools = ToolRegistry()
    memory = MemoryStore()
    retriever = Retriever()

    return {
        "stt": stt_service,
        "llm": llm_service,
        "tts": tts_service,
        "fallback_handler": fallback_handler,
        "tools": tools,
        "memory": memory,
        "retriever": retriever
    }

