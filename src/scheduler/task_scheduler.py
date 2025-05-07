from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from database import SessionLocal
from service.task_service import generate_tasks


def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")

    @scheduler.scheduled_job(CronTrigger(minute='*/1'))  # запуск каждый день в 00:00 UTC -- в проде надо поменять на CronTrigger(hour=0) CronTrigger(minute='*/1') -- каждую минуту
    def scheduled_task_generation():
        db = SessionLocal()
        try:
            generate_tasks(db)
        finally:
            db.close()

    scheduler.start()

