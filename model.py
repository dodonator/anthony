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
        description = self.description
        status = self.status
        job_id = self.job_id
        creation = self.creation_date
        output = f"Job({title=}, {description=}, {status=}, {job_id=}, {creation=})"
        return output


class Tag:
    pass


class Day:
    pass


Job_Status = namedtuple("Job_Status", ("name", "prefix", "code"))

Finished = Job_Status("Fininished", "[+]", 0)
Open = Job_Status("Open", "[.]", 1)
Postponed = Job_Status("Postponed", "[>]", 2)
Cancelled = Job_Status("Cancelled", "[x]", 3)


def _convert(value, padding=6):
    return f"{value:0{padding}x}"
