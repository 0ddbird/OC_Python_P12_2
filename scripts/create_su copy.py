import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.users.models import SuperUser

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
engine = sqlalchemy.create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

super_user = SuperUser(
    username="admin",
    password="admin",
    email="admin@test.com",
)

session.add(super_user)
session.commit()
