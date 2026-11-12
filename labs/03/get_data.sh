#!/bin/bash
# get_data.sh: lädt die Rohdaten für mein Feiertags-Profil (Lab 1, dataset.md)
# herunter und zeigt einen ersten Blick darauf.
#
# Aufruf:  ./get_data.sh          (im Ordner des Skripts; legt data/raw/ an, falls es fehlt)
#          ./get_data.sh > get_data.txt   speichert den ersten Blick in einer Datei
#
# Quelle 1 (Hauptquelle):
#   "Feiertag (Deutschland)", Version 271794065 vom 01.11.2026, Autor:innen der
#   deutschsprachigen Wikipedia, https://de.wikipedia.org/w/index.php?oldid=271794065,
#   CC BY-SA 4.0. Ich lade genau diese Version, damit sich der Inhalt nicht ändert.
# Quelle 2 (Anreicherung):
#   "Schulferien NRW", Ministerium für Schule und Bildung des Landes Nordrhein-Westfalen,
#   https://www.govdata.de/suche/daten/schulferien-nrw55d5d,
#   Datenlizenz Deutschland – Namensnennung – 2.0

# Hauptquelle: URL und Zieldatei
url="https://de.wikipedia.org/w/index.php?title=Feiertag_(Deutschland)&oldid=271794065&action=render"
out="data/raw/wikipedia_feiertage.html"

# Zweite Datei für die Anreicherung (Task 8 in Lab 1)
url2="https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/Schulferien/OpenData_Ferientermine_2027.csv"
out2="data/raw/schulferien_nrw.csv"

mkdir -p data/raw

for pair in "$url $out" "$url2 $out2"; do
  set -- $pair            # $1 = URL, $2 = Zieldatei
  curl -fsSL -A "data-integration-labs/lenmer100 (TH Koeln, student project)" -o "$2" "$1" || exit 1
  echo "$(date +"%Y-%m-%d %H:%M:%S") $1 -> $2" >> data/raw/SOURCES.txt

  echo "===== $2"
  echo "== Size";  ls -lh "$2"
  echo "== Type";  file "$2"
  echo "== Lines"; wc -l < "$2"
done

# Spalten und erste Zeilen ergeben nur bei der CSV Sinn.
# Zeile 1 der CSV ist "sep=;", ein Hinweis für Excel, der Header steht in Zeile 2.
echo "===== $out2"
echo "== Columns";     sed -n 2p "$out2" | tr ';' '\n' | wc -l
echo "== First lines"; head -n 3 "$out2"

# Prüfsumme jeder Datei: ändert sich, sobald sich der Inhalt der Quelle ändert
for f in "$out" "$out2"; do
  echo "== Checksum $f"; git hash-object --no-filters "$f"
done

# Abgleich mit labs/01/dataset.md (Stand 12.11.2026):
# - Die Wikipedia-Seite ist hier HTML (action=render). In dataset.md stehen 75.783 Bytes
#   Wikitext, das ist die Größe des Quelltexts, nicht des gerenderten HTML. Die Zahl der
#   Zeilen sagt bei HTML wenig, weil die Zeilenumbrüche vom Renderer abhängen.
# - Die Ferien-CSV enthält alle Schuljahre ab 2018/19, in dataset.md stehen nur die
#   18 Ferienzeiträume der Schuljahre 2024/25 bis 2027/28. Deshalb hat die CSV mehr Zeilen.
#   Die CSV hat 6 Spaltennamen, aber jede Datenzeile endet mit einem ";". Ein Programm, das
#   nach ";" trennt, sieht deshalb 7 Felder, das letzte leer.
# - Die URL auf www.schulministerium.nrw.de leitet auf apps.schulministerium.nrw.de um.
#   curl folgt der Umleitung wegen -L.
# - Zweimal ausgeführt: Die Datendateien werden ersetzt (curl -o überschreibt), aber
#   data/raw/SOURCES.txt wächst um eine Zeile pro Datei und Lauf (nach zwei Läufen 4 Zeilen,
#   weil ich zwei Dateien lade). Den Unterschied macht ">>": Es hängt an, ">" würde die
#   Datei jedes Mal neu schreiben.
