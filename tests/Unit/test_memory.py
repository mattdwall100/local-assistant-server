from assistant_server.memory.store import MemoryStore


def test_memory_store_saves_and_loads_messages() -> None:
    # Arrange
    memory = MemoryStore()
    messages = [{"role": "user", "content": "hello"}]

    # Act
    session_id = memory.update(None, messages)
    loaded_messages = memory.load(session_id)

    # Assert
    assert session_id
    assert loaded_messages == messages


def test_memory_store_returns_empty_history_for_missing_session() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    messages = memory.load("missing-session")

    # Assert
    assert messages == []
