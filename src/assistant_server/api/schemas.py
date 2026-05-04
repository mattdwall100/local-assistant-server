from typing import Generator, Any
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class readyResponse(BaseModel):
    # Later add more detailed readiness checks, including checking services status
    status: str = "ready"


class ChatRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=120)


class ChatResponse(BaseModel):
    text: str
    session_id: str | None = None


# For sending audio streams as output of Piper
class AudioStream:
    def __init__(self, 
                 generator: Generator[Any, Any, Any], 
                 sample_rate: int = 16000, 
                 fallback_text: str | None = None
                 ) -> None:
        self.generator = generator
        self.sample_rate = sample_rate
        self.fallback_text = fallback_text


class FallbackStream(StreamingResponse):
    def __init__(self, 
                 generator: Generator[Any, Any, Any], 
                 fallback_text: str, 
                 session_id: str
                 ) -> None:
        super().__init__(
            generator,
            media_type="application/octet-stream",
            headers={"X-Session-ID": session_id or "", "X-Fallback-TXT": fallback_text},
        )
        self.fallback_text = fallback_text
