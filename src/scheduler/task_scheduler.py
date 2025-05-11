from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from sqlalchemy.orm import Session

from database import SessionLocal, Task, User
from service.fcm_service import send_fcm_notification
from service.task_service import generate_tasks

scheduler = BackgroundScheduler(timezone="UTC")


def start_scheduler():
    @scheduler.scheduled_job(CronTrigger(minute='*/1'))
    def scheduled_task_generation():
        db = SessionLocal()
        try:
            generate_tasks(db)
        finally:
            db.close()

    @scheduler.scheduled_job(CronTrigger(minute='*/1'))
    def check_scheduled_tasks():
        now = datetime.utcnow().replace(second=0, microsecond=0)

        db = SessionLocal()
        try:
            tasks = db.query(Task).filter(Task.scheduled_at == now).all()
            for task in tasks:
                user = db.get(User, task.user_id)
                if not user or not user.fcm_token:
                    continue

                plant_name = task.plant.name if task.plant else "растения"

                print(f"Отправляем пуш по задаче #{task.id} на {now}")
                send_fcm_notification(
                    token=user.fcm_token,
                    title="Напоминание 🌿",
                    body=f"Пора {task.care_type} для {plant_name}"
                )
        finally:
            db.close()


    scheduler.start()
