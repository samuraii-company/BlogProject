import pytest
from httpx import AsyncClient
from database.test_db import app


class TestRegister:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.user_data = {
            "email": "test2@gmail.com",
            "password": "password",
            "password2": "password",
            "username": "Oleg",
        }
        self.user_data_2 = {
            "email": "test3@gmail.com",
            "password": "password",
            "password2": "password",
            "username": "Oleg",
        }
        self.user_data_3 = {
            "email": "test3@gmail.com",
            "password": "password",
            "password2": "password2",
            "username": "Oleg2",
        }

    @pytest.mark.asyncio
    async def test_register(self):

        async with self.client as ac:
            response = await ac.post("/register", json=self.user_data)
            assert response.status_code == 201

            response = await ac.post("/register", json=self.user_data)
            assert response.status_code == 400

            response = await ac.post("/register", json=self.user_data_2)
            assert response.status_code == 400

            response = await ac.post("/register", json=self.user_data_3)
            assert response.status_code == 400
