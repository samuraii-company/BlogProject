from . import models
from . import schemas
from auth.schemas import TokenData
from users import models as user_models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


async def get_posts(id: int, database: Session):
    """Get posts by query params id"""

    return database.query(models.Posts).join(user_models.Users).filter(models.Posts.author == id).all()


async def create_post(post: schemas.Post, database: Session, author_id: int):
    """Create New Post"""

    _new_post = models.Posts(title=post.title, text=post.text, author=author_id)

    database.add(_new_post)
    database.commit()
    database.refresh(_new_post)


async def get_post_by_id(id: int, database: Session):
    """Get post by id"""

    return database.query(models.Posts).filter(models.Posts.id == id).first()


async def delete_post(id: int, database: Session, user: TokenData):
    """Delete Post"""

    _post = database.query(models.Posts).filter(models.Posts.id == id).first()
    if any([_post.author == user.id, user.is_stuff is True]):
        database.query(models.Posts).filter(models.Posts.id == id).delete()
        database.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete not your post")
