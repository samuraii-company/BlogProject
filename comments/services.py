from . import models
from . import schemas
from posts.models import Posts
from auth.schemas import TokenData
from users import models as user_models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


async def get_comments(id: int, database: Session):
    """Get comments by post"""
    return database.query(models.Comments).join(Posts).filter(models.Comments.post == id).all()


async def create_comment(comment: schemas.Comment, database: Session, id: int):
    """Create new comment"""
    try:
        _comment = models.Comments(text=comment.text, author=id, post=comment.post)
        database.add(_comment)

        _comments_count = (
            database.query(Posts)
            .filter(Posts.id == comment.post)
            .update({Posts.comments_count: Posts.comments_count + 1}, synchronize_session=False)
        )

        database.commit()
    except Exception as ex:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


async def delete_comment(id: int, database: Session, current_user: TokenData):
    """Delete comment"""

    _coment = database.query(models.Comments).filter(models.Comments.id == id).first()
    if any([_coment.author == current_user.id, current_user.is_stuff is True]):
        try:
            _comment = database.query(models.Comments).filter(models.Comments.id == id).first()
            _comments_count = (
                database.query(Posts)
                .filter(Posts.id == _comment.post)
                .update({Posts.comments_count: Posts.comments_count - 1}, synchronize_session=False)
            )
            database.query(models.Comments).filter(models.Comments.id == id).delete()
            database.commit()
        except Exception:
            database.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete not your comment")
