from datetime import datetime
from pydantic import BaseModel
from database.models import GenderEnum
from typing import Optional

class BaseUser(BaseModel):
    full_name: str
    age: int
    gender: GenderEnum

    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    created_at: datetime


class UpdateUser(BaseModel):
    full_name: Optional[str]
    age: Optional[int]
    gender: Optional[GenderEnum]