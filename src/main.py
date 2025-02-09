from typing import Annotated, Any, Generator

from fastapi import FastAPI, Depends
from psycopg import Connection
from psycopg_pool import ConnectionPool
from pydantic import BaseModel

from settings import get_settings

settings = get_settings()
app = FastAPI()

pool = ConnectionPool(
    conninfo=f"postgresql://{settings.database_user}:{settings.database_password.get_secret_value()}@{settings.database_host}:{settings.database_port}/{settings.database_name}",
    open=True,
)


def get_connection_from_pool() -> Generator[Connection, Any, None]:
    print("running get_connection_from_pool")
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)


@app.get("/health")
def read_root():
    return {"status": "healthy"}


class Author(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


class AuthorService:
    def __init__(self, conn: Annotated[Connection, Depends(get_connection_from_pool)]):
        self.conn = conn

    def get_all_authors(self) -> list[Author]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM authors")
            authors = cur.fetchall()

        return [
            Author(
                id=author[0],
                first_name=author[1],
                middle_name=author[2],
                last_name=author[3],
            )
            for author in authors
        ]


@app.get("/authors")
def read_item(service: Annotated[AuthorService, Depends()]) -> list[Author]:
    return service.get_all_authors()
