from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_password: SecretStr
    database_user: str
    database_name: str
    database_host: str
    database_port: int


@lru_cache()
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = Settings()
    print(settings.model_dump_json(indent=2))
