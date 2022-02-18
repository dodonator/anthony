from __future__ import annotations

import datetime

from Item import Item


class Task(Item):
    content: str
    done: bool
    active: bool
    execution_date: datetime.date

    def __init__(
        self,
        title: str,
        content="",
        done=False,
        active=True,
        execution_date=None,
    ) -> None:

        super().__init__(title)
        self.content = content
        self.done = done
        self.active = active

        if execution_date is None:
            self.execution_date = datetime.date.today()
        else:
            self.execution_date = execution_date

    def __repr__(self) -> str:
        return f"Task({self.title}, {self.execution_date})"

    def to_dict(self) -> dict:
        """Returns Task as dict."""

        task_dict = dict()
        task_dict["item_id"] = self.item_id
        task_dict["title"] = self.title
        task_dict["content"] = self.content
        task_dict["done"] = self.done
        task_dict["active"] = self.active
        task_dict["execution_date"] = self.execution_date

        return task_dict

    @staticmethod
    def from_dict(task_dict: dict) -> Task:
        """Generates Task from dict."""
        item_id = task_dict.get("item_id")
        title = task_dict.get("title", "")
        content = task_dict.get("content", "")
        done = task_dict.get("done", False)
        active = task_dict.get("active", True)
        execution_date = task_dict.get("execution_date", None)

        task = Task(title, content, done, active, execution_date)
        task.item_id = item_id

        return task
