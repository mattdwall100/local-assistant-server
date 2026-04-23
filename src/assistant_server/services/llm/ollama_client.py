import ollama
from assistant_server.core.config import get_settings

settings = get_settings()

class OllamaClient:
    def __init__(self):
        self.model_name = settings.model_name

    def complete(self, prompt: str) -> str:
        response = ollama.chat(
            self.model_name,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.message