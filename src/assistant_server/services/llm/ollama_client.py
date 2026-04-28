import ollama
from assistant_server.core.config import get_settings
from assistant_server.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

class OllamaClient:
    def __init__(self):
        self.model_name = settings.model_name

    def complete(
            self, 
            messages: list[dict[str, str]],
            tool_list: list[callable]
            ) -> str:
        response = ollama.chat(
            self.model_name,
            messages=messages,
            tools=tool_list
        )
        logger.debug(f"llm_request_payload | message_count={len(messages)}")
        return response