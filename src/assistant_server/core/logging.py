"""Core logging logic and configuration."""
# everywhere else should just import the logger from this module, and use it for logging, rather than configuring logging separately in each module. This way we can ensure a consistent logging configuration across the entire application, and avoid issues with multiple loggers or conflicting configurations. By centralizing logging in the core module, we can also easily manage log levels, formats, and handlers from a single location, making it easier to maintain and update our logging strategy as needed.
import logging
from .config import get_settings

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level), # Since settings.log_level is a string, we use getattr to get the corresponding logging level constant from the logging module (e.g. logging.INFO, logging.DEBUG, etc.)
    format="[%(asctime)s]{%(name)s}<%(levelname)s>:: %(message)s",
    )

def get_logger() -> logging.Logger:
    """Get a logger instance with the file name."""
    return logging.getLogger(__name__)
