from dataclasses import dataclass
from typing import Tuple

from assistant_server.services.llm.base import LlmService
from assistant_server.services.stt.base import SttService
from assistant_server.services.tts.base import TtsService

from assistant_server.memory.store import MemoryStore
from assistant_server.rag.retriever import Retriever
from assistant_server.tools.base import ToolRegistry

from .state import SessionState
from assistant_server.core.logging import get_logger
from assistant_server.utils.latency_logger import log_latency

logger = get_logger(__name__)

# Currently handling engine, state, contracts all at once.
# state is everything that persists across turns (tool results, session id, responses etc.)

@dataclass(frozen=True)
class PipelineResult:
    text: str
    session_id: str | None


class AssistantPipeline:
    def __init__(self) -> None:
        self._stt = SttService()
        self._llm = LlmService()
        self._tts = TtsService()

        self._tools = ToolRegistry()
        self._memory = MemoryStore()
        self._retriever = Retriever()

    def run(self, audio_bytes: bytes, session_id: str | None) -> Tuple[bytes, str]:
        """Runs the full STT -> (LLM + tools) -> TTS Pipeline"""
        logger.info(f"pipeline_started | session_id={session_id}")
        
        with log_latency(logger, "pipeline_completed", session_id=session_id):
            # Give to STT
            with log_latency(logger, "stt_completed", session_id=session_id):
                text = self._stt.transcribe(audio_bytes)
    
            # Give to LLM for a reply
            result = self.run_llm(text, session_id)
            reply = result.text
            resolved_id = result.session_id
    
            # Give to TTS (Create the audio bytes stream)
            # This generates the stream object, real TTS latency is measured in chunks by the client or in a deeper wrapper
            with log_latency(logger, "tts_stream_initialized", session_id=resolved_id):
                stream_response = self._tts.stream_synthesize(reply)
    
            return stream_response, resolved_id


    def run_llm(self, text: str, session_id: str | None = None) -> PipelineResult:
        """Main pipeline method to process user input and return a response, along with an updated session id."""

        #Context Aggregation
        user_prompt = {"role": "user", "content": text}
        memory_context = self._memory.load(session_id)
        retrieval_context = self._retriever.retrieve(text)
        tool_list = self._tools.toolRegistry()

        memory_context.append(user_prompt)
        messages = memory_context

        # Call 1 to LLM
        with log_latency(logger, "llm_inference_completed", session_id=session_id, phase="initial_call"):
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
            logger.info(f"tool_evaluation_started | session_id={session_id} tool_count={len(response.message.tool_calls)}")
            for tool in response.message.tool_calls:
                if function_to_call := self._tools.toolDict().get(tool.function.name):
                    toolsCalled = True

                    with log_latency(logger, "tool_execution_completed", session_id=session_id, tool_name=tool.function.name):
                        tool_response = function_to_call(**tool.function.arguments)
                        messages.append({'role': 'tool', 'content': str(tool_response), 'tool_name': tool.function.name})
                else:
                    logger.warning(f"tool_not_found | session_id={session_id} tool_name={tool.function.name}")
            
            if toolsCalled:
                with log_latency(logger, "llm_inference_completed", session_id=session_id, phase="post_tool_call"):
                    response = self._llm.complete(messages, retrieval_context=None, tool_list=None)
                
                messages.append({
                    "role": "assistant",
                    "content": response.message.content
                })
            else:
                session_state.toolCallFailed()

        session_state.messages = messages
        session_state.response = response

        return session_state
