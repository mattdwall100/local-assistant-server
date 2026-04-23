from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings for the local assistant server
    # First we provide default values for each setting, and also specify the corresponding environment variable name using the `alias` parameter in the Field function.
    app_name: str = Field(default="Local AI Assistant", alias="APP_NAME")
    app_env: Literal["dev", "test", "prod"] = Field(default="dev", alias="APP_ENV")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # We configure the settings model to read from a .env file, and to ignore any extra fields that are not defined in the model. This allows us to have a flexible configuration setup, where we can easily add new settings without having to worry about validation errors for unknown fields.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# lru_cache is a decorator that allows us to cache the result of the get_settings function, so that it only reads the configuration from the environment variables once, and then returns the cached settings object on subsequent calls. This can improve performance by avoiding unnecessary re-reading of environment variables, while still allowing us to easily access the settings throughout our application.
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

