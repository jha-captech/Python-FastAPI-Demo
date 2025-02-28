from functools import lru_cache

from loguru import logger
from psycopg_pool import AsyncConnectionPool

from settings import get_settings


@lru_cache(maxsize=1)
def get_pool() -> AsyncConnectionPool:
    logger.info("Creating connection pool")

    settings = get_settings()

    return AsyncConnectionPool(
        conninfo=f"postgresql://{settings.database_user}:{settings.database_password.get_secret_value()}@{settings.database_host}:{settings.database_port}/{settings.database_name}",
        open=False,
    )
