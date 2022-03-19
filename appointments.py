from datetime import datetime

import typer

from IO import date_to_path, load_page, save_page
from model import Appointment, Page

app = typer.Typer()


@app.command()
def add():
    appointment: Appointment = input_appointment()
    date = appointment.start.date()
    path = date_to_path(date)
    page: Page | None = load_page(path)
    if page is None:
        page = Page(date)
    page.add(appointment)
    save_page(page)
    typer.echo(f"saved appointment {appointment} at {path}")


@app.command()
def list():
    pass


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
