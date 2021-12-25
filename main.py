import pandoc
from pandoc.types import Header
from pathlib import Path
from pprint import pprint

filename = "bullet_journal.md"
filepath = Path(filename)

with filepath.open("r") as file:
    text = file.read()

doc = pandoc.read(text)

header = [element for element in doc[1] if isinstance(element, Header)]

print(header)
