from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

import appException
from database import Care, Task, TaskStatus
from schema.plant import Interval
import calendar

from service.service import DefaultService


class TaskService(DefaultService):
    def get_today_tasks(self, user_id: int) -> list:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        today_end = today_start + timedelta(days=1)
        yesterday_start = today_start - timedelta(days=1)

        today_tasks = self.session.scalars(
            select(Task)
            .options(joinedload(Task.plant))
            .where(Task.user_id == user_id)
            .where(Task.scheduled_at >= today_start)
            .where(Task.scheduled_at < today_end)
        ).all()

        today_keys = {(t.care_id, t.user_id, t.plant_id) for t in today_tasks}

        overdue_candidates = self.session.scalars(
            select(Task)
            .options(joinedload(Task.plant))
            .where(Task.user_id == user_id)
            .where(Task.status == TaskStatus.OVERDUE)
            .where(Task.scheduled_at >= yesterday_start)
            .where(Task.scheduled_at < today_start)
        ).all()

        filtered_overdue = [
            task for task in overdue_candidates
            if (task.care_id, task.user_id, task.plant_id) not in today_keys
        ]

        return sorted(today_tasks + filtered_overdue, key=lambda t: t.scheduled_at)

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

    def postpone_task(self, task_id: int) -> None:
        task = self.session.get(Task, task_id)

        if not task:
            raise appException.task.TaskNotFound()

        today = datetime.utcnow().date()
        task_date = task.scheduled_at.date()


        new_date = task.scheduled_at + timedelta(days=1)

        existing = self.session.scalar(
            select(Task)
            .where(Task.user_id == task.user_id)
            .where(Task.care_id == task.care_id)
            .where(Task.plant_id == task.plant_id)
            .where(Task.scheduled_at == new_date)
        )

        if existing:
            self.session.delete(task)
        else:
            task.scheduled_at = new_date
            task.status = TaskStatus.PENDING

        self.session.commit()

    def mark_tasks_as_overdue(self) -> None:
        now = datetime.utcnow()
        overdue_threshold = now - timedelta(days=1)

        self.session.execute(
            update(Task)
            .where(Task.status == TaskStatus.PENDING)
            .where(Task.scheduled_at < overdue_threshold)
            .values(status=TaskStatus.OVERDUE)
        )
        self.session.commit()


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
        tz = ZoneInfo(tz)
        for i in range(count):
            day_offset = i * daily_slots
            local_dt = (start_time + timedelta(days=day_offset)).replace(
                hour=9,
                minute=0,
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
            dt = datetime(year, month, day, 9, 0, tzinfo=tz)
            dates.append(dt)

    return sorted(dates)


def generate_tasks(db: Session):
    TaskService(db).mark_tasks_as_overdue()
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
                    plant_id=care.plant_id,
                    care_type=care.type,
                    scheduled_at=scheduled_time,
                    status=TaskStatus.PENDING,
                )
                db.add(task)

    db.commit()