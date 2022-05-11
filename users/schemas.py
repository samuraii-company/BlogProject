from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "username": "Samuraii",
                "email": "test@gmail.com",
                "password": "secretpassword",
                "password2": "secretpassword",
            }
        }


class OutUser(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "username": "Samuraii"}}
