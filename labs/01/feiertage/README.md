# Feiertage, Ferien und Events für Köln/NRW

Hier liegen das Skript und die daraus gebauten Tabellen zu meinem Datensatz-Profil [`../dataset.md`](../dataset.md).

| Datei | Inhalt | Lizenz der Daten |
| --- | --- | --- |
| [`get_feiertage.py`](get_feiertage.py) | baut alle CSVs aus den Rohdaten | Code: MIT (siehe [`LICENSE`](../../../LICENSE)) |
| [`feiertage_de_2024-2027.csv`](feiertage_de_2024-2027.csv) | gesetzliche Feiertage aller Länder, 70 Zeilen | CC BY-SA 4.0 (abgeleitet aus Wikipedia) |
| [`schulferien_nrw_2024-2027.csv`](schulferien_nrw_2024-2027.csv) | 18 Ferienzeiträume NRW | Datenlizenz Deutschland – Namensnennung – 2.0 (Schulministerium NRW) |
| [`events_koeln_2024-2027.csv`](events_koeln_2024-2027.csv) | 16 Kölner Karnevalstage | aus den Wikipedia-Daten berechnet, CC BY-SA 4.0 |
| [`kalender_koeln_2024-07-01_2027-12-31.csv`](kalender_koeln_2024-07-01_2027-12-31.csv) | ein Eintrag pro Tag, die Tabelle für den Join | gemischt: Feiertage und Karneval unter CC BY-SA 4.0, Schulferien unter dl-de/by-2-0. Ein veröffentlichter Datensatz mit diesen Spalten muss selbst unter CC BY-SA 4.0 stehen, siehe `dataset.md`, Task 8 |
| [`run_log.txt`](run_log.txt) | Ausgabe des letzten Laufs vom 10.11.2026 | |
| [`probe_join.py`](probe_join.py) | kurzer Join-Test mit zwei Monaten DB-Daten | Code: MIT. Braucht `data-2025-05.parquet` und `data-2026-02.parquet` von [piebro/deutsche-bahn-data](https://huggingface.co/datasets/piebro/deutsche-bahn-data) im selben Ordner (nicht im Repo) |

Neu bauen:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 get_feiertage.py      # lädt die Rohdaten nach raw/ (nicht im Repo) und schreibt die CSVs neu
```

Namensnennungen (TASL) für alle Quellen stehen in [`../dataset.md`](../dataset.md).
