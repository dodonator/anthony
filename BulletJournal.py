import csv

from Job import Job
from typing import Iterable, List
from pathlib import Path
from datetime import date, timedelta


class BulletJournal:
    tasks: List[Job]
    past_path: Path
    present_path: Path
    header = ["job id", "title", "description", "status", "creation date"]

    def __init__(self) -> None:
        # generating paths
        today = date.today()
        yesterday = today + timedelta(days=-1)
        self.past_path = Path(f"{yesterday.isoformat()}.csv")
        self.present_path = Path(f"{today.isoformat()}.csv")

        # initialize file for today
        if not self.present_path.exists():
            self.present_path.touch()

        if not self.present_path.stat().st_size:
            with self.present_path.open("w", newline="") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(self.header)

        # initiate job list
        self.tasks = list()
        self.load_past()
        self.load_present()

    def __iter__(self) -> Iterable[Job]:
        """iterates over all jobs"""
        for job in self.tasks:
            yield job

    def __len__(self) -> int:
        """returns number of all jobs

        Returns:
            int: number of jobs
        """
        return len(self.tasks)

    def load_past(self):
        """loads active jobs from the past"""
        if not self.past_path.exists():
            return
        with self.past_path.open("r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                if job.status == 0:
                    self.tasks.append(job)

    def load_present(self):
        """loads job from the present"""
        with self.present_path.open("r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                self.tasks.append(job)

    def save(self):
        """saves jobs from the present to memory"""
        with self.present_path.open("w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(self.header)

            for job in self.tasks:
                row = [
                    job.job_id,
                    job.title,
                    job.description,
                    str(job.status),
                    job.creation_date.isoformat(),
                ]
                writer.writerow(row)


if __name__ == "__main__":
    BJ = BulletJournal()
