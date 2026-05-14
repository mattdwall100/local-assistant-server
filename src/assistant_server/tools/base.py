"""Interface and base classes for tools."""

from collections.abc import Callable
from typing import Any

from .implementations.time import *
from .implementations.papers import *
from .registry import Registry


class ToolRegistry:
    """Placeholder tool registry for future function/tool calling."""

    def __init__(self):

        # Old style of specifying ollama tools, not currently in use
        self._registry: list[object] = Registry.get()

        self._tools: dict[str, Callable[[Any], str]] = {
            "get_time": get_time,
            "get_date": get_date,
            "get_papers": get_papers,
            "list_titles": list_titles,
            "get_summary": get_summary,
            "get_staged_title": get_staged_title,
            "stage_paper": stage_paper,
            "print_paper": print_paper,
        }

    def toolList(self) -> list[Callable[[Any], str]]:
        return list(self._tools.values())

    def toolDict(self) -> dict[str, Callable[[Any], str]]:
        return self._tools
