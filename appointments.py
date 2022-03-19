from datetime import datetime

import typer

from model import Appointment

app = typer.Typer()

if __name__ == "__main__":
    app()


@app.command()
def add():
    pass


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
