from uuid import uuid4


class Item:
    item_id: str
    title: str

    def __init__(self, title: str):
        self.note_id = uuid4().hex
        self.title = title

    def __str__(self) -> str:
        return f"Item({self.title})"
