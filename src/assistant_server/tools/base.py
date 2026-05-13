"""Interface and base classes for tools."""

from collections.abc import Callable
from typing import Any

from .implementations.time import getDate, getTime
from .registry import Registry


class ToolRegistry:
    """Placeholder tool registry for future function/tool calling."""

    # Old style of specifying ollama tools, not currently in use 
    _registry: list[object] = Registry.get()

    _tools: dict[str, Callable[[Any], str]] = {
        "getTime": getTime,
        "getDate": getDate,
    }

    def toolRegistry(self) -> list[Callable[[Any], str]]:
        # print(self._registry)
        # return self._registry
        return list(self._tools.values())

    def toolDict(self) -> dict[str, Callable[[Any], str]]:
        return self._tools
