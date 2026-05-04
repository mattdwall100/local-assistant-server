import io

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from ..core.logging import get_logger
from ..orchestrator.pipeline import AssistantPipeline
from ..services.stt.base import SttService
from ..services.tts.base import TtsService
from ..utils.latency_logger import log_latency
from .schemas import ChatRequest, ChatResponse, HealthResponse

api_router = APIRouter()
pipeline = AssistantPipeline()

logger = get_logger(__name__)


@api_router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@api_router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    logger.info(f"request_received | endpoint=/chat session_id={payload.session_id}")
    with log_latency(logger, "request_completed", endpoint="/chat", session_id=payload.session_id):
        result = pipeline.run_llm(payload.text, payload.session_id)
        return ChatResponse(text=result.text, session_id=result.session_id)


@api_router.post("/transcribe", response_model=ChatResponse)
async def transcribe(
    file: UploadFile = File(...), session_id: str | None = Form(None)
) -> ChatResponse:
    logger.info(f"request_received | endpoint=/transcribe session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/transcribe", session_id=session_id):
        audio_bytes = await file.read()
        audio_stream = io.BytesIO(audio_bytes)
        audio_stream.seek(0)

        text = pipeline.transcribe(audio_stream)
        return ChatResponse(text=text, session_id=session_id)


@api_router.post("/synthesize")
def synthesize(payload: ChatRequest) -> StreamingResponse:
    """Send a stream of bytes back to the client, speaking the text sent"""
    logger.info(f"request_received | endpoint=/synthesize session_id={payload.session_id}")
    with log_latency(
        logger, "request_completed", endpoint="/synthesize", session_id=payload.session_id
    ):
        return StreamingResponse(
            pipeline.stream_synthesize(payload.text),
            media_type="application/octet-stream",
            headers={"X-Session-ID": ""},
        )


@api_router.post("/speak")
async def speak(
    file: UploadFile = File(...), session_id: str | None = Form(None)
) -> StreamingResponse:
    logger.info(f"request_received | endpoint=/speak session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/speak", session_id=session_id):
        # Recieve raw bytes and format to wrapped BytesIO
        raw_bytes = await file.read()
        audio_bytes = io.BytesIO(raw_bytes)
        audio_bytes.seek(0)

        # Send to pipeline
        stream_response, resolved_id = pipeline.run(audio_bytes, session_id)

        # NOTE May not be necessary anymore
        # if has .fallback_text, is a AudioStream object, send as is
        if hasattr(stream_response, "fallback_text"):
            return stream_response

        # Send back the stream response
        return StreamingResponse(
            stream_response,
            media_type="application/octet-stream",
            headers={
                "X-Session-ID": resolved_id or "",
            },
        )
