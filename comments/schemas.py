from pydantic import BaseModel
from datetime import datetime
from users.schemas import OutUser


class Comment(BaseModel):
    text: str
    post: int


class OutComments(BaseModel):
    id: int
    text: str
    created_at: datetime
    comment_author: OutUser

    class Config:
        orm_mode = True
