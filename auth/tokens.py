from typing import Optional
from datetime import datetime, timedelta
from .settings import *
from .schemas import TokenData
from jose import jwt, JWTError

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

