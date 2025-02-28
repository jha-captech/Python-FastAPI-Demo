from typing import Annotated, AsyncGenerator

from fastapi import Depends
from loguru import logger
from psycopg import AsyncConnection

from services.author import AuthorService
from services.db import get_pool


async def get_conn() -> AsyncGenerator[AsyncConnection, None]:
    logger.debug("getting connection pool")
    pool = get_pool()

    async with pool.connection() as conn:
        logger.debug("yielding connection from pool")
        yield conn


SessionDep = Annotated[AsyncConnection, Depends(get_conn)]


def get_author_service(conn: SessionDep) -> AuthorService:
    return AuthorService(conn)


AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]
