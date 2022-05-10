from . import models
from sqlalchemy.orm import Session


async def user_exists(id: int, database: Session):
    """Check user exists in system"""

    return database.query(models.Users).filter(models.Users.id == id).first()
