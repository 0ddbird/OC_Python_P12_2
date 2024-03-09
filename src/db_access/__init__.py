import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()
DB_PATH = os.getenv("DB_PATH")


def get_db_session():
    engine = sqlalchemy.create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
