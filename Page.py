from __future__ import annotations

import datetime
from typing import Iterator, List

from model import Appointment
from Item import Item
from Note import Note
from Task import Task


class Page:
    date: datetime.date
    items: List[List[Item], str]

    def __init__(self, date: datetime.date) -> None:
        self.date = date
        self.items = list()

    def __iter__(self) -> Iterator[Item]:
        """Iterates over the items of the page."""
        for element in self.items:
            yield element

    def __str__(self) -> str:
        return f"Page({self.date})"

    def add(self, item: Item):
        """Adds an item to the page."""
        if isinstance(item, Appointment):
            item_type = "Appointment"
        elif isinstance(item, Note):
            item_type = "Note"
        elif isinstance(item, Task):
            item_type = "Task"
        else:
            raise NotImplementedError(f"Unknown item type {type(item)}")

        self.items.append((item, item_type))

    def appointments(self) -> Iterator[Appointment]:
        """Returns all appointments."""
        for item, item_type in self.items:
            if item_type == "Appointment":
                yield item

    def notes(self) -> Iterator[Note]:
        """Returns all notes."""
        for item, item_type in self.items:
            if item_type == "Note":
                yield item

    def tasks(self) -> Iterator[Task]:
        """Returns all Tasks."""
        for item, item_type in self.items:
            if item_type == "Task":
                yield item

    def find(self, title: str) -> Item:
        """Find item in page by title."""
        for item, item_type in self.items:
            if item.title == title:
                return item

        return None

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
