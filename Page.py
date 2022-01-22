from __future__ import annotations

import datetime
from typing import Iterator

from Appointment import Appointment
from Note import Note
from Task import Task


class Page:
    date: datetime.date
    entries: list

    def __init__(self, date: datetime.date) -> None:
        self.date = date
        self.entries = list()

    def __iter__(self) -> Iterator:
        for element in self.entries:
            yield element

    def add(self, element):
        """Adds an element."""
        if isinstance(element, Appointment):
            element_type = "Appointment"
        elif isinstance(element, Note):
            element_type = "Note"
        elif isinstance(element, Task):
            element_type = "Task"

        self.entries.append((element, element_type))

    def appointments(self) -> Iterator[Appointment]:
        """Returns all appointments."""
        for element, element_type in self.entries:
            if element_type == "Appointment":
                yield element

    def notes(self) -> Iterator[Note]:
        """Returns all notes."""
        for element, element_type in self.entries:
            if element_type == "Note":
                yield element

    def tasks(self) -> Iterator[Task]:
        """Returns all Tasks."""
        for element, element_type in self.entries:
            if element_type == "Task":
                yield element

    def to_dict(self) -> dict:
        """Returns Page as a dict."""
        page_dict = dict()
        page_dict["date"] = self.date
        entries = [(e.to_dict(), e_type) for (e, e_type) in self.entries]
        page_dict["entries"] = entries
        return page_dict

    @staticmethod
    def from_dict(page_dict: dict) -> Page:
        """Generates Page from dict."""
        date = page_dict.get("date")
        page = Page(date)

        entries = page_dict.get("entries")
        for element_dict, element_type in entries:
            if element_type == "Appointment":
                element = Appointment.from_dict(element_dict)
            elif element_type == "Note":
                element = Note.from_dict(element_dict)
            elif element_type == "Task":
                element = Task.from_dict(element_dict)
            else:
                continue

            page.entries.append(element, element_type)
        return page
