from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base

MANAGER = "manager"
SALES = "sales"
SUPPORT = "support"
ALL = [MANAGER, SALES, SUPPORT]


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    users = relationship("User", back_populates="departments")
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


def get_or_create_department(conn, department_name):
    department = conn.query(Department).filter_by(name=department_name).first()
    if department is None:
        department = department(name=department_name)
        conn.add(department)
        conn.commit()
    return department
