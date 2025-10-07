from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TokenBlackList(Base):
    __tablename__ = 'token_black_list'

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"), index=True)
    tokenHash = Column(String, unique=True)
    timeToDelete = Column(DateTime)


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