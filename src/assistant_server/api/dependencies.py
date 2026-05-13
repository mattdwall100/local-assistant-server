from fastapi import Request

from ..orchestrator.pipeline import AssistantPipeline


def get_orchestrator(request: Request) -> AssistantPipeline:
    return request.app.state.orchestrator
