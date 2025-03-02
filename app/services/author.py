from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from psycopg.rows import dict_row

from models.author import Author
from services.exceptions import AuthorAlreadyExistsError, AuthorNotFoundError

if TYPE_CHECKING:
    from psycopg import AsyncConnection


class AuthorService:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get_all_authors(self) -> list[Author]:
        logger.info("Getting all authors")

        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT a.id, a.first_name, a.middle_name, a.last_name
                FROM authors as a
                """
            )

            authors = await cur.fetchall()

        return [Author(**author) for author in authors]

    async def get_author_by_id(self, author_id: int) -> Author | None:
        logger.info(f"Getting author with id {author_id}")

        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT a.id, a.first_name, a.middle_name, a.last_name
                FROM authors as a
                WHERE a.id = %(author_id)s
                """,
                {"author_id": author_id},
            )

            author = await cur.fetchone()

        if author is None:
            return None

        return Author(**author)

    async def create_author(self, author: Author) -> Author:
        logger.info(f"Creating author with first name {author.first_name}")

        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT COUNT(*)
                FROM authors
                WHERE LOWER(first_name) = LOWER(%(first_name)s)
                  AND COALESCE(LOWER(middle_name), '') = COALESCE(LOWER(%(middle_name)s), '')
                  AND LOWER(last_name) = LOWER(%(last_name)s)
                """,
                {
                    "first_name": author.first_name,
                    "middle_name": author.middle_name,
                    "last_name": author.last_name,
                },
            )

            response = await cur.fetchone()

            if response.get("count", 0) > 0:
                raise AuthorAlreadyExistsError(
                    "An author with the same name already exists"
                )

            await cur.execute(
                """
                    INSERT INTO authors (first_name, middle_name, last_name)
                    VALUES (%(first_name)s, %(middle_name)s, %(last_name)s)
                    RETURNING id
                    """,
                {
                    "first_name": author.first_name,
                    "middle_name": author.middle_name,
                    "last_name": author.last_name,
                },
            )

            response = await cur.fetchone()

        author.id = response["id"]

        return author

    async def update_author(self, author: Author) -> None:
        logger.info(f"Updating author with id {author.id}")

        async with self.conn.cursor(row_factory=dict_row) as cur:
            # check if input values will cause a conflict
            await cur.execute(
                """
                SELECT COUNT(*)
                FROM authors
                WHERE id <> %(id)s
                  AND LOWER(first_name) = LOWER(%(first_name)s)
                  AND COALESCE(LOWER(middle_name), '') = COALESCE(LOWER(%(middle_name)s), '')
                  AND LOWER(last_name) = LOWER(%(last_name)s)
                """,
                {
                    "id": author.id,
                    "first_name": author.first_name,
                    "middle_name": author.middle_name,
                    "last_name": author.last_name,
                },
            )

            response = await cur.fetchone()

            if response.get("count", 0) > 0:
                raise AuthorAlreadyExistsError(
                    "An author with the same name already exists"
                )

            # update author
            await cur.execute(
                """
                UPDATE authors
                SET first_name = %(first_name)s,
                   middle_name = %(middle_name)s,
                   last_name = %(last_name)s
                WHERE id = %(id)s
                RETURNING id
                """,
                {
                    "id": author.id,
                    "first_name": author.first_name,
                    "middle_name": author.middle_name,
                    "last_name": author.last_name,
                },
            )

            response = await cur.fetchone()

            if response is None:
                raise AuthorNotFoundError("Author not found")

    async def delete_author(self, author_id: int) -> None:
        logger.info(f"Deleting author with id {author_id}")

        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                DELETE
                FROM authors
                WHERE id = %(id)s
                RETURNING id
                """,
                {"id": author_id},
            )

            response = await cur.fetchone()

            if response is None:
                raise AuthorNotFoundError("Author not found")
