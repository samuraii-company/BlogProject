import pytest
from httpx import AsyncClient
from database.test_db import app
from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users
from posts.models import Posts


class TestComments:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.database = next(override_get_db())
        self.new_user = Users(username="Test3", email="test3@gmail.com", password="password")
        self.post = Posts(text="Test", author=self.new_user.id)
        self.database.add(self.new_user)
        self.database.add(self.post)
        self.database.commit()
        self.database.refresh(self.new_user)
        self.database.refresh(self.post)
        self.user_access_token = create_access_token({"sub": "test@gmail.com", "id": 1, "is_stuff": False})
        self.user_access_token_2 = create_access_token(
            {"sub": self.new_user.email, "id": self.new_user.id, "is_stuff": False}
        )
        self.bad_id: int = 100

    @pytest.mark.asyncio
    async def test_comments(self):
        async with self.client as ac:
            response = await ac.get(
                f"api/v1/comments/?post={self.post.id}",
            )
            assert response.status_code == 404

            response = await ac.post(
                "api/v1/comments/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={"text": "Test Comment", "post": self.post.id},
            )
            assert response.status_code == 201

            response = await ac.post(
                "api/v1/comments/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={"text": "Test Comment", "post": self.bad_id},
            )
            assert response.status_code == 404

            response = await ac.get(
                f"api/v1/comments/?post={self.post.id}",
            )
            assert response.status_code == 200

            response = await ac.get(
                f"api/v1/comments/?post={self.bad_id}",
            )
            assert response.status_code == 404

            response = await ac.delete(
                "api/v1/comments/1/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 400

            response = await ac.delete(
                "api/v1/comments/1/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 200

            response = await ac.delete(
                "api/v1/comments/1/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 404
