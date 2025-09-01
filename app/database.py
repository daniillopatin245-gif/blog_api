# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Создаём engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Проверяет соединение перед запросом
    echo=False  # Включи, чтобы видеть SQL-запросы (для отладки)
)

# Сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для внедрения сессии в FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()