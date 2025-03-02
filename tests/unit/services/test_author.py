from unittest.mock import MagicMock, AsyncMock

import pytest

from models.author import Author
from services.author import AuthorService
from services.exceptions import AuthorAlreadyExistsError, AuthorNotFoundError


class TestAuthorService:
    async def test_get_all_authors(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "first_name": "John", "middle_name": "M", "last_name": "Doe"},
            {"id": 2, "first_name": "Jane", "middle_name": "A", "last_name": "Smith"},
        ]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        result = await service.get_all_authors()

        expected_result = [
            Author(id=1, first_name="John", middle_name="M", last_name="Doe"),
            Author(id=2, first_name="Jane", middle_name="A", last_name="Smith"),
        ]

        assert result == expected_result
        assert mock_cursor.fetchall.await_count == 1

    async def test_get_author_by_id_author_found(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.return_value = {
            "id": 1,
            "first_name": "John",
            "middle_name": "M",
            "last_name": "Doe",
        }

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        result = await service.get_author_by_id(1)

        expected_result = Author(
            id=1, first_name="John", middle_name="M", last_name="Doe"
        )

        assert result == expected_result
        assert mock_cursor.fetchone.await_count == 1

    async def test_get_author_by_id_author_not_found(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        result = await service.get_author_by_id(1)

        expected_result = None

        assert result == expected_result
        assert mock_cursor.fetchone.await_count == 1

    async def test_create_author_successfully_with_middle_name(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.side_effect = [{"count": 0}, {"id": 1}]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=0,
            first_name="John",
            middle_name="M",
            last_name="Doe",
        )

        result = await service.create_author(test_input)

        expected_result = Author(
            id=1,
            first_name="John",
            middle_name="M",
            last_name="Doe",
        )

        assert result == expected_result
        assert mock_cursor.fetchone.await_count == 2

    async def test_create_author_successfully_without_middle_name(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.side_effect = [{"count": 0}, {"id": 1}]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=0,
            first_name="John",
            middle_name=None,
            last_name="Doe",
        )

        result = await service.create_author(test_input)

        expected_result = Author(
            id=1,
            first_name="John",
            middle_name=None,
            last_name="Doe",
        )

        assert result == expected_result
        assert mock_cursor.fetchone.await_count == 2

    async def test_create_author_author_already_exists(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.return_value = {"count": 1}

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=0,
            first_name="John",
            middle_name=None,
            last_name="Doe",
        )

        with pytest.raises(AuthorAlreadyExistsError):
            await service.create_author(test_input)

        assert mock_cursor.fetchone.await_count == 1

    async def test_update_author_successfully(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.side_effect = [{"count": 0}, {"id": 1}]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=1,
            first_name="John",
            middle_name="M",
            last_name="Doe",
        )

        await service.update_author(test_input)

        assert mock_cursor.fetchone.await_count == 2
        assert mock_cursor.execute.call_count == 2

    async def test_update_author_author_does_not_exist(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.side_effect = [{"count": 0}, None]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=1,
            first_name="John",
            middle_name="M",
            last_name="Doe",
        )

        with pytest.raises(AuthorNotFoundError):
            await service.update_author(test_input)

        assert mock_cursor.execute.call_count == 2
        assert mock_cursor.fetchone.await_count == 2

    async def test_update_author_author_already_exists(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.side_effect = [{"count": 1}]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        test_input = Author(
            id=1,
            first_name="John",
            middle_name="M",
            last_name="Doe",
        )

        with pytest.raises(AuthorAlreadyExistsError):
            await service.update_author(test_input)

        assert mock_cursor.execute.call_count == 1
        assert mock_cursor.fetchone.await_count == 1

    async def test_delete_author_successfully(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.return_value = {"id": 1}

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        await service.delete_author(1)

        assert mock_cursor.execute.await_count == 1
        assert mock_cursor.fetchone.await_count == 1

    async def test_delete_author_author_does_not_exist(self):
        mock_cursor = AsyncMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        service = AuthorService(conn=mock_conn)

        with pytest.raises(AuthorNotFoundError):
            await service.delete_author(1)

        assert mock_cursor.execute.await_count == 1
        assert mock_cursor.fetchone.await_count == 1
