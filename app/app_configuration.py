import os
from functools import lru_cache

from pydantic.v1 import BaseSettings


def get_env(env_name: str | None):
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_path = f"{base_path}/.env.{env_name}" if env_name else f"{base_path}/.env"

    # Do not use the App Logger or logging here as it corrupts the logger configuration.
    print(f"Loading environment variables from '{env_path}'")
    return f"{base_path}/.env.{env_name}" if env_name else f"{base_path}/.env"

class AppSettings(BaseSettings):
    app_name: str
    env: str

    class Config:
        allow_population_by_field_name = True
        case_sensitive = False

class MqttSettings(BaseSettings):
    broker: str
    port: int
    topic: str
    client_id: str

    class Config:
        allow_population_by_field_name = True
        case_sensitive = False


class Settings(BaseSettings):
    APP: AppSettings
    MQTT: MqttSettings

    class Config:
        env_name = os.environ.get("ENV")
        allow_population_by_field_name = True
        case_sensitive = False
        env_nested_delimiter = "__"  # Allows nested configuration via environment variables
        env_file = get_env(env_name=env_name)


@lru_cache
def get_settings() -> Settings:
    return Settings()
