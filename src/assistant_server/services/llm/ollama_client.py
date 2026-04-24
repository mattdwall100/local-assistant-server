import ollama
from assistant_server.core.config import get_settings

settings = get_settings()

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
        print(messages)
        return response