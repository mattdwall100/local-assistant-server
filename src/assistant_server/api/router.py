from fastapi import APIRouter
from fastapi import UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional

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


@api_router.post("/transcribe", response_model=ChatResponse)
async def transcribe(file: UploadFile = File(...),
                     session_id: Optional[str] = Form(None)) -> ChatResponse:
    audio_bytes = await file.read()
    audio_stream = io.BytesIO(audio_bytes)
    audio_stream.seek(0)

    text = stt_service.transcribe(audio_stream)
    return ChatResponse(text=text, session_id=session_id) 


@api_router.post('/synthesize')
def synthesize(payload: ChatRequest) -> StreamingResponse:
    """Send a stream of bytes back to the client, speaking the text sent"""
    return StreamingResponse(
        tts_service.stream_synthesize(payload.text),
        media_type='application/octet-stream',
        headers={
            "X-Session-ID": ""
        }
    )


@api_router.post("/speak")
async def speak(file: UploadFile = File(...),
                     session_id: Optional[str] = Form(None)) -> StreamingResponse:
    # Recieve raw bytes and format to wrapped BytesIO
    raw_bytes = await file.read()
    audio_bytes = io.BytesIO(raw_bytes)
    audio_bytes.seek(0)

    # Send to pipeline
    stream_response, resolved_id = pipeline.run(audio_bytes, session_id)

    # Send back the stream response
    return StreamingResponse(
        stream_response,
        media_type='application/octet-stream',
        headers={
            "X-Session-ID": resolved_id
        }
    )
