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

