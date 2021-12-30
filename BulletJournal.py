import csv

from model import Job
from typing import Iterable, List
from pathlib import Path


class BulletJournal:
    tasks: List[Job]
    archive_path: Path
    active_path: Path

    def __init__(self, archive_path, active_path) -> None:
        # converting to Path
        if isinstance(archive_path, str):
            archive_path = Path(archive_path)
        self.archive_path = archive_path

        if isinstance(active_path, str):
            active_path = Path(active_path)
        self.active_path = active_path

        # initialize files
        header = ["job id", "title", "description", "status", "creation date"]
        if not self.archive_path.exists():
            self.archive_path.touch()

        if not self.archive_path.stat().st_size:
            with self.archive_path.open("w", newline="") as archive:
                writer = csv.writer(archive, delimiter=",")
                writer.writerow(header)

        if not self.active_path.exists():
            self.active_path.touch()

        # initiate job list
        self.tasks = list()
        self.load_active()

    def __iter__(self) -> Iterable[Job]:
        """iterates over all jobs"""
        for job in self.task:
            yield job

    def __len__(self) -> int:
        """returns number of all jobs

        Returns:
            int: number of jobs
        """
        return len(self.tasks)

    def load_active(self):
        """loads active jobs from memory"""
        if not self.active_path.exists():
            return

        with self.active_path.open("r", newline="") as active:
            reader = csv.DictReader(active, delimiter=",")
            for row in reader:
                job = Job.from_dict(row)
                self.tasks.append(job)

    def save_active(self):
        """saves active jobs to memory"""
        active_jobs = list(filter(lambda j: j.status.code >= 2, self.tasks))
        header = ["job id", "title", "description", "status", "creation date"]

        with self.active_path.open("w", newline="") as active:
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

        with self.archive_path.open("a", newline="") as archive:
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
    BJ = BulletJournal("archive.csv", "active.csv")
