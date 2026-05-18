from collections.abc import Iterator, Sequence

from ..core.logging import get_logger
from ..services.llm.ollama_client import ToolCall

logger = get_logger(__name__)


class SessionState:
    """Class to hold the state of a session, including memory, retriever, and tools."""

    def __init__(
        self,
        session_id: str,
        response_message: str | Iterator[str] | None,
        tool_calls: Sequence[ToolCall] | None,
        messages: list[dict[str, str]],
    ) -> None:
        self._session_id = session_id
        self.response_message = response_message
        self.tool_calls = tool_calls
        self._messages = messages
        self.toolsCalledStatus = False

    # Getters and setters for session state
    @property
    def session_id(self) -> str:
        return self._session_id

    # Session id should not be changeable after initialisation

    # Getter and setter for messages
    @property
    def messages(self) -> list[dict[str, str]]:
        return self._messages

    @messages.setter
    def messages(self, new_messages: list[dict[str, str]]) -> None:
        if not isinstance(new_messages, list) or not all(isinstance(m, dict) for m in new_messages):
            logger.error(f"Attempted to set messages to non-list of dicts: {new_messages}")
        else:
            self._messages = new_messages
