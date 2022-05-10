from users import schemas
from users import models

from auth import hashing

from sqlalchemy.orm import Session


async def new_user_register(user: schemas.User, database: Session):
    """Create new user"""

    _user = models.Users(email=user.email, username=user.username, password=hashing.get_password_hash(user.password))

    database.add(_user)
    database.commit()
    database.refresh(_user)
