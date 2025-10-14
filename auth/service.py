from sqlalchemy.orm import Session
from .security import verify_password
from .repository import get_user_by_username_or_email

def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_username_or_email(login, db)

    if(user is None):
        return False
    if(verify_password(password, user.password_hash) == False):
        return False
    
    return user