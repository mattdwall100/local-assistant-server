"""Interface and base classes for tools."""

from collections.abc import Callable
from typing import Any

from mypy_extensions import KwArg

from .implementations.papers import (
    get_papers,
    get_staged_id,
    get_summary,
    list_titles,
    print_paper,
    stage_paper,
)
from .implementations.time import get_date, get_time
from .registry import Registry


class ToolRegistry:
    """Placeholder tool registry for future function/tool calling."""

    def __init__(self) -> None:
        # Old style of specifying ollama tools, not currently in use
        self._registry: list[object] = Registry.get()

        self._tools: dict[str, Callable[[KwArg(Any)], str]] = {
            "get_papers": get_papers,
            "get_summary": get_summary,
            "stage_paper": stage_paper,
            "print_paper": print_paper,
            "get_time": get_time,
            "get_date": get_date,
            "list_titles": list_titles,
            "get_staged_id": get_staged_id,
        }

    def toolList(self) -> list[Callable[[KwArg(Any)], str]]:
        return list(self._tools.values())

    def toolDict(self) -> dict[str, Callable[[KwArg(Any)], str]]:
        return self._tools
