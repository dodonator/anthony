import datetime
import re
from pathlib import Path

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

from Page import Page


def init_dir(path: Path):
    """Initialize source directory."""
    if not path.exists():
        path.mkdir()

    year = datetime.date.today().year
    year_path = path / str(year)

    if not year_path.exists():
        year_path.mkdir()


def extract_page_files(path: Path):
    """Extracts paths to pages from given path."""
    yaml_files = path.glob("**/*.yaml")
    page_files = list()
    for path in yaml_files:
        stem = path.stem
        match = re.match(r"\d{4}-\d{2}-\d{2}", stem)
        if match:
            page_files.append(path)
    return page_files


def save_page(path: Path, page: Page):
    """Saves a page to a given path."""
    page_dict = page.to_dict()
    with path.open("w") as file:
        dump(page_dict, file, Dumper=Dumper)


def load_page(path: Path) -> Page:
    """Loads a page from a given path."""
    with path.open("r") as file:
        page_dict = load(file, Loader=Loader)

    page = Page.from_dict(page_dict)
    return page


def load_last_page(path: Path) -> Page:
    """Returns the chronologically last page."""
    page_files = extract_page_files(path)
    page_files.sort(key=lambda p: p.stem)
    last_path = page_files.pop()
    return load_page(last_path)


def initialize_page(source_path: Path):
    today = datetime.date.today()

    last_page = load_last_page(source_path)

    if last_page.date != today:
        # load active tasks
        old_tasks = [task for task in last_page.tasks() if task.active]

        # create new page
        page = Page(today)

        # add old tasks to page
        for task in old_tasks:
            page.add(task)

        # create path for page
        page_path = source_path / Path(f"{page.date.isoformat()}.yaml")
        page_path.touch()

        # save page to path
        save_page(page_path, page)
    else:
        page = last_page
