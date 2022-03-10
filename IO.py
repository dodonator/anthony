import datetime
import re
from pathlib import Path
from typing import Generator, List, Optional

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


def last_recent_page(path: Path) -> Optional[Page]:
    # load all pages
    page_files: List[Path] = extract_page_files(path)
    # sort pages by date
    sorted_files = sorted(page_files, key=lambda p: p.stem, reverse=True)
    # get last page
    for current_path in sorted_files:
        page = load_page(current_path)
        if page is not None:
            return page


def save_page(path: Path, page: Page):
    """Saves a page to a given path."""
    page_dict = page.to_dict()
    with path.open("w") as file:
        dump(page_dict, file, Dumper=Dumper)


def load_page(path: Path) -> Optional[Page]:
    """Loads a page from a given path."""
    with path.open("r") as file:
        page_dict = load(file, Loader=Loader)

    if page_dict is not None:
        page = Page.from_dict(page_dict)
        return page
