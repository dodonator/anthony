import datetime
import re
from pathlib import Path
from typing import Generator, Iterator, Optional

from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from yaml import dump, load

from model import Appointment, Item, Note, Page

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


def create_page_file(date: datetime.date) -> Path:
    """Creates page file for given date.

    Args:
        date (datetime.date): date of Page

    Returns:
        Path: path to page file
    """
    page = Page(date)
    path = page_to_path(page)
    if not path.exists():
        path.touch()
        save_page(page)
    return path


def last_recent_page(path: Path) -> Optional[Page]:
    """Returns the last recent page.

    Args:
        path (Path): root path

    Returns:
        Optional[Page]: last page (or None if no page was found)
    """
    # load all pages
    page_files: list[Path] = extract_page_files(path)
    # sort pages by date
    sorted_files = sorted(page_files, key=lambda p: p.stem, reverse=True)
    # get last page
    for current_path in sorted_files:
        page = load_page(current_path)
        if page is not None:
            return page


def date_to_path(date: datetime.date) -> Path:
    """Generates path from given date.

    Args:
        date (datetime.date): date for page

    Returns:
        Path: path for page file
    """
    filename: str = f"{date.isoformat()}.yaml"
    year: int = date.year
    path: Path = DIRECTORY / str(year) / filename
    return path


def page_to_path(page: Page) -> Path:
    """Generates path to save page at.

    Args:
        page (Page): page to save

    Returns:
        Path: path at which the page will be saved
    """
    date: datetime.date = page.date
    path: Path = date_to_path(date)
    return path


def get_current_page(path: Path) -> Page:
    """Returns the current page.

    Args:
        path (Path): source path

    Returns:
        Page: last saved page or new page
    """
    last_page = last_recent_page(path)
    if last_page is None:
        new_page = Page()
        return new_page
    else:
        return last_page


def daily_page(path: Path) -> Page:
    """Returns page for today.

    Loads the page for the current date or creates a new page.

    Args:
        path (Path): source path

    Returns:
        Page: page for today
    """
    today = datetime.date.today()
    last_page = last_recent_page(path)
    if last_page is None:
        today_page = Page()
    elif last_page.date != today:
        today_page = Page()
    else:
        today_page = last_page
    return today_page


def save_page(page: Page):
    """Saves page.

    Args:
        page (Page): page to save
    """
    path = page_to_path(page)
    page_dict = page.to_dict()
    with path.open("w") as file:
        dump(page_dict, file, Dumper=Dumper)


def load_page(path: Path) -> Optional[Page]:
    """Loads page from given path.

    Returns None if the file at the given path was empty.

    Args:
        path (Path): path to load from

    Returns:
        Optional[Page]: loaded page
    """
    with path.open("r") as file:
        page_dict = load(file, Loader=Loader)

    if page_dict is not None:
        page = Page.from_dict(page_dict)
        return page


def safe_load(path: Path) -> Page:
    date = datetime.date.fromisoformat(path.stem.rstrip(".yaml"))
    if not path.exists():
        path.touch()
        page = Page(date)
    else:
        page = load_page(path)
        if page is None:
            page = Page(date)
    return page


def aggregate_pages(path: Path) -> Iterator[Page]:
    """Aggregates all pages from source path.

    Args:
        path (Path): source path

    Yields:
        Iterator[Page]: Iterator of all pages
    """
    all_page_files = extract_page_files(path)
    for path in all_page_files:
        page: Page | None = load_page(path)
        if page is not None:
            yield page


def aggregate_by_itemtype(path: Path, item_type: type) -> Iterator[Item]:
    """Aggregates all items of an given item type.

    Args:
        path (Path): source path
        item_type (type): type of items to aggregate

    Yields:
        Iterator[Item]: all items of given type
    """
    for page in aggregate_pages(path):
        for item in page.get_by_itemtype(item_type):
            yield item


def aggregate_appointment(path: Path) -> Iterator[Appointment]:
    """Aggregates all appointments from given path.

    Args:
        path (Path): source path

    Yields:
        Iterator[Appointment]: all appointments at given source path
    """
    for page in aggregate_pages(path):
        for appointment in page.appointments():
            yield appointment


def aggregate_notes(path: Path) -> Iterator[Note]:
    """Aggregates all notes from given path.

    Args:
        path (Path): source path

    Yields:
        Iterator[Note]: all notes at given source path
    """
    for page in aggregate_pages(path):
        for note in page.notes():
            yield note
