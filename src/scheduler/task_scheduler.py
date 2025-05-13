from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

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
        now_utc = datetime.utcnow().replace(second=0, microsecond=0)

        db = SessionLocal()
        try:
            tasks = db.query(Task).all()

            for task in tasks:
                user = db.get(User, task.user_id)
                if not user or not user.fcm_token:
                    continue

                user_tz = ZoneInfo(user.timezone)
                task_time_local = task.scheduled_at.astimezone(user_tz)
                now_local = now_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(user_tz)

                if task_time_local.replace(second=0, microsecond=0) == now_local:
                    plant_name = task.plant.name if task.plant else "растения"
                    print(f"⏰ Отправляем пуш по задаче #{task.id} на {task_time_local}")

                    send_fcm_notification(
                        token=user.fcm_token,
                        title="Напоминание 🌿",
                        body=f"Пора {task.care_type} для {plant_name}"
                    )
        finally:
            db.close()

    scheduler.start()
