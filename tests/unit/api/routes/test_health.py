from api.routes.health import health


def test_health_alt():
    response = health()

    assert response["status"] == "healthy"
