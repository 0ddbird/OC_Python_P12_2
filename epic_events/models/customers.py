from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", back_populates="customers")

    contract = relationship("Contract", back_populates="customer")

    sales_rep_id = Column(Integer, ForeignKey("sales_rep.id"))
    sales_rep = relationship("SalesRep", back_populates="customers")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"Customer(name={self.name}, company={self.company}, sales_rep_id={self.sales_rep.id})"

    def __str__(self):
        return f"Customer {self.id}: {self.name}"
