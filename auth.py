from pydantic import BaseModel, ConfigDict
from typing import Optional
import os
from datetime import datetime
from auth_security import verify_token
from auth_security import oauth2_scheme
from fastapi import Depends, HTTPException, status
from database import get_db
from services.user_service import get_user_by_username_or_email



SECRET_KEY = os.getenv("SECRET_KEY", "qwertyuiop")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    
def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  # важно для Swagger
    )
     
    token_data = verify_token(token)
    if(token_data is None):
        raise ValueError
    user = get_user_by_username_or_email(token_data.username, db)
    if(user is None):
        raise ValueError
    return user


