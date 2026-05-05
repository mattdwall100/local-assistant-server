import ollama
from collections.abc import Callable
from ...core.config import get_settings
from ...core.logging import get_logger
from ollama import ChatResponse

settings = get_settings()
logger = get_logger(__name__)


class OllamaClient:
    def __init__(self):
        self.model_name = settings.model_name

    def complete(self, messages: list[dict[str, str]], tool_list: list[Callable]) -> ChatResponse:
        response = ollama.chat(self.model_name, messages=messages, tools=tool_list)
        logger.debug(f"llm_request_payload | message_count={len(messages)}")
        return response
