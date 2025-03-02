from fastapi.testclient import TestClient


class TestHealthIntegration:
    def test_healthy(self, client: TestClient):
        response = client.get("/health")

        assert response.status_code == 200
