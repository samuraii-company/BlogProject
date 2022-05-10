import pytest
from httpx import AsyncClient
from database.test_db import app


class TestLogin:

    params = [
        {"username": "test@gmail.com", "password": "password", "status_code": 200},
        {"username": "test2@gmail.com", "password": "password", "status_code": 400},
        {"username": "test@gmail.com", "password": "password1", "status_code": 400},
    ]

    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("params", params)
    async def test_login(self, params):

        async with self.client as ac:
            response = await ac.post(
                "/login",
                data={
                    "username": params["username"],
                    "password": params["password"],
                },
            )
            assert response.status_code == params["status_code"]
