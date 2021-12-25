from dataclasses import dataclass
from uuid import uuid4, UUID
from collections import namedtuple


@dataclass
class Job:
    title: str
    description: str
    status: "Job_Status"
    job_id: UUID

    def __init__(self, title: str, description, status: "Job_Status") -> None:
        self.title = title
        self.description = description
        self.status = status
        self.job_id = uuid4()

    def __str__(self) -> str:
        prefix = self.status.prefix
        return f"{prefix} {self.title} {self.job_id}"


class Tag:
    pass


class Day:
    pass


Job_Status = namedtuple("Job_Status", ("name", "prefix", "code"))

Finished = Job_Status("Fininished", "[+]", 0)
Open = Job_Status("Open", "[.]", 1)
Postponed = Job_Status("Postponed", "[>]", 2)
Cancelled = Job_Status("Cancelled", "[x]", 3)
