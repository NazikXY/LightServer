from pydantic import BaseModel


class BaseUser(BaseModel):
    login: str


class UserCreate(BaseUser):
    name: str
    password: str


class User(BaseUser):
    id: int
    name: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
