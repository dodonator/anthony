from dataclasses import dataclass
from uuid import uuid4, UUID


@dataclass
class Job:
    title: str
    description: str
    status: int
    job_id: UUID


class Tag:
    pass


class Day:
    pass
