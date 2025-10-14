from sqlalchemy.orm import Session
from chat.schemas import ChatRequest, UniversalChatRequest
from chat.repository import Conversations, Messages
from core.contracts import ChatMessage


def get_universal_context(db: Session, user_request: ChatRequest, user_id: int) -> UniversalChatRequest:
    system = user_request.system_prompt_override
    if(not system):
        system = db.query(Conversations.system_prompt).filter(Conversations.id == user_request.conversation_id).scalar()
    chat_history = db.query(Messages.role, Messages.content).filter(Messages.conversation_id == user_request.conversation_id).order_by(Messages.created_at).all()
    chat_history_in_messages = [ChatMessage(role=r, content=c) for r, c in chat_history]
    target_model = user_request.target_model
    if(not target_model):
        target_model = db.query(Conversations.default_model).filter(Conversations.id == user_request.conversation_id).scalar()
    
    universal_context = UniversalChatRequest(conversation_id=user_request.conversation_id, user_id=user_id.id, system_prompt=system, messages=chat_history_in_messages, target_model=target_model)

    return  universal_context

