import datetime
from pathlib import Path

import typer

from Appointment import Appointment
from IO import init_dir, initialize_page, save_page
from Item import Item
from Note import Note
from Task import Task

source_path = Path("./source/")

app = typer.Typer()


@app.command()
def add(item_type: str):
    if item_type == "appointment":
        title: str = typer.prompt("title")
        content: str = typer.prompt("content")
        start_iso: str = typer.prompt("start")
        start: datetime.datetime = datetime.datetime.fromisoformat(start_iso)
        appointment = Appointment(title, content, start)
        page.add(appointment)
        typer.echo(f"added {appointment}")

    elif item_type == "note":
        title = typer.prompt("title")
        description = typer.prompt("description")
        note = Note(title, description)
        page.add(note)
        typer.echo(f"added {note}")

    elif item_type == "task":
        title = typer.prompt("title: ")
        content = typer.prompt("content: ")
        done = typer.confirm("done? ")
        active = typer.confirm("active? ")
        execution_date_iso = typer.prompt("execution date (ISO): ")
        execution_date = datetime.date.fromisoformat(execution_date_iso)
        task = Task(title, content, done, active, execution_date)
        page.add(task)
        typer.echo(f"added {task}")

    else:
        pass

    save_page(path, page)


@app.command()
def list(item_type: str = ""):

    if item_type == "appointment":
        items = page.appointments()

    elif item_type == "note":
        items = page.notes()

    elif item_type == "task":
        items = page.tasks()

    else:
        items = [i[0] for i in page.items]
        appointments = page.appointments()
        print("Appointments: ")
        for appointment in appointments:
            print(f"* {appointment}")
        print()

        notes = page.notes()
        print("Notes: ")
        for note in notes:
            print(f"* {note}")
        print()

        tasks = page.tasks()
        print("Tasks: ")
        for task in tasks:
            print(f"* {task}")
        print()

        return

    for item in items:
        print(item)


@app.command()
def show(
    title: str,
    full: bool = False,
):
    result = page.find(title)
    if result is not None:
        if full:
            typer.echo(repr(result))
        else:
            typer.echo(result)


@app.command()
def complete(title: str):
    """Completes the task successfully."""
    item: Item = page.find(title)
    if isinstance(item, Task):
        task: Task = item
    else:
        raise Exception("You can only complete Tasks.")

    task.done = True
    task.active = False

    typer.echo(f"Completed the task {task} successfull.")


@app.command()
def cancel(title: str):
    """Completes the task unsuccessfully."""
    item: Item = page.find(title)
    if isinstance(item, Task):
        task: Task = item
    else:
        raise Exception("You can only complete Tasks.")

    task.done = False
    task.active = False

    typer.echo(f"Cancelled the task {task}.")


if __name__ == "__main__":
    init_dir(source_path)
    page, path = initialize_page(source_path)
    app()
    save_page(path, page)
