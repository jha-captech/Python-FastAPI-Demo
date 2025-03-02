from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest

from api.routes.author import (
    AuthorResponse,
    get_all_authors,
    get_author_by_id,
    AuthorRequest,
    create_author,
    update_author,
    delete_author,
)
from models.author import Author
from services.author import AuthorService
from services.exceptions import AuthorAlreadyExistsError, AuthorNotFoundError
from tests.helper import to_json_string


@pytest.fixture
def mock_service():
    service = AsyncMock(AuthorService)
    return service


async def test_get_all_authors_returns_all_authors(mock_service) -> None:
    mock_service.get_all_authors.return_value = [
        AsyncMock(id=1, first_name="John", middle_name="A", last_name="Doe"),
        AsyncMock(id=2, first_name="Jane", middle_name="B", last_name="Smith"),
    ]

    response = await get_all_authors(mock_service)

    assert response == [
        AuthorResponse(id=1, first_name="John", middle_name="A", last_name="Doe"),
        AuthorResponse(id=2, first_name="Jane", middle_name="B", last_name="Smith"),
    ]


async def test_get_author_by_id_returns_author(mock_service) -> None:
    mock_service.get_author_by_id.return_value = AsyncMock(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )

    response = await get_author_by_id(1, mock_service)

    assert response == AuthorResponse(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )


async def test_get_author_by_id_returns_not_found(mock_service) -> None:
    mock_service.get_author_by_id.return_value = None

    response = await get_author_by_id(2, mock_service)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.body == to_json_string({"detail": "Author not found"})


async def test_create_author_successfully(mock_service):
    mock_service.create_author.return_value = Author(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )

    input_request = AuthorRequest(first_name="John", middle_name="A", last_name="Doe")

    response = await create_author(input_request, mock_service)

    assert response == AuthorResponse(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )


async def test_create_author_already_exists(mock_service):
    mock_service.create_author.side_effect = AuthorAlreadyExistsError(
        "An author with the same name already exists"
    )

    input_request = AuthorRequest(first_name="John", middle_name="A", last_name="Doe")

    response = await create_author(input_request, mock_service)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.body == to_json_string(
        {"detail": "Author with provided name already exists"}
    )


async def test_update_author_successfully(mock_service):
    mock_service.update_author.return_value = Author(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )

    input_request = AuthorRequest(first_name="John", middle_name="A", last_name="Doe")

    response = await update_author(1, input_request, mock_service)

    assert response is None


async def test_update_author_already_exists(mock_service):
    mock_service.update_author.side_effect = AuthorAlreadyExistsError(
        "An author with the same name already exists"
    )

    input_request = AuthorRequest(first_name="John", middle_name="A", last_name="Doe")

    response = await update_author(1, input_request, mock_service)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.body == to_json_string(
        {"detail": "Author with provided name already exists"}
    )


async def test_update_author_author_not_found(mock_service):
    mock_service.update_author.side_effect = AuthorNotFoundError("Author not found")

    input_request = AuthorRequest(first_name="John", middle_name="A", last_name="Doe")

    response = await update_author(1, input_request, mock_service)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.body == to_json_string({"detail": "Author not found"})


async def test_delete_author_successfully(mock_service):
    response = await delete_author(1, mock_service)

    assert response is None


async def test_delete_author_not_found(mock_service):
    mock_service.delete_author.side_effect = AuthorNotFoundError("Author not found")

    response = await delete_author(1, mock_service)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.body == to_json_string({"detail": "Author not found"})
