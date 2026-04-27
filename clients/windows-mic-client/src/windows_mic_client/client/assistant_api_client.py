from __future__ import annotations
from typing import Any
import requests


class AssistantAPIClient:
    def __init__(self, base_url: str, timeout_seconds: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def health(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/health",
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def transcribe(self, audio_bytes: bytes) -> dict[str, Any]:
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        response = requests.post(
            f"{self.base_url}/transcribe",
            files=files,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

