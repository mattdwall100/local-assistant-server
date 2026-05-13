from collections.abc import Generator
from typing import Any

from .piper_client import PiperTTS


class TtsService:
    """Text-to-speech service abstraction."""

    # add more type hints in future when added
    def __init__(self, tts_client: PiperTTS) -> None:
        self.voice = tts_client

    def synthesize_file(self, text: str, output_path: str) -> None:
        self.voice.synthesize_file(text, output_path)

    def stream_synthesize(self, text: str) -> Generator[Any, Any, Any]:
        yield from self.voice.stream_synthesize(text)
