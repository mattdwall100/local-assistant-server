from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse


from ..api.dependencies import get_orchestrator
from ..core.logging import get_logger
from ..orchestrator.pipeline import AssistantPipeline
from ..utils.latency_logger import log_latency
from .schemas import ActivityResponse, ChatRequest, ChatResponse, HealthResponse, FallbackStream

api_router = APIRouter()

logger = get_logger(__name__)


@api_router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@api_router.post("/chat", response_model=ChatResponse)
def chat(
    orchestrator: Annotated[AssistantPipeline, Depends(get_orchestrator)], payload: ChatRequest
) -> ChatResponse:
    session_id = payload.session_id or ""
    logger.info(f"request_received | endpoint=/chat session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/chat", session_id=session_id):
        session_state = orchestrator.run_llm(payload.text, session_id)

        if session_state.response_message is None:
           session_state.response_message = ""
        if not isinstance(session_state.response_message, str):
            session_state.response_message = "".join(session_state.response_message)

        return ChatResponse(
            text=session_state.response_message, session_id=session_state.session_id
        )


@api_router.get("/activity", response_model=ActivityResponse)
def activity(
    orchestrator: Annotated[AssistantPipeline, Depends(get_orchestrator)],
) -> ActivityResponse:
    logger.info("request_received | endpoint=/activity")
    try:
        return ActivityResponse(
            last_activity_time=orchestrator.get_activity(),
            status_code=200,
        )
    except Exception as e:
        logger.error(f"/activity failed | internal server error exception={e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@api_router.post("/transcribe", response_model=ChatResponse)
async def transcribe(
    orchestrator: Annotated[AssistantPipeline, Depends(get_orchestrator)],
    file: Annotated[UploadFile, File()],
    session_id: Annotated[str | None, Form()] = None,
) -> ChatResponse:
    session_id = session_id or ""

    logger.info(f"request_received | endpoint=/transcribe session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/transcribe", session_id=session_id):
        audio_bytes = await file.read()
        audio_stream = BytesIO(audio_bytes)
        audio_stream.seek(0)

        text = orchestrator.transcribe(audio_stream)
        return ChatResponse(text=text, session_id=session_id)


@api_router.post("/synthesize")
def synthesize(
    orchestrator: Annotated[AssistantPipeline, Depends(get_orchestrator)],
    payload: ChatRequest,
) -> StreamingResponse:
    """Send a stream of bytes back to the client, speaking the text sent"""
    session_id = payload.session_id or ""
    logger.info(f"request_received | endpoint=/synthesize session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/synthesize", session_id=session_id):
        return StreamingResponse(
            orchestrator.stream_synthesize(payload.text),
            media_type="application/octet-stream",
            headers={"X-Session-ID": ""},
        )


@api_router.post("/speak")
async def speak(
    orchestrator: Annotated[AssistantPipeline, Depends(get_orchestrator)],
    file: Annotated[UploadFile, File()],
    session_id: Annotated[str | None, Form()] = None,
) -> StreamingResponse:
    session_id = session_id or ""
    logger.info(f"request_received | endpoint=/speak session_id={session_id}")
    with log_latency(logger, "request_completed", endpoint="/speak", session_id=session_id):
        # Recieve raw bytes and format to wrapped BytesIO
        raw_bytes = await file.read()
        audio_bytes = BytesIO(raw_bytes)
        audio_bytes.seek(0)

        # Send to pipeline
        stream_response, resolved_id = orchestrator.run(audio_bytes, session_id)

        # NOTE May not be necessary anymore
        # if has .fallback_text, is a AudioStream object, send as is
        if isinstance(stream_response, FallbackStream):
            return stream_response

        # Send back the stream response
        return StreamingResponse(
            stream_response,
            media_type="application/octet-stream",
            headers={
                "X-Session-ID": resolved_id or "",
            },
        )
