from collections.abc import Callable

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .core.config import get_settings
from .core.logging import get_logger
from .dependencies import Services, create_services
from .orchestrator.pipeline import AssistantPipeline


def create_app(
    service_factory: Callable[[], Services] = create_services,
) -> FastAPI:
    services = service_factory()
    orchestrator = AssistantPipeline(
        stt=services.stt,
        llm=services.llm,
        routing_llm=services.routing_llm,
        tts=services.tts,
        fallback_handler=services.fallback_handler,
        memory=services.memory,
        tools=services.tools,
        retriever=services.retriever,
    )

    app = FastAPI(title=get_settings().app_name)
    app.state.orchestrator = orchestrator

    # Allow the browser-based web client (served from file:// or any local origin) to call
    # this API and read the custom response headers on /speak. No credentials are used.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Session-ID", "X-Transcript", "X-Tool-Calls", "X-Fallback-TXT"],
    )

    app.include_router(api_router)
    return app


if __name__ == "__main__":
    get_logger(__name__).info("Starting assistant server...")

    settings = get_settings()
    # app = create_app(settings)

    uvicorn.run(
        "assistant_server.main:create_app",
        factory=True,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "dev",
        log_level=settings.log_level.lower(),
    )
