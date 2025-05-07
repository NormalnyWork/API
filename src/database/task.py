from datetime import datetime

from sqlalchemy import DateTime, func, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from schema.task import TaskStatus


class Task(Base):
    __tablename__ = "Task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    care_id: Mapped[int] = mapped_column(ForeignKey("Care.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

