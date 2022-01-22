import cmd


class AnthonyShell(cmd.Cmd):
    intro = """
Welcome to anthony your bullet journal.
Type help or ? to list commands.
"""
    prompt = "[anthony] "

    # ToDo: implement commands


if __name__ == "__main__":
    AnthonyShell().cmdloop()
