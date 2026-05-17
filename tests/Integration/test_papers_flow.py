from unittest.mock import patch

from assistant_server.memory.store import MemoryStore
from assistant_server.tools.implementations import papers as paper_tools


class _DailyPaper:
    def __init__(
        self,
        *,
        id: str,
        title: str | None,
        summary: str | None,
        organization=None,
    ) -> None:
        self.id = id
        self.title = title
        self.summary = summary
        self.organization = organization


class _FakeHfApi:
    def __init__(self, papers: list[_DailyPaper]) -> None:
        self._papers = papers

    def list_daily_papers(self, sort: str, limit: int):
        assert sort == "trending"
        assert limit == 50
        return iter(self._papers)


def _valid_daily_papers(prefix: str) -> list[_DailyPaper]:
    return [
        _DailyPaper(
            id=f"2401.0000{internal_id}",
            title=f"{prefix} Paper {internal_id}",
            summary=f"{prefix} Summary {internal_id}",
        )
        for internal_id in range(1, 7)
    ]


def test_papers_tools_fetch_and_query_flow_with_mocked_hf_api() -> None:
    # Arrange
    memory = MemoryStore()
    daily_papers = [
        _DailyPaper(id="missing-summary", title="Missing Summary", summary=None),
        _DailyPaper(id="missing-title", title=None, summary="Missing title"),
        *_valid_daily_papers("Fetched"),
    ]

    # Act
    with patch.object(paper_tools, "HfApi", return_value=_FakeHfApi(daily_papers)):
        fetched = paper_tools.get_papers(memory=memory, session_id="session-1")

    titles = paper_tools.list_titles(memory=memory, session_id="session-1")
    summary = paper_tools.get_summary(3, memory=memory, session_id="session-1")
    stage_result = paper_tools.stage_paper(3, memory=memory, session_id="session-1")
    staged_id = paper_tools.get_staged_id(memory=memory, session_id="session-1")
    print_result = paper_tools.print_paper(memory=memory, session_id="session-1")

    # Assert
    expected_titles = (
        "1: Fetched Paper 1. 2: Fetched Paper 2. 3: Fetched Paper 3. "
        "4: Fetched Paper 4. 5: Fetched Paper 5."
    )
    assert fetched == expected_titles
    assert titles == expected_titles
    assert summary == "Fetched Summary 3"
    assert stage_result == "Successfully staged paper with id=3"
    assert staged_id == "3"
    assert print_result == "Successfully sent staged paper 3 to the printer"


def test_papers_flow_keeps_fetched_and_staged_papers_session_scoped() -> None:
    # Arrange
    memory = MemoryStore()

    # Act
    with patch.object(paper_tools, "HfApi", return_value=_FakeHfApi(_valid_daily_papers("First"))):
        paper_tools.get_papers(memory=memory, session_id="first-session")
    with patch.object(paper_tools, "HfApi", return_value=_FakeHfApi(_valid_daily_papers("Second"))):
        paper_tools.get_papers(memory=memory, session_id="second-session")

    first_stage = paper_tools.stage_paper(2, memory=memory, session_id="first-session")
    second_stage = paper_tools.stage_paper(4, memory=memory, session_id="second-session")

    # Assert
    assert (
        paper_tools.get_summary(2, memory=memory, session_id="first-session") == "First Summary 2"
    )
    assert (
        paper_tools.get_summary(2, memory=memory, session_id="second-session") == "Second Summary 2"
    )
    assert first_stage == "Successfully staged paper with id=2"
    assert second_stage == "Successfully staged paper with id=4"
    assert (
        paper_tools.get_staged_id(memory=memory, session_id="first-session") == "2"
    )
    assert (
        paper_tools.get_staged_id(memory=memory, session_id="second-session") == "4"
    )
