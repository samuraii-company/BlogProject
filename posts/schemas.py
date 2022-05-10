from pydantic import BaseModel
from users import schemas
from comments import schemas as com_schemas
from typing import Optional, List
from datetime import datetime


class Post(BaseModel):
    title: str
    text: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Test Title",
                "text": "Test Text",
            }
        }


class OutPosts(BaseModel):
    id: int
    title: str
    likes_count: Optional[int]
    comments_count: Optional[int]
    created_at: datetime
    post_author: schemas.OutUser

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Test Title",
                "likes_count": 100,
                "comments_count": 140,
                "created_at": "2022-05-10T23:20:50.977088",
                "post_author": {"id": 1, "username": "Samuraii"},
            }
        }


class OutDetailPost(BaseModel):
    id: int
    title: str
    text: str
    likes_count: Optional[int]
    comments_count: Optional[int]
    created_at: datetime
    post_author: schemas.OutUser
    comments: Optional[List[com_schemas.OutComments]] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Test Title",
                "text": "Test Text",
                "created_at": "2022-05-10T23:20:50.977088",
                "likes_count": 100,
                "comments_count": 140,
                "post_author": {"id": 1, "username": "Samuraii"},
                "comments": [],
            }
        }
