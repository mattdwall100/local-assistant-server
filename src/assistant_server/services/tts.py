class TtsService:
    """Text-to-speech service abstraction."""

    def synthesize(self, text: str) -> bytes:
        raise NotImplementedError("TTS integration will be implemented in a later milestone.")

