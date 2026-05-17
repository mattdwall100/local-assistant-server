from collections.abc import Callable, Iterable
from typing import Any

import re
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
    ) -> ChatResponse | Iterable[ChatResponse]:
        response = self.client.chat(self.model_name, messages=messages, tools=tool_list)
        logger.debug(f"llm_request_payload | message_count={len(messages)}")
        return response
    
    def stream_complete(self, messages: list[dict[str, str]]) -> Iterable[str]:
        logger.info(f"stream_complete started | streaming llm response, messages={messages}")
        token_stream = self.client.chat(self.model_name, messages=messages, stream=True)
        buffer = ""

        sentence_end_pattern = re.compile(r"([.!?]),")

        for chunk in token_stream:
            text = chunk["message"]["content"] or ""
            buffer += text

            while True:
                match = sentence_end_pattern.search(buffer)
                if not match:
                    break

                end_index = match.end()
                sentence = buffer[:end_index].strip()
                buffer = buffer[end_index:]

                if sentence:
                    yield sentence

        if buffer.strip():
            yield buffer.strip()


