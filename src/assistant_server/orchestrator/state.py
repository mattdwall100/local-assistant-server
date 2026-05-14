from ollama import ChatResponse

from ..core.logging import get_logger

logger = get_logger(__name__)


class SessionState:
    """Class to hold the state of a session, including memory, retriever, and tools."""

    def __init__(
        self, session_id: str, response: ChatResponse | None, messages: list[dict[str, str]]
    ) -> None:
        self.__session_id = session_id
        self.__response = response
        self.__messages = messages
        self.toolFailStatus = False

    # Getters and setters for session state
    @property
    def session_id(self) -> str:
        return self.__session_id

    # Session id should not be changeable after initialisation

    # Getters and setters for response
    @property
    def response(self) -> ChatResponse | None:
        return self.__response

    # Response should be ChatResponse object
    @response.setter
    def response(self, new_reponse: object) -> None:
        if not isinstance(new_reponse, ChatResponse):
            logger.error(f"Attempted to set response to non-ChatResponse object: {new_reponse}")
        else:
            self.__response = new_reponse

    # Getter and setter for messages
    @property
    def messages(self) -> list[dict[str, str]]:
        return self.__messages

    @messages.setter
    def messages(self, new_messages: list[dict[str, str]]) -> None:
        if not isinstance(new_messages, list) or not all(isinstance(m, dict) for m in new_messages):
            logger.error(f"Attempted to set messages to non-list of dicts: {new_messages}")
        else:
            self.__messages = new_messages

    # uesless at the moment, will help in future tool loop with contracts and states
    def toolCallFailed(self) -> None:
        logger.warning(
            f"Tool call failed for session {self.session_id}. Current state: {self.__dict__}"
        )
        self.toolFailStatus = True
