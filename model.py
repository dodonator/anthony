from __future__ import annotations

import datetime
from typing import Generic, Iterator, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, validator

from errors import UnknownItemType

REGISTERED_ITEMS = {}
T = TypeVar("T")


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


class ItemContainer(Generic[T]):
    members: list[T]

    def __init__(self, members=None) -> None:
        if members is not None:
            self.members = list(members)
        else:
            self.members = list()

    def __iter__(self) -> Iterator:
        for item in self.members:
            yield item

    def append(self, item: T):
        self.members.append(item)


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
                raise UnknownItemType(f"Unknown item type {type(item)}")
            case _:
                raise ValueError(f"Unknown type {type(item)}")

    def to_dict(self) -> dict:
        page_dict = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, ItemContainer):
                page_dict[key] = [item.to_record() for item in value]
            else:
                page_dict.update({key: value})

        return page_dict
