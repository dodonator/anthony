from collections import namedtuple
from datetime import date


class Job:
    title: str
    description: str
    status: "Job_Status"
    job_id: str
    job_counter: int = 0
    creation_date: date

    def __init__(
        self, title: str, description, status: "Job_Status", creation_date=None
    ) -> None:
        self.title = title
        self.description = description
        self.status = status
        if creation_date is None:
            creation_date = date.today()
        self.creation_date = creation_date

        creation_year = self.creation_date.year
        self.job_id = f"{creation_year}-{_convert(Job.job_counter)}"
        Job.job_counter += 1

    def __str__(self) -> str:
        prefix = self.status.prefix
        return f"{prefix} {self.title} {self.job_id}"

    def __repr__(self) -> str:
        title = self.title
        desc = self.description
        status = self.status
        job_id = self.job_id
        creation = self.creation_date
        output = f"Job({title=}, {desc=}, {status=}, {job_id=}, {creation=})"
        return output

    @staticmethod
    def from_dict(d: dict):
        job_id = d["job id"]
        title = d["title"]
        description = d["description"]
        status = job_stati[int(d["status"])]
        creation_date_iso = d["creation date"]
        creation_date = date.fromisoformat(creation_date_iso)
        j = Job(title, description, status, creation_date)
        j.job_id = job_id

        return j


class Tag:
    pass


class Day:
    pass


Job_Status = namedtuple("Job_Status", ("name", "prefix", "code"))

Finished = Job_Status("Fininished", "[+]", 0)
Cancelled = Job_Status("Cancelled", "[x]", 1)
Open = Job_Status("Open", "[.]", 2)
Postponed = Job_Status("Postponed", "[>]", 3)

job_stati = [Finished, Cancelled, Open, Postponed]


def _convert(value, padding=6):
    return f"{value:0{padding}x}"
