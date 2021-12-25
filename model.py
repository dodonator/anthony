from dataclasses import dataclass
from uuid import uuid4, UUID
from collections import namedtuple
from itertools import tee


@dataclass
class Job:
    title: str
    description: str
    status: "Job_Status"
    job_id: str
    job_counter: int = 0

    def __init__(self, title: str, description, status: "Job_Status") -> None:
        self.title = title
        self.description = description
        self.status = status
        self.job_id = _convert(Job.job_counter)
        Job.job_counter += 1

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


def _pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _convert(value, length=6):
    h = hex(value)[2:]
    h = h.rjust(length, "0")
    return "-".join(("".join(t) for t in _pairwise(h)))
