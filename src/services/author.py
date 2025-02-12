from loguru import logger
from psycopg import AsyncConnection

from models.author import Author


class AuthorService:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get_all_authors(self) -> list[Author]:
        logger.info("Getting all authors")

        async with self.conn.cursor() as cur:
            await cur.execute("SELECT * FROM authors")
            authors = await cur.fetchall()

        return [
            Author(
                id=author[0],
                first_name=author[1],
                middle_name=author[2],
                last_name=author[3],
            )
            for author in authors
        ]

    async def get_author_by_id(self, author_id: int) -> Author:
        logger.info(f"Getting author with id {author_id}")

        async with self.conn.cursor() as cur:
            await cur.execute("SELECT * FROM authors WHERE id = %s", (author_id,))
            author = await cur.fetchone()

        return Author(
            id=author[0],
            first_name=author[1],
            middle_name=author[2],
            last_name=author[3],
        )
