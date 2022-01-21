from __future__ import annotations

import datetime
from uuid import uuid4


class Appointment:
    appointment_id: str
    title: str
    content: str
    start: datetime.datetime

    def __init__(
        self,
        title: str,
        content: str,
        start: datetime.datetime,
    ) -> None:

        self.appointment_id = uuid4().hex
        self.title = title
        self.content = content
        self.start = start

    def to_dict(self) -> dict:
        """Returns Appointment as dict."""
        appointment_dict = dict()
        appointment_dict["title"] = self.title
        appointment_dict["content"] = self.content
        appointment_dict["start"] = self.start
        return appointment_dict

    @staticmethod
    def from_dict(appointment_dict: dict) -> Appointment:
        """Generates Appointment from dict."""
        appointment_id = appointment_dict.get("appointment_id")
        title = appointment_dict.get("title")
        content = appointment_dict.get("content")
        start = appointment_dict.get("start")

        appointment = Appointment(title, content, start)
        appointment.appointment_id = appointment_id

        return appointment
