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

    def __repr__(self) -> str:
        return f"Appointment({self.title}, {self.start})"

    def to_dict(self) -> dict:
        """Returns Appointment as dict."""
        appointment_dict = dict()
        appointment_dict["item_id"] = self.item_id
        appointment_dict["title"] = self.title
        appointment_dict["content"] = self.content
        appointment_dict["start"] = self.start
        return appointment_dict

    @staticmethod
    def from_dict(appointment_dict: dict) -> Appointment:
        """Generates Appointment from dict."""
        item_id = appointment_dict.get("item_id")
        title: str = appointment_dict.get("title")
        content: str = appointment_dict.get("content")
        start: datetime.datetime = appointment_dict.get("start")

        appointment = Appointment(title, content, start)
        appointment.item_id = item_id

        return appointment
