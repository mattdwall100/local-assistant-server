class SttService:
    """Speech-to-text service abstraction."""

    def transcribe(self, audio_bytes: bytes) -> str:
        raise NotImplementedError("STT integration will be implemented in a later milestone.")

