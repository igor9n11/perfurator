from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

# check_same_thread=False нужен для SQLite: FastAPI обрабатывает запросы
# в разных потоках, а по умолчанию SQLite это запрещает.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей в models.py."""


def get_db():
    """Зависимость FastAPI: открывает сессию БД на время запроса и закрывает после."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создаёт таблицы для всех моделей, если их ещё нет."""
    Base.metadata.create_all(bind=engine)
