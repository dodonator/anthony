import csv
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

from Task import Task


class BulletJournal:
    jobs: dict
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
        self.jobs = dict()
        self.load_past()
        self.load_present()

    def __iter__(self) -> Iterable[Job]:
        """iterates over all jobs"""
        for job_id in self.jobs:
            job = self.jobs[job_id]
            yield job

    def __len__(self) -> int:
        """returns number of all jobs

        Returns:
            int: number of jobs
        """
        return len(self.jobs)

    def load_past(self):
        """loads active jobs from the past"""
        if not self.past_path.exists():
            return
        with self.past_path.open("r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                if job.status == 0:
                    self.jobs[job.job_id] = job

    def load_present(self):
        """loads job from the present"""
        with self.present_path.open("r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                self.jobs[job.job_id] = job

    def save(self):
        """saves jobs from the present to memory"""
        with self.present_path.open("w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(self.header)

            for job_id, job in self.jobs.items():
                row = [
                    job.job_id,
                    job.title,
                    job.description,
                    str(job.status),
                    job.creation_date.isoformat(),
                ]
                writer.writerow(row)

    def add(self, title, description="", status=0, creation_date=None):
        """adds job to BulletJournal"""
        job = Job(title, description, status, creation_date)
        self.jobs[job.job_id] = job
        return job

    def complete(self, job_id: str):
        """marks a job as completed"""
        job = self.jobs[job_id]
        job.status = 1

    def cancel(self, job_id: str):
        """marks a job as cancelled"""
        job = self.jobs[job_id]
        job.status = 2


if __name__ == "__main__":
    BJ = BulletJournal()
