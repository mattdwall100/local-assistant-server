from assistant_server.tools.base import ToolRegistry


def test_tool_registry_exposes_default_tools() -> None:
    # Arrange
    registry = ToolRegistry()

    # Act
    tools = registry.toolDict()
    tool_list = registry.toolRegistry()

    # Assert
    assert "getTime" in tools
    assert "getDate" in tools
    assert callable(tools["getTime"])
    assert callable(tools["getDate"])
    assert tools["getTime"] in tool_list
    assert tools["getDate"] in tool_list


def test_registered_tools_execute_successfully() -> None:
    # Arrange
    registry = ToolRegistry()
    tools = registry.toolDict()

    # Act
    time_value = tools["getTime"]()
    date_value = tools["getDate"]()

    # Assert
    assert isinstance(time_value, str)
    assert ":" in time_value
    assert isinstance(date_value, str)
    assert len(date_value.split("-")) == 3
