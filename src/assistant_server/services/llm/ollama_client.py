from collections.abc import Callable
from typing import Any

import ollama
from ollama import ChatResponse

from ...core.config import get_settings
from ...core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class OllamaClient:
    def __init__(self) -> None:
        self.model_name = settings.modelname
        self.client = ollama

    def warmup(self) -> None:
        self.client.generate(
            model=self.model_name,
            prompt="",
            stream=False,
        )

    def complete(
        self, messages: list[dict[str, str]], tool_list: list[Callable[[Any], str]]
    ) -> ChatResponse:
        response = self.client.chat(self.model_name, messages=messages, tools=tool_list)
        logger.debug(f"llm_request_payload | message_count={len(messages)}")
        return response
