from collections.abc import Callable
from typing import Any

from ollama import ChatResponse

from .ollama_client import OllamaClient


class LlmService:
    """LLM service abstraction."""

    def __init__(self, llm_client: OllamaClient) -> None:
        self.client = llm_client

    def warmup(self) -> None:
        self.client.warmup()

    def complete(
        self,
        messages: list[dict[str, str]],
        retrieval_context: list[str] | None,
        tool_list: list[Callable[[Any], str]] | None,
    ) -> ChatResponse:
        del retrieval_context

        return self.client.complete(messages, tool_list)
