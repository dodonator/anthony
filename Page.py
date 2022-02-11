from __future__ import annotations

import datetime
from typing import Iterator, List, Tuple

from Appointment import Appointment
from Note import Note
from Task import Task


class Page:
    date: datetime.date
    items: List[Tuple[Appointment | Note | Task], str]

    def __init__(self, date: datetime.date) -> None:
        self.date = date
        self.items = list()

    def __iter__(self) -> Iterator:
        for element in self.items:
            yield element

    def __str__(self) -> str:
        return f"Page({self.date})"

    def add(self, element):
        """Adds an element."""
        if isinstance(element, Appointment):
            element_type = "Appointment"
        elif isinstance(element, Note):
            element_type = "Note"
        elif isinstance(element, Task):
            element_type = "Task"
        else:
            raise NotImplementedError(f"Unknown element type {type(element)}")

        self.items.append((element, element_type))

    def appointments(self) -> Iterator[Appointment]:
        """Returns all appointments."""
        for element, element_type in self.items:
            if element_type == "Appointment":
                yield element

    def notes(self) -> Iterator[Note]:
        """Returns all notes."""
        for element, element_type in self.items:
            if element_type == "Note":
                yield element

    def tasks(self) -> Iterator[Task]:
        """Returns all Tasks."""
        for element, element_type in self.items:
            if element_type == "Task":
                yield element

    def to_dict(self) -> dict:
        """Returns Page as a dict."""
        page_dict = dict()
        page_dict["date"] = self.date
        items = [[i.to_dict(), i_type] for (i, i_type) in self.items]
        page_dict["items"] = items
        return page_dict

    @staticmethod
    def from_dict(page_dict: dict) -> Page:
        """Generates Page from dict."""
        date = page_dict.get("date")
        page = Page(date)

        items = page_dict.get("items")
        for item_dict, item_type in items:
            if item_type == "Appointment":
                item = Appointment.from_dict(item_dict)
            elif item_type == "Note":
                item = Note.from_dict(item_dict)
            elif item_type == "Task":
                item = Task.from_dict(item_dict)
            else:
                continue

            page.items.append([item, item_type])
        return page
