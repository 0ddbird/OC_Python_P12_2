import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
DB_PATH = os.getenv("DB_PATH")

engine = sqlalchemy.create_engine(DB_PATH)

Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from epic_events.models.companies import Company  # noqa F401
from epic_events.models.contracts import Contract  # noqa F401
from epic_events.models.customers import Customer  # noqa F401
from epic_events.models.events import Event  # noqa F401
from epic_events.models.users import Admin, Manager, SalesRep, SupportRep  # noqa F401


# def get_db_session():
#     engine = sqlalchemy.create_engine(DB_PATH)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session
