from __future__ import annotations

from .client.assistant_api_client import AssistantAPIClient
from .config import get_client_settings
from .audio.recorder import MicrophoneRecorder, PushToTalkController


def run() -> None:
    settings = get_client_settings()
    api = AssistantAPIClient(
        base_url=settings.assistant_api_base_url,
        timeout_seconds=settings.assistant_api_timeout_seconds,
    )

    health = api.health()
    print(f"Assistant API healthy: {health}")

    mic_controller = PushToTalkController(
        MicrophoneRecorder(
            sample_rate=settings.mic_sample_rate,
            channels=settings.mic_channels,
        ),
        api=api,
    )

    


if __name__ == "__main__":
    run()
