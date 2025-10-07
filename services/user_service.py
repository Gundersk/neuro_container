from sqlalchemy.orm import Session
from models import User, TokenBlackList
from typing import Optional
from sqlalchemy import or_
from security import hash_password, verify_password
from fastapi import Depends
from auth_security import oauth2_scheme
from auth_security import verify_token
from datetime import timedelta
from database import get_db

def get_user_by_username_or_email(login: str, db: Session):
    return(db.query(User).filter(or_(User.email == login,  User.username == login)).first())

def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_username_or_email(login, db)

    if(user is None):
        return False
    if(verify_password(password, user.password_hash) == False):
        return False
    
    return user
    
def create_user(db: Session, username: str, password: str, email: Optional[str] = None):

    if(get_user_by_username_or_email(username, db)):
        raise ValueError("Пользователь с таким именем существует")
    if(email and get_user_by_username_or_email(email, db)):
        raise ValueError("Пользователь с таким email существует")

    password_hash = hash_password(password)
    user = User(username=username, password_hash=password_hash, email=email)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        db.rollback()
        raise RuntimeError('Ошибка при  создании пользователя')

def throw_token_to_black_list(token: str, db: Session):
    token_data = verify_token(token)
    user = db.query(User).filter(User.username == token_data.username).first()
    token_throw = TokenBlackList(userId=user.id, tokenHash=token, timeToDelete=token_data.expire)
    db.add(token_throw)
    db.commit()
    db.refresh(token_throw)
    return token_throw

def check_token_in_black_list(tokenHash: str, db = Session):
    return db.query(TokenBlackList).filter(TokenBlackList.tokenHash == tokenHash).first()