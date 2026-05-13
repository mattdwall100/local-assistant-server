from io import BytesIO

from .fasterWhisper_client import FasterWhisperSTT


class SttService:
    """Speech-to-text service abstraction."""

    def __init__(self, stt_client: FasterWhisperSTT) -> None:
        self.stt_client = stt_client

    def transcribe(self, audio_bytes: BytesIO) -> str:
        text: str = self.stt_client.transcribe(audio_bytes)
        return text
