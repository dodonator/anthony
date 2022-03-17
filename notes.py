import rich
import typer

from IO import DIRECTORY, aggregate_notes, daily_page, page_to_path, save_page
from model import Note, Page

app = typer.Typer()
page: Page


@app.command()
def add():
    note_data = {}
    note_data["title"] = typer.prompt("note title: ")
    note_data["content"] = typer.prompt("note content: ")
    note = Note(**note_data)
    page.add(note)
    typer.echo(f"added note {note} to page {page}")
    save_page(page)


@app.command()
def list():
    for note in notes:
        rich.print(note)


@app.command()
def remove(title: str):
    for note in notes:
        if note.title == title:
            page.remove(note)
    save_page(page)


@app.callback()
def main():
    global page
    page = daily_page(DIRECTORY)
    global path
    path = page_to_path(page)
    global notes
    notes = aggregate_notes(DIRECTORY)
    typer.echo(f"current page {path}")


if __name__ == "__main__":
    app()
