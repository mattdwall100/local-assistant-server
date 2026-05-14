import pytest

from assistant_server.memory.papers import PapersManager
from assistant_server.memory.store import MemoryStore


def _paper_kwargs(internal_id: int, title: str | None = None) -> dict[str, object]:
    return {
        "internal_id": internal_id,
        "title": title or f"Paper {internal_id}",
        "summary": f"Summary {internal_id}",
        "arxiv_id": f"2401.0000{internal_id}",
        "organization": None,
    }


def test_memory_store_returns_same_papers_manager_for_existing_session() -> None:
    # Arrange
    memory = MemoryStore()
    papers = memory.get_papers_manager("session-1")
    papers.save_paper(**_paper_kwargs(1))

    # Act
    same_papers = memory.get_papers_manager("session-1")

    # Assert
    assert same_papers.get_summary(1) == "Summary 1"


def test_memory_store_keeps_papers_isolated_between_sessions() -> None:
    # Arrange
    memory = MemoryStore()
    memory.get_papers_manager("session-1").save_paper(**_paper_kwargs(1))

    # Act
    other_papers = memory.get_papers_manager("session-2")

    # Assert
    with pytest.raises(AttributeError):
        other_papers.get_summary(1)


def test_papers_manager_lists_titles_after_five_papers_are_saved() -> None:
    # Arrange
    papers = PapersManager()
    for internal_id in range(1, 6):
        papers.save_paper(**_paper_kwargs(internal_id))

    # Act
    titles = papers.list_titles()

    # Assert
    assert titles == ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"]


def test_papers_manager_requires_complete_fetch_before_listing_titles() -> None:
    # Arrange
    papers = PapersManager()
    for internal_id in range(1, 5):
        papers.save_paper(**_paper_kwargs(internal_id))

    # Act / Assert
    with pytest.raises(AttributeError, match="couldnt find all papers"):
        papers.list_titles()


def test_papers_manager_returns_summary_for_saved_internal_id() -> None:
    # Arrange
    papers = PapersManager()
    papers.save_paper(**_paper_kwargs(1, title="Readable Paper"))

    # Act
    summary = papers.get_summary(1)

    # Assert
    assert summary == "Summary 1"


def test_papers_manager_rejects_invalid_summary_internal_id() -> None:
    # Arrange
    papers = PapersManager()

    # Act / Assert
    with pytest.raises(ValueError, match="internal_id must be in"):
        papers.get_summary(6)


def test_papers_manager_stages_and_clears_selected_paper() -> None:
    # Arrange
    papers = PapersManager()
    for internal_id in range(1, 6):
        papers.save_paper(**_paper_kwargs(internal_id))

    # Act
    papers.stage_paper(3)

    # Assert
    assert papers.get_staged_title() == "Paper 3"
    assert papers.get_staged_to_print().summary == "Summary 3"

    papers.remove_staged()
    with pytest.raises(AttributeError, match="No paper was staged"):
        papers.get_staged_title()


def test_papers_manager_rejects_invalid_paper_payload() -> None:
    # Arrange
    papers = PapersManager()

    # Act / Assert
    with pytest.raises(ValueError, match="did not pass validation"):
        papers.save_paper(
            internal_id=1,
            title="Missing required fields",
        )
