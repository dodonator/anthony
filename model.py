from __future__ import annotations

import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator

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
        print(cls.__name__)
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
        return self.id == other.id

    def __hash__(self) -> int:
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
