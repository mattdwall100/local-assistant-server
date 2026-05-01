import wave
from piper import PiperVoice
from pathlib import Path
from assistant_server.core.config import get_settings


# Default paths
settings = get_settings()
VOICE_PATH = settings.tts_voice_path
OUTPUT_PATH = settings.tts_output_path


class PiperTTS:
    def __init__(self, voice_path: str = VOICE_PATH, output_path: str = OUTPUT_PATH):
        self.voice = PiperVoice.load(voice_path)
        self.output_path = output_path

    def synthesize_file(self, text: str, output_path: str = None) -> None:
        """Synthesize the given text and save it to the specified output path."""
        # Default outputpath is set to self.output_path if not provided
        if output_path is not None:
            self.output_path = str(Path(output_path))

        with wave.open(self.output_path, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)
    
    def stream_synthesize(self, text: str):
        """Example of streaming synthesis, yielding audio chunks as they are generated."""
        for chunk in self.voice.synthesize(text):
            yield chunk.audio_int16_bytes