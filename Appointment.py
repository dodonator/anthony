from __future__ import annotations

import datetime

from Item import Item


class Appointment(Item):
    content: str
    start: datetime.datetime

    def __init__(
        self,
        title: str,
        content: str,
        start: datetime.datetime,
    ) -> None:

        super().__init__(title)
        self.content = content
        self.start = start

    def __str__(self) -> str:
        return f"Appointment({self.title}, {self.start})"

    def to_dict(self) -> dict:
        """Returns Appointment as dict."""
        appointment_dict = dict()
        appointment_dict["appointment_id"] = self.appointment_id
        appointment_dict["title"] = self.title
        appointment_dict["content"] = self.content
        appointment_dict["start"] = self.start
        return appointment_dict

    @staticmethod
    def from_dict(appointment_dict: dict) -> Appointment:
        """Generates Appointment from dict."""
        appointment_id = appointment_dict.get("appointment_id")
        title: str = appointment_dict.get("title")
        content: str = appointment_dict.get("content")
        start: datetime.datetime = appointment_dict.get("start")

        appointment = Appointment(title, content, start)
        appointment.appointment_id = appointment_id

        return appointment


def parse_appointment(line: str) -> Appointment:
    """
    Reads an appointment from an comma seperated string.
    'title, [content,] start_date'
    """
    elements = line.split(",")

    if len(elements) == 2:
        title, start_iso = elements
        content = ""
    elif len(elements) == 3:
        title, content, start_iso = elements
    else:
        raise Exception("Couldn't parse appointment.")

    start_iso = start_iso.lstrip()
    content = content.lstrip()
    start_date = datetime.datetime.fromisoformat(start_iso)
    appointment = Appointment(title, content, start_date)
    return appointment
