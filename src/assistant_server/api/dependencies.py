from typing import cast

from fastapi import Request

from ..orchestrator.pipeline import AssistantPipeline


def get_orchestrator(request: Request) -> AssistantPipeline:
    # app.state is dynamically types in fastapi so we cast as required type
    # instead of setting as Any and checking type ( with isinstance() ) so
    # that mocks can be used for AssistantPipeline in tests
    return cast(AssistantPipeline, request.app.state.orchestrator)
