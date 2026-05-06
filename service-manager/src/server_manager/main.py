from .config import get_LM_settings, ServiceConfigRegistry
from .runtime import Runtime
from .state import StatusManager
from .orchestrator import Orchestrator


def main():
    settings = get_LM_settings()
    config_registry = ServiceConfigRegistry._from_yaml(settings.services_config_path)

    runtime = Runtime()

    status_manager = StatusManager.from_runtime_and_config(runtime, config_registry)

    orchestrator = Orchestrator(
        runtime=runtime,
        status_manager=status_manager,
        config_registry=config_registry,
    )

    monitor = Monitor(
        orchestrator=orchestrator,
        interval_seconds=settings.monitor_interval_seconds,
    )


if __name__ == "__main__":
    main()
