import cmd
import datetime
from collections import namedtuple
from pathlib import Path
from typing import List

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

Task = namedtuple("Task", ("id", "title", "description", "status", "creation"))


class BulletJournalShell(cmd.Cmd):
    intro = "Welcome to you bullet journal. Type help or ? to list commands.\n"
    prompt = "[bullet-journal] "
    journal: List[Task] = list()
    task_id = 0
    path = Path("tasks.yaml")

    def do_add(self, line):
        """
        Usage:
        add [title], [description], [status], [creation]
        """
        elements = line.strip().split(",")
        elements = list(map(str.strip, elements))
        elements += [None] * (4 - len(elements))
        title = elements[0]
        description = elements[1] if elements[1] is not None else ""
        status = int(elements[2]) if elements[2] is not None else 0
        creation_date = (
            datetime.date.fromisoformat(elements[3])
            if elements[3] is not None
            else datetime.date.today()
        )
        task = Task(self.task_id, title, description, status, creation_date)
        print(f"created {task}")
        self.journal.append(task)
        save_task(task, self.path)
        self.task_id += 1

    def do_list(self, line):
        """lists all tasks"""
        for task in self.journal:
            print(f"{task.id} | {task.title} | {task.creation}")

    def do_close(self, line):
        # save_tasks(self.journal, self.path)
        return True

    def preloop(self) -> None:
        journal = load_tasks(self.path)
        self.journal = journal if journal is not None else list()
        return super().preloop()

    def postcmd(self, stop, line):
        # prints a new line after each command
        print()
        return cmd.Cmd.postcmd(self, stop, line)


def save_tasks(task_list: List[Task], path: Path):
    with path.open("w") as file:
        dump(task_list, file, Dumper=Dumper)


def save_task(task: Task, path: Path):
    with path.open("a") as file:
        dump([task], file, Dumper=Dumper)


def load_tasks(path: Path):
    with path.open("r") as file:
        task_list = load(file, Loader=Loader)
    return task_list


if __name__ == "__main__":
    BulletJournalShell().cmdloop()
