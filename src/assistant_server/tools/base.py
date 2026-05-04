"""Interface and base classes for tools."""
# This will allow orchestrator to work with the toolset without needing to know implementation details, and also allow tools to be modular and independently developed.

from collections.abc import Callable

from .implementations.time import getDate, getTime
from .registry import Registry


class ToolRegistry:
    """Placeholder tool registry for future function/tool calling."""

    _registry: dict[str, object] = Registry.get()

    _tools: dict[str, Callable] = {
        "getTime": getTime,
        "getDate": getDate,
    }

    def toolRegistry(self) -> list[Callable]:
        # print(self._registry)
        # return self._registry
        return list(self._tools.values())

    def toolDict(self) -> list[dict[str, Callable]]:
        return self._tools
