from .piper_client import PiperTTS


class TtsService:
    """Text-to-speech service abstraction."""

    def __init__(self):
        self.voice = PiperTTS()
    
    def synthesize(self, text: str, output_path: str = None) -> None:
        self.voice.synthesize(text)

    def stream_synthesize(self, text: str, output_path:str = None) -> bytes:
        for chunk in self.voice.stream_synthesize(text):
            yield chunk

