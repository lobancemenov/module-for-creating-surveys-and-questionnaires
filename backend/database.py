from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ===== Строка подключения =====
# Для PostgreSQL (оценка 4-5):
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/survey_db"

# Для SQLite (только для тестирования):
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# ===== Создание движка =====
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}  # Раскомментировать для SQLite
)

# ===== Сессия БД =====
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# ===== Базовый класс для моделей =====
Base = declarative_base()

# ===== Зависимость для получения сессии =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()