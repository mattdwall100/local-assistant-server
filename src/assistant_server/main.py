from fastapi import FastAPI

from assistant_server.api.router import api_router
from assistant_server.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)
    return app

from .core.logging import get_logger
logger = get_logger()

logger.info("Starting local assistant server...")

app = create_app()



# This is the main application entry point:
# - To run the server, use the command: `uvicorn assistant_server.main:app --reload`
# - The `--reload` flag enables hot-reloading during development, so the server will automatically restart when you make changes to the code.
# - It should include the fast api app, exposed to uvicorn, and any necessary startup events or middleware such as CORS, logging, etc.
# - we configure the app to incude the api routers
# - we add any other necessary server set up features.
# - We attach startup and shutdown hooks/events to the app, to handle any necessary initialization and cleanup tasks when the server starts and stops.
# - 