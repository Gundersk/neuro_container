from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    expire: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponce(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LoginResponce(BaseModel):
    access_token: str
    token_type: str
    user: UserResponce
    

