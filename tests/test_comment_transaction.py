from fastapi import Depends
import pytest

from database.test_db import override_get_db

from comments.services import create_comment
from comments.schemas import Comment


class TestCommentTransaction:
    @pytest.mark.asyncio
    async def test_falied_transaction_create(self):
        with pytest.raises(Exception):
            database = next(override_get_db())
            comment = Comment(text="Test", post=12)
            response = await create_comment(comment, database, 12)
