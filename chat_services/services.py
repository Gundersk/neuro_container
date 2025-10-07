from sqlalchemy.orm import Session
from models import Conversations, Messages
from datetime import datetime
from typing import Literal, Optional
from chat_services.pydentic_models import Role, ChatRequest
from fastapi import Depends, HTTPException
from auth import get_current_user
from models import User
from chat_services.pydentic_models import ChatMessage, UniversalChatRequest, Role
from openai import OpenAI
import os
import logging, traceback

logger = logging.getLogger("app.providers")

def get_conversations(db: Session, conversations_id: int, user_id: int):
    return db.query(Conversations).filter(Conversations.id == conversations_id, Conversations.user_id == user_id).first()



def create_conversations(
        db: Session, 
        title:str, 
        user_id: int, 
        model: str | None = None, 
        system_prompt: str | None = None
):
    chat = Conversations(
        title=title, 
        user_id=user_id, 
        default_model=model, 
        system_prompt=system_prompt, 
        timestamps=datetime.utcnow()
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def create_message(
        db: Session, 
        role: Role,
        content: str, 
        conversation_id: int, 
        model: str, 
        error: Optional[str] = None
        ):
    message = Messages(conversation_id=conversation_id, content=content, role=role, model=model, error=error, created_at=datetime.utcnow())
    try:
        db.add(message)
        db.commit()
        db.refresh(message)
    except:
        raise RuntimeError("Ошибка добавления сообщения в базу данных")
    return message
    
def get_universal_context(db: Session, user_request: ChatRequest, current_user: User) -> UniversalChatRequest:
    system = user_request.system_prompt_override
    if(not system):
        system = db.query(Conversations.system_prompt).filter(Conversations.id == user_request.conversation_id).scalar()
    chat_history = db.query(Messages.role, Messages.content).filter(Messages.conversation_id == user_request.conversation_id).order_by(Messages.created_at).all()
    chat_history_in_messages = [ChatMessage(role=r, content=c) for r, c in chat_history]
    target_model = user_request.target_model
    if(not target_model):
        target_model = db.query(Conversations.default_model).filter(Conversations.id == user_request.conversation_id).scalar()
    
    universal_context = UniversalChatRequest(conversation_id=user_request.conversation_id, user_id=current_user.id, system_prompt=system, messages=chat_history_in_messages, target_model=target_model)

    return  universal_context
  

def models_adapter(universal_context: UniversalChatRequest):
    if(universal_context.target_model.startswith('deepseek')):
        base_url = "https://api.deepseek.com"
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=base_url)
    elif(universal_context.target_model.startswith('gpt')):
        base_url = "https://api.openai.com/v1"
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), base_url=base_url)
    else:
        raise ValueError(f"Unknown model provider for '{universal_context.target_model}'")
    
    provider_message = list()
    provider_message.extend([m.model_dump() for m in universal_context.messages])
        
    if(universal_context.system_prompt):
        provider_message.insert(0, {'role': 'system', 'content': universal_context.system_prompt})
    try:
        completion = client.chat.completions.create(
            model=universal_context.target_model,
            messages=provider_message
        )
    except Exception as e:
        logger.error('Provider error: {type(e).__name__}, {e}', exc_info=True)
        raise

    return(completion.choices[0].message.content)
    
    
    
    