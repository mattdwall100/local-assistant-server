from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings for the local assistant server
    # default vals and .env names
    app_name: str = Field(default="Local AI Assistant", alias="APP_NAME")
    app_env: Literal["dev", "test", "prod"] = Field(default="dev", alias="APP_ENV")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    stt_device: str = Field(default="cpu", alias="STT_DEVICE")
    stt_FW_model_path: str = Field(default="tiny", alias="STT_FW_MODEL_PATH")
    modelname: str = Field(default="granite4:350m", alias="MODEL_NAME")
    tts_voice_path: str = Field(default="models/tts/en_GB-alan-medium.onnx", alias="TTS_VOICE_PATH")
    tts_output_path: str = Field(default="tests/voice_results/output.wav", alias="TTS_OUTPUT_PATH")
    fallback_path: str = Field(default="assets/fallback_audio", alias="FALLBACK_PATH")
    printer_name: str = Field(default="", alias="PRINTER_NAME")

    # read .env and ignore extra fields
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# cache result of get_settings
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
