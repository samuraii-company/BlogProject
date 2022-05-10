from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from typing import List

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from auth.jwt import get_stuff_user
from . import services
from . import schemas
from . import validators

from database.db import get_db
from auth.schemas import TokenData

router = APIRouter(tags=["users"], prefix="/api/v1/users")


@router.get("/", response_model=List[schemas.OutUser])
async def get_all_users(database: Session = Depends(get_db)):
    """Get all users"""
    users = await services.get_all_users(database)
    return users


@router.get("/{id}/", response_model=schemas.OutUser)
async def get_user_by_id(id: int, database: Session = Depends(get_db)):
    """Get user by id"""

    _user = await services.get_user_by_id(id, database)
    if not _user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

    return _user


@router.delete("/{id}/", response_class=JSONResponse)
async def delete_user_by_id(
    id: int, database: Session = Depends(get_db), current_user: TokenData = Depends(get_stuff_user)
):
    """Delete user by id"""

    _user = await validators.user_exists(id, database)
    if not _user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await services.delete_user_by_id(id, database)

    return JSONResponse(status_code=status.HTTP_200_OK, content="User was deleted")
