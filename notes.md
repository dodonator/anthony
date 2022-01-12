# notes

Das Projekt ist inspiriert von meinem analogen BulletJournal und [diesem](https://entropia.de/GPN19:Plain_Text:_Die_unertr%C3%A4gliche_Leichtigkeit_des_Seins) GPN Talk. Es soll eine CLI geben, die das Verwalten von Tasks ermöglichen soll. Niklas hat eine Überlegungen zu einer ToDo Liste in einem [Blog Artikel](https://www.ytvwld.de/blog/ToDo.html) verfasst.

## tasks

* Ein Task besitzt einen Namen, einen Status, eine optionale Beschreibung, ein Erstelldatum und eine ID
* Ein Task hat initial den Status geöffnet (status = open)
* Ein Task kann verschoben werden (status -> post poned)
* Ein Task kann abgebrochen werden (status -> cancelled)

## Dateien

### today.md

Diese Datei speichert die Tasks des aktuellen Tages menschenlesbar ab. Es können Tasks über die CLI hinzugefügt werden oder als erledigt markiert werden. Der h1 Header der Datei trägt das aktuelle Datum.

### history.csv

Diese Datei enthält alle beendeten Tasks. Ein Task gilt als beendet, wenn er entweder abgebrochen oder ausgeführt wurde. Zu jedem Task wird hierbei der Titel, die Beschreibung, der Status, das Erstelldatum, das Abschlussdatum sowie die ID gespeichert.

### Laden und Speichern von Tasks

1. Das Programm wird gestartet
2. Die `today.md` Datei wird eingelesen.
3. Das Datum der Datei wird mit dem aktuellem Datum verglichen. Sind die Daten gleich geht es weiter mit Punkt 6.
4. Alle Tasks die in der `today.md` Datei entweder als ausgeführt oder als abgebrochen markiert sind werden in die `history.csv` Datei geschrieben, als Abschlussdatum wird das Datum der `today.md` Datei angegeben.
5. Alle Tasks, die in der `today.md` Datei entweder als verschoben oder als offen markiert sind werden in eine neue `today.md` Datei mit dem aktuellem Datum geschrieben.
6. Tasks können nun über die CLI hinzugefügt oder bearbeitet werden.

## Speichern von Tasks

Tasks sollen in menschenlesbarer plain text Dateien gespeichert werden. Siehe als [Beispiel](./example.md)

## geplante Features

* tagging
* filter Funktion

### karma system

Ein Karmascore soll Prokrastination quantifizieren.

* Ein erledigter Task bringt +1
* Ein verschobebener Task bringt -1
* Ein abgebrochner Task bringt -1
