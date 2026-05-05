from pydantic import BaseModel


class ServiceConfig(BaseModel):
    display_name: str
    systemd_unit: str
    health_url: str | None = None
    public_url: str | None = None
    idle_timeout_seconds: int = 600
    enabled: bool = True


class ServiceStatus(BaseModel):
    name: str
    running: bool
    healthy: bool | None = None
    last_activity_at: str | None = None
    idle_seconds: int | None = None
    seconds_until_sleep: int | None = None
