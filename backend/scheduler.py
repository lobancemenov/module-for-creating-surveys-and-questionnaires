"""
Планировщик фоновых задач для Survey API
Используется APScheduler для периодического выполнения задач
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from database import SessionLocal
from models import SurveyModel

# ===== Логирование =====
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ===== Глобальный планировщик =====
scheduler = AsyncIOScheduler()

# ===== КОНФИГУРАЦИЯ (из env или default) =====
# Для тестирования ставим маленькие интервалы
# Для production увеличить до дней/недель
AUTO_DEACTIVATE_DAYS = int(__import__('os').environ.get('AUTO_DEACTIVATE_DAYS', 1))  # дней до деактивации
AUTO_DELETE_DAYS = int(__import__('os').environ.get('AUTO_DELETE_DAYS', 7))  # дней до удаления
CLEANUP_INTERVAL_HOURS = int(__import__('os').environ.get('CLEANUP_INTERVAL_HOURS', 1))  # как часто запускать


# ===== ЗАДАЧА 1: Авто-деактивация старых опросов =====
def auto_deactivate_old_surveys():
    """
    Деактивирует опросы, созданные больше чем AUTO_DEACTIVATE_DAYS дней назад
    """
    db = SessionLocal()
    try:
        cutoff_date = datetime.now() - timedelta(days=AUTO_DEACTIVATE_DAYS)

        # Находим активные опросы старше cutoff_date
        old_surveys = db.query(SurveyModel).filter(
            SurveyModel.is_active == True,
            SurveyModel.created_at < cutoff_date
        ).all()

        deactivated_count = 0
        for survey in old_surveys:
            survey.is_active = False
            deactivated_count += 1
            logger.info(f"Деактивирован опрос #{survey.id} '{survey.title}'")

        db.commit()

        if deactivated_count > 0:
            logger.info(f"✅ Авто-деактивация: {deactivated_count} опросов деактивировано")
        else:
            logger.info("ℹ️ Авто-деактивация: нет опросов для деактивации")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Ошибка авто-деактивации: {str(e)}")
    finally:
        db.close()


# ===== ЗАДАЧА 2: Авто-удаление старых неактивных опросов =====
def auto_delete_inactive_surveys():
    """
    Удаляет неактивные опросы, которые были деактивированы больше чем AUTO_DELETE_DAYS дней назад
    """
    db = SessionLocal()
    try:
        # Для простоты удаляем неактивные опросы старше cutoff_date
        cutoff_date = datetime.now() - timedelta(days=AUTO_DELETE_DAYS)

        # Находим неактивные опросы старше cutoff_date
        old_inactive = db.query(SurveyModel).filter(
            SurveyModel.is_active == False,
            SurveyModel.created_at < cutoff_date
        ).all()

        deleted_count = 0
        for survey in old_inactive:
            db.delete(survey)
            deleted_count += 1
            logger.info(f"Удалён опрос #{survey.id} '{survey.title}'")

        db.commit()

        if deleted_count > 0:
            logger.info(f"✅ Авто-удаление: {deleted_count} опросов удалено")
        else:
            logger.info("ℹ️ Авто-удаление: нет опросов для удаления")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Ошибка авто-удаления: {str(e)}")
    finally:
        db.close()


# ===== ЗАДАЧА 3: Полная очистка (деактивация + удаление) =====
def cleanup_all_surveys():
    """
    Запускает обе задачи очистки
    """
    logger.info("🧹 Запуск полной очистки опросов...")
    auto_deactivate_old_surveys()
    auto_delete_inactive_surveys()
    logger.info("🧹 Очистка завершена")


# ===== ИНИЦИАЛИЗАЦИЯ ПЛАНИРОВЩИКА =====
def start_scheduler():
    """
    Запускает планировщик с задачами
    """
    # Задача 1: Авто-деактивация каждый час
    scheduler.add_job(
        func=auto_deactivate_old_surveys,
        trigger=IntervalTrigger(hours=CLEANUP_INTERVAL_HOURS),
        id='auto_deactivate_surveys',
        name='Авто-деактивация старых опросов',
        replace_existing=True
    )

    # Задача 2: Авто-удаление каждый день в 3 ночи
    scheduler.add_job(
        func=auto_delete_inactive_surveys,
        trigger=CronTrigger(hour=3, minute=0),  # в 3:00 ночи
        id='auto_delete_surveys',
        name='Авто-удаление неактивных опросов',
        replace_existing=True
    )

    # Задача 3: Логирование статуса (каждые 6 часов)
    scheduler.add_job(
        func=lambda: logger.info("📊 Scheduler status: OK"),
        trigger=IntervalTrigger(hours=6),
        id='scheduler_health_check',
        name='Проверка здоровья планировщика',
        replace_existing=True
    )

    # Запуск планировщика
    scheduler.start()
    logger.info("⏰ Планировщик задач запущен")

    # Вывод информации о задачах
    for job in scheduler.get_jobs():
        logger.info(f"  📋 Задача: {job.name} | Next run: {job.next_run_time}")


# ===== ОСТАНОВКА ПЛАНИРОВЩИКА =====
def stop_scheduler():
    """
    Останавливает планировщик при закрытии приложения
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("⏰ Планировщик задач остановлен")


# ===== РУЧНОЙ ЗАПУСК (для тестирования через API) =====
def run_cleanup_now():
    """
    Запускает очистку немедленно (для тестирования)
    """
    logger.info("🚀 Ручной запуск очистки...")
    cleanup_all_surveys()
    return {"message": "Очистка выполнена", "timestamp": datetime.now().isoformat()}