from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, field_validator


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"


class TaskOut(BaseModel):
    id: int
    care_type: str
    scheduled_at: int
    status: TaskStatus = TaskStatus.PENDING
    plant_name: str
    plant_image: str

    class Config:
        orm_mode = True
        from_attributes = True

    @field_validator("scheduled_at", mode="before")
    @classmethod
    def convert_created_at_to_timestamp(cls, value: datetime | int) -> int:
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value
