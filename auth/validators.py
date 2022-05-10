from typing import Optional

from sqlalchemy.orm import Session
from users import models
from users import schemas

from fastapi import (
    HTTPException,
    status,
)


async def user_validation(user: schemas.User, database: Session):
    """User Validation"""

    if not user.password == user.password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords don't match")

    if (
        database.query(models.Users)
        .filter(models.Users.email == user.email or models.Users.username == user.username)
        .first()
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")

    return True
