from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import BigInteger, Text, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column(Text, nullable=False)
    email: Mapped[EmailStr] = mapped_column(Text, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    fcm_token: Mapped[str] = mapped_column(Text, nullable=True)

    timezone: Mapped[str] = mapped_column(Text, nullable=False, default="UTC")
    workday_start: Mapped[int] = mapped_column(Integer, default=9)
    workday_end: Mapped[int] = mapped_column(Integer, default=18)

    cares: Mapped[list["Care"]] = relationship(
        "Care", back_populates="user", cascade="all, delete"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )