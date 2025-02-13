from collections.abc import Generator
from unittest.mock import patch, AsyncMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with patch("app.settings.get_settings"):
        with patch("app.services.db.pool", new_callable=AsyncMock):
            from app.main import app

            with TestClient(app) as c:
                yield c
