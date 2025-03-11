from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseORM

if TYPE_CHECKING:
    from app.db.models.project import ProjectORM
    from app.db.models.user import UserORM


class TimeEntryORM(BaseORM):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    hours: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="time_entries")
    project: Mapped["ProjectORM"] = relationship(
        "ProjectORM", back_populates="time_entries"
    )
