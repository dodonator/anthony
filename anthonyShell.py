import cmd
import sys


class AnthonyShell(cmd.Cmd):
    intro = """
Welcome to anthony your bullet journal.
Type help or ? to list commands.
"""
    prompt = "[anthony] "

    # ToDo: implement commands

    def do_exit(self, line):
        """Exits the programm."""
        sys.exit()


if __name__ == "__main__":
    AnthonyShell().cmdloop()
