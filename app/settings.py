from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.joinpath(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    database_password: SecretStr
    database_user: str
    database_name: str
    database_host: str
    database_port: int


@lru_cache(maxsize=1)
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = Settings(
        database_password="password",
        database_user="user",
        database_name="name",
        database_host="host",
        database_port=0000,
    )
    print(settings.model_dump_json(indent=2))
