from sqlalchemy.orm import Session
from chat.models import Conversations, Messages
from core.contracts import Role
from typing import Optional
from datetime import datetime

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

def list_messages(db: Session, conversation_id: int, limit: int = 50, offset: int = 0):
    return (
        db.query(Messages)
        .filter(Messages.conversation_id == conversation_id)
        .order_by(Messages.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )