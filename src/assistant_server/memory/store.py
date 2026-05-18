import uuid

from pydantic import BaseModel, ConfigDict

from ..core.logging import get_logger
from .papers import PapersManager

logger = get_logger(__name__)


class SessionMemory(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history: list[dict[str, str]]
    papers_manager: PapersManager


class MemoryStore:
    """In-memory placeholder session store for early milestones."""

    def __init__(self) -> None:
        self._sessions: dict[str, SessionMemory] = {}

    def _new_session(self, resolved_session: str) -> None:
        logger.info(
            f"_new_session | creating SessionMemory for resolved_session={resolved_session}"
        )
        self._sessions[resolved_session] = SessionMemory(
            chat_history=[], papers_manager=PapersManager()
        )

    def resolve_session(self, session_id: str) -> str:
        session_id = session_id or ""
        if not isinstance(session_id, str):
            raise ValueError(
                f"resolve_session failed | session_id must be str, session_id={session_id}"
            )

        # if exists and recorded, return as is
        if session_id in self._sessions.keys():
            return session_id

        # if str empty, create id, if not, use as is. create record for result
        resolved_session = session_id or str(uuid.uuid4())
        self._new_session(resolved_session)
        return resolved_session

    def load_chat_history(self, session_id: str) -> list[dict[str, str]]:
        try:
            resolved_session = self.resolve_session(session_id)
        except ValueError as e:
            logger.error(
                f"load_chat_history failed | session_id must be str, session_id={session_id}"
            )
            raise e

        return self._sessions[resolved_session].chat_history

    def update_chat_history(self, session_id: str, messages: list[dict[str, str]]) -> str:
        # Protective of chat history
        session_id = session_id or ""
        if not isinstance(messages, list):
            raise ValueError(
                f"update_chat_history failed | messages must be list, messages={messages}"
            )

        for message in messages:
            if not isinstance(message, dict):
                raise ValueError(
                    f"update_chat_history failed | message must be dict, messages={messages}"
                )

            for key, value in message.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ValueError(
                        f"update_chat_history failed | \
                            message items must be str's, messages={messages}"
                    )

        try:
            resolved_session = self.resolve_session(session_id)
        except ValueError as e:
            logger.error(
                f"update_chat_history failed | session_id must be str, session_id={session_id}"
            )
            raise e

        self._sessions[resolved_session].chat_history = messages
        return resolved_session

    def get_papers_manager(self, session_id: str) -> PapersManager:
        try:
            resolved_session = self.resolve_session(session_id)
        except ValueError as e:
            logger.error(
                f"update_chat_history failed | session_id must be str, session_id={session_id}"
            )
            raise e

        return self._sessions[resolved_session].papers_manager
