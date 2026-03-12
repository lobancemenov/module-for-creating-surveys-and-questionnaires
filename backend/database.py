from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# ===== Строка подключения =====
# Для PostgreSQL:
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/survey_db"
)

# Для SQLite (раскомментируйте если нужно):
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# ===== Создание движка =====
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True
    )

# ===== Сессия БД =====
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# ===== Базовый класс =====
Base = declarative_base()

# ===== Зависимость =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()