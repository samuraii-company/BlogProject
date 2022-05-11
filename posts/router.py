from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from auth.jwt import get_current_user
from . import services
from . import schemas
from . import validators

from database.db import get_db
from auth.schemas import TokenData


router = APIRouter(tags=["posts"], prefix="/api/v1/posts")


@router.get("/", response_model=List[schemas.OutPosts])
async def get_all_posts(user: int = None, database: Session = Depends(get_db)):
    """Get all posts

    return List[Posts] by user id or list[shuffle(Posts)]
    """

    if not user:
        posts = await services.get_all_posts(database)
    else:
        posts = await services.get_posts(user, database)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found")

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_posts(
    post: schemas.Post, database: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    await services.create_post(post, database, current_user.id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Post was created")


@router.get("/{id}/", response_model=schemas.OutDetailPost)
async def get_post_by_id(id: int, database: Session = Depends(get_db)):

    _post = await services.get_post_by_id(id, database)

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return _post


@router.delete("/{id}/", response_class=JSONResponse)
async def delete_post_by_id(
    id: int, database: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    """Delete post by id"""

    _post = await validators.post_exists(id, database)
    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    await services.delete_post(id, database, current_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content="Post was deleted")
