from collections.abc import Callable, Iterator, Sequence
from typing import Any
from ollama import ChatResponse
from ...core.logging import get_logger
from .ollama_client import OllamaClient, ToolCall

logger = get_logger(__name__)


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
    ) -> tuple[str, Sequence[ToolCall] | None  | None]:
        del retrieval_context
        logger.info(f"complete started | messages={messages}")

        return self.client.complete(messages, tool_list)

    def stream_complete(
        self,
        messages: list[dict[str, str]],
    ) -> Iterator[ChatResponse]:
        """Stream (without tool calls)"""
        logger.info(f"stream_complete started | streaming llm response, messages={messages}")
        yield from self.client.stream_complete(messages)
