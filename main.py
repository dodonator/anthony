import pandoc
from pandoc.types import Header
from pathlib import Path

filename = "bullet_journal.md"
filepath = Path(filename)

with filepath.open("r") as file:
    text = file.read()

doc = pandoc.read(text)

for element in doc[1]:
    if isinstance(element, Header):
        header_title = element[2]
        print(f"{header_title!r}")
