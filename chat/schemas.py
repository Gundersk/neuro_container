from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import Literal
from datetime import datetime
from enum import Enum
import core.contracts as contracts





# API-СХЕМЫ: запросы и ответы клиента

# Что клиент отправляет при отправке сообщения
class ChatRequest(BaseModel):   
    conversation_id: int
    message: str
    target_model: Optional[str] = None
    system_prompt_override: Optional[str] = None
    stream: bool = False

# Что API возвращает клиенту после обработки сообщения

class ChatResponse(BaseModel):
    conversation_id: int
    message: contracts.ChatMessage
    model: str

# API-СХЕМЫ: работа с чатами

# Запрос на создание нового чата
class ConversationsRequest(BaseModel):
    title: Optional[str] = None
    default_model: Optional[str] = None
    system_prompt: Optional[str] = None

# Ответ при получении чата
class ConversationOut(BaseModel):
    id: int
    title: Optional[str]
    default_model: Optional[str]
    system_prompt: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)     # Позволяет вернуть SQLAlchemy-модель напрямую

class UniversalChatRequest(BaseModel):
    conversation_id : int
    user_id: int
    system_prompt: Optional[str] = None
    messages: list[contracts.ChatMessage]
    target_model: str