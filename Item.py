from __future__ import annotations

from uuid import uuid4


class Item:
    item_id: str
    title: str

    def __init__(self, title: str):
        self.note_id = uuid4().hex
        self.title = title

    def __repr__(self) -> str:
        return f"Item({self.title})"

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: Item) -> bool:
        return self.item_id == other.item_id
