from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import appException
from database import Care, Task, TaskStatus
from schema.plant import Interval
import calendar
import random

from service.service import DefaultService


class TaskService(DefaultService):
    def get_today_tasks(self, user_id: int) -> list:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        today_end = today_start + timedelta(days=1)

        tasks = self.session.scalars(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.scheduled_at >= today_start)
            .where(Task.scheduled_at < today_end)
            .order_by(Task.scheduled_at)
        ).all()

        return tasks

    def update_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise appException.task.TaskNotFound()
        if task:
            task.status = new_status
            self.session.commit()
            self.session.refresh(task)
            return task
        return None

def is_new_interval(now: datetime, last: datetime, interval: Interval) -> bool:
    if interval == Interval.DAY:
        return now.date() > last.date()
    elif interval == Interval.WEEK:
        return now.isocalendar()[1] > last.isocalendar()[1] or now.year > last.year
    elif interval == Interval.MONTH:
        return now.month > last.month or now.year > last.year
    return False


def generate_distribution_dates(interval: str, count: int, user, tz: str, start_time: datetime) -> list[datetime]:
    dates = []

    if interval == Interval.DAY:
        total_minutes = (user.workday_end - user.workday_start) * 60
        step = total_minutes // (count + 1)
        for i in range(count):
            dt = start_time.replace(
                hour=user.workday_start,
                minute=0,
                second=0,
                microsecond=0
            ) + timedelta(minutes=step * (i + 1))
            dates.append(dt)

    elif interval == Interval.WEEK:
        total_days = 7
        daily_slots = total_days // count if count <= total_days else 1
        total_minutes = (user.workday_end - user.workday_start) * 60
        step_minutes = total_minutes // (count + 1)
        tz = ZoneInfo(tz)
        for i in range(count):
            day_offset = i * daily_slots
            time_offset = step_minutes * (i + 1)
            hour = user.workday_start + time_offset // 60
            minute = time_offset % 60
            local_dt = (start_time + timedelta(days=day_offset)).replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
                tzinfo=tz

            )

            dates.append(local_dt)

    elif interval == Interval.MONTH:
        tz = ZoneInfo(tz)
        year = start_time.year
        month = start_time.month
        days_in_month = calendar.monthrange(year, month)[1]
        step = days_in_month // (count + 1)
        for i in range(count):
            day = 1 + step * (i + 1)
            day = min(day, days_in_month)
            hour = random.randint(user.workday_start, user.workday_end - 1)
            minute = random.choice([0, 15, 30, 45])
            dt = datetime(year, month, day, hour, minute, tzinfo=tz)
            dates.append(dt)

    return sorted(dates)


def generate_tasks(db: Session):
    cares = db.scalars(select(Care).join(Care.user)).all()
    now = datetime.utcnow()

    for care in cares:
        user = care.user
        timezone = ZoneInfo(user.timezone)
        now_local = now.astimezone(timezone)

        last_task = db.scalars(
            select(Task)
            .where(Task.care_id == care.id)
            .order_by(Task.scheduled_at.desc())
            .limit(1)
        ).first()

        if not last_task or is_new_interval(now_local, last_task.scheduled_at.astimezone(timezone), care.interval):
            db.execute(
                update(Task)
                .where(Task.care_id == care.id)
                .where(Task.status == TaskStatus.PENDING)
                .values(status=TaskStatus.OVERDUE)
            )

            distribution = generate_distribution_dates(
                interval=care.interval,
                count=care.count or 1,
                user=user,
                tz=user.timezone,
                start_time=now_local
            )

            for scheduled_time in distribution:
                task = Task(
                    care_id=care.id,
                    user_id=user.id,
                    title=f"{care.type.title()} plant {care.plant_id}",
                    scheduled_at=scheduled_time,
                    status=TaskStatus.PENDING,
                )
                db.add(task)

    db.commit()