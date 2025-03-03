from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_manager = Column(Boolean, default=False)
    time_entries = relationship("TimeEntry", back_populates="user")