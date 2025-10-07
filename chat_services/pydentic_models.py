from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import Literal
from datetime import datetime
from enum import Enum
from models import Messages


class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    tool = "tool"

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"] = "user"
    content: str

class ChatRequest(BaseModel):   
    conversation_id: int
    message: str
    target_model: Optional[str] = None
    system_prompt_override: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    conversation_id: int
    message: ChatMessage
    model: str

class ConversationsRequest(BaseModel):
    title: Optional[str] = None
    default_model: Optional[str] = None
    system_prompt: Optional[str] = None


class ConversationOut(BaseModel):
    id: int
    title: Optional[str]
    default_model: Optional[str]
    system_prompt: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True) 

class UniversalChatRequest(BaseModel):
    conversation_id : int
    user_id: int
    system_prompt: Optional[str] = None
    messages: list[ChatMessage]
    target_model: str
    

def PackResponse(message: Messages) -> ChatResponse:
    chat_message = ChatMessage(role=Role.assistant.value, content=message.content)
    chat_response = ChatResponse(conversation_id=message.conversation_id, message=chat_message, model=message.model)
    return chat_response
