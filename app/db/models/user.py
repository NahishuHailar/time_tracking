from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM

if TYPE_CHECKING:
    from .project_user import ProjectUserORM
    from .time_entry import TimeEntryORM


class UserORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )

    projects: Mapped[List["ProjectUserORM"]] = relationship(
        "ProjectUserORM", back_populates="user"
    )
    time_entries: Mapped[List["TimeEntryORM"]] = relationship(
        "TimeEntryORM", back_populates="user"
    )
