from assistant_server.memory.store import MemoryStore
from assistant_server.tools.implementations import papers as paper_tools


def _save_papers(memory: MemoryStore, session_id: str, count: int = 5) -> None:
    papers = memory.get_papers_manager(session_id)
    for internal_id in range(1, count + 1):
        papers.save_paper(
            internal_id=internal_id,
            title=f"Paper {internal_id}",
            summary=f"Summary {internal_id}",
            id=f"2401.0000{internal_id}",
            organization=None,
        )


def test_list_titles_returns_numbered_titles_for_session_papers() -> None:
    # Arrange
    memory = MemoryStore()
    _save_papers(memory=memory, session_id="session-1")

    # Act
    result = paper_tools.list_titles(memory=memory, session_id="session-1")

    # Assert
    assert result == "1: Paper 1. 2: Paper 2. 3: Paper 3. 4: Paper 4. 5: Paper 5."


def test_list_titles_returns_fetch_first_error_when_no_papers_are_loaded() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    result = paper_tools.list_titles(memory=memory, session_id="session-1")

    # Assert
    assert result == "ERROR: Need to get papers before listing them"


def test_get_summary_returns_saved_summary() -> None:
    # Arrange
    memory = MemoryStore()
    _save_papers(memory=memory, session_id="session-1")

    # Act
    result = paper_tools.get_summary(2, memory=memory, session_id="session-1")

    # Assert
    assert result == "Summary 2"


def test_get_summary_returns_validation_error_for_invalid_internal_id() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    result = paper_tools.get_summary(0, memory=memory, session_id="session-1")

    # Assert
    assert result == "ERROR: Invalid internal_id used, must be between 1 and 5, tried with 0"


def test_get_summary_returns_missing_error_for_unloaded_internal_id() -> None:
    # Arrange
    memory = MemoryStore()
    memory.get_papers_manager("session-1").save_paper(
        internal_id=1,
        title="Only Paper",
        summary="Only Summary",
        id="2401.00001",
        organization=None,
    )

    # Act
    result = paper_tools.get_summary(2, memory=memory, session_id="session-1")

    # Assert
    assert result == "ERROR: Couldnt find all the paper for id=2"


def test_stage_paper_sets_staged_paper_for_later_tools() -> None:
    # Arrange
    memory = MemoryStore()
    _save_papers(memory, "session-1")

    # Act
    result = paper_tools.stage_paper(4, memory=memory, session_id="session-1")

    # Assert
    assert result == "Successfully staged paper with id=4"
    assert paper_tools.get_staged_id(memory=memory, session_id="session-1") == "4"


def test_stage_paper_returns_missing_error_when_paper_was_not_loaded() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    result = paper_tools.stage_paper(1, memory=memory, session_id="session-1")

    # Assert
    assert result == "ERROR: Couldnt find the paper for id=1"


def test_get_staged_title_returns_error_when_nothing_is_staged() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    result = paper_tools.get_staged_id(memory=memory, session_id="session-1")

    # Assert
    assert result == "ERROR: No paper is staged"
