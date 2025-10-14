from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Базовое сообщение


class UniversalChatResponce(BaseModel):
    content: str
    model: str
    created_at: datetime
    tokens_used: Optional[int] = None
    provider = Optional[str] = None