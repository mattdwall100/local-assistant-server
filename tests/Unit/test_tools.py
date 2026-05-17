from assistant_server.memory.store import MemoryStore
from assistant_server.tools.base import ToolRegistry


def test_tool_registry_exposes_default_tools() -> None:
    session_id = "test_id"
    # Arrange
    memory = MemoryStore()
    registry = ToolRegistry()

    # Act
    tools = registry.toolDict()
    tool_list = registry.toolList()

    # Assert
    assert "get_time" in tools
    assert "get_date" in tools
    assert callable(tools["get_time"])
    assert callable(tools["get_date"])
    assert tools["get_time"] in tool_list
    assert tools["get_date"] in tool_list


def test_registered_tools_execute_successfully() -> None:
    session_id = "test_id"
    # Arrange
    memory = MemoryStore()
    registry = ToolRegistry()
    tools = registry.toolDict()

    # Act
    time_value = tools["get_time"]()
    date_value = tools["get_date"]()

    # Assert
    assert isinstance(time_value, str)
    assert ":" in time_value
    assert isinstance(date_value, str)
    assert len(date_value.split("-")) == 3
