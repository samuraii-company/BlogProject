from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import hashing
from users import models
from users import schemas
from . import services
from . import validators
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .jwt import create_access_token
from database import db

router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db.get_db)):
    """Login request"""

    user = database.query(models.Users).filter(models.Users.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")

    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")

    access_token = create_access_token(data={"id": user.id, "sub": user.email, "stuff": user.is_stuff})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.User)
async def register(user: schemas.User, database: Session = Depends(db.get_db)):
    """Create New User"""
    await validators.user_validation(user, database)
    await services.new_user_register(user, database)
    return JSONResponse(status_code=201, content={"status": "User was created"})
