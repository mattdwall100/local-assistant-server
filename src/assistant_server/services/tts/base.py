from .piper_client import PiperTTS
from typing import Generator, Any



class TtsService:
    """Text-to-speech service abstraction."""

    def __init__(self):
        self.voice = PiperTTS()
    
    def synthesize(self, text: str) -> None:
        self.voice.synthesize(text)

    def stream_synthesize(self, text: str) -> Generator[Any, Any, Any]:
        for chunk in self.voice.stream_synthesize(text):
            yield chunk

