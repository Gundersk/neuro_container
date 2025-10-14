from .security import verify_password, hash_password
from .tokens import verify_token
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import User, TokenBlackList

def get_user_by_username_or_email(login: str, db: Session):
    return(db.query(User).filter(or_(User.email == login,  User.username == login)).first())


    
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