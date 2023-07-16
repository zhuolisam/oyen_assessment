from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenCreate(TokenBase):
    username: str | None = None


class LoginSessionBase(BaseModel):
    created_at: datetime


class LoginSessionInDB(LoginSessionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
