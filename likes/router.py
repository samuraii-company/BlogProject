from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from auth.jwt import get_current_user
from . import services
from . import schemas
from . import validators

from posts.validators import post_exists

from database.db import get_db
from auth.schemas import TokenData


router = APIRouter(tags=["likes"], prefix="/api/v1/likes")


@router.post("/", response_class=JSONResponse)
async def like(
    like: schemas.Like, database: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    """Add like on post or delete likes from post"""

    _post = await post_exists(like.post, database)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    _like = await validators.like_exists(like.post, database, current_user.id)

    if not _like:
        await services.add_like(like, database, current_user.id)
    else:
        await services.delete_like(like, database, current_user.id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success"})
