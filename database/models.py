import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
)
import enum

from database.database import Base


class GenderEnum(enum.IntEnum):
    male = 0
    female = 1

class Car:
    user_id = Column(Integer, ForeignKey("users.id"))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(Enum(GenderEnum))
    created_at = Column(DateTime, default=datetime.datetime.now())
