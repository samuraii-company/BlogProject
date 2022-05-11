from pydantic import BaseModel


class Like(BaseModel):
    post: int
