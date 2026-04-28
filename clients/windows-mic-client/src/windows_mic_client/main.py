from __future__ import annotations

from .client.assistant_api_client import AssistantAPIClient
from .config import get_client_settings
from .audio.recorder import MicrophoneRecorder, PushToTalkController
from .audio.player import AudioPlayer
from .orchestrator.orchestrator import ClientOrchestrator


def run() -> None:
    settings = get_client_settings()

    # Initialise Output layer objects according to settings
    api = AssistantAPIClient(
        base_url=settings.assistant_api_base_url,
        timeout_seconds=settings.assistant_api_timeout_seconds
    )
    player = AudioPlayer()

    # Initialise Orchestration layer
    orchestrator = ClientOrchestrator(
        api=api,
        player=player
    )
    orchestrator.synthesize("Alfred Awake")

    # Initialise input/control layer
    mic_controller = PushToTalkController(
        MicrophoneRecorder(
            sample_rate=settings.mic_sample_rate,
            channels=settings.mic_channels,
            block_size=settings.mic_block_size
        ),
        orchestrator=orchestrator
    )


if __name__ == "__main__":
    run()
