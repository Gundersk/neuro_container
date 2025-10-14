from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum

# Роли сообщений в чате
class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    tool = "tool"

class ChatMessage(BaseModel):       
    role: Literal["system", "user", "assistant", "tool"] = "user"
    content: str

# Что отправляем в LLM слой сервиса
class UniversalChatRequest(BaseModel):
    conversation_id : int
    user_id: int
    system_prompt: Optional[str] = None
    messages: list[ChatMessage]
    target_model: str