import cmd
import datetime
from collections import namedtuple
from pathlib import Path
from typing import Dict
from venv import create

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

Task = namedtuple("Task", ("id", "title", "description", "status", "execution", "creation"))


class BulletJournalShell(cmd.Cmd):
    intro = "Welcome to you bullet journal. Type help or ? to list commands.\n"
    prompt = "[bullet-journal] "
    journal: dict
    path = Path("tasks.yaml")

    def do_add(self, line):
        """
        Usage:
        add [title], [description], [status], [execution]
        """
        elements = line.strip().split(",")
        elements = list(map(str.strip, elements))
        elements += [None] * (4 - len(elements))
        title = elements[0]
        description = elements[1] if elements[1] is not None else ""
        status = int(elements[2]) if elements[2] is not None else 0
        execution_date = datetime.date.fromisoformat(elements[3]) if elements[3] is not None else datetime.date.today()
        creation_date = datetime.date.today()

        task = Task(self.task_id, title, description, status, execution_date, creation_date)
        print(f"created {task}")
        self.journal[self.task_id] = task
        self.task_id += 1

    def do_list(self, line):
        """
        Usage:
        list all | today | open | closed
        """
        today = datetime.date.today()
        match line.strip():
            case "today":
                journal = dict(filter(lambda t: t[1].execution == today, self.journal.items()))

            case "open":
                journal = dict(filter(lambda t: t[1].status == 0, self.journal.items()))

            case "closed":
                journal = dict(filter(lambda t: t[1].status == 1, self.journal.items()))

            case "all" | "":
                journal = self.journal

        for tid, task in journal.items():
            print(f"{tid} | {task.title} | {task.creation}")

    def do_close(self, line):
        return True

    def preloop(self) -> None:
        journal = load_tasks(self.path)
        if journal is None:
            self.journal = dict()
            self.task_id = 0
        else:
            self.journal = journal
            self.task_id = max(journal.keys()) + 1

        return super().preloop()

    def postloop(self) -> None:
        save_tasks(self.journal, self.path)
        return super().postloop()

    def postcmd(self, stop, line):
        # prints a new line after each command
        print()
        return cmd.Cmd.postcmd(self, stop, line)


def save_tasks(task_dict: Dict[int, Task], path: Path):
    data = {tid: task._asdict() for tid, task in task_dict.items()}
    with path.open("w") as file:
        dump(data, file, Dumper=Dumper)


def load_tasks(path: Path):
    with path.open("r") as file:
        task_list = load(file, Loader=Loader)
    if task_list:
        return _tasks_from_dict(task_list)

def _tasks_from_dict(task_dict: Dict[int, Dict]) -> Dict[int, Task]:
    result = dict()
    for tid, t_dict in task_dict.items():
        result[tid] = Task(**t_dict)
    return result

if __name__ == "__main__":
    BulletJournalShell().cmdloop()
