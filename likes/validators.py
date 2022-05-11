from . import models
from sqlalchemy.orm import Session


async def like_exists(post_id: int, database: Session, user_id: int):
    """Check if user already liked this post"""

    return database.query(models.Likes).filter(models.Likes.post == post_id, models.Likes.user == user_id).first()
