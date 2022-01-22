import datetime
import re
from pathlib import Path
from typing import Tuple

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


def initialize_page(source_path: Path) -> Tuple[Page, Path]:
    """Initialize the page for current date."""

    today = datetime.date.today()

    # extract all page files
    page_files = extract_page_files(source_path)

    # sort page files chronologically
    page_files.sort(key=lambda p: p.stem)

    # check if there are any page files
    if page_files:

        # get path to last page file
        last_path = page_files.pop()

        # load last page
        last_page = load_page(last_path)

        if last_page.date != today:
            # create new page
            page = Page(today)

            # create path for page
            year = page.date.year
            path = source_path / Path(str(year)) / Path(f"{page.date.isoformat()}.yaml")
            path.touch()

            # load active tasks
            old_tasks = [task for task in last_page.tasks() if task.active]

            # add old tasks to page
            for task in old_tasks:
                page.add(task)

            # save page to path
            save_page(path, page)

        else:
            page = last_page
            page = last_path
    else:
        # create new page
        page = Page(today)

        # create path for page
        year = page.date.year
        path = source_path / Path(str(year)) / Path(f"{page.date.isoformat()}.yaml")
        path.touch()

        # save page to path
        save_page(path, page)

    return page, path
