from pathlib import Path

from faster_whisper import WhisperModel

from ...core.config import get_settings

settings = get_settings()


class FasterWhisperSTT:
    """Client for the Faster Whisper speech-to-text model."""

    def __init__(
        self,
        model_path_or_type: str = settings.stt_FW_model_path,
        stt_device: str = settings.stt_device,
    ):
        if "/" in model_path_or_type:  # if is a directory
            model_path_or_type = str(Path(model_path_or_type))
        self.model = WhisperModel(
            model_path_or_type, device=stt_device, compute_type="float32", local_files_only=True
        )

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe the given audio bytes and return the transcribed text."""
        segments, info = self.model.transcribe(audio_bytes)
        text = " ".join(segment.text for segment in segments)

        return text
