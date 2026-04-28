from fastapi import FastAPI

from .api.router import api_router
from .core.config import get_settings
from .core.logging import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)
    return app


logger.info("Starting assistant server...")
app = create_app()
