from __future__ import annotations

from .client.assistant_api_client import AssistantAPIClient
from .config import get_client_settings
from .audio.recorder import MicrophoneRecorder, PushToTalkController
from .audio.player import AudioPlayer


def run() -> None:
    settings = get_client_settings()
    api = AssistantAPIClient(
        base_url=settings.assistant_api_base_url,
        timeout_seconds=settings.assistant_api_timeout_seconds,
        player=AudioPlayer()
    )

    health = api.health()
    print(f"Assistant API healthy: {health}")

    api.synthesize("Alfred Awake")

    mic_controller = PushToTalkController(
        MicrophoneRecorder(
            sample_rate=settings.mic_sample_rate,
            channels=settings.mic_channels,
            block_size=settings.mic_block_size
        ),
        api=api,
    )

    

    


if __name__ == "__main__":
    run()
