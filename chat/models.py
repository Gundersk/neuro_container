from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from core.database import Base

class Conversations(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    default_model = Column(String)
    system_prompt = Column(String)
    timestamps = Column(DateTime)

class Messages(Base):
    __tablename__ = 'messangers'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    content = Column(String)
    role = Column(String)
    model = Column(String)
    error = Column(String)
    created_at = Column(DateTime)