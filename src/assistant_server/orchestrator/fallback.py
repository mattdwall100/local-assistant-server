from ..services.tts.base import TtsService
from ..core.config import get_settings
from ..core.logging import get_logger
from ..api.schemas import FallbackStream
from pathlib import Path
from typing import Generator

settings = get_settings()
logger = get_logger(__name__)

class FallbackHandler:
    """Fallback handler for graceful degredation whenever a pipeline module fails.
    Returns FallbackStream object, so must be returned alongside resolved_id/session_id for API"""
    def __init__(self, tts: TtsService):
        self.tts = tts

        self.fallback_path = settings.fallback_path
        self.fallback_message = {
            "stt": "Sorry, I had trouble understanding that. ",
            "llm": "Sorry, I'm having trouble thinking straight...",
            "tts": "Sorry, I'm having trouble getting my words out..."
        }

    def handle(self, event_name: str, exception: Exception, session_id: str) -> Generator | FallbackStream:
        if not event_name in self.fallback_message.keys():
            logger.error(f"unknown event_name | event_name={event_name}")
            raise ValueError("Unknown event name")

        fallback_text = self.fallback_message[event_name] + " The exception was: " + str(exception)
        
        # First try to send adaptive message via TTS (no fallback text)
        try:
            return self.tts.stream_synthesize(fallback_text)
        except Exception as e:
            logger.warning(f"Primary Fallback Failed | event_name={event_name}")
            logger.debug(f"Fallback Error | {e}")

        # Next we try to send a pre-recorded fallback message and the fallback text
        try:
            resolved_path = Path(self.fallback_path + "/" + event_name + ".wav")
            
            with open(resolved_path, "rb") as f:
                 fallback_bytes = f.read()

            return FallbackStream(
                self.bytes_to_stream(fallback_bytes), 
                fallback_text,
                session_id
                )
        except Exception as e:
            logger.warning(f"Secondary Fallback Failed | event_name={event_name}")
            logger.debug(f"Fallback Error | {e}")    

        # Finally we try to return no audio but the fallback text
        try:
            return FallbackStream(
                self.bytes_to_stream(bytes()), 
                fallback_text,
                session_id
                )
        except Exception as e:
            logger.warning(f"Final Fallback Failed | event_name={event_name}")
            logger.debug(f"Fallback Error | {e}")    

        return FallbackStream(
            self.bytes_to_stream(bytes()),
            "<Failed to gather>",
            session_id
            )       

    def bytes_to_stream(self, audio_bytes: bytes, chunk_size: int = 4096):
        for i in range(0, len(audio_bytes), chunk_size):
            yield audio_bytes[i:i + chunk_size]