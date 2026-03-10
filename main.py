from fastapi import FastAPI
from database import Base, engine
from routes import router

# ===== Создание таблиц БД =====
Base.metadata.create_all(bind=engine)

# ===== Приложение FastAPI =====
app = FastAPI(
    title="Survey API",
    description="Модуль для создания опросов",
    version="0.2.0"
)

# ===== Приветствие =====
@app.get("/")
async def home():
    return {
        "message": "Это API для управления опросами. Перейдите на /docs для тестирования.",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# ===== Подключение роутов =====
app.include_router(router)

# ===== Запуск: uvicorn main:app --reload =====