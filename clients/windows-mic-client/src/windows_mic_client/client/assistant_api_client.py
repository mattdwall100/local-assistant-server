from __future__ import annotations
from typing import Any
import requests


class AssistantAPIClient:
    def __init__(self, base_url: str, timeout_seconds: float = 300.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds


    def health(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/health",
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def transcribe(self, audio_bytes: bytes, session_id: str | None) -> dict[str, Any]:
        """Transcribes audio bytes into text using piper python API"""
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"session_id": session_id}

        response = requests.post(
            f"{self.base_url}/transcribe",
            files=files,
            data=data,
            timeout=self.timeout_seconds,
        )

        return response.json()
    
    def synthesize(self, text: str, session_id: str | None) -> Any:
        payload = {'text': text, 'session_id' : session_id}
        response = requests.post(
            f'{self.base_url}/synthesize',
            json=payload,
            timeout=self.timeout_seconds,
            stream=True
        )
        resolved_id = response.headers.get("X-Session-ID")
        return response, resolved_id
    
    def speak(self, audio_bytes: bytes, session_id: str | None) -> Any:
        """Runs full pipeline on endpoint"""

        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"session_id": session_id}

        response = requests.post(
            f"{self.base_url}/speak",
            files=files,
            data=data,
            timeout=self.timeout_seconds,
        )
        resolved_id = response.headers.get("X-Session-ID")
        return response, resolved_id
        iter_response = response.iter_content(chunk_size=None)
        

        return iter_response, resolved_session_id
    

        
