import os
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from epic_events.models.departments import Department  # noqa: F401
from epic_events.models.users import Base, User  # noqa: F401
from epic_events.models.companies import Company  # noqa: F401
from epic_events.models.customers import Customer  # noqa: F401
from epic_events.models.contracts import Contract  # noqa: F401
from epic_events.models.events import Event  # noqa: F401


load_dotenv()

DB_PATH = os.getenv("DB_PATH")

engine = sqlalchemy.create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(bind=engine)
session.commit()

manager_department = Department(name="manager")
sales_department = Department(name="sales")
support_department = Department(name="support")

session.add_all([manager_department, sales_department, support_department])
session.commit()

super_user = User(
    username="admin",
    password="admin",
    email="admin@ee.com",
    is_superuser=True,
    department=manager_department,
)

session.add(super_user)
session.commit()
