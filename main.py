import cmd
import datetime
from collections import namedtuple
from typing import List

Task = namedtuple("Task", ("id", "title", "description", "status", "creation"))


class BulletJournalShell(cmd.Cmd):
    intro = "Welcome to you bullet journal. Type help or ? to list commands.\n"
    prompt = "[bullet-journal] "
    journal: List[Task] = list()
    task_id = 0

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
        self.task_id += 1

    def do_list(self, line):
        """lists all tasks"""
        for task in self.journal:
            print(f"{task.id} | {task.title} | {task.creation}")

    def postcmd(self, stop, line):
        # prints a new line after each command
        print()
        return cmd.Cmd.postcmd(self, stop, line)


if __name__ == "__main__":
    BulletJournalShell().cmdloop()
