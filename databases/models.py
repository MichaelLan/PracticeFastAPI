from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String, unique=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name_group = Column(String(100), index=True)
    city = Column(String(100), index=True)
    link = Column(String(100), index=True)
