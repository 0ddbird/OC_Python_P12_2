from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.db_access import Base


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
