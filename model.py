import datetime
from typing import Optional

from pydantic import BaseModel


class Appointment(BaseModel):
    id: Optional[str]
    title: str
    content: str
    start: datetime.datetime


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
