# Lab 3 · Task 6: Die Geschichte eines Datensatzes

Repository: [datasets/co2-ppm](https://github.com/datasets/co2-ppm), geklont neben mein Lab-Repo (nicht hinein). Alle Fragen beziehen sich auf `data/co2-mm-mlo.csv`. Stand des Klons: 12.11.2026, letzter Commit `52f2be5` vom 01.11.2026.

```bash
cd ~
git clone https://github.com/datasets/co2-ppm.git
cd co2-ppm
```

## Versionen

```bash
git log --oneline -- data/co2-mm-mlo.csv | wc -l
git log --format="%an" -- data/co2-mm-mlo.csv | sort | uniq -c | sort -rn
git log --format="%ad" --date=format:%Y -- data/co2-mm-mlo.csv | sort | uniq -c
```

```text
48
     30 github-actions
     15 Soren Jones
      1 subhankar
      1 Luccas Gomes
      1 Joel
     10 2015
      4 2016
      2 2017
     10 2024
     11 2025
     11 2026
```

48 Commits haben die Datei geändert. 15 davon stammen von Soren Jones (2015 bis Januar 2017, von Hand), je einer von subhankar (2017), Joel (2024) und Luccas Gomes (2026), und 30 vom Bot `github-actions` (seit April 2024). **Von 2018 bis 2023 hat niemand die Datei angefasst.** In dieser Zeit war der neueste Monat darin der Dezember 2016:

```bash
git log --format="%h %ad %an %s" --date=short --until=2018-01-01 -1 -- data/co2-mm-mlo.csv
git show af2c0a6:data/co2-mm-mlo.csv | tail -n 1
```

```text
af2c0a6 2017-03-13 subhankar [s] update date format from yyyy-mm to yyyy-mm-dd ref - #8
2016-12-01,2016.958,404.48,404.48,405.25,29
```

Wer in diesen sechs Jahren die Datei heruntergeladen hat, bekam also Daten, die bis zu sieben Jahre alt waren, ohne dass die Datei das irgendwo gesagt hätte.

## Der Tag, an dem die Daten verschwanden

```bash
git log --stat -- data/co2-mm-mlo.csv | less     # durchgeblättert, dann gezielt gesucht:
git log --format="%h %ad" --date=short --numstat -- data/co2-mm-mlo.csv | grep -v '^$' | paste - - | awk '$4 > $3 + 100'
git show --stat --format="%h %ad %an %s" --date=iso 0c74626
git show 0c74626:data/co2-mm-mlo.csv
```

```text
0c74626 2026-03-01	0	814	data/co2-mm-mlo.csv
0c74626 2026-03-01 01:14:53 +0000 github-actions Commit from GitHub Actions (Update Data from NOAA)

 data/co2-annmean-gl.csv |  12 +-
 data/co2-gr-gl.csv      |  20 +-
 data/co2-gr-mlo.csv     |   6 +-
 data/co2-mm-gl.csv      | 401 ++++++++++++------------
 data/co2-mm-mlo.csv     | 814 ------------------------------------------------
 5 files changed, 220 insertions(+), 1033 deletions(-)
Date,Decimal Date,Average,Interpolated,Trend,Number of Days
```

Das Update vom **01.03.2026** (`0c74626`) hat 814 Zeilen gelöscht. Übrig blieb nur der Header. Ein Skript wie mein `get_data.sh` hätte an diesem Tag ohne Fehler eine Datei mit einer einzigen Zeile heruntergeladen, denn für den Server war alles in Ordnung (HTTP 200).

```bash
git log --format="%h %ad %an %s" --date=iso -1 4ae30e8
git show 4ae30e8 -- scripts/process.sh
```

```text
4ae30e8 2026-03-03 20:29:58 -0300 Luccas Gomes fix: harden NOAA fetch and restore co2-mm-mlo output
...
-  curl ftp://aftp.cmdl.noaa.gov/products/trends/co2/$file > tmp/$file
+  curl --fail --silent --show-error --location ftp://aftp.cmdl.noaa.gov/products/trends/co2/$file -o tmp/$file
+  if [ ! -s "tmp/$file" ]; then
+    echo "Download failed or empty file: $file" >&2
+    exit 1
+  fi
```

Repariert hat es **Luccas Gomes** am 03.03.2026 (`4ae30e8`, über [PR #16](https://github.com/datasets/co2-ppm/pull/16)), also **zwei Tage später** (umgerechnet etwa 70 Stunden nach dem kaputten Update). Die Reparatur wendet genau die Lektion aus Lab 2 an: `curl -f` (`--fail`) bricht bei einem Serverfehler ab, statt eine Fehlerseite oder eine leere Datei zu speichern, und `-o` statt `>` schreibt erst, wenn etwas ankommt. Zusätzlich prüft `[ ! -s ... ]`, ob die Datei leer ist.

## Alte Zahlen ändern sich

```bash
git show --stat 8c40972
git diff 8c40972~1 8c40972 -- data/co2-mm-mlo.csv | grep -c "^+[0-9]"
git diff 8c40972~1 8c40972 -- data/co2-mm-mlo.csv | grep -c "^-[0-9]"
diff <(git show 8c40972~1:data/co2-mm-mlo.csv | cut -d, -f1) <(git show 8c40972:data/co2-mm-mlo.csv | cut -d, -f1)
git diff 8c40972~1 8c40972 --word-diff --word-diff-regex='[^,]+' -- data/co2-mm-mlo.csv | grep "\[-" | head -n 4
```

```text
 data/co2-mm-mlo.csv     | 103 +++---
52
51
822a823
> 2026-08
1982-12,1982.9583,340.78,[-341.70-]{+341.71+},26,0.30,0.11
1993-10,1993.7917,354.23,[-357.60-]{+357.61+},28,0.29,0.11
1995-07,1995.5417,361.78,[-361.10-]{+361.11+},28,0.36,0.13
2020-02,2020.1250,414.32,[-413.40-]{+413.41+},28,0.69,0.25
```

Das Update vom 01.10.2026 hat **einen** Monat hinzugefügt (2026-08) und **51** bestehende Monate geändert. 52 Zeilen kamen dazu, 51 fielen weg, und nur bei 2026-08 unterscheidet sich die Liste der Monate. Der älteste geänderte Monat ist **Dezember 1982**. Die Word-Diff zeigt, dass sich meist nur die vierte Zahl (der saisonbereinigte Wert) um 0,01 ändert. NOAA rechnet also rückwirkend neu. Für mich heißt das: Zahlen, die ich aus einem Download im September berechnet habe, lassen sich mit einem Download im Oktober nicht mehr genau nachrechnen. Ich muss mir merken, welche Version ich benutzt habe.

## Ein Header, der nicht mehr passt

```bash
git show 8c40972:data/co2-mm-mlo.csv | head -n 2
git show af2c0a6:data/co2-mm-mlo.csv | head -n 2
git show 8c40972:data/co2-mm-mlo.csv | head -n 1 | tr , '\n' | wc -l
git show 8c40972:data/co2-mm-mlo.csv | sed -n 2p | tr , '\n' | wc -l
```

```text
Date,Decimal Date,Average,Interpolated,Trend,Number of Days
1958-03,1958.2027,315.71,314.44,-01,-9.99,-0.99
Date,Decimal Date,Average,Interpolated,Trend,Number of Days
1958-03-01,1958.208,315.71,315.71,314.62,-1
6
7
```

Am 01.10.2026 hat der Header **6** Namen, eine Zeile aber **7** Werte. Am 13.03.2017 passten beide (6 und 6). Außerdem ist das Datum wieder `1958-03` statt `1958-03-01`, die Änderung aus `af2c0a6` ist also verloren gegangen. Seit wann der Header nicht mehr passt, zeigt eine Schleife über alle Versionen:

```bash
for c in $(git log --reverse --format=%h -- data/co2-mm-mlo.csv); do
  echo "$c $(git log -1 --format=%ad --date=short $c) header=$(git show $c:data/co2-mm-mlo.csv | head -1 | tr , '\n' | wc -l) row=$(git show $c:data/co2-mm-mlo.csv | sed -n 2p | tr , '\n' | wc -l)"
done | sed -n '16,18p'
```

```text
af2c0a6 2017-03-13 header=6 row=6
ed48c9c 2024-02-13 header=6 row=7
50dcc34 2024-04-01 header=6 row=7
```

Seit **`ed48c9c` vom 13.02.2024** (Joel, *Add automatic updates of data*): Seitdem kommt die Datei aus dem Skript, das die NOAA-Textdatei mit ihren sieben Spalten übernimmt, aber den alten Header schreibt. Wer die Datei mit pandas liest, bekommt verschobene Spalten. Auf GitHub ist das Problem bekannt: [Issue #18](https://github.com/datasets/co2-ppm/issues/18) *„co2-mm-gl.csv and co2-mm-mlo.csv have incorrect number of header names vs columns“* vom 04.05.2026 ist noch offen. Es gibt einen Fix, [PR #19](https://github.com/datasets/co2-ppm/pull/19) *„fix: csv headers from source text files“* vom 12.07.2026, aber er ist am 12.11.2026 noch nicht gemergt. Behoben ist es also noch nicht.

## Version festnageln

```bash
git rev-parse 8c40972
curl -fsSL https://raw.githubusercontent.com/datasets/co2-ppm/8c4097238570147adf6fa97ad357315528dac4c5/data/co2-mm-mlo.csv | tail -n 1
git checkout 0c74626
wc -l data/co2-mm-mlo.csv
git status | head -n 1
git switch main
```

```text
8c4097238570147adf6fa97ad357315528dac4c5
2026-08,2026.6250,427.55,429.51,17,0.36,0.17
1 data/co2-mm-mlo.csv
HEAD detached at 0c74626
```

Diese URL liefert die Datei immer so, wie sie am 01.10.2026 war:
<https://raw.githubusercontent.com/datasets/co2-ppm/8c4097238570147adf6fa97ad357315528dac4c5/data/co2-mm-mlo.csv>

Die Version vom Tag, an dem die Daten verschwanden, hat genau **1** Zeile (nur den Header). Den Zustand dazwischen nennt Git **detached HEAD**: `HEAD` zeigt direkt auf einen Commit und nicht auf einen Branch.

## Fazit

In unserem Projekt-README schreibe ich zu jedem Datensatz das Abrufdatum und eine feste Version dazu: bei Git-Quellen die URL mit dem vollen Commit-Hash, bei Wikipedia die `oldid` (wie in meinem Feiertags-Profil, Version 271794065). Bei einem Portal ohne Git, wie in Lab 1, speichere ich das Abrufdatum und eine Prüfsumme der Datei (`git hash-object`, wie in Task 3), damit man sieht, ob sich die Quelle seitdem geändert hat. Wenn die Lizenz es erlaubt, legen wir die benutzte Rohdatei zusätzlich selbst ab, zum Beispiel mit einem DOI auf Zenodo, weil das Portal alte Versionen sonst einfach überschreibt.
