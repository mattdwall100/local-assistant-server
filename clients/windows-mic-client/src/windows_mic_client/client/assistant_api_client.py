from __future__ import annotations
from typing import Any
import requests
from ..audio.player import AudioPlayer


class AssistantAPIClient:
    def __init__(self, base_url: str, player: AudioPlayer, timeout_seconds: float = 300.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.player = player

    def health(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/health",
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def transcribe(self, audio_bytes: bytes, session_id: str = None) -> dict[str, Any]:
        """Transcribes audio bytes into text using piper python API"""
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"session_id": session_id}

        response = requests.post(
            f"{self.base_url}/transcribe",
            files=files,
            data=data,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()
    
    def synthesize(self, text: str) -> Any:
        payload = {'text': text, 'session_id' : None}
        response = requests.post(
            f'{self.base_url}/synthesize',
            json=payload,
            timeout=self.timeout_seconds,
            stream=True
        )
        iter_response = response.iter_content(chunk_size=None)
        self.player.play_wav_stream(iter_response)
        print("response played")

        session_id = response.headers.get("X-Session-ID")
        print("Session ID:", session_id)

        return iter_response
    

    def speak(self, audio_bytes: bytes, session_id: str = None) -> Any:
        """Runs full pipeline on endpoint"""

        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"session_id": session_id}

        response = requests.post(
            f"{self.base_url}/speak",
            files=files,
            data=data,
            timeout=self.timeout_seconds,
        )
        iter_response = response.iter_content(chunk_size=None)
        self.player.play_wav_stream(iter_response)
        print("response played")

        session_id = response.headers.get("X-Session-ID")
        print("Session ID:", session_id)

        return iter_response
    

        
