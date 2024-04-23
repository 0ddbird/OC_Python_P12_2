import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from epic_events.models.users import User

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
engine = sqlalchemy.create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

super_user = User(
    username="admin", password="admin", email="admin@ee.com", is_superuser=True
)

session.add(super_user)
session.commit()
