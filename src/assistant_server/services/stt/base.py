from .fasterWhisper_client import FasterWhisperSTT


class SttService:
    """Speech-to-text service abstraction."""

    def __init__(self, stt_client) -> None:
        self.stt_client = stt_client

    def transcribe(self, audio_bytes: bytes) -> str:
        text = self.stt_client.transcribe(audio_bytes)
        return text
