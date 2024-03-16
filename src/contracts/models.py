from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.sql import func

from src.db_access import Base


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    signed = Column(Boolean, default=False)
    value = Column(Numeric(precision=10, scale=2), nullable=False)
    amount_due = Column(Numeric(precision=10, scale=2), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), unique=True)
    sales_rep_id = Column(Integer, ForeignKey("sales_rep.id"), unique=True)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=True, unique=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
