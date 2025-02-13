from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.deps import AuthorServiceDep


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


class ErrorResponse(BaseModel):
    detail: str


router = APIRouter(prefix="/author", tags=["author"])


@router.get("/", response_model=list[AuthorResponse])
async def get_all_authors(service: AuthorServiceDep):
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


@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_author_by_id(author_id: int, service: AuthorServiceDep):
    author = await service.get_author_by_id(author_id)

    if author is None:
        return JSONResponse(status_code=404, content={"detail": "Author not found"})

    return AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        middle_name=author.middle_name,
        last_name=author.last_name,
    )
