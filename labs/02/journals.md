# Lab 2 · Task 3: Eine halbe Million Zeitschriftenartikel

Alle Befehle laufen in `labs/02/shell-lesson`, also in den entpackten Beispieldaten der Library Carpentry ([shell-lesson.zip](https://librarycarpentry.org/lc-shell/data/shell-lesson.zip)). Lange Ausgaben sind mit `head` gekürzt.

## Form

```bash
head -n 1 2014-01_JA.tsv | tr "\t" "\n" | cat -n
```

```text
     1	File
     2	Creator
     3	Issue
     4	Volume
     5	Journal
     6	ISSN
     7	ID
     8	Citation
     9	Title
    10	Place Labe
    11	Language
    12	Publisher
    13	Date
```

```bash
for f in *.tsv; do head -n 1 "$f"; done | sort | uniq -c | cut -c 1-60
for f in *.tsv; do echo "$f $(tail -n +2 "$f" | wc -l)"; done
```

```text
      4 File	Creator	Issue	Volume	Journal	ISSN	ID	Citation	T
2014-01-31_JA-africa.tsv 13711
2014-01-31_JA-america.tsv 27391
2014-01_JA.tsv 507731
2014-02-02_JA-britain.tsv 5374
```

Die Datei hat 13 Spalten. Spalte 10 heißt `Place Labe`, da fehlt am Ende das `l` von *Place Label*. Alle vier Dateien haben denselben Header, denn `uniq -c` fasst die vier ersten Zeilen zu einer zusammen (Anzahl 4). Ohne Header enthalten sie 507.731 (alle), 27.391 (america), 13.711 (africa) und 5.374 (britain) Artikel.

## Fehlende Werte

```bash
cut -f 11 2014-01_JA.tsv | tail -n +2 | grep -c "^$"
cut -f 11 2014-01_JA.tsv | tail -n +2 | sort | uniq -c | sort -rn
```

```text
36100
 403284 eng
  40155 fre
  36100 
  28192 ger
```

36.100 Artikel haben keine Sprache. Es gibt nur drei Sprachen: Englisch (403.284), Französisch (40.155) und Deutsch (28.192). Zusammen mit den leeren sind das genau 507.731.

## Jahre

```bash
cut -f 13 2014-01_JA.tsv | tail -n +2 | sort | uniq -c | sort -rn | head -n 5
cut -f 13 2014-01_JA.tsv | tail -n +2 | sort -n | uniq -c | tail -n 5
```

```text
  30813 1997
  28215 1998
  27968 1996
  27916 2002
  27335 2001
...
  24912 2010
  24788 2011
  21804 2012
   8430 2013
     20 2077
```

```bash
awk -F"\t" '$13==2077' 2014-01_JA.tsv | cut -f 5 | sort | uniq -c
awk -F"\t" '$13==2077' 2014-01_JA.tsv | cut -f 3,4,8,13 | head -n 2
awk -F"\t" '$5=="FRANCAIS DANS LE MONDE"' 2014-01_JA.tsv | cut -f 4,13 | sort -n | uniq -c | grep -E "\s35[0-9]\s"
```

```text
     20 FRANCAIS DANS LE MONDE
SUPP	353	FRANCAIS DANS LE MONDE 353(SUPP), 2-2. (2077)	2077
SUPP	353	FRANCAIS DANS LE MONDE 353(SUPP), 4-5. (2077)	2077
     20 351	2007
     20 353	2077
     18 357	2008
```

Die meisten Artikel stammen aus 1997 (30.813). 2077 kann nicht stimmen, die Datei ist von 2014. Alle 20 Artikel kommen aus *Français dans le monde*, Band 353 (Supplement). Band 351 ist von 2007 und Band 357 von 2008, gemeint war also sehr wahrscheinlich **2007** (Zahlendreher 2077). Außerdem haben 22.370 Artikel gar kein Jahr.

## Zeilen sind keine Felder

```bash
grep -ic africa 2014-01_JA.tsv
cut -f 9 2014-01_JA.tsv | grep -ic africa
grep -i africa 2014-01_JA.tsv | awk -F"\t" 'tolower($9) !~ /africa/' | cut -f 5,8 | head -n 3
```

```text
33577
13711
NORTHEAST AFRICAN STUDIES	NORTHEAST AFRICAN STUDIES 1(2/3), 7-18. (1994)
NORTHEAST AFRICAN STUDIES	NORTHEAST AFRICAN STUDIES 1(2/3), 19-48. (1994)
NORTHEAST AFRICAN STUDIES	NORTHEAST AFRICAN STUDIES 1(2/3), 49-74. (1994)
```

33.577 Zeilen enthalten *africa*, aber nur 13.711 Titel. `grep` durchsucht die ganze Zeile, also auch Zeitschriftenname, Zitat und Dateiname. Ein Artikel aus *Northeast African Studies* zählt deshalb mit, auch wenn sein Titel nichts mit Afrika zu tun hat.

## Woher kommt eine Datei?

```bash
tail -n +2 2014-01_JA.tsv | cut -f 9 | grep -i africa > /tmp/t_full.txt
tail -n +2 2014-01-31_JA-africa.tsv | cut -f 9 > /tmp/t_africa.txt
wc -l /tmp/t_full.txt /tmp/t_africa.txt
diff /tmp/t_full.txt /tmp/t_africa.txt | wc -l
```

```text
  13711 /tmp/t_full.txt
  13711 /tmp/t_africa.txt
  27422 total
0
```

Für Afrika stimmt die Behauptung: gleiche Anzahl, gleiche Titel in gleicher Reihenfolge, `diff` findet nichts. Auch die ganzen Zeilen sind identisch (`diff` auf die vollständigen Zeilen gibt ebenfalls 0 aus).

```bash
tail -n +2 2014-01_JA.tsv | awk -F"\t" 'tolower($9) ~ /america/' > /tmp/am_full.tsv
tail -n +2 2014-01-31_JA-america.tsv > /tmp/am_file.tsv
wc -l /tmp/am_full.tsv /tmp/am_file.tsv
diff <(cut -f 9 /tmp/am_full.tsv) <(cut -f 9 /tmp/am_file.tsv)
```

```text
  27391 /tmp/am_full.tsv
  27391 /tmp/am_file.tsv
  54782 total
12280c12280
< British Trade with Spanish America, 1763Ã¯Â¿Â½1808 - by Pearce, A. J.
---
> British Trade with Spanish America, 1763ï¿½1808 - by Pearce, A. J.
```

Für Amerika stimmt es fast: 27.391 Titel auf beiden Seiten, aber eine Zeile unterscheidet sich. Der Gedankenstrich in *1763–1808* ist in beiden Dateien kaputt (Ersatzzeichen `�`), in der großen Datei aber noch einmal falsch kodiert. Die Teildatei wurde also nicht einfach mit `grep` aus der großen Datei geschnitten, irgendwo dazwischen lag ein Werkzeug, das die Kodierung verändert hat.

## Tabellenkalkulations-Schaden

```bash
cut -f 3 2014-01_JA.tsv | tail -n +2 | sort | uniq -c | sort -rn | head -n 10
awk -F"\t" '$3=="01-Feb"' 2014-01_JA.tsv | cut -f 3,8 | head -n 3
awk -F"\t" '$3=="03-Apr"' 2014-01_JA.tsv | cut -f 3,8 | head -n 2
cut -f 3 2014-01_JA.tsv | tail -n +2 | grep -cE "^[0-9]{2}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$"
```

```text
  99743 1
  96514 2
  75421 3
  58325 4
  30668 
   9650 5
   5325 6
   4219 01-Feb
   3157 03-Apr
   2736 7
01-Feb	WASHINGTON MONTHLY 28(1/2), 4-9. (1996)
01-Feb	WASHINGTON MONTHLY 28(1/2), 9-16. (1996)
01-Feb	WASHINGTON MONTHLY 28(1/2), 17-25. (1996)
03-Apr	INTERNATIONALES ASIENFORUM 26(3/4), 233-248. (1995)
03-Apr	INTERNATIONALES ASIENFORUM 26(3/4), 249-285. (1995)
11632
```

`01-Feb` und `03-Apr` sind keine Heftnummern. In der Spalte `Citation` derselben Zeilen steht `28(1/2)` bzw. `26(3/4)`: Es waren Doppelhefte, also `1/2` und `3/4`. Eine Tabellenkalkulation hat das als Datum gelesen (1. Februar, 3. April) und so wieder gespeichert. Betroffen sind 11.632 Zeilen mit 23 verschiedenen Pseudo-Daten wie `02-Mar`, `08-Sep` oder `11-Dec`. Werte wie `SUM`, `WIN` oder `SUPP` sind dagegen echte Heftbezeichnungen (Sommer, Winter, Supplement), keine Schäden.
