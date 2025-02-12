from pydantic import BaseModel


class Author(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
