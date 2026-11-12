# Lab 2 · Task 5: Erst lesen, dann freigeben

Ich habe die Befehle mit `man`, [explainshell.com](https://explainshell.com) und den [tldr pages](https://tldr.sh) nachgeschlagen. Nr. 3 und Nr. 4 habe ich in einem Wegwerf-Ordner (`sandbox`) mit Testdateien ausprobiert, nicht im Projekt.

| # | Befehl | Was er macht | Entscheidung | Warum / was ich stattdessen freigebe |
| --- | --- | --- | --- | --- |
| 1 | `ls -la data/raw` | Listet alle Dateien in `data/raw` auf, auch versteckte, mit Rechten, Größe und Datum. | freigeben | Liest nur, ändert nichts. |
| 2 | `wc -l data/raw/*.csv` | Zählt die Zeilen jeder CSV-Datei in `data/raw` und die Summe. | freigeben | Liest nur. |
| 3 | `sort -u data/raw/stations.csv > data/raw/stations.csv` | Soll die Datei sortieren und Duplikate entfernen. Die Shell leert die Zieldatei aber mit `>`, **bevor** `sort` sie liest. Im Test war `stations.csv` danach 0 Byte groß. | nach Änderung freigeben | `sort -u -o data/raw/stations.csv data/raw/stations.csv` (`sort` liest erst alles und schreibt dann) oder in eine neue Datei: `sort -u data/raw/stations.csv > data/raw/stations_unique.csv`. Außerdem fasse ich Rohdaten nicht an, das Ergebnis gehört in einen anderen Ordner. |
| 4 | `rm * .bak` | Wegen des Leerzeichens sind das zwei Argumente: `*` löscht **alle** Dateien im Ordner, danach meldet `rm`, dass es `.bak` nicht gibt. Im Test war der Ordner danach leer. Es gibt keinen Papierkorb. | nach Änderung freigeben | Erst anschauen: `ls *.bak`, dann `rm -i *.bak` (ohne Leerzeichen, fragt bei jeder Datei nach). |
| 5 | `find . -name "*.csv" -size +100M` | Sucht ab dem aktuellen Ordner alle CSV-Dateien, die größer als 100 MB sind. | freigeben | Liest nur. Gut, um große Dateien zu finden, bevor sie aus Versehen in Git landen. |
| 6 | `chmod -R 777 .` | Gibt rekursiv **allen** Nutzern Lese-, Schreib- und Ausführrechte auf jede Datei und jeden Ordner im Projekt. | ablehnen | Das löst kein echtes Problem und öffnet alles. Wenn nur ein Skript nicht startet: `chmod +x get_data.sh`. |
| 7 | `curl -fsSL https://example.com/install.sh \| bash` | Lädt ein Skript aus dem Internet und führt es sofort aus, ohne dass ich es sehe. | ablehnen | Nur nach Änderung: erst herunterladen und lesen, `curl -fsSL -o install.sh https://example.com/install.sh`, dann `less install.sh`, und erst danach selbst entscheiden, ob ich `bash install.sh` ausführe. Lieber eine Installation über den Paketmanager (`brew`, `pip`). |
| 8 | `cat ~/.ssh/id_ed25519` | Gibt meinen **privaten** SSH-Schlüssel aus. Damit landet er in der Ausgabe und damit beim Agenten. | ablehnen | Für ein Datenprojekt gibt es dafür keinen Grund. Wenn jemand meinen Schlüssel braucht, dann höchstens den öffentlichen: `cat ~/.ssh/id_ed25519.pub`. |
| 9 | `ps aux \| grep python` | Listet alle laufenden Prozesse und filtert die mit `python` heraus. Die `grep`-Zeile selbst taucht mit auf. | freigeben | Liest nur. |
| 10 | `pip install pandsa` | Installiert ein Paket namens `pandsa`, das ist ein Tippfehler für `pandas`. | nach Änderung freigeben | `pip install pandas`. Am 12.11.2026 gab es `pandsa` auf PyPI nicht (`https://pypi.org/pypi/pandsa/json` → 404). Genau solche Namen registrieren Angreifer aber gern (Typosquatting), dann würde fremder Code installiert. |

Die Regel, die ich mitnehme: Befehle, die nur lesen (`ls`, `wc`, `find`, `ps`), gebe ich frei. Alles mit `>`, `rm`, `chmod`, `| bash` oder geheimen Dateien lese ich Zeichen für Zeichen und probiere es im Zweifel in einer Sandbox aus.
