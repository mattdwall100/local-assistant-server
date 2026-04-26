from .piper_client import PiperTTS


voice_path = ".....en_GB-alan-medium.onnx"
output_path = "output.wav"

class TtsService:
    """Text-to-speech service abstraction."""
    def __init__(self):
        self.voice = PiperTTS(voice_path)
    
    def synthesize(self, text: str, output_path: str) -> None:
        self.voice.synthesize(text, output_path)
        

    def stream_synthesize(self, text: str, output_path:str) -> None:
        for chunk in self.voice.stream_synthesize(text):
            # Process the chunk (e.g., save to file, stream to client, etc.)
            yield chunk

