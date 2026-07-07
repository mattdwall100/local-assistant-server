from collections.abc import Iterator
from typing import Any

from ...core.logging import get_logger
from ...utils.latency_logger import log_latency
from .piper_client import PiperTTS

logger = get_logger(__name__)


class TtsService:
    """Text-to-speech service abstraction."""

    # add more type hints in future when added
    def __init__(self, tts_client: PiperTTS) -> None:
        self.voice = tts_client

    def synthesize_file(self, text: str, output_path: str) -> None:
        self.voice.synthesize_file(text, output_path)

    def stream_synthesize(self, text: str) -> Iterator[Any]:
        yield from self.voice.stream_synthesize(text)

    def stream_in_stream_out(self, text_chunks: Iterator[str]) -> Iterator[Any]:
        # Time from first consumption of this generator to first LLM sentence
        with log_latency(logger, "first_tts_text_received"):
            first_text = next((text for text in text_chunks if text.strip()), None)

        if first_text is None:
            return

        # Time to synthesize the first audio chunk of the first sentence
        audio_stream = self.voice.stream_synthesize(first_text)
        with log_latency(logger, "first_tts_audio_chunk"):
            first_audio = next(audio_stream, None)
        if first_audio is not None:
            yield first_audio
        yield from audio_stream

        for text in text_chunks:
            if not text.strip():
                continue

            yield from self.voice.stream_synthesize(text)
