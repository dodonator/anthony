import cmd
import sys
from pathlib import Path

from Appointment import parse_appointment
from IO import init_dir, initialize_page, save_page
from Note import parse_note
from Page import Page
from Task import parse_task


class AnthonyShell(cmd.Cmd):
    intro = """
Welcome to anthony your bullet journal.
Type help or ? to list commands.
"""
    prompt = "[anthony] "
    source_path = Path("./source/")
    current_page: Page
    current_path: Path

    # ToDo: implement commands

    def do_add(self, line):
        """
        Adds Appointment, Note or Task to current Page.
        Usage:
            add Appointment <title>, [<content>], start_date (YYYY-MM-DD[*HH:MM])
            add Note <title>, [<content>]
            add Task <title>, [<content>], [<done>], [<active>], [<execution_date>]
        """
        tmp = line.index(" ")
        element_type = str.capitalize(line[:tmp])
        element = line[tmp:]

        if element_type == "Appointment":
            appointment = parse_appointment(element)
            self.current_page.add(appointment)
            print(f"Added Appointment: {appointment}")

        elif element_type == "Note":
            note = parse_note(element)
            self.current_page.add(note)
            print(f"Added Note: {note}")

        elif element_type == "Task":
            task = parse_task(element)
            self.current_page.add(task)
            print(f"Added Task: {task}")
        else:
            raise NotImplementedError(f"Unknown element type: {element_type}")

    def do_list(self, line):
        """List all items on current page."""
        print("Appointments:")
        for appo in self.current_page.appointments():
            print(f"\t{appo}")
        print()

        print("Notes:")
        for note in self.current_page.notes():
            print(f"\t{note}")
        print()

        print("Tasks:")
        for task in self.current_page.tasks():
            print(f"\t{task}")
        print()

    def do_exit(self, line):
        """Exits the programm."""
        sys.exit()

    def do_info(self, line):
        """Prints info concerning the current working directory."""
        print(f"source path: {self.source_path.absolute()}")
        print(f"current page: {self.current_page}")
        print(f"current page (path): {self.current_path}")

    def preloop(self) -> None:
        init_dir(self.source_path)
        page, path = initialize_page(self.source_path)
        self.current_page = page
        self.current_path = path
        return super().preloop()

    def postcmd(self, stop: bool, line: str) -> bool:
        print()
        save_page(self.current_path, self.current_page)
        return super().postcmd(stop, line)


if __name__ == "__main__":
    AnthonyShell().cmdloop()
