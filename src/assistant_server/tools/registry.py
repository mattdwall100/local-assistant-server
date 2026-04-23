"""Interface and base classes for tools."""
# This will allow orchestrator to work with the toolset without needing to know implementation details, and also allow tools to be modular and independently developed.

from .implementations.time import getTime



class ToolRegistry:
    """Placeholder tool registry for future function/tool calling."""
    
    _tools: dict[str, callable] = {
        'getTime': getTime,
    }

    def toolList(self) -> list[callable]:
        return self._tools.values()

    def toolDict(self) -> list[dict[str, callable]]:
        return self._tools
