from dataclasses import dataclass

from assistant_server.memory.store import MemoryStore
from assistant_server.rag.retriever import Retriever
from assistant_server.services.llm.base import LlmService
from assistant_server.tools.registry import ToolRegistry


# Currently handling engine, state, contracts all at once.
# state is everything that persists across turns (tool results, session id, responses etc.)

@dataclass(frozen=True)
class PipelineResult:
    text: str
    session_id: str | None


class AssistantPipeline:
    def __init__(self) -> None:
        self._llm = LlmService()
        self._tools = ToolRegistry()
        self._memory = MemoryStore()
        self._retriever = Retriever()

    def run(self, text: str, session_id: str | None = None) -> PipelineResult:
        # Placeholder orchestration contract for future STT -> tool loop -> TTS flow.

        #Context Aggregation
        user_prompt = {"role": "user", "content": text}
        memory_context = self._memory.load(session_id)
        retrieval_context = self._retriever.retrieve(text)
        tool_list = self._tools.toolList()
        
        # Call 1 to LLM
        response = self._llm.complete(user_prompt, memory_context, retrieval_context, tool_list)
        llm_text = response.content

        # Refactor Later:
        # Tool Loop

        if response.tool_calls:
            for tool in response.tool_calls:
                # Ollama turns our function list into a much of ToolCall objects, they contain a function field,
                # which is a Function object, holding a name and arguments, so we get our function from the name
                if function_to_call := self._tools.toolDict().get(tool.function.name):
                    print(f'Calling tool {tool.function.name} with arguments {tool.function.arguments}')
                    tool_response = function_to_call(**tool.function.arguments)
                    print(f'Tool response: {tool_response}')
                else:
                    print(f'Tool {tool.function.name} not found in registry.')
                
            # we use the result of the last successful tool call it seems
            # this should be replaced later with a memory call

            # add memory to get tool augmented response from LLM





        resolved_session = self._memory.save(session_id=session_id, user_text=text, assistant_text=llm_text)
        return PipelineResult(text=llm_text, session_id=resolved_session)
    


