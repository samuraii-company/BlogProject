from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from auth.jwt import get_current_user
from . import services
from . import schemas
from . import validators

from posts.validators import post_exists

from database.db import get_db
from auth.schemas import TokenData


router = APIRouter(tags=["comments"], prefix="/api/v1/comments")


@router.get("/", response_model=List[schemas.OutComments])
async def get_comments_by_post(post: int = Query(...), database: Session = Depends(get_db)):
    """Get comments by post"""

    _post = await post_exists(post, database)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    _comments = await services.get_comments(post, database)

    if not _comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found")

    return _comments


@router.post("/")
async def create_comment(
    comment: schemas.Comment, database: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    """Create new comment"""

    _post = await post_exists(comment.post, database)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    await services.create_comment(comment, database, current_user.id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Comment was added")


@router.delete("/{id}/", response_class=JSONResponse)
async def delete_comment(
    id: int, database: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    """Delete comment"""

    _comment = await validators.comment_exists(id, database)
    if not _comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    await services.delete_comment(id, database, current_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content="Comment was deleted")
