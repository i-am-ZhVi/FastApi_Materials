import pytest
from httpx import AsyncClient

class TestUserEndpoints:
    @pytest.mark.asyncio
    async def test_get_current_user_success(self, async_client: AsyncClient):
        # Register and login to get token
        await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "currentuser@example.com",
                "password": "password123",
                "full_name": "Current User"
            }
        )

        login_response = await async_client.post(
            "api/v1/auth/login",
            json={
                "email": "currentuser@example.com",
                "password": "password123"
            }
        )

        token = login_response.json()["access_token"]

        response = await async_client.get(
            "api/v1/users/me",
            cookies={
                "access_token": token
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "currentuser@example.com"
        assert data["full_name"] == "Current User"

    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, async_client: AsyncClient):
        response = await async_client.get("api/v1/users/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, async_client: AsyncClient):

        response = await async_client.get(
            "api/v1/users/me",
            cookies={
                "access_token": "fake token"
            }
        )

        assert response.status_code == 401
