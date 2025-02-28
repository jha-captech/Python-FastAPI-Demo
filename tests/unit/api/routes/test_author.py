from http import HTTPStatus
from unittest.mock import AsyncMock

from starlette.responses import JSONResponse

from api.routes.author import AuthorResponse, get_all_authors, get_author_by_id


async def test_get_all_authors_returns_all_authors() -> None:
    mock_service = AsyncMock()

    mock_service.get_all_authors.return_value = [
        AsyncMock(id=1, first_name="John", middle_name="A", last_name="Doe"),
        AsyncMock(id=2, first_name="Jane", middle_name="B", last_name="Smith"),
    ]

    response = await get_all_authors(mock_service)

    expected_response = [
        AuthorResponse(id=1, first_name="John", middle_name="A", last_name="Doe"),
        AuthorResponse(id=2, first_name="Jane", middle_name="B", last_name="Smith"),
    ]

    assert response == expected_response


async def test_get_author_by_id_returns_author() -> None:
    mock_service = AsyncMock()

    mock_service.get_author_by_id.return_value = AsyncMock(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )

    response = await get_author_by_id(1, mock_service)

    expected_response = AuthorResponse(
        id=1, first_name="John", middle_name="A", last_name="Doe"
    )
    assert response == expected_response


async def test_get_author_by_id_returns_not_found() -> None:
    mock_service = AsyncMock()

    mock_service.get_author_by_id.return_value = None

    response = await get_author_by_id(2, mock_service)

    expected_response = JSONResponse(
        status_code=HTTPStatus.NOT_FOUND, content={"detail": "Author not found"}
    )
    assert response.status_code == expected_response.status_code
    assert response.body == expected_response.body
