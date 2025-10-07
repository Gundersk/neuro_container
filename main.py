from models import*
from database import*
from auth import*
from services.user_service import*
from fastapi import Depends, FastAPI, Response
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from auth_security import Token, create_access_token, token_not_blacklisted
import uvicorn
from chat_services.pydentic_models import ChatRequest, ConversationsRequest, Role, ChatResponse, PackResponse
from chat_services.services import get_conversations, create_conversations, create_message, get_universal_context, models_adapter

app = FastAPI()
create_tables()


@app.post('/register') 
def register(user_data: UserCreate, db = Depends(get_db)) -> UserResponce:
    user = create_user(db, user_data.username, user_data.password, user_data.email)
    return user

@app.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if(not user):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({'sub': user.username})
    return Token(access_token=token, token_type="bearer")

@app.post('/logout')
def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    thow_token = throw_token_to_black_list(token, db)
    return {"Успешно вышли"}

@app.post('/chat')
def chat_endpoint(
        request_data: ChatRequest,
        db = Depends(get_db),
        current_user = Depends(get_current_user), 
        logout_check = Depends(token_not_blacklisted), 
        ):
    if(not get_conversations(db, request_data.conversation_id, current_user.id)):
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = create_message(
        db, 
        Role.user.value, 
        request_data.message, 
        request_data.conversation_id, 
        request_data.target_model)
    universal_context = get_universal_context(db, request_data, current_user)
    completion = ''
    error = ''
    try:
        completion = models_adapter(universal_context)
    except:
        error = 'Ошибка отправки сообщения'
    new_message = create_message(
        db, 
        Role.assistant.value, 
        completion, 
        request_data.conversation_id,
        universal_context.target_model,
        error
        )
    response = PackResponse(new_message)
    return response
    
    

@app.post('/conversations')
def crate_chat(
        request_data: ConversationsRequest, 
        db = Depends(get_db), 
        current_user = Depends(get_current_user), 
        logout_check = Depends(token_not_blacklisted)
):
    chat = create_conversations(db, request_data.title, current_user.id, request_data.default_model, request_data.system_prompt)
    return chat

@app.get('/user/me')
def read_user_me(current_user: User = Depends(get_current_user), logout_check = Depends(token_not_blacklisted)):
    return current_user

@app.get('/protected-data')
def get_protected_data(current_user: User = Depends(get_current_user), logout_check = Depends(token_not_blacklisted)):
    return{"message": "YOOO", "user_id": current_user.id}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)