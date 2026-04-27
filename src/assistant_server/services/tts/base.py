from .piper_client import PiperTTS


class TtsService:
    """Text-to-speech service abstraction."""

    def __init__(self):
        self.voice = PiperTTS()
    
    def synthesize(self, text: str, output_path: str = None) -> None:
        self.voice.synthesize(text)

    def stream_synthesize(self, text: str, output_path:str = None) -> None:
        for chunk in self.voice.stream_synthesize(text):
            # Process the chunk (e.g., save to file, stream to client, etc.)
            yield chunk

