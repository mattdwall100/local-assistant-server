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

    def __init__(self, sample_rate: int, channels: int, block_size: int) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.frames = []
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.frames.append(indata.copy())

    def start(self):
        # New recording with fresh frames list
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.block_size,
            dtype='int16',
            callback=self._callback
        )
        self.stream.start()
    
    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        if self.frames:
            audio_array = np.concatenate(self.frames)
            audio_bytes = numpy_to_wav_bytes(audio_array, self.sample_rate)
            return audio_bytes
        else:
            print("No frame data found")
            return None


    def record(self, max_duration: float, wait: bool = True) -> bytes:
        """Record audio for a specified duration and return the audio data as bytes."""
        audio = sd.rec(
            int(max_duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'
        )
        print("Recording started...")
        if wait:
            sd.wait()  # Wait until max wait time is finished
        # turn to wav bytes before returning to controller and api
        audio_bytes = numpy_to_wav_bytes(np.asarray(audio, dtype='int16'), self.sample_rate)

        return audio_bytes
        #return np.asarray(audio, dtype="int16").tobytes()


class PushToTalkController:
    """Push to talk controls handler for MicrophoneRecorder"""

    def __init__(self, recorder: MicrophoneRecorder, api: AssistantAPIClient):
        self.recorder = recorder
        self.api = api
        self.is_recording = False

        self.listen_for_keypresses()

    def start_recording(self, key) -> None:
        if key == keyboard.Key.space and not self.is_recording:
            self.is_recording = True
            print("Recording...")
            self.recorder.start() 

    def stop_recording(self, key) -> None:
        if key == keyboard.Key.space and self.is_recording:
            self.is_recording = False
            audio_bytes = self.recorder.stop() # Stop the recording immediately and save bytes
            print("Recording stopped.")                       

            # Process the recorded audio data
            if not audio_bytes:
                print("No audio found")
            elif len(audio_bytes)< 1025:
                print("Audio too short")
            else:
                self.handle_audio(audio_bytes)

    def handle_audio(self, audio_bytes) -> None:
        """Handle the recorded audio data, e.g., by sending it to the Assistant API."""
        if audio_bytes is not None:
            # Here you would send audio_bytes to the Assistant API for transcription
            print(f"Recorded audio data length: {len(audio_bytes)} bytes")

            # Audio file test
            #debug_dir = Path(r'C:\Users\Admin\Documents\Projects\Local-AI-Assistant\local-assistant-server\clients\windows-mic-client\tests\audio_files')
            #debug_dir.mkdir(exist_ok=True)
            #filename = debug_dir / f"mic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            #filename.write_bytes(audio_bytes)

            #transcribed_json = self.api.transcribe(audio_bytes)
            #print(transcribed_json)

            print("Sending Speak Request...")
            response = self.api.speak(audio_bytes, session_id="TestSession")
            print("Success")
            
    
    def listen_for_keypresses(self) -> None:
        """Listen for keypresses to control recording."""
        listener = keyboard.Listener(
            on_press=self.start_recording,
            on_release=self.stop_recording
        )
        
        listener.start()
        listener.join()


