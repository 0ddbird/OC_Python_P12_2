import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import configure_mappers, relationship, sessionmaker

load_dotenv()
DB_PATH = os.getenv("DB_PATH")

Base = declarative_base()


def setup_relations():
    from src.companies.models import Company
    from src.contracts.models import Contract
    from src.customers.models import Customer
    from src.events.models import Event
    from src.users.models import SalesRep, SupportRep

    SalesRep.customers = relationship(Customer, back_populates="sales_rep")
    SalesRep.contracts = relationship(Contract, back_populates="sales_rep")
    SupportRep.events = relationship(Event, back_populates="support_rep")
    Customer.company = relationship(Company, backref="sales_rep")
    Customer.contract = relationship(Contract, back_populates="customer")
    Company.customers = relationship(Customer, backref="sales_rep")
    Contract.customer = relationship(Customer, back_populates="contract")
    Event.contract = relationship(Contract, back_populates="event")
    Event.support_rep = relationship(SupportRep, back_populates="event")


configure_mappers()


def get_db_session():
    engine = sqlalchemy.create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
