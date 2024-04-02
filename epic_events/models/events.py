from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from epic_events.models import Base


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    attendees = Column(Integer)
    location = Column(String(255))
    notes = Column(String(1000), default="")

    contract_id = Column(
        Integer, ForeignKey("contract.id"), unique=True, nullable=False
    )
    contract = relationship("Contract", back_populates="event")

    support_rep_id = Column(Integer, ForeignKey("support_rep.id"))
    support_rep = relationship("SupportRep", back_populates="events")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
