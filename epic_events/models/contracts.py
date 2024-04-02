from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    signed = Column(Boolean, default=False)
    value = Column(Numeric(precision=10, scale=2), nullable=False)
    amount_due = Column(Numeric(precision=10, scale=2), nullable=False)

    customer_id = Column(Integer, ForeignKey("customer.id"), unique=True)
    customer = relationship("Customer", back_populates="contract")

    sales_rep = relationship("SalesRep", back_populates="contracts")
    sales_rep_id = Column(Integer, ForeignKey("sales_rep.id"), unique=True)

    event = relationship("Event", back_populates="contract")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
