import cmd
import datetime
from collections import namedtuple
from pathlib import Path
from typing import List

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

Task = namedtuple("Task", ("id", "title", "description", "status", "execution", "creation"))


class BulletJournalShell(cmd.Cmd):
    intro = "Welcome to you bullet journal. Type help or ? to list commands.\n"
    prompt = "[bullet-journal] "
    journal: List[Task] = list()
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
        self.journal.append(task)
        save_task(task, self.path)
        self.task_id += 1

    def do_list(self, line):
        """
        Usage:
        list all | today | open | closed
        """
        today = datetime.date.today()
        match line.strip():
            case "today":
                task_list = list(filter(lambda t: t.execution == today, self.journal))

            case "open":
                task_list = list(filter(lambda t: t.status == 0, self.journal))

            case "closed":
                task_list = list(filter(lambda t: t.status == 1, self.journal))

            case "all" | "":
                task_list = self.journal

        for task in task_list:
            print(f"{task.id} | {task.title} | {task.creation}")

    def do_close(self, line):
        # save_tasks(self.journal, self.path)
        return True

    def preloop(self) -> None:
        journal = load_tasks(self.path)
        if journal is None:
            self.journal = list()
            self.task_id = 0
        else:
            self.journal = journal
            self.task_id = journal[-1].id + 1

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
        dump([task._asdict()], file, Dumper=Dumper)


def load_tasks(path: Path):
    with path.open("r") as file:
        task_list = load(file, Loader=Loader)
    return task_list


if __name__ == "__main__":
    BulletJournalShell().cmdloop()
