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

    scheduler.start()


# def schedule_fcm_push(task_id: int, run_time: datetime):
#     def job():
#         db = Session()
#         try:
#             task = db.get(Task, task_id)
#             if not task:
#                 return
#
#             user = db.get(User, task.user_id)
#             if not user or not user.fcm_token:
#                 return
#
#             plant_name = task.plant.name if task.plant else "растения"
#
#             send_fcm_notification(
#                 token=user.fcm_token,
#                 title="Напоминание 🌿",
#                 body=f"Пора {task.care_type} для {plant_name}"
#             )
#         finally:
#             db.close()

    scheduler.add_job(
        job,
        trigger=DateTrigger(run_date=run_time),
        id=f"task_push_{task_id}",
        replace_existing=True,
    )
