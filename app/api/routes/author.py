from __future__ import annotations

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from api.deps import AuthorServiceDep
from models.author import Author
from services.exceptions import AuthorAlreadyExistsError, AuthorNotFoundError


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str


class AuthorRequest(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=50)]
    middle_name: Annotated[str | None, Field(min_length=1, max_length=50)]
    last_name: Annotated[str, Field(min_length=1, max_length=50)]


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


def to_author(author: AuthorRequest, author_id: int = 0) -> Author:
    """Mapper to convert AuthorRequest model to Author model"""
    return Author(
        id=author_id,
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
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}},
)
async def create_author(author_request: AuthorRequest, service: AuthorServiceDep):
    """Create an author. If it already exists, a 409 is returned."""
    author = to_author(author_request)

    try:
        new_author = await service.create_author(author)
    except AuthorAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Author with provided name already exists"},
        )

    return to_author_response(new_author)


@router.put(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
async def update_author(
    author_id: int, author_input: AuthorRequest, service: AuthorServiceDep
):
    """Update an author by id. If that author is not found, a 404 is returned."""
    author = to_author(author_input, author_id)

    try:
        await service.update_author(author)
    except AuthorNotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Author not found"},
        )
    except AuthorAlreadyExistsError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Author with provided name already exists"},
        )


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def delete_author(author_id: int, service: AuthorServiceDep):
    """Delete an author by id. If that author is not found, a 404 is returned."""
    try:
        await service.delete_author(author_id)
    except AuthorNotFoundError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Author not found"},
        )
