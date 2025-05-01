from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Plant(Base):
    __tablename__ = "Plant"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column(Text, nullable=False)
    image: Mapped[Text] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("User.id", ondelete="CASCADE"), nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )