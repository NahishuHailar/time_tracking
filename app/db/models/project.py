from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    time_entries = relationship("TimeEntry", back_populates="project")
