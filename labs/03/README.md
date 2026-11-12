# Lab 3 · Version Control Software

Meine Abgabe zu [Lab 3](https://github.com/breuert/data-integration/blob/main/labs/version_control_software.md).

| Datei | Task | Inhalt |
| --- | --- | --- |
| [`graph.md`](graph.md), [`git-graph.png`](git-graph.png) | 1 | Vorhersagen und Antworten zu den Commit-Graphen, Screenshot nach Runde 4 |
| [`git.md`](git.md) | 2–4 | Setup, Schritt für Schritt, Undo |
| [`.gitignore`](.gitignore) | 3 | hält `data/raw/` aus Git heraus |
| [`get_data.sh`](get_data.sh) | 3–4 | lädt meine Rohdaten herunter |
| [`countries.csv`](countries.csv), [`conflict.md`](conflict.md) | 5 | Branches, Merge und Konflikt |
| [`history.md`](history.md) | 6 | Geschichte von `datasets/co2-ppm` |
| [`team.md`](team.md) | 7 | Roadmap im Team über Issues und Pull Requests |

## `data/raw/` neu bauen

Die Rohdaten liegen nicht im Repository, nur das Skript, das sie holt. So baut man sie neu (Bash oder zsh, mit `curl`):

```bash
cd labs/03
./get_data.sh            # legt data/raw/ an und lädt beide Dateien
./get_data.sh > get_data.txt   # optional: den ersten Blick speichern
```

Das Skript lädt:

| Datei in `data/raw/` | Quelle | Lizenz |
| --- | --- | --- |
| `wikipedia_feiertage.html` | *Feiertag (Deutschland)*, Version 271794065 vom 01.11.2026, Autor:innen der deutschsprachigen Wikipedia, <https://de.wikipedia.org/w/index.php?oldid=271794065> | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de) |
| `schulferien_nrw.csv` | *Schulferien NRW*, Ministerium für Schule und Bildung des Landes Nordrhein-Westfalen, <https://www.govdata.de/suche/daten/schulferien-nrw55d5d> | [Datenlizenz Deutschland – Namensnennung – 2.0](https://www.govdata.de/dl-de/by-2-0) |

Jeder Lauf hängt eine Zeile pro Datei an `data/raw/SOURCES.txt` an (Datum, URL, Ziel) und gibt am Ende eine Prüfsumme (`git hash-object`) jeder Datei aus. Ändert sich die Prüfsumme, hat sich die Quelle geändert. Die Wikipedia-Datei ist auf eine feste Version gepinnt und sollte gleich bleiben, die Ferien-CSV kann sich ändern, wenn das Ministerium neue Schuljahre ergänzt.
