# Could maybe split this into a base.py and then an ollama_client.py, that way can switch to llama.cpp later if needed, without switching the interface.
# this is an abstraction layer for the LLM, by keeping our code modular we can easily swap out the underlying implementation (ollama, llama.cpp, etc.)
# for now we will just leave as, in future refactor all services to be modular and abstracted via a wrapper interface
from .ollama_client import OllamaClient


class LlmService:
    """LLM service abstraction."""

    def __init__(self):
        self.client = OllamaClient() ## In the future this can be changed if needed

    def complete(
        self,
        user_text: dict[str, str],
        memory_context: list[str],
        retrieval_context: list[str],
        tool_list: list[callable],
    ) -> str:
        del memory_context, retrieval_context, tool_list
        
        return self.client.complete(user_text, tool_list)
