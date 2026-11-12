# AI_USAGE

Hier protokolliere ich, wo ich KI-Werkzeuge benutzt habe, wie im Kurs verlangt: Datum und Task, Werkzeug und Modell, Prompt, was ich übernommen, geändert oder verworfen habe, und wie ich es geprüft habe.

Werkzeug in allen Einträgen: **Grok Bot**, ein KI-Assistent mit Zugriff auf einen eigenen Linux-Rechner, Shell, Web-Suche und GitHub-Zugriff sowie auf mein MacBook, wenn ich ihn darum bitte. Modell: nicht angegeben (die App nennt kein Modell).

## 10.11.2026 · Lab 1, Tasks 5–8 (`dataset.md`, `feiertage/`)

- **Prompt (sinngemäß):** „Hilf mir, die Feiertage für Köln/NRW aus Wikipedia als CSV zu bauen, mit anderen Quellen abzugleichen und daraus mein dataset.md zu schreiben.“
- **Übernommen:** `get_feiertage.py` (Parsen der Wikipedia-Tabelle samt Hintergrundfarben, Abgleich mit dem Paket `holidays` und feiertage-api.de, Schulferien, Kalendertabelle (ohne FC-Heimspiele)), Gliederung und erste Fassung des Profils, der kurze Join-Test `probe_join.py`.
- **Geändert / verworfen:** von mir nicht nachgetragen.
- **Wie geprüft:** Das Skript gleicht drei Quellen automatisch ab (NRW: 37/37/37 Feiertage, keine Abweichung) und listet jede Abweichung auf (6 Tage in Hessen). Persönliche Stichprobe gegen das FTG NW: von mir noch nicht nachgetragen.

## 12.11.2026 · Lab 1, Task 1 (Profil-README) und Task 2 (README, LICENSE)

- **Prompt (sinngemäß):** „Bereite mein Profil-README und das Lab-Repo mit README und MIT-Lizenz vor, nichts erfinden.“
- **Übernommen:** Text des Profil-README, README dieses Repos, `LICENSE` (MIT-Vorlage von GitHub, mit der API-Vorlage `api.github.com/licenses/mit` verglichen).
- **Geändert / verworfen:** von mir nicht nachgetragen.
- **Wie geprüft (vom Assistenten):** Profil-README und Lab-README nach dem Push live auf GitHub gelesen; die Links zum Kurs, zum Lab-Repo und zum Team-Repo zeigen auf die richtigen Seiten. Ob ich die Seite selbst im Browser angeklickt habe, ist hier nicht festgehalten.

## 12.11.2026 · Lab 1, Task 3 (`cheatsheet.md`)

- **Prompt (sinngemäß):** „Schreib den Markdown-Spickzettel mit allen Features aus der Tabelle, teste jedes im CommonMark-Standard und auf GitHub.“
- **Übernommen:** alle Einträge. Der Assistent hat die Datei aus einer Liste von Einträgen erzeugt, damit Quelltext und Ergebnis garantiert gleich sind.
- **Wie geprüft (vom Assistenten):** jeden Eintrag mit `commonmark.py` (Python-Implementierung des CommonMark-Standards) gerendert und das ganze Dokument über die GitHub-Markdown-API (`POST /markdown`, Modus `gfm`). Die Labels CommonMark/GitHub folgen diesem Test. Die Anker im Inhaltsverzeichnis sind nach GitHubs Regel gebildet, aber noch nicht auf der echten Seite angeklickt.
- **Noch offen für mich:** stichprobenartig im CommonMark Dingus gegenprüfen und nach dem Push jeden Link im Inhaltsverzeichnis der veröffentlichten Datei anklicken; Pitfalls um eigene Erfahrungen ergänzen.

## 12.11.2026 · Lab 1, Task 4 (`open-source.md`)

- **Prompt (sinngemäß):** „Untersuche pandas wie in Task 4 verlangt, mit echten Zahlen von der GitHub-API und Links zu jeder Quelle.“
- **Übernommen:** alle Antworten. Die Zahlen stammen aus Abfragen vom 12.11.2026 (`/repos/pandas-dev/pandas`, `/community/profile`, `/contributors`, `/releases/latest`, Suche nach offenen Issues und PRs) und von pandas.pydata.org (Governance, Sponsors, Contributing Guide).
- **Geändert / verworfen:** von mir nicht nachgetragen.
- **Wie geprüft (vom Assistenten):** Nach dem Veröffentlichen liefert `https://api.github.com/repos/lenmer100/data-integration-labs` den Wert `license.spdx_id = MIT` (12.11.2026). Die drei SPDX-Beispiele in `open-source.md` sind in der Datei mit diesem API-Wert nachgetragen. Ein zusätzliches persönliches Öffnen der Links im Browser habe ich nicht festgehalten.

## 12.11.2026 · Lab 1, Tasks 5–8 (Überarbeitung)

- **Prompt (sinngemäß):** „Prüf mein dataset.md gegen die Aufgabe und die Quellen und verbessere es.“
- **Übernommen:** Fakten-Tabelle an den Anfang verschoben (Task 6 verlangt das), pandas-Version korrigiert (3.1 statt 3.0), Namensnennung für die DB-Daten ergänzt, Hinweis auf die Nachprüfung.
- **Wie geprüft (vom Assistenten):** Wikipedia-Version, Größe und Lizenz über die MediaWiki-API, Trefferzahlen und Lizenzfelder von GovData und Open.NRW über die CKAN-API, alle Statistiken (Min, Max, Mittel, leere Zellen, Zeilen) mit pandas aus den CSVs neu berechnet, Lizenz der DB-Daten über die Hugging-Face-API. Alles stimmte mit dem Text überein.

## 12.11.2026 · Lab 2, Tasks 3–5 (`journals.md`, `get_data.sh`, `approve.md`)

- **Prompt (sinngemäß):** „Bearbeite Task 3 bis 5 von Lab 2 mit echten Befehlen und Ausgaben.“
- **Übernommen:** Der Assistent hat alle Befehle in `journals.md` auf seinem Linux-Rechner (bash) in den Beispieldaten ausgeführt und die echten Ausgaben eingefügt. Befehle, die es auf dem Mac nicht gibt (`grep -P`, `md5sum`), hat er durch `awk` und `uniq -c` ersetzt. `get_data.sh` stammt aus dem Entwurf vom 10.11. und wurde an die Aufgabe angepasst (zwei Variablen, `SOURCES.txt`, erster Blick, Kommentar am Ende). `get_data.txt` ist die Ausgabe eines Laufs auf dem Linux-Rechner des Assistenten, der Benutzername ist durch `<user>` ersetzt. Für `approve.md` hat er die Befehle 3 und 4 in einem Wegwerf-Ordner getestet und `pandsa` auf PyPI nachgeschlagen.
- **Geändert / verworfen:** von mir nicht nachgetragen.
- **Wie geprüft (vom Assistenten):** Die Befehle in `journals.md` liefen auf seinem Linux-Rechner; `get_data.sh` erzeugt `data/raw/` und `SOURCES.txt`. Eine eigene Wiederholung auf dem Mac in einem leeren Ordner habe ich nicht festgehalten.
- **Tasks 1 und 2:** siehe den Eintrag weiter unten vom 12.11.2026 (Abend): `shell.md` und `bashcrawl.log` hat der Assistent auf meinem MacBook erzeugt, nicht ich allein in einem eigenen Terminal.

## 12.11.2026 · Lab 3, Tasks 1 und 3–6

- **Prompt (sinngemäß):** „Bereite Lab 3 vor, so weit es ohne meinen Rechner und meinen GitHub-Login geht.“
- **Übernommen:** Task 1: Antworten in `graph.md` zuerst als Entwurf, mit echtem Git nachgestellt. Den Graphen und die Hashes in der späteren Fassung (Abend) hat der Assistent ebenfalls lokal nachgespielt, nicht im Browser-Visualizer; siehe den Eintrag unten. Tasks 3–5: Der Assistent hat die Schritte in diesem Repository auf seinem Linux-Rechner ausgeführt (Skript kopieren, `.gitignore`, zwei getrennte Commits mit `git add -p`, README, Undo-Übungen, Branches und Konflikt in `countries.csv`). Die Ausgaben in `git.md` und `conflict.md` sind echt und stammen aus diesem Lauf. Task 6: `history.md` mit echten Befehlen in einem Klon von `datasets/co2-ppm`, Issue und PR über die GitHub-API nachgeschlagen.
- **Wichtig:** Der „schon gepushte“ kaputte Commit in Task 4 war beim Revert nur lokal, weil das Repo noch nicht auf GitHub lag. Die Antwort zu `revert` statt `reset` gilt trotzdem.
- **Geändert / verworfen:** von mir nicht nachgetragen.
- **Wie geprüft (vom Assistenten):** `git log --oneline -- labs/03` zeigt getrennte Commits pro Schritt; `grep` findet keine Konfliktmarken in `countries.csv`. Eine zusätzliche persönliche Kontrolle habe ich nicht festgehalten.
- **Tasks 2 und 7:** siehe den Eintrag vom 12.11.2026 (Abend). Klon, Git-Konfiguration, `git.md` Setup, Issue #19 und PR #20 hat der Assistent mit meinem GitHub-Login auf dem MacBook ausgeführt. Ein Review eines fremden Team-PRs stand zu diesem Zeitpunkt noch aus. Später am 12.11.2026 habe ich zu Robels PR #22 ein Review mit Änderungswünschen (`REQUEST_CHANGES`) abgegeben; den Text hat der Assistent entworfen, ich habe ihn freigegeben: https://github.com/dis-bahn-wetter/bahn-wetter/pull/22#pullrequestreview-5881482890

## 12.11.2026 · FC-Spalten entfernt und Abgabe vorbereitet

- **Prompt (sinngemäß):** „Mach die Git-Aufgabe fertig, nimm die FC-Heimspiele wegen der ODbL-Lizenz raus, und veröffentliche das vorbereitete Lab-Repo und die Feiertags-Zeile im Team-Repo.“
- **Übernommen:** Entfernen der OpenLigaDB-Daten (Spalten `ist_fc_heimspiel`, `fc_anstoss`, `fc_gegner` und die 51 Heimspiel-Zeilen) aus Skript, CSVs und `dataset.md`; Anpassen der Feiertags-Zeile an das README-Format des Team-Repos; Anlegen der öffentlichen Repos und des Pull Requests.
- **Geändert / verworfen:** Die vorbereitete Schulferien-Zeile im Team-README habe ich nicht eingereicht, weil Robel die Schulferien in Issue #5 übernimmt. Die FC-Daten sind nicht mehr im Repo.
- **Wie geprüft:** Spalten und Dateien nach der Änderung durchsucht (keine OpenLigaDB-Daten mehr in den CSVs); Zeilen- und Spaltenzahlen in `dataset.md` an die neuen Dateien angepasst; Team-Branch auf den aktuellen `main` gesetzt.

## 12.11.2026 · Lab 2 Tasks 1–2 und Lab 3 Tasks 1, 2 und 7 (auf meinem MacBook)

- **Prompt (sinngemäß):** „Bring die Labs auf den Stand der offiziellen Aufgaben, mit echten Ausgaben von meinem Mac, und committe und pushe das.“
- **Übernommen:** `labs/02/shell.md` und `labs/02/bashcrawl.log` aus einer echten zsh-Sitzung auf meinem MacBook (inkl. `sleep 600`/`kill`, `git --version`, und einem Durchlauf von bashcrawl bis `cat end`). `labs/03/git-graph.png` und die ausgefüllten Antworten in `graph.md` aus einem lokalen Nachspielen der vier Visualizer-Runden (nicht aus dem Browser-Tool). Abschnitt *Setup* in `git.md` aus `git clone`, `git config --global` und `git log` auf diesem Mac. `team.md` mit Issue #19, PR #20 und dem echten `git log --oneline --graph -15` des Team-Repos. Dieser `AI_USAGE.md`-Eintrag.
- **Geändert / verworfen:** Der Assistent hat bashcrawl nicht von Hand in Terminal.app gespielt, sondern die Befehle in einer interaktiven zsh auf dem Mac ausgeführt und die History danach wie verlangt zugeschnitten. Den Commit-Graphen hat er nicht im Visualizing-Git-Tool erzeugt, sondern lokal nachgestellt und als Bild gezeichnet; das steht in `graph.md`. PR #20 hat er nicht gemergt. Zum Zeitpunkt der ersten `team.md`-Fassung gab es noch keinen offenen fremden PR. Später am Abend lagen Robels PRs #21 und #22 vor: den Text für das Review mit Änderungswünschen zu #22 hat der Assistent entworfen, ich habe ihn freigegeben und das Review am 12.11.2026 abgeschickt (https://github.com/dis-bahn-wetter/bahn-wetter/pull/22#pullrequestreview-5881482890).
- **Wie geprüft (vom Assistenten):** In `bashcrawl.log` steht der erste `cd` in `entrance` und `cat end` (mindestens einmal). Nach dem Kampf existierte die Datei `end`, Inventar war `armour,sword,amulet,`. `git config --global user.email` ist die noreply-Adresse, kein privates Gmail. Vor dem Push: Checkliste gegen die offiziellen Lab-Texte; nach dem Push: Dateien und Commits live auf GitHub geprüft.
- **Wo nur ich etwas ergänzen kann:** persönliche Stichproben (FAIR, Cheatsheet-Anker im Browser, `get_data.sh` selbst in einem leeren Ordner auf dem Mac).
