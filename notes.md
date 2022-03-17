# notes

Das Projekt ist inspiriert von meinem analogen BulletJournal und [diesem](https://entropia.de/GPN19:Plain_Text:_Die_unertr%C3%A4gliche_Leichtigkeit_des_Seins) GPN Talk. Es soll eine CLI geben, die das Verwalten von Tasks ermöglichen soll. Niklas hat eine Überlegungen zu einer ToDo Liste in einem [Blog Artikel](https://www.ytvwld.de/blog/ToDo.html) verfasst.

## Appointments

Appointments sind Termine.

```python
class Appointment:
    appointment_id: str  # uuid4().hex
    title: str  # title of the appointment
    content: str  # details of the appointment
    start: datetime.datetime  # start time of the appointment
```

## Notes

Notes sind Notizen.

```python
class Note:
    note_id: str  # uuid4().hex
    title: str  # title of the note
    content: str  # details of the note
```

## Tasks

Tasks sind Aufgaben.

```python
class Task:
    task_id: str  # uuid4().hex
    title: str  # title of the task
    content: str  # details of the task
    done: bool  # if the task is completed
    active: bool  # if the task is active (relevant for Page)
    execution_date: datetime.date  # date the task should be executed
```

### Task status

Ein Task besitzt zwei flags: `done` , welches angibt, ob ein Task erledigt wurde und `active` , welches angibt, ob ein Task an dem aktuellen Tag respektive auf der aktuellen Seite noch erledigt werden kann. Aus der Kombination dieser beiden Werte ergibt sich der Status eines Tasks. Nur Tasks, welche als `active` markiert sind werden auf die nächste Page übernommen.

|              | done=True | done=False |
|--------------|-----------|------------|
| active=True  | moved     | open       |
| active=False | completed | cancelled  |

## Pages

Eine Page betrachtet einen Tag und beinhaltet alle Termine, Notizen und Aufgaben, die an diesem Tag anfallen.

```python
class Page:
    date: datetime.date  # date of the page
    entries: list  # List[Appointment | Note | Task]
```

## CLI commands

```anthony [Appointment | Note | Task] [command]```

### Appointment (Termin)

Die commands für Aufgaben betreffen sowohl die Page für den aktuellen Tag, als auch die Pages vergangener Tage.

command | Argument | Beschreibung
--- | --- | ---
add | None | Fügt einen neuen Termin hinzu der entsprechenden Page hinzu.
list | date | Listet alle Termine am angegebenen Tag auf.
remove | title | Entfernt diesen Termin.
export | filename | Exportiert alle Termine im markdown Format in die angegebene Datei.

### Notes (Notiz)

Alle commands für Notizen betreffen alle gespeicherten Pages.

command | Argument | Beschreibung
--- | --- | ---
add | None | Fügt eine neue Notiz der aktuellen Page hinzu.
list | None | Listet alle bisherigen Notizen.
remove | title | Entfernt diese Notiz.
export | filename | Exportiert alle Notizen im markdown Format in die angegebene Datei.

### Tasks (Aufgaben)

Die commands für Aufgaben betreffen sowohl die aktuelle Page als auch zurückliegende Pages.

command | Argument | Beschreibung
--- | --- | ---
add | None | Fügt eine neue Aufgabe zur aktuellen Page hinzu.
list | status |Listet alle Aufgaben mit dem angegebenen status auf.
remove | title | Entfernt Aufgabe mit dem gegebenen Titel.
export | filename | Exportiert Aufgabe im markdown Format in die angegebene Datei.
status | title | Gibt den Status der Aufgabe mit diesem Titel an.
complete | title | Markiert diese Aufgabe als erledigt.
cancel | title | Bricht diese Aufgabe ab.
repeat | title | Markiert diese Aufgabe als erledigt und legt sie als Wiedervorlage an.
postpone | title | Bricht die Aufgabe für heute ab und verschiebt sie auf die nächste Page.
