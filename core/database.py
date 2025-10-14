from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_URL = 'sqlite:///./chat_app.db'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()