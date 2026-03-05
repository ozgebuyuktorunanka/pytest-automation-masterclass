"""
API Testleri — /users endpoint'leri

JS Playwright'taki request fixture ile karşılaştırma:

  Playwright:                       pytest + httpx:
  ──────────────────────────────────────────────────────────────
  const response = await           response = api_client.get(
    request.get('/users/1')          '/users/1'
                                   )
  expect(response.status()).toBe(200)  assert response.status_code == 200
  const body = await response.json()   data = response.json()
  expect(body.name).toBe('Alice')      assert data["name"] == "Alice"
"""
import pytest


class TestGetUsers:

    @pytest.mark.api
    def test_get_all_users_returns_200(self, api_client):
        """api_client fixture'ı conftest.py'den otomatik inject edilir."""
        response = api_client.get("/users")

        assert response.status_code == 200

    @pytest.mark.api
    def test_get_all_users_returns_list(self, api_client):
        response = api_client.get("/users")
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 2  # Seed data: Alice + Bob

    @pytest.mark.api
    def test_get_user_by_id_returns_correct_user(self, api_client):
        response = api_client.get("/users/1")
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == 1
        assert data["name"] == "Alice Smith"
        assert data["email"] == "alice@example.com"

    @pytest.mark.api
    def test_get_nonexistent_user_returns_404(self, api_client):
        response = api_client.get("/users/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestCreateUser:

    @pytest.mark.api
    def test_create_user_returns_201(self, api_client, sample_user):
        """
        sample_user fixture'ı conftest.py'den gelir.
        Her testte temiz DB var (reset_database autouse fixture sayesinde).
        """
        response = api_client.post("/users", json=sample_user)

        assert response.status_code == 201

    @pytest.mark.api
    def test_create_user_persists_data(self, api_client, sample_user):
        api_client.post("/users", json=sample_user)

        # Şimdi geri okuyalım
        response = api_client.get(f"/users/{sample_user['id']}")
        data = response.json()

        assert data["name"] == sample_user["name"]
        assert data["email"] == sample_user["email"]

    @pytest.mark.api
    def test_create_duplicate_user_returns_409(self, api_client, sample_user):
        api_client.post("/users", json=sample_user)

        # Aynı user'ı tekrar gönder
        response = api_client.post("/users", json=sample_user)

        assert response.status_code == 409


class TestDeleteUser:

    @pytest.mark.api
    def test_delete_user_returns_204(self, api_client):
        response = api_client.delete("/users/1")
        assert response.status_code == 204

    @pytest.mark.api
    def test_deleted_user_no_longer_exists(self, api_client):
        api_client.delete("/users/1")
        response = api_client.get("/users/1")
        assert response.status_code == 404

    @pytest.mark.api
    def test_delete_nonexistent_user_returns_404(self, api_client):
        response = api_client.delete("/users/9999")
        assert response.status_code == 404
