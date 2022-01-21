import datetime
from pathlib import Path
from pprint import pprint

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

from Day import Appointment, Day, Note, Task

source_path = Path("journal")


def init_dir(path: Path):

    if not path.exists():
        path.mkdir()

    year = datetime.date.today().year
    year_path = source_path / str(year)

    if not year_path.exists():
        year_path.mkdir()


def extract_yaml_files(path: Path):
    yaml_files = list(source_path.glob("**/*.yaml"))
    return yaml_files


def save_day(path: Path, day: Day):
    day_dict = day.to_dict()
    with path.open("w") as file:
        dump(day_dict, file, Dumper=Dumper)


date = datetime.date.today()
day = Day(date)
path = Path(f"{date.isoformat()}.yaml")

appointment = Appointment("Freitagsfoo", "Freitagsfoo", datetime.date(2022, 1, 21))
task = Task("Aufgabe", "dinge tun")
note = Note("Notiz", "dinge aufschreiben")

day.add(appointment)
day.add(note)
day.add(task)

pprint(day.to_dict())

save_day(path, day)
