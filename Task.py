from __future__ import annotations

import datetime


class Task:
    task_id: int
    title: str
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
    ):
        self.title = title
        self.content = content
        self.done = done
        self.active = active

        if execution_date is None:
            self.execution_date = datetime.date.today()
        else:
            self.execution_date = execution_date

    def to_dict(self) -> Task:
        """Returns Task as dict."""

        task_dict = dict()
        task_dict["task_id"] = self.task_id
        task_dict["title"] = self.title
        task_dict["content"] = self.content
        task_dict["done"] = self.done
        task_dict["active"] = self.active
        task_dict["execution_date"] = self.execution_date

        return task_dict

    @staticmethod
    def from_dict(task_dict: dict) -> Task:
        """Generates Task from dict."""
        task = Task()
        return task
