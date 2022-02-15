from __future__ import annotations

from Item import Item


class Note(Item):
    content: str

    def __init__(
        self,
        title: str,
        content="",
    ):
        super.__init__(title)
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


def parse_note(line: str) -> Note:
    """
    Parses an note from an comma seperated string.
    'title, [content]'
    """
    if "," in line:
        title, content = line.split(",")
        content = content.lstrip()
    else:
        title = line
        content = ""
    note = Note(title, content)
    return note
