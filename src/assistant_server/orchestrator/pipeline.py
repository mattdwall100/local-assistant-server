import re
from collections.abc import Callable, Generator, Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from itertools import chain
from typing import Any

from mypy_extensions import KwArg

from ..api.schemas import FallbackStream
from ..core.logging import get_logger
from ..memory.store import MemoryStore
from ..rag.retriever import Retriever
from ..services.llm.base import LlmService
from ..services.llm.ollama_client import OllamaClient
from ..services.stt.base import SttService
from ..services.stt.fasterWhisper_client import FasterWhisperSTT
from ..services.tts.base import TtsService
from ..services.tts.piper_client import PiperTTS
from ..tools.base import ToolRegistry
from ..utils.latency_logger import log_latency
from .fallback import FallbackHandler
from .state import SessionState

logger = get_logger(__name__)

# Currently handling engine, state, contracts all at once.
# state is everything that persists across turns (tool results, session id, responses etc.)


@dataclass(frozen=True)
class PipelineResult:
    text: str
    session_id: str


class AssistantPipeline:
    def __init__(
        self,
        stt: FasterWhisperSTT,
        llm: OllamaClient,
        routing_llm: OllamaClient,
        tts: PiperTTS,
        fallback_handler: FallbackHandler,
        memory: MemoryStore,
        tools: ToolRegistry,
        retriever: Retriever,
    ) -> None:
        logger.info("AssistantPipeline __init__ starting...")
        self._stt = SttService(stt)
        self._llm = LlmService(llm)
        self._routing_llm = LlmService(routing_llm)
        with log_latency(logger, "ollama warmup() complete"):
            self._llm.warmup()
            self._routing_llm.warmup()
        self._tts = TtsService(tts)

        self._fallback_handler = fallback_handler
        self._memory = memory
        self._tools = tools
        self._retriever = retriever

        self._activity = datetime.now()

    def run(
        self, audio_bytes: BytesIO, session_id: str
    ) -> tuple[Iterator[Any] | FallbackStream, str]:
        """Runs the full STT -> (LLM + tools) -> TTS Pipeline

         - "with log_latency" is a context manager to track and log event latency
         - "self.fallback_handler.handle(event_name, e)" attempts to return a graceful degredation
        of AudioStream's containing fallback audio, with fallback text in header"""

        logger.info(f"pipeline_started | session_id={session_id}")
        session_id = self._memory.resolve_session(session_id)
        self.update_activity()  # Update activity to now

        with log_latency(logger, "pipeline_completed", session_id=session_id):
            # Give to STT
            try:
                with log_latency(logger, "stt_completed", session_id=session_id):
                    text = self._stt.transcribe(audio_bytes)
            except Exception as e:
                # error logged by log_latency error handling
                return self._fallback_handler.handle("stt", e, session_id), session_id

            # Give to LLM for a reply
            try:
                # run main llm pipeline
                session_state = self.run_llm(text, session_id)
            except Exception as e:
                # no log_latency to log the error here
                logger.error(f"run_llm failed | exception={str(e)}")
                return self._fallback_handler.handle("llm", e, session_id), session_id

            resolved_id = session_state.session_id

            # Give to TTS (Create the audio bytes stream), This generates the stream object,
            # real TTS latency is measured in chunks by the client or in a deeper wrapper
            try:
                with log_latency(logger, "tts_stream_setup", session_id=resolved_id):
                    if session_state.response_message is None:
                        session_state.response_message = ""

                    if isinstance(session_state.response_message, str):
                        stream_response = self._tts.stream_synthesize(
                            session_state.response_message
                        )
                    else:
                        stream_response = self._tts.stream_in_stream_out(
                            session_state.response_message
                        )
            except Exception as e:
                # log_latency logs error
                return self._fallback_handler.handle("tts", e, resolved_id), resolved_id

            return stream_response, resolved_id

    def run_llm(self, text: str, session_id: str = "") -> SessionState:
        """Main pipeline method: process user input, return response w/ resolved session id."""
        session_id = self._memory.resolve_session(session_id)

        # Context Aggregation
        user_prompt = {"role": "user", "content": text}
        memory_context = self._memory.load_chat_history(session_id)
        retrieval_context = self._retriever.retrieve(text)
        tool_list = self._tools.toolList()

        memory_context.append(user_prompt)
        messages = memory_context

        # Call to tool routing LLM
        with log_latency(
            logger, "routing_llm_inference_completed", session_id=session_id, phase="initial_call"
        ):
            # THIS ACTS AS THE ROUTING LLM CALL
            response_message, tool_calls = self._routing_llm.router_complete(user_prompt, tool_list)

        # Save response to chat history
        # messages.append({"role": "assistant", "content": response_message})

        # Initialise session state object to pass session info b/n orchestrator functionalities
        # For future use when loop becomes complicated and contracts are involved
        session_state = SessionState(
            session_id=session_id,
            response_message=response_message,
            tool_calls=tool_calls,
            messages=messages,
        )

        # Check for tool calls, if they exist call them and update state accordingly,
        # then update message sequence etc and make new call
        session_state = self.tool_calling(session_state)

        # CHAT LLM STREAM RESPONSE, AND UPDATES CHAT HISTORY
        with log_latency(logger, "llm_stream_setup", session_id=session_id, phase="post_tool_call"):
            iter_response = self.remember_llm_stream(
                session_state.messages, session_state.session_id
            )

        # and gain a reoslved session id (new if was empty, same if was given)
        # self._memory.update_chat_history(
        #    session_id=session_state.session_id, messages=session_state.messages
        # )
        session_state.response_message = iter_response
        self.update_activity()  # Update last active status to now
        return session_state

    def tool_calling(self, session_state: SessionState) -> SessionState:
        # This is all Ollama / llm service logic that can be isolated once loop is multi-step

        """Checks for tool calls in the response, executes them,
        updates the session state, and makes a new LLM call if needed."""

        response_message = session_state.response_message
        tool_calls = session_state.tool_calls
        messages = session_state.messages
        session_id = session_state.session_id

        if tool_calls:
            logger.info(
                f"tool_calling evals started | \
                    session_id={session_id} tool_count={len(tool_calls)}"
            )
            for tool in tool_calls:
                if function_to_call := self._tools.toolDict().get(tool.function.name):
                    with log_latency(
                        logger,
                        "tool_execution_completed",
                        session_id=session_id,
                        tool_name=tool.function.name,
                    ):
                        # Inject tool dependencies as necessary
                        tool_response = self.call_tool_with_injected_dependencies(
                            function_to_call,
                            tool.function.arguments,
                            memory=self._memory,
                            session_id=session_id,
                        )
                        messages.append({"role": "assistant", "content": response_message})
                        messages.append(
                            {
                                "role": "tool",
                                "content": str(tool_response),
                                "tool_name": tool.function.name,
                            }
                        )
                    session_state.toolsCalledStatus = True
                else:
                    logger.warning(
                        f"tool_not_found | session_id={session_id} tool_name={tool.function.name}"
                    )

        session_state.messages = messages
        return session_state

    def call_tool_with_injected_dependencies(
        self,
        func: Callable[[KwArg(Any)], str],
        func_kwargs: Mapping[str, Any],
        *,  # force label below args
        memory: MemoryStore,
        session_id: str,
    ) -> str:
        # copy dict or dict-like Mapping
        kwargs_new = dict(func_kwargs)
        # add memory/session_id dependencies
        kwargs_new["memory"] = memory
        kwargs_new["session_id"] = session_id

        return func(**kwargs_new)

    def remember_llm_stream(self, messages: list[dict[str, str]], session_id: str) -> Iterator[str]:
        token_stream = self._llm.stream_complete(messages)
        buffer = ""
        aggregated_text = []

        # Flush on sentence-ending punctuation followed by whitespace
        sentence_end_pattern = re.compile(r"[.!?,]+(?=\s)")
        # Safety flush threshold so long punctuation-free runs still reach TTS
        max_buffer_chars = 400

        # Time from first consumption of this generator to first Ollama token
        with log_latency(logger, "first_llm_token_received", session_id=session_id):
            first_chunk = next(token_stream, None)

        for chunk in chain([first_chunk] if first_chunk is not None else [], token_stream):
            text = chunk["message"]["content"] or ""
            buffer += text
            aggregated_text.append(text)

            while True:
                match = sentence_end_pattern.search(buffer)
                if not match:
                    break

                end_index = match.end()
                sentence = buffer[:end_index].strip()
                buffer = buffer[end_index:]

                if sentence:
                    yield sentence

            if len(buffer) >= max_buffer_chars:
                sentence = buffer.strip()
                buffer = ""
                if sentence:
                    yield sentence

        if buffer.strip():
            yield buffer.strip()

        message = "".join(aggregated_text)
        messages.append({"role": "assistant", "content": message})
        self._memory.update_chat_history(session_id, messages)

    def transcribe(self, audio_bytes: BytesIO) -> str:
        return self._stt.transcribe(audio_bytes)

    def stream_synthesize(self, text: str) -> Generator[bytes, Any, Any]:
        yield from self._tts.stream_synthesize(text)

    def update_activity(self) -> None:
        """Updates latest activity time to now, called upon request and return of pipeline calls"""
        logger.info("update_activity suceeded")
        self._activity = datetime.now()

    def get_activity(self) -> str:
        """Returns latest activity time. Used for external lifecycle management of app instance"""
        return str(self._activity)
