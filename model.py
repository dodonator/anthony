import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator


class Item(BaseModel):
    id: Optional[str] = None
    title: str
    content: str

    @validator("id", pre=True, always=True)
    def id_must_be_valid_uuid(cls, v):
        if v is not None:
            v = UUID(v).hex
        else:
            v = uuid4().hex
        return v


class Appointment(Item):
    start: datetime.datetime


class Note(Item):
    pass


class Task(Item):
    done: bool
    active: bool
    execution_date: datetime.date
