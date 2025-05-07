from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Plant(Base):
    __tablename__ = "Plant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("User.id", ondelete="CASCADE"), nullable=False
    )

    care: Mapped[list["Care"]] = relationship(
        "Care", back_populates="plant", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

class Care(Base):
    __tablename__ = "Care"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    interval: Mapped[str] = mapped_column(Text, nullable=True)
    count: Mapped[int] = mapped_column(BigInteger, nullable=True)

    plant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("Plant.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("User.id", ondelete="CASCADE"), nullable=False
    )

    plant: Mapped["Plant"] = relationship(
        "Plant", back_populates="care"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="cares"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )