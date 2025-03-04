from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORM

class ProjectUserORM(BaseORM):
    __tablename__ = "project_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String, default='employee', nullable=False)

    project: Mapped["ProjectORM"] = relationship("ProjectORM", back_populates="users")
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="projects")

    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_user_project"),)
