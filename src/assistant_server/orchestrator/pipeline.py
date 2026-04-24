from dataclasses import dataclass

from assistant_server.memory.store import MemoryStore
from assistant_server.rag.retriever import Retriever
from assistant_server.services.llm.base import LlmService
from assistant_server.tools.base import ToolRegistry

from .state import SessionState


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
# 
    def run(self, text: str, session_id: str | None = None) -> PipelineResult:
        """Main pipeline method to process user input and return a response, along with an updated session id."""

        #Context Aggregation
        user_prompt = {"role": "user", "content": text}
        memory_context = self._memory.load(session_id)
        retrieval_context = self._retriever.retrieve(text)
        tool_list = self._tools.toolRegistry()

        memory_context.append(user_prompt)
        messages = memory_context

        # Call 1 to LLM
        print(messages)
        response = self._llm.complete(messages, retrieval_context, tool_list)
        
        # Save response to chat history
        messages.append({
            "role": "assistant",
            "content": response.message.content
        })

        # Initialise session state oobject to pass session information between orchestrator functionalities
        session_state = SessionState(
            session_id=session_id,
            response=response,
            messages=messages
        )

        # Check for tool calls, if they exist call them and update state accordingly, then update message sequence etc and make new call
        session_state = self.tool_calling(session_state)

        # Update our memory of chat history, and gain a reoslved session id (new if was empty, same if was given)
        resolved_session = self._memory.update(
            session_id=session_state.session_id, 
            messages=session_state.messages
            )
        
        return PipelineResult(
            text=session_state.response.message.content, 
            session_id=resolved_session
            )
    
    def tool_calling(self, session_state: SessionState) -> SessionState:
        """Checks for tool calls in the response, executes them, updates the session state, and makes a new LLM call if needed."""

        response = session_state.response
        messages = session_state.messages
        session_id = session_state.session_id


        toolsCalled = False
        if response.message.tool_calls:
            print('attempting tool calls')
            for tool in response.message.tool_calls:
                # Ollama turns our function list into a much of ToolCall objects, they contain a function field,
                # which is a Function object, holding a name and arguments, so we get our function from the name
                if function_to_call := self._tools.toolDict().get(tool.function.name):
                    toolsCalled = True

                    print(f'Calling tool {tool.function.name} with arguments {tool.function.arguments}')
                    tool_response = function_to_call(**tool.function.arguments)
                    print(f'Tool response: {tool_response}')
                    messages.append({'role': 'tool', 'content': str(tool_response), 'tool_name': tool.function.name})
                    print("added tool response to messages")
                else:
                    # If a tool call fails by name call
                    print(f'Tool {tool.function.name} not found in registry.')
            

            # if there was a successful tool call, toolsCalled = True
            if toolsCalled:
                # we will get a new tool-augmented response to overwrite the first, we provide it no tool calls because we dont want an infinite loop
                response = self._llm.complete(messages, retrieval_context=None, tool_list=None)
                # save response to chat history
                 # Save response to chat history
                messages.append({
                    "role": "assistant",
                    "content": response.message.content
                })
            else:
                # TEMPORARY {if all tool calls fail, we return with a disclaimer
                session_state.toolCallFailed()


        session_state.messages = messages
        session_state.response = response

        return session_state
    
    


