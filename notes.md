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

## Pages

Eine Page betrachtet einen Tag und beinhaltet alle Termine, Notizen und Aufgaben, die an diesem Tag anfallen.

```python
class Page:
    date: datetime.date  # date of the page
    entries: list  # List[Appointment | Note | Task]
```
