from fastapi import APIRouter
from fastapi import UploadFile, File

from .schemas import ChatRequest, ChatResponse, HealthResponse
from ..orchestrator.pipeline import AssistantPipeline

from ..services.tts.base import TtsService
from ..services.stt.base import SttService
import io


api_router = APIRouter()
pipeline = AssistantPipeline()

tts_service = TtsService()
stt_service = SttService()


@api_router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@api_router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    result = pipeline.run(payload.text, payload.session_id)
    return ChatResponse(text=result.text, session_id=result.session_id)

@api_router.post('/synthesize', response_model=ChatResponse)
def synthesize(payload: ChatRequest) -> ChatRequest:
    
    #output_path = f"{payload.session_id}.wav" if payload.session_id else "output.wav"
    tts_service.synthesize(payload.text)
    return payload

@api_router.post("/transcribe", response_model=ChatResponse)
async def transcribe(file: UploadFile = File(...)) -> ChatResponse:
    audio_bytes = await file.read()
    audio_stream = io.BytesIO(audio_bytes)
    audio_stream.seek(0)

    text = stt_service.transcribe(audio_stream)
    return ChatResponse(text=text, session_id=None)