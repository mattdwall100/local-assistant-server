from __future__ import annotations


class AudioPlayer:
    def __init__(self, sample_rate: int, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def play_bytes(self, audio_bytes: bytes) -> None:
        """Play the given audio bytes."""
