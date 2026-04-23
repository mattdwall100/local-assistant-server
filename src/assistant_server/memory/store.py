import uuid


class MemoryStore:
    """In-memory placeholder session store for early milestones."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[str]] = {}

    def load(self, session_id: str | None) -> list[str]:
        if session_id is None:
            return []
        return self._sessions.get(session_id, [])

    def save(self, session_id: str | None, user_text: str, assistant_text: str) -> str:
        resolved_session = session_id or str(uuid.uuid4()) # generates a new id if None
        self._sessions.setdefault(resolved_session, []).extend(
            [f"user: {user_text}", f"assistant: {assistant_text}"]
        )
        return resolved_session

