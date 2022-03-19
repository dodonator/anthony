import typer

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
