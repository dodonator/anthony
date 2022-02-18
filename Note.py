from __future__ import annotations

from Item import Item


class Note(Item):
    content: str

    def __init__(
        self,
        title: str,
        content="",
    ):
        super().__init__(title)
        self.content = content

    def __repr__(self) -> str:
        return f"Note({self.title})"

    def to_dict(self) -> dict:
        """Returns Note as dict."""

        note_dict = dict()
        note_dict["item_id"] = self.item_id
        note_dict["title"] = self.title
        note_dict["content"] = self.content

        return note_dict

    @staticmethod
    def from_dict(note_dict: dict) -> Note:
        """Generates Note from dict."""
        item_id: str = note_dict.get("item_id")
        title: str = note_dict.get("title")
        content: str = note_dict.get("content")

        note = Note(title, content)
        note.item_id = item_id

        return note
