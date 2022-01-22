import datetime
from pathlib import Path
from pprint import pprint

from IO import load_last_page, load_page, save_page
from Page import Page


def active_tasks(page: Page) -> list[Page]:
    tasks = page.tasks()
    active_tasks = [task for task in tasks if task.active]
    return active_tasks


today = datetime.date.today()
source_path = Path(".")

last_page = load_last_page(source_path)

if last_page.date != today:
    # load active tasks
    old_tasks = active_tasks(last_page)

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

pprint(page.to_dict())
