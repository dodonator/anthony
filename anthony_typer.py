import typer

app = typer.Typer()


@app.command()
def add(type: str, title: str):
    pass


@app.command()
def list(type: str = ""):
    pass


@app.command()
def delete(title: str):
    pass


if __name__ == "__main__":
    app()
