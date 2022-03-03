from __future__ import annotations

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


class Appointment(Item):
    start: datetime.datetime


class Note(Item):
    pass


class Task(Item):
    done: bool
    active: bool
    execution_date: datetime.date
