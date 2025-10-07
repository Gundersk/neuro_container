from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from pydantic import BaseModel
from typing import Optional
from fastapi import Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from models import TokenBlackList


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = os.getenv("SECRET_KEY", "qwertyuiop")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    expire: Optional[datetime] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if(expires_delta):
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        expire: datetime = payload.get('exp')
        if(username is None):
            return None
        return TokenData(username=username, expire=expire)
    except JWTError:
        return None

def token_not_blacklisted(tokenHash = Depends(oauth2_scheme), db = Depends(get_db)):
    token =  db.query(TokenBlackList).filter(TokenBlackList.tokenHash == tokenHash).first()
    if(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token

