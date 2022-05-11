from sqlalchemy.orm import Session
from . import models


async def get_all_users(database: Session):
    """Get all users"""

    return database.query(models.Users).all()


async def get_user_by_id(id: int, database: Session):
    """Get user by id"""

    return database.query(models.Users).filter(models.Users.id == id).first()


async def delete_user_by_id(id: int, database: Session):
    """Delete user by id"""

    database.query(models.Users).filter(models.Users.id == id).delete()
    database.commit()
