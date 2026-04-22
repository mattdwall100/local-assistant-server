from fastapi import APIRouter

from assistant_server.api.schemas import ChatRequest, ChatResponse, HealthResponse
from assistant_server.orchestrator.pipeline import AssistantPipeline

api_router = APIRouter()
pipeline = AssistantPipeline()


@api_router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@api_router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    result = pipeline.run(payload.text, payload.session_id)
    return ChatResponse(text=result.text, session_id=result.session_id)

