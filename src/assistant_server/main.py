from collections.abc import Callable
from typing import Any
import uvicorn
from fastapi import FastAPI

from .api.router import api_router
from .core.config import get_settings
from .core.logging import get_logger
from .dependencies import create_services
from .orchestrator.pipeline import AssistantPipeline


def create_app(
    service_factory: Callable[[], dict[str, object]] = create_services,
) -> FastAPI:
    services = service_factory()
    orchestrator = AssistantPipeline(**services)

    app = FastAPI(title=get_settings().app_name)
    app.state.orchestrator = orchestrator

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
