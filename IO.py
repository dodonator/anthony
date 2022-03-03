import datetime
import re
from pathlib import Path
from typing import Generator, Tuple

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

from model import Page

# file directory example:
#
# files/
# └── 2022
#     ├── 2022-02-11.yaml
#     ├── 2022-02-15.yaml
#     ├── 2022-02-18.yaml
#     └── 2022-03-03.yaml

# steps:
# 1. Initialize folder structure
# 2. glob yaml files
# 3. load last recent page
# 4. create new page

DIRECTORY = Path("files")


def init_folder_structure(path: Path):
    """Initializes folder structure at given path.

    Args:
        path (Path): location fo folder structure
    """
    if not path.exists():
        path.mkdir()

    current_year: int = datetime.date.today().year
    year_path: Path = path / Path(str(current_year))

    if not year_path.exists():
        year_path.mkdir()


def extract_page_files(path: Path) -> list[Path]:
    """Extracts all page file from directory.

    Args:
        path (Path): root directory

    Returns:
        list[Path]: page files
    """
    yaml_files: Generator = path.glob("**/*.yaml")

    page_files = [
        yaml_path
        for yaml_path in yaml_files
        if re.match(r"\d{4}-\d{2}-\d{2}", yaml_path.stem)
    ]
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


def generate_path_from_page(source_path: Path, page: Page) -> Path:
    """Generates a path to a page given a source path."""
    date = page.date
    year = date.year
    path = source_path / Path(str(year)) / Path(f"{date.isoformat()}.yaml")
    return path


def initialize_page(source_path: Path) -> Tuple[Page, Path]:
    """Initialize the page for current date."""

    today = datetime.date.today()

    # extract all page files
    page_files = extract_page_files(source_path)

    # check if there are any page files
    if page_files:
        # sort page files chronologically
        page_files.sort(key=lambda p: p.stem)

        # get path to last page file
        last_path = page_files.pop()

        # load last page
        last_page = load_page(last_path)

        if last_page.date != today:
            # create new page
            page = Page(today)

            # create path for page
            path = generate_path_from_page(source_path, page)
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
            path = last_path
    else:
        # create new page
        page = Page(today)

        # create path for page
        path = path = generate_path_from_page(source_path, page)
        path.touch()

        # save page to path
        save_page(path, page)

    return page, path
