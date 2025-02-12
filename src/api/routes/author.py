from fastapi import APIRouter
from pydantic import BaseModel

from api.deps import AuthorServiceDep


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


router = APIRouter(prefix="/author", tags=["author"])


@router.get("/")
async def get_all_authors(service: AuthorServiceDep) -> list[AuthorResponse]:
    authors = await service.get_all_authors()
    return [
        AuthorResponse(
            id=author.id,
            first_name=author.first_name,
            middle_name=author.middle_name,
            last_name=author.last_name,
        )
        for author in authors
    ]


@router.get("/{author_id}")
async def get_author_by_id(author_id: int, service: AuthorServiceDep) -> AuthorResponse:
    author = await service.get_author_by_id(author_id)
    return AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        middle_name=author.middle_name,
        last_name=author.last_name,
    )
