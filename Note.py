from __future__ import annotations

from uuid import uuid4


class Note:
    note_id: str
    title: str
    content: str

    def __init__(
        self,
        title: str,
        content="",
    ):
        self.note_id = uuid4().hex
        self.title = title
        self.content = content

    def __str__(self) -> str:
        return f"Note({self.title})"

    def to_dict(self) -> dict:
        """Returns Note as dict."""

        note_dict = dict()
        note_dict["note_id"] = self.note_id
        note_dict["title"] = self.title
        note_dict["content"] = self.content

        return note_dict

    @staticmethod
    def from_dict(note_dict: dict) -> Note:
        """Generates Note from dict."""
        note_id: str = note_dict.get("note_id")
        title: str = note_dict.get("title")
        content: str = note_dict.get("content")

        note = Note(title, content)
        note.note_id = note_id

        return note
