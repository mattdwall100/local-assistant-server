from ...core.config import get_settings
from faster_whisper import WhisperModel

settings = get_settings()

class FasterWhisperSTT:
    """Client for the Faster Whisper speech-to-text model."""

    def __init__(self, model_size: str = settings.faster_whisper_model):
        self.model = WhisperModel(model_size, device="cpu")

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe the given audio bytes and return the transcribed text."""
        segments, info = self.model.transcribe(audio_bytes)
        text = " ".join(segment.text for segment in segments)

        return text
