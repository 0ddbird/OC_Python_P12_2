from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    customers = relationship("Customer", back_populates="company")
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


def get_or_create_company(conn, company_name):
    company = conn.query(Company).filter_by(name=company_name).first()
    if company is None:
        company = Company(name=company_name)
        conn.add(company)
        conn.commit()
    return company
