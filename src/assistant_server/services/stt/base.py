from .fasterWhisper_client import FasterWhisperSTT


class SttService:
    """Speech-to-text service abstraction."""

    def __init__(self) -> None:
        self.stt_client = FasterWhisperSTT("tiny")

    def transcribe(self, audio_bytes: bytes) -> str:
        text = self.stt_client.transcribe(audio_bytes)
        return text
