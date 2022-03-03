import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator


class Appointment(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    start: datetime.datetime

    @validator("id", pre=True, always=True)
    def id_must_be_valid_uuid(cls, v):
        if v is not None:
            v = UUID(v).hex
        else:
            v = uuid4().hex
        return v


class Note(BaseModel):
    id: Optional[str]
    title: str
    content: str


class Task(BaseModel):
    id: Optional[str]
    title: str
    content: str
    done: bool
    active: bool
    execution_date: datetime.date
