# Could maybe split this into a base.py and then an ollama_client.py, that way can switch to llama.cpp later if needed, without switching the interface.
# this is an abstraction layer for the LLM, by keeping our code modular we can easily swap out the underlying implementation (ollama, llama.cpp, etc.)
# for now we will just leave as, in future refactor all services to be modular and abstracted via a wrapper interface
from .ollama_client import OllamaClient
from collections.abc import Callable

class LlmService:
    """LLM service abstraction."""

    def __init__(self, llm_client):
        self.client = llm_client  ## In the future this can be changed if needed

    def complete(
        self,
        messages: list[dict[str, str]],
        retrieval_context: list[str],
        tool_list: list[Callable],
    ) -> str:
        del retrieval_context

        return self.client.complete(messages, tool_list)
