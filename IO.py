import datetime
import re
from pathlib import Path
from typing import Generator

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
