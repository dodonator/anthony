import csv

from model import Job
from typing import Iterable, List
from pathlib import Path
from datetime import date, timedelta


class BulletJournal:
    tasks: List[Job]
    past_path: Path
    present_path: Path

    def __init__(self) -> None:
        # generating paths
        today = date.today()
        yesterday = today + timedelta(days=-1)
        self.past_path = Path(f"{yesterday.isoformat()}.csv")
        self.present_path = Path(f"{today.isoformat()}.csv")

        # initialize files
        header = ["job id", "title", "description", "status", "creation date"]
        if not self.past_path.exists():
            self.past_path.touch()

        if not self.past_path.stat().st_size:
            with self.past_path.open("w", newline="") as archive:
                writer = csv.writer(archive, delimiter=",")
                writer.writerow(header)

        if not self.present_path.exists():
            self.present_path.touch()

        # initiate job list
        self.tasks = list()
        self.load_active()

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

    def load_active(self):
        """loads active jobs from memory"""
        if not self.present_path.exists():
            return

        with self.present_path.open("r", newline="") as active:
            reader = csv.DictReader(active, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                self.tasks.append(job)

    def save_active(self):
        """saves active jobs to memory"""
        active_jobs = list(filter(lambda j: j.status.code >= 2, self.tasks))
        header = ["job id", "title", "description", "status", "creation date"]

        with self.present_path.open("w", newline="") as active:
            writer = csv.writer(active, delimiter=",")
            writer.writerow(header)

            for job in active_jobs:
                job_id = job.job_id
                title = job.title
                description = job.description
                status = str(job.status.code)
                creation = job.creation_date.isoformat()

                writer.writerow([job_id, title, description, status, creation])

    def save_archive(self):
        """saves inactive jobs to memory"""
        inactive_jobs = list(filter(lambda j: j.status.code < 2, self.tasks))

        with self.past_path.open("a", newline="") as archive:
            writer = csv.writer(archive, delimiter=",")

            for job in inactive_jobs:
                job_id = job.job_id
                title = job.title
                description = job.description
                status = str(job.status.code)
                creation = job.creation_date.isoformat()

                writer.writerow([job_id, title, description, status, creation])

    def save(self):
        """saves jobs"""
        self.save_active()
        self.save_archive()


if __name__ == "__main__":
    BJ = BulletJournal()
