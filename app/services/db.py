from loguru import logger
from psycopg_pool import AsyncConnectionPool

from app.settings import get_settings

settings = get_settings()

logger.info("Creating connection pool")
pool = AsyncConnectionPool(
    conninfo=f"postgresql://{settings.database_user}:{settings.database_password.get_secret_value()}@{settings.database_host}:{settings.database_port}/{settings.database_name}",
    open=False,
)
