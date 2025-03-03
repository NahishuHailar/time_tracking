from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class TimeEntry(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    hours = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user = relationship("User", back_populates="time_entries")
    project = relationship("Project", back_populates="time_entries")    