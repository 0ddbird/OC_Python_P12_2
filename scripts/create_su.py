import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.users.models import Admin

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
engine = sqlalchemy.create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

super_user = Admin(
    username="admin", password="admin", email="admin@ee.com", user_type="admin"
)

session.add(super_user)
session.commit()
