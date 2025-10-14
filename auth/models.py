from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from core.database import Base
from datetime import datetime

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
