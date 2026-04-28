from __future__ import annotations
import io
import soundfile as sf
import sounddevice as sd
import numpy as np
from typing import Iterable
from fastapi.responses import StreamingResponse

import threading
from ..core.logging import get_logger

logger = get_logger(__name__)


class AudioPlayer:
    def __init__(self, sample_rate: int = 22050, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.stop_flag = threading.Event()

        self.current_stream = None

    def play_wav_bytes(self, audio_bytes: bytes) -> None:
        """Play the given audio bytes."""
        logger.info(f"playback_started | bytes={len(audio_bytes)}")
        audio_array, sr = sf.read(
            io.BytesIO(audio_bytes)
        )
        sd.play(audio_array, sr)
        sd.wait()
        logger.info("playback_finished | status=completed")

    def play_wav_stream(self, response: StreamingResponse) -> None:
        self.stop_flag.clear()

        # chunk generator
        block_seconds = 0.2 # number of seconds of audio
        block_frames = int(self.sample_rate * block_seconds)
        block_bytes = block_frames * 2  # int16 mono: 2 bytes per frame

        chunk_iterator = response.iter_content(chunk_size=block_bytes)

        def _play_callback():
            self.current_stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16'
            )
            self.current_stream.start()
            logger.info("playback_started | type=stream")
            
            try:
                # Writes chunks to stream until stopped
                for chunk in chunk_iterator:
                    if self.stop_flag.is_set():
                        logger.info("playback_finished | status=interrupted")
                        break
                    elif not chunk:
                        continue
                    else:
                        audio = np.frombuffer(chunk, dtype='int16')
                        self.current_stream.write(audio)
            finally:
                response.close() # Closes the HTTP stream, to save bandwidth
                try:
                    if self.current_stream:
                        self.current_stream.abort()
                        self.current_stream.close()
                finally:
                    self.current_stream = None
                    logger.info("playback_finished | status=completed")

        threading.Thread(target=_play_callback, daemon=True).start()
    
    def stop_playback(self):
        self.stop_flag.set()
