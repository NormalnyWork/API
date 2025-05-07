from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"


class TaskOut(BaseModel):
    id: int
    title: str
    care_id: int
    user_id: int
    scheduled_at: datetime
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime

    class Config:
        orm_mode = True