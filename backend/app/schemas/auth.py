from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_role: str
    username: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True
