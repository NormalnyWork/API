from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar
import random

from database import User


def generate_distribution_dates(interval: str, count: int, user: User, tz: str, start_time: datetime) -> list[datetime]:
    dates = []

    if interval == "DAY":
        total_seconds = (user.workday_end - user.workday_start) * 3600
        step = total_seconds // count
        for i in range(count):
            hour = user.workday_start + (step * i) // 3600
            minute = ((step * i) % 3600) // 60
            dt = start_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            dates.append(dt)

    elif interval == "WEEK":
        start = start_time
        for i in range(count):
            day_offset = (i * 7) // count
            hour = random.randint(user.workday_start, user.workday_end - 1)
            dt = start + timedelta(days=day_offset)
            dt = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
            dates.append(dt)

    elif interval == "MONTH":
        year = start_time.year
        month = start_time.month
        days_in_month = calendar.monthrange(year, month)[1]

        used_days = set()
        for i in range(count):
            while True:
                day = random.randint(1, days_in_month)
                if day not in used_days:
                    used_days.add(day)
                    break
            dt = datetime(year, month, day, user.workday_start, 0, tzinfo=ZoneInfo(tz))
            dates.append(dt)

    return sorted(dates)
