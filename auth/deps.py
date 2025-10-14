from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from fastapi import Depends, status
from .tokens import verify_token
from .repository import get_user_by_username_or_email
from core.database import get_db
from .models import TokenBlackList

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  
    )
     
    token_data = verify_token(token)
    if(token_data is None):
        raise ValueError
    user = get_user_by_username_or_email(token_data.username, db)
    if(user is None):
        raise ValueError
    return user

def token_not_blacklisted(tokenHash = Depends(oauth2_scheme), db = Depends(get_db)):
    token =  db.query(TokenBlackList).filter(TokenBlackList.tokenHash == tokenHash).first()
    if(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token
