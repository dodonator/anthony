from dataclasses import dataclass
from uuid import uuid4, UUID


@dataclass
class Job:
    title: str
    description: str
    status: int
    job_id: UUID

    def __init__(self, title: str, description, status) -> None:
        self.title = title
        self.description = description
        self.status = status
        self.job_id = uuid4()


class Tag:
    pass


class Day:
    pass
