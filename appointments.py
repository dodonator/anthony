from datetime import date, datetime

import typer

from IO import DIRECTORY, aggregate_appointments, date_to_path, safe_load, save_page
from model import Appointment, Page

app = typer.Typer()


@app.command()
def add():
    appointment: Appointment = input_appointment()
    date = appointment.start.date()
    path = date_to_path(date)
    page: Page = safe_load(path)
    page.add(appointment)
    save_page(page)
    typer.echo(f"added appointment {appointment} to  page {page}")


@app.command()
def list(date_str: str):
    d: date = date.fromisoformat(date_str)
    appointments = aggregate_appointments(DIRECTORY)
    for appointment in appointments:
        if appointment.start.date() >= d:
            typer.echo(appointment)


@app.command()
def remove():
    pass


def input_appointment() -> Appointment:
    appointment_data = {}
    appointment_data["title"] = typer.prompt("appointment title: ")
    appointment_data["content"] = typer.prompt("appointment content: ")
    appointment_date = typer.prompt("appointment date (YYYY-MM-DD): ")
    appointment_time = typer.prompt("appointment time (hh:mm): ")

    isoformat: str = f"{appointment_date} {appointment_time}"
    appointment_start: datetime = datetime.fromisoformat(isoformat)
    appointment_data["start"] = appointment_start
    appointment = Appointment(**appointment_data)
    return appointment


if __name__ == "__main__":
    app()
