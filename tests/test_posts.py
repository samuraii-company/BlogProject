import pytest
from httpx import AsyncClient
from database.test_db import app
from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users


class TestPosts:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.database = next(override_get_db())
        self.new_user = Users(username="Test3", email="test3@gmail.com", password="password")
        self.database.add(self.new_user)
        self.database.commit()
        self.database.refresh(self.new_user)
        self.user_access_token = create_access_token({"sub": "test@gmail.com", "id": 1, "is_stuff": False})
        self.user_access_token_2 = create_access_token(
            {"sub": self.new_user.email, "id": self.new_user.id, "is_stuff": False}
        )
        self.bad_id: int = 100

    @pytest.mark.asyncio
    async def test_posts(self):
        async with self.client as ac:
            response = await ac.get(
                f"api/v1/posts/?q={self.new_user.id}",
            )
            assert response.status_code == 404

            response = await ac.post(
                f"api/v1/posts/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={"title": "Test", "text": "Text text"},
            )
            assert response.status_code == 201

            response = await ac.get(
                f"api/v1/posts/?q={self.new_user.id}",
            )
            assert response.status_code == 200

            await ac.get(
                f"api/v1/posts/1/",
            )
            assert response.status_code == 200

            response = await ac.delete(
                f"api/v1/posts/1/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 400

            response = await ac.delete(
                f"api/v1/posts/1/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 200

            response = await ac.delete(
                f"api/v1/posts/1/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_by_id_bad(self):
        async with self.client as ac:
            response = await ac.get(
                f"api/v1/posts/200/",
            )
            assert response.status_code == 404
