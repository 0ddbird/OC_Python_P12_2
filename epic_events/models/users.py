from passlib.hash import bcrypt
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    is_superuser = Column(Boolean, default=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    customers = relationship("Customer", back_populates="sales_rep")
    contracts = relationship("Contract", back_populates="sales_rep")
    events = relationship("Event", back_populates="support_rep")
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department = relationship("Department", back_populates="users")

    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)
