from __future__ import annotations
import sounddevice as sd
import numpy as np
from pynput import keyboard

from typing import Optional

from ..client.assistant_api_client import AssistantAPIClient
from .audio_utils import numpy_to_wav_bytes

from pathlib import Path
from datetime import datetime

class MicrophoneRecorder:
    """Controls recording using sounddevice"""

    def __init__(self, sample_rate: int, channels: int) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def record(self, max_duration: float, wait: bool = True) -> bytes:
        """Record audio for a specified duration and return the audio data as bytes."""
        audio = sd.rec(
            int(max_duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'
        )

        if wait:
            sd.wait()  # Wait until max wait time is finished

        # turn to wav bytes before returning to controller and api
        audio_bytes = numpy_to_wav_bytes(np.asarray(audio, dtype='int16'), self.sample_rate)


        return audio_bytes
        #return np.asarray(audio, dtype="int16").tobytes()

    def stream(self, frames: Optional[int] = None):
        """Stream audio data in real-time. If frames is None, stream indefinitely until stopped.
        """


class PushToTalkController:
    """Push to talk controls handler for MicrophoneRecorder"""

    def __init__(self, recorder: MicrophoneRecorder, api: AssistantAPIClient):
        self.recorder = recorder
        self.api = api
        self.is_recording = False
        self.audio_bytes = None

        self.max_duration = 5  # Max recording duration in seconds

        self.listen_for_keypresses()

    def start_recording(self, key) -> None:
        if key == keyboard.Key.space and not self.is_recording:
            self.is_recording = True
            print("Recording started...")
            self.audio_bytes = self.recorder.record(self.max_duration, wait=True)

    def stop_recording(self, key) -> None:
        if key == keyboard.Key.space and self.is_recording:
            self.is_recording = False
            print("Recording stopped.")
            sd.stop() # Stop the recording immediately

            # Process the recorded audio data
            self.handle_audio()

    def handle_audio(self) -> None:
        """Handle the recorded audio data, e.g., by sending it to the Assistant API."""
        if self.audio_bytes is not None:
            # Here you would send audio_bytes to the Assistant API for transcription
            print(f"Recorded audio data length: {len(self.audio_bytes)} bytes")

            # Audio file test
            debug_dir = Path(r'C:\Users\Admin\Documents\Projects\Local-AI-Assistant\local-assistant-server\clients\windows-mic-client\tests\audio_files')
            debug_dir.mkdir(exist_ok=True)
            filename = debug_dir / f"mic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            filename.write_bytes(self.audio_bytes)


            transcribed_json = self.api.transcribe(self.audio_bytes)
            print(transcribed_json)
    
    def listen_for_keypresses(self) -> None:
        """Listen for keypresses to control recording."""
        listener = keyboard.Listener(
            on_press=self.start_recording,
            on_release=self.stop_recording
        )
        
        listener.start()
        listener.join()


