from collections.abc import Callable, Iterator, Sequence
from typing import Any, TypeAlias

import ollama
from mypy_extensions import KwArg
from ollama import ChatResponse, Message

# from ...orchestrator.state import ToolCall
from ...core.config import get_settings
from ...core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


ToolCall: TypeAlias = Message.ToolCall
ToolCallFunction: TypeAlias = Message.ToolCall.Function


class OllamaClient:
    def __init__(self, modelname: str) -> None:
        self.model_name = modelname
        self.client = ollama

    def warmup(self) -> None:
        self.client.generate(
            model=self.model_name,
            prompt="",
            stream=False,
        )

    def complete(
        self,
        messages: list[dict[str, str]],
        tool_list: list[Callable[[KwArg(Any)], str]] | None = None,
    ) -> tuple[str, Sequence[ToolCall]]:
        if not tool_list:
            tool_list = []

        response = self.client.chat(
            self.model_name, messages=messages, tools=tool_list, stream=False
        )
        logger.debug(f"llm_request_payload | message_count={len(messages)}")
        return response.message.content or "", response.message.tool_calls or []

    def stream_complete(self, messages: list[dict[str, str]]) -> Iterator[ChatResponse]:
        """Will stream phrase-by-phrase chunks"""

        logger.info(f"stream_complete started | streaming llm response, messages={messages}")
        yield from self.client.chat(self.model_name, messages=messages, stream=True)
