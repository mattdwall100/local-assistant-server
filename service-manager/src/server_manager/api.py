from fastapi import APIRouter
from .schemas import ServiceListResponse, ServiceStatus

router = APIRouter()


@router.get("/services", response_model=ServiceListResponse)
def get_services() -> ServiceListResponse:
    pass


@router.get("/services/{name}/status", response_model=ServiceStatus)
def get_service_status(name: str) -> ServiceStatus:
    # validate name
    # call orchesrator.get_status(name)
    pass


@router.post("/services/{name}/start")
def start_service(name: str) -> ServiceStatus:
    # validate name
    # call orchestrator.start(name)
    pass


@router.post("/services/{name}/stop")
def stop_service(name: str) -> ServiceStatus:
    # validate name
    # call orchestrator.stop(name)
    pass
