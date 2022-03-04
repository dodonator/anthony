from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator

from errors import UnknownItemType

REGISTERED_ITEMS = {}


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

    def __init_subclass__(cls):
        REGISTERED_ITEMS[cls.__name__] = cls

    def __str__(self) -> str:
        """Returns the item title as string representation.

        Returns:
            str: title
        """
        return self.title

    def __repr__(self) -> str:
        """Returns a summary of the item as str.

        Returns:
            str: item attributes
        """
        attrs = self.__dict__.items()
        kv_pairs = [f"{key}={value!r}" for key, value in attrs if key != "id"]
        return f"{self.__class__.__name__}({', '.join(kv_pairs)})"

    def __rich__(self) -> dict:
        """Returns the dict for using rich.

        Returns:
            _type_: item dict
        """
        return self.__dict__

    def __eq__(self, other: Item) -> bool:
        """Checks for equality of two Items

        Args:
            other (Item): another item

        Returns:
            bool: result
        """
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            self.id = uuid4().hex

        return int(self.id, 16)

    @staticmethod
    def from_dict(item_data: dict) -> Item:
        """Generates Item from dict.

        Args:
            item_data (dict): item data

        Returns:
            Item: resulting Item
        """
        item: Item = Item(**item_data)
        return item

    def to_dict(self) -> dict:
        """Returns Item as dict.

        Returns:
            dict: item dict
        """
        item_dict: dict = self.__dict__
        return item_dict

    def to_record(self) -> tuple[dict, str]:
        """Returns Item as an record.

        Returns:
            tuple[dict, str]: item_dict, item_type
        """
        return self.__dict__, self.__class__.__name__

    @classmethod
    def from_record(cls, record: tuple[dict, str]) -> Item:
        """Creates Item given from an dict and an item type.

        Args:
            record (tuple[dict, str]): item_dict, item_type

        Returns:
            Item: item
        """
        item_dict, item_type_str = record
        return REGISTERED_ITEMS[item_type_str](**item_dict)


class Appointment(Item):
    start: datetime.datetime


class Note(Item):
    pass


class Task(Item):
    done: bool
    active: bool
    execution_date: datetime.date


class Page:
    date: datetime.date
    entries: dict[str, list[Item]]

    def __init__(self, date: datetime.date) -> None:
        self.date = date
        self.entries = dict()
        for name in REGISTERED_ITEMS:
            self.entries[name] = list()

    def __str__(self) -> str:
        return self.date.isoformat()

    def __repr__(self) -> str:
        return f"Page({self.date})"

    def __rich__(self) -> dict:
        return self.to_dict()

    def __eq__(self, other: Page) -> bool:
        return self.to_dict() == other.to_dict()

    def add(self, item: Item):
        type_name = item.__class__.__name__
        if type_name in self.entries:
            self.entries[type_name].append(item)
        else:
            raise UnknownItemType(f"Unknown item type {type_name}")

    def to_dict(self) -> dict:
        page_dict = dict()
        page_dict["date"] = self.date
        page_dict["entries"] = dict()
        for item_type, item_list in self.entries.items():
            record_list = [item.to_record() for item in item_list]
            page_dict["entries"][item_type] = record_list
        return page_dict

    @staticmethod
    def from_dict(page_dict) -> Page:
        date = page_dict["date"]
        page = Page(date)
        for item_type, record_list in page_dict["entries"].items():
            if not record_list:
                continue
            for record in record_list:
                item = Item.from_record(record)
                page.add(item)

        return page
