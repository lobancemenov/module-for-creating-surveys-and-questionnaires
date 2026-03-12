from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import router
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Создание таблиц БД =====
logger.info("📦 Создание таблиц БД...")
Base.metadata.create_all(bind=engine)
logger.info("✅ Таблицы созданы")

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
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Приветствие =====
@app.get("/")
async def home():
    return {
        "message": "Survey API работает!",
        "docs": "/docs",
        "endpoints": "/surveys"
    }

# ===== Health Check =====
@app.get("/health")
async def health():
    return {"status": "ok"}

# ===== Подключение роутов =====
app.include_router(router)

# ===== Проверка роутов при старте =====
@app.on_event("startup")
async def print_routes():
    logger.info("\n=== ЗАРЕГИСТРИРОВАННЫЕ РОУТЫ ===")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ', '.join(route.methods)
            logger.info(f"{methods:20} {route.path}")
    logger.info("=== КОНЕЦ СПИСКА ===\n")