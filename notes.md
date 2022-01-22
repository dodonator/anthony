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

* add [appointment, note, task] - Fügt ein neues Item der aktuellen Page hinzu.
* list [appontment, note, task, _] - Listet alle Items eines Typs oder alle Items der aktuellen Page auf.
* export [path] - Exportiert die aktuelle Page als markdown Datei.

### Task Actions

Die folgenden Aktionen können auf Tasks der aktuellen Page ausgeführt werden. Jede Aktion ist dabei auch als command vorhanden.

* complete task
  Der Task wird beendet ( `done = True` , `active = False` ). Ein Karma Punkt wird generiert.

* cancel task
  Der Task wird abgebrochen ( `done = False` , `active = False` ) und an späteren Tagen nicht mehr angezeigt. Ein Karma Punkt wird abgezogen.

* move task
  Der Task wird verschoben ( `done = True` , `active = True` ). Der Task kann somit am aktuellen Tag nicht mehr vollendet werden. Da der Task als `active` markiert ist, wird er am nächsten Tag wieder geladen werden. Ein Karma Punkt wird abgezogen.

* repeat task [date]
  Der Task wird wiederholt (sofern er abgeschlossen oder abgebrochen ist). Standartmäßig wird der Task am folgenden Tag als offen ( `done = False` , `active = True` ) angezeigt. Alternativ kann das Datum angegeben werden, zu dem der Task wiederholt werden soll.
