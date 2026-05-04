from collections.abc import Generator
from typing import Any

from .piper_client import PiperTTS


class TtsService:
    """Text-to-speech service abstraction."""

    def __init__(self) -> None:
        self.voice = PiperTTS()

    def synthesize_file(self, text: str, output_path: str) -> None:
        self.voice.synthesize_file(text, output_path)

    def stream_synthesize(self, text: str) -> Generator[Any, Any, Any]:
        for chunk in self.voice.stream_synthesize(text):
            yield chunk
