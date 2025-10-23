import pytest
from httpx import AsyncClient

class TestAuthEndpoints:
    @pytest.mark.asyncio
    async def test_register_success(self, async_client: AsyncClient):
        response = await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, async_client: AsyncClient):
        await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "full_name": "First User"
            }
        )

        response = await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "full_name": "Second User"
            }
        )

        assert response.status_code == 400
        assert "User with this email already exists" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, async_client: AsyncClient):
        response = await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "full_name": "Test User"
            }
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient):
        await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123",
                "full_name": "Login User"
            }
        )

        response = await async_client.post(
            "api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, async_client: AsyncClient):
        await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123",
                "full_name": "Login User"
            }
        )

        response = await async_client.post(
            "api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, async_client: AsyncClient):
        response = await async_client.post(
            "api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
