from . import models
from sqlalchemy.orm import Session


async def post_exists(id: int, database: Session):
    """Check post exists in system"""

    return database.query(models.Posts).filter(models.Posts.id == id).first()
