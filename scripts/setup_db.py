import os
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from src.users.models import Base, Admin, Manager, SalesRep, SupportRep  # noqa: F401

load_dotenv()

DB_PATH = os.getenv("DB_PATH")

engine = sqlalchemy.create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(bind=engine)
session.commit()
