from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseORM

if TYPE_CHECKING:
    from app.db.models.project_user import ProjectUserORM
    from app.db.models.time_entry import TimeEntryORM


class ProjectORM(BaseORM):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    time_entries: Mapped[List["TimeEntryORM"]] = relationship(
        "TimeEntryORM", back_populates="project", cascade="all, delete-orphan"
    )
    users: Mapped[List["ProjectUserORM"]] = relationship(
        "ProjectUserORM", back_populates="project", cascade="all, delete-orphan"
    )
