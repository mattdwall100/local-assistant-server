import uuid


class MemoryStore:
    """In-memory placeholder session store for early milestones."""

    def __init__(self) -> None:
        # Connects uuids with message histories
        self._sessions: dict[str, list[dict[str, str]]] = {}

    def load(self, session_id: str | None) -> list[dict[str, str]]:
        if session_id is None:
            return []
        messages = self._sessions.get(session_id, [])
        if messages:
            return messages
        else:
            return []
        
    def update(self, session_id: str | None, messages: list[dict[str,]]) -> str:
        resolved_session = session_id or str(uuid.uuid4()) # generates a new id if None
        self._sessions[resolved_session] = messages
        return resolved_session

