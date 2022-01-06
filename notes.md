# notes

Das Projekt ist inspiriert von meinem analogen BulletJournal und [diesem](https://entropia.de/GPN19:Plain_Text:_Die_unertr%C3%A4gliche_Leichtigkeit_des_Seins) GPN Talk. Es soll eine CLI geben, die das Verwalten von Tasks ermöglichen soll.

## tasks

* Ein Task hat einen Namen, einen Status, eine optionale Beschreibung und eine ID
* Ein Task hat initial den Status geöffnet (status = open)
* Ein Task kann verschoben werden (status -> post poned)
* Ein Task kann abgebrochen werden (status -> cancelled)

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
