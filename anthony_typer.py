import datetime
from pathlib import Path

import typer

from IO import init_dir, initialize_page, save_page
from Note import Note
from Task import Task

source_path = Path("./source/")

app = typer.Typer()


@app.command()
def add(item_type: str):
    if item_type == "appointment":
        pass

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

    for item in items:
        print(item)


@app.command()
def delete(title: str):
    pass


if __name__ == "__main__":
    init_dir(source_path)
    page, path = initialize_page(source_path)
    app()
    save_page(path, page)
