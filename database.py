from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = 'sqlite:///./chat_app.db'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()