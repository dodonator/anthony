import datetime
import re
from pathlib import Path

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

from Page import Appointment, Note, Page, Task

source_path = Path("journal")


def init_dir(path: Path):

    if not path.exists():
        path.mkdir()

    year = datetime.date.today().year
    year_path = source_path / str(year)

    if not year_path.exists():
        year_path.mkdir()


def extract_page_files(path: Path):
    yaml_files = path.glob("**/*.yaml")
    page_files = list()
    for path in yaml_files:
        stem = path.stem
        match = re.match(r"\d{4}-\d{2}-\d{2}", stem)
        if match:
            page_files.append(path)
    return page_files


def save_page(path: Path, page: Page):
    page_dict = page.to_dict()
    with path.open("w") as file:
        dump(page_dict, file, Dumper=Dumper)


def load_page(path: Path) -> Page:
    with path.open("r") as file:
        page_dict = load(file, Loader=Loader)

    page = Page.from_dict(page_dict)
    return page
