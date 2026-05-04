"""Tool Register"""


class Registry:
    getTime_tool = {
        "type": "function",
        "function": {
            "name": "getTime",
            "description": "Get the current time",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }

    getDate_tool = {
        "type": "function",
        "function": {
            "name": "getDate",
            "description": "Get the current date",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }

    _registry: list[object] = [
        getTime_tool,
        getDate_tool,
    ]

    @classmethod
    def get(cls) -> list[object]:
        return cls._registry
