import pytest
from httpx import AsyncClient

class TestFullUserFlow:
    @pytest.mark.asyncio
    async def test_full_user_registration_and_authentication_flow(self, async_client: AsyncClient):
        register_response = await async_client.post(
            "api/v1/auth/register",
            json={
                "email": "flow@example.com",
                "password": "password123",
                "full_name": "Flow User"
            }
        )

        assert register_response.status_code == 200
        user_data = register_response.json()
        assert user_data["email"] == "flow@example.com"

        login_response = await async_client.post(
            "api/v1/auth/login",
            json={
                "email": "flow@example.com",
                "password": "password123"
            }
        )

        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data

        token = token_data["access_token"]

        me_response = await async_client.get(
            "api/v1/users/me",
            cookies={
                "access_token": token
            }
        )

        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["email"] == "flow@example.com"
        assert me_data["full_name"] == "Flow User"
