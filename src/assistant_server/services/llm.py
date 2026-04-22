class LlmService:
    """LLM service abstraction."""

    def complete(
        self,
        user_text: str,
        memory_context: list[str],
        retrieval_context: list[str],
        tool_schemas: list[dict[str, object]],
    ) -> str:
        del memory_context, retrieval_context, tool_schemas
        return f"Echo (placeholder): {user_text}"

