from ..core.config import get_settings
from ..core.logging import get_logger
from pathlib import Path
from ..audio.player import AudioPlayer

settings = get_settings()
logger = get_logger(__name__)

class FallbackHandler:
    """Fallback handler for graceful degredation whenever a pipeline module fails.
    Plays message"""
    def __init__(self, player: AudioPlayer):
        self.player = player
        self.fallback_path = settings.fallback_path

    def handle(self, event_name: str) -> None:
        if not event_name in self.fallback_message.keys():
            logger.error(f"unknown event_name | event_name={event_name}")
            raise ValueError("Unknown event name, should be 'server_not_found' or 'bad_audio'")

        resolved_path = Path(self.fallback_path + "/" + event_name + ".wav")

        logger.info(f"Fallback_played | event_name={event_name}")
        self.player.play_file(resolved_path)