from enum import Enum

from passlib.hash import bcrypt
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserType(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SALES_REP = "sales_rep"
    SUPPORT_REP = "support_rep"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    type = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }

    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)


class Admin(User):
    __tablename__ = "admin"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": UserType.ADMIN.value,
    }


class Manager(User):
    __tablename__ = "manager"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": UserType.MANAGER.value,
    }


class SalesRep(User):
    __tablename__ = "sales_rep"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": UserType.SALES_REP.value,
    }


class SupportRep(User):
    __tablename__ = "support_rep"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": UserType.SUPPORT_REP.value,
    }
