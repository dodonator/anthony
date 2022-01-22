import cmd
import sys
from pathlib import Path

from IO import init_dir, initialize_page
from Page import Page


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

    def do_exit(self, line):
        """Exits the programm."""
        sys.exit()

    def do_info(self, line):
        """Prints info concerning the current working directory."""
        print(f"source path: {self.source_path}")
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
        return super().postcmd(stop, line)


if __name__ == "__main__":
    AnthonyShell().cmdloop()
