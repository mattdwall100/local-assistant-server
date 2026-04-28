from ..client.assistant_api_client import AssistantAPIClient
from ..audio.player import AudioPlayer
from typing import Any

class ClientOrchestrator:
    def __init__(self, api: AssistantAPIClient, player: AudioPlayer) -> None:
        self.api = api
        self.player = player

        self.__session_id = None

    # Getter, setter, deleter for session_id
    @property
    def session_id(self) -> str | None:
        return self.__session_id
    
    @session_id.setter
    def session_id(self, value: str) -> None:
        if not isinstance(value, str):
            print("Error: Tried to write non-string to session id")
        elif self.__session_id is not None and self.__session_id != value:
            print("Error: Attempted overwrite of existing session_id")
        elif not value:
            print("Session ID was a falsy string, setting to None")
            self.__session_id = None
        else:
            # Either id is currently None or new value is same as current
            self.__session_id = value
    
    @session_id.deleter
    def session_id(self) -> None:
        self._session_id = None

    # Stop current speech by raising flag in speaker, to be used by push-to-talk
    def stop_speech(self):
        self.player.stop_playback()

    def health(self) -> dict[str, Any]:
        response_json = self.api.health()
        print(response_json)
    
    def speak(self, audio_bytes: bytes):
        print("Sending Speak Request...")
        response, ressolved_id = self.api.speak(audio_bytes, self.session_id)
        print("Success")

        self.player.play_wav_stream(response)

        self.session_id = ressolved_id
        print(f"session id: {self.session_id}")

    def transcribe(self, audio_bytes: bytes):
        response_json = self.api.transcribe(audio_bytes, self.session_id)
        print(response_json)

    def synthesize(self, text: str) -> None:
        iter_response, resolved_session_id = self.api.synthesize(text, self.session_id)
        self.player.play_wav_stream(iter_response)
        self.session_id = resolved_session_id


        