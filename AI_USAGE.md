# AI_USAGE

Hier protokolliere ich, wo ich KI-Werkzeuge benutzt habe, wie im Kurs verlangt: Datum und Task, Werkzeug und Modell, Prompt, was ich übernommen, geändert oder verworfen habe, und wie ich es geprüft habe.

<!-- ENTWURF, vom KI-Assistenten vorbereitet. Lennart: jeden Eintrag lesen, bei "Geändert" und "Wie geprüft" deine eigenen Schritte ergänzen und das Modell eintragen. Erst danach committen/pushen. -->

Werkzeug in allen Einträgen: **Grok Bot**, ein KI-Assistent mit Zugriff auf einen eigenen Linux-Rechner, Shell, Web-Suche und lesenden GitHub-Zugriff. Modell: <!-- TODO Lennart: Modellname eintragen, falls die App ihn anzeigt, sonst "nicht angegeben" -->

## 10.11.2026 · Lab 1, Tasks 5–8 (`dataset.md`, `feiertage/`)

- **Prompt (sinngemäß):** „Hilf mir, die Feiertage für Köln/NRW aus Wikipedia als CSV zu bauen, mit anderen Quellen abzugleichen und daraus mein dataset.md zu schreiben.“
- **Übernommen:** `get_feiertage.py` (Parsen der Wikipedia-Tabelle samt Hintergrundfarben, Abgleich mit dem Paket `holidays` und feiertage-api.de, Schulferien, FC-Heimspiele, Kalendertabelle), Gliederung und erste Fassung des Profils, der kurze Join-Test `probe_join.py`.
- **Geändert / verworfen:** <!-- TODO Lennart -->
- **Wie geprüft:** Das Skript gleicht drei Quellen automatisch ab (NRW: 37/37/37 Feiertage, keine Abweichung) und listet jede Abweichung auf (6 Tage in Hessen). <!-- TODO Lennart: eigene Stichproben, z. B. NRW-Feiertage 2026 gegen das FTG NW -->

## 12.11.2026 · Lab 1, Task 1 (Profil-README) und Task 2 (README, LICENSE)

- **Prompt (sinngemäß):** „Bereite mein Profil-README und das Lab-Repo mit README und MIT-Lizenz vor, nichts erfinden.“
- **Übernommen:** Text des Profil-README, README dieses Repos, `LICENSE` (MIT-Vorlage von GitHub, mit der API-Vorlage `api.github.com/licenses/mit` verglichen).
- **Geändert / verworfen:** <!-- TODO Lennart -->
- **Wie geprüft:** <!-- TODO Lennart: Profil-README gelesen, Links angeklickt -->

## 12.11.2026 · Lab 1, Task 3 (`cheatsheet.md`)

- **Prompt (sinngemäß):** „Schreib den Markdown-Spickzettel mit allen Features aus der Tabelle, teste jedes im CommonMark-Standard und auf GitHub.“
- **Übernommen:** alle Einträge. Der Assistent hat die Datei aus einer Liste von Einträgen erzeugt, damit Quelltext und Ergebnis garantiert gleich sind.
- **Wie geprüft (vom Assistenten):** jeden Eintrag mit `commonmark.py` (Python-Implementierung des CommonMark-Standards) gerendert und das ganze Dokument über die GitHub-Markdown-API (`POST /markdown`, Modus `gfm`). Die Labels CommonMark/GitHub folgen diesem Test. Die Anker im Inhaltsverzeichnis sind nach GitHubs Regel gebildet, aber noch nicht auf der echten Seite angeklickt.
- **Noch zu tun:** <!-- TODO Lennart: im CommonMark Dingus stichprobenartig gegenprüfen, nach dem Push jeden Link im Inhaltsverzeichnis anklicken, Pitfalls um eigene Erfahrungen ergänzen -->

## 12.11.2026 · Lab 1, Task 4 (`open-source.md`)

- **Prompt (sinngemäß):** „Untersuche pandas wie in Task 4 verlangt, mit echten Zahlen von der GitHub-API und Links zu jeder Quelle.“
- **Übernommen:** alle Antworten. Die Zahlen stammen aus Abfragen vom 12.11.2026 (`/repos/pandas-dev/pandas`, `/community/profile`, `/contributors`, `/releases/latest`, Suche nach offenen Issues und PRs) und von pandas.pydata.org (Governance, Sponsors, Contributing Guide).
- **Geändert / verworfen:** <!-- TODO Lennart -->
- **Wie geprüft:** <!-- TODO Lennart: mindestens die drei spdx_id-Links selbst im Browser öffnen, nach dem Veröffentlichen den Wert für lenmer100/data-integration-labs eintragen -->

## 12.11.2026 · Lab 1, Tasks 5–8 (Überarbeitung)

- **Prompt (sinngemäß):** „Prüf mein dataset.md gegen die Aufgabe und die Quellen und verbessere es.“
- **Übernommen:** Fakten-Tabelle an den Anfang verschoben (Task 6 verlangt das), pandas-Version korrigiert (3.1 statt 3.0), Namensnennung für die DB-Daten ergänzt, Hinweis auf die Nachprüfung.
- **Wie geprüft (vom Assistenten):** Wikipedia-Version, Größe und Lizenz über die MediaWiki-API, Trefferzahlen und Lizenzfelder von GovData und Open.NRW über die CKAN-API, alle Statistiken (Min, Max, Mittel, leere Zellen, Zeilen) mit pandas aus den CSVs neu berechnet, Lizenz der DB-Daten über die Hugging-Face-API. Alles stimmte mit dem Text überein.

## 12.11.2026 · Lab 2, Tasks 3–5 (`journals.md`, `get_data.sh`, `approve.md`)

- **Prompt (sinngemäß):** „Bearbeite Task 3 bis 5 von Lab 2 mit echten Befehlen und Ausgaben.“
- **Übernommen:** Der Assistent hat alle Befehle in `journals.md` auf seinem Linux-Rechner (bash) in den Beispieldaten ausgeführt und die echten Ausgaben eingefügt. Befehle, die es auf dem Mac nicht gibt (`grep -P`, `md5sum`), hat er durch `awk` und `uniq -c` ersetzt. `get_data.sh` stammt aus dem Entwurf vom 10.11. und wurde an die Aufgabe angepasst (zwei Variablen, `SOURCES.txt`, erster Blick, Kommentar am Ende). `get_data.txt` ist die Ausgabe eines Laufs auf dem Linux-Rechner des Assistenten, der Benutzername ist durch `<user>` ersetzt. Für `approve.md` hat er die Befehle 3 und 4 in einem Wegwerf-Ordner getestet und `pandsa` auf PyPI nachgeschlagen.
- **Geändert / verworfen:** <!-- TODO Lennart -->
- **Wie geprüft:** <!-- TODO Lennart: z. B. zwei Befehle aus journals.md selbst laufen lassen, get_data.sh auf dem Mac in einem leeren Ordner ausführen -->
- **Nicht mit KI:** Task 1 (`shell.md`, meine eigene Shell) und Task 2 (bashcrawl) habe ich selbst gemacht. <!-- TODO Lennart: nur stehen lassen, wenn es stimmt -->

## 12.11.2026 · Lab 3, Tasks 1 und 3–6

- **Prompt (sinngemäß):** „Bereite Lab 3 vor, so weit es ohne meinen Rechner und meinen GitHub-Login geht.“
- **Übernommen:** Task 1: Antworten in `graph.md` als Entwurf, mit echtem Git nachgestellt (der Screenshot und die Hashes kommen von mir aus dem Visualizer). Tasks 3–5: Der Assistent hat die Schritte in diesem Repository auf seinem Linux-Rechner ausgeführt (Skript kopieren, `.gitignore`, zwei getrennte Commits mit `git add -p`, README, Undo-Übungen, Branches und Konflikt in `countries.csv`). Die Ausgaben in `git.md` und `conflict.md` sind echt und stammen aus diesem Lauf. Task 6: `history.md` mit echten Befehlen in einem Klon von `datasets/co2-ppm`, Issue und PR über die GitHub-API nachgeschlagen.
- **Wichtig:** Der „schon gepushte“ kaputte Commit in Task 4 war beim Revert nur lokal, weil das Repo noch nicht auf GitHub lag. Die Antwort zu `revert` statt `reset` gilt trotzdem.
- **Geändert / verworfen:** <!-- TODO Lennart -->
- **Wie geprüft:** <!-- TODO Lennart: git log --oneline -- labs/03 und git status selbst laufen lassen, conflict.md mit der Datei vergleichen -->
- **Nicht mit KI:** Task 2 (Klonen, Push, Setup-Fragen in `git.md`) und Task 7 (Issue, Pull Request, Review im Team-Repo) mache ich selbst. <!-- TODO Lennart: nur stehen lassen, wenn es stimmt -->
