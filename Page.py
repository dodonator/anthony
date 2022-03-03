from __future__ import annotations

import datetime
from typing import Generic, TypeVar

from model import Appointment, Item, Note, Task

T = TypeVar("T")


class ItemContainer(Generic[T]):
    members: list[T]

    def __init__(self, members=None) -> None:
        if members is not None:
            self.members = list(members)
        else:
            self.members = list()

    def append(self, item: T):
        self.members.append(item)


class Page:
    date: datetime.date
    appointments: ItemContainer[Appointment]
    notes: ItemContainer[Note]
    tasks: ItemContainer[Task]

    def __init__(self, date: datetime.date) -> None:
        self.date = date
        self.appointments: ItemContainer[Appointment] = ItemContainer()
        self.notes: ItemContainer[Note] = ItemContainer()
        self.tasks: ItemContainer[Task] = ItemContainer()

    def __str__(self) -> str:
        return self.date.isoformat()

    def __repr__(self) -> str:
        return f"Page({self.date})"

    def add(self, item: Item):
        match item:
            case Appointment():
                self.appointments.append(item)
            case Note():
                self.notes.append(item)
            case Task():
                self.tasks.append(item)
            case Item():
                raise ValueError(f"Unknown item type {type(item)}")
            case _:
                raise ValueError(f"Unknown type {type(item)}")
