"""
database.py
Устанавливает соединение с базой данных
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from config import settings

load_dotenv()

DATABASE_HOST = settings.database_url
Base = declarative_base()
engine = create_engine(DATABASE_HOST, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Инициализация базы данных."""
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)


def get_db():
    """Создает сессию для доступа к базе данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
