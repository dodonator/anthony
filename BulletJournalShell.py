import cmd
from BulletJournal import BulletJournal


class BulletJournalShell(cmd.Cmd):
    intro = "Welcome to you bullet journal. Type help or ? to list commands.\n"
    prompt = "[bullet-journal] "
    journal = BulletJournal()

    def do_add(self, line):
        job = self.journal.add(*line.split(" "))
        print(f"created job {job}")
        print()

    def do_list(self, line):
        for job in self.journal:
            print(job)
        print()


if __name__ == "__main__":
    BulletJournalShell().cmdloop()
