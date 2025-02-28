from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.deps import AuthorServiceDep
from models.author import Author
from services.exceptions import AuthorAlreadyExistsError


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


class AuthorCreateRequest(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str


class ErrorResponse(BaseModel):
    detail: str


def to_author_response(author: Author) -> AuthorResponse:
    """Mapper to convert Author model to AuthorResponse model"""
    return AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        middle_name=author.middle_name,
        last_name=author.last_name,
    )


def to_author(author: AuthorCreateRequest) -> Author:
    return Author(
        id=0,
        first_name=author.first_name,
        middle_name=author.middle_name,
        last_name=author.last_name,
    )


router = APIRouter(prefix="/author", tags=["author"])


@router.get("/", response_model=list[AuthorResponse])
async def get_all_authors(service: AuthorServiceDep):
    """Get all authors."""
    authors = await service.get_all_authors()

    return [to_author_response(author) for author in authors]


@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
    responses={HTTPStatus.NOT_FOUND: {"model": ErrorResponse}},
)
async def get_author_by_id(author_id: int, service: AuthorServiceDep):
    """Get an author by id. If that author is not found, a 404 is returned."""
    author = await service.get_author_by_id(author_id)

    if author is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND, content={"detail": "Author not found"}
        )

    return to_author_response(author)


@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=HTTPStatus.CREATED,
    responses={HTTPStatus.CONFLICT: {"model": ErrorResponse}},
)
async def create_author(author: AuthorCreateRequest, service: AuthorServiceDep):
    """Create an author. If it already exists, a 409 is returned."""
    author = to_author(author)

    try:
        author = await service.create_author(author)
    except AuthorAlreadyExistsError:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={
                "detail": f"An author with name {author.first_name}"
                + f"{f' {author.middle_name} ' if author.middle_name else ' '}"
                + f"{author.last_name} already exists"
            },
        )

    return to_author_response(author)
