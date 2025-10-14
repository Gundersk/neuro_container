from fastapi import APIRouter, Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .models import User
import core.database as database
import auth.schemas as auth_schemas
import auth.repository as auth_repository
import auth.deps as auth_deps
import auth.service as auth_service
import auth.tokens as auth_tokens

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

@router.post('/register') 
def register(user_data: auth_schemas.UserCreate, 
             db = Depends(database.get_db)) -> auth_schemas.UserResponce:
    user = auth_repository.create_user(db, user_data.username, user_data.password, user_data.email)
    return user

@router.post('/login', response_model=auth_schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
          db = Depends(database.get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if(not user):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_tokens.create_access_token({'sub': user.username})
    return auth_schemas.Token(access_token=token, token_type="bearer")

@router.post('/logout')
def logout(current_user = Depends(auth_deps.get_current_user), 
           token: str = Depends(auth_deps.oauth2_scheme), 
           db = Depends(database.get_db)):
    thow_token = auth_repository.throw_token_to_black_list(token, db)
    return {"Успешно вышли"}

@router.get('/user/me', response_model=auth_schemas.UserResponce) 
def read_user_me(current_user = Depends(auth_deps.get_current_user), 
                logout_check = Depends(auth_deps.token_not_blacklisted)) -> auth_schemas.UserResponce:
    return current_user