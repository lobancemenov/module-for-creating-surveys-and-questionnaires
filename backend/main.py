from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← ДОБАВИТЬ
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

# ===== CORS Middleware (ОБЯЗАТЕЛЬНО!) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Vue/Vite dev server
        "http://localhost:5173",    # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Разрешить все заголовки
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