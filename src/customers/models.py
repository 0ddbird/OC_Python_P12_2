from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.companies.models import Company
from src.db_access import Base


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship(Company, backref="sales_rep")
    contract_id = Column(Integer, ForeignKey("contract.id"))
    sales_rep_id = Column(Integer, ForeignKey("sales_rep.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
