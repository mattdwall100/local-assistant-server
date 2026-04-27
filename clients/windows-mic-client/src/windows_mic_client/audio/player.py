from __future__ import annotations
import io
import soundfile as sf
import sounddevice as sd
from fastapi.responses import StreamingResponse
import numpy as np
from typing import Iterable



class AudioPlayer:
    def __init__(self, sample_rate: int = 22050, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def play_wav_bytes(self, audio_bytes: bytes) -> None:
        """Play the given audio bytes."""
        audio_array, sr = sf.read(
            io.BytesIO(audio_bytes)
        )
        sd.play(audio_array, sr)
        sd.wait()

    def play_wav_stream(self, chunk_iterator: Iterable) -> None:
        stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16'
        )

        stream.start()

        for chunk in chunk_iterator:
            if not chunk:
                continue
            else:
                audio = np.frombuffer(chunk, dtype='int16')
                stream.write(audio)

        stream.stop()
        stream.close()

