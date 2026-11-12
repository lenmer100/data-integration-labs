# Lab 3 · Task 5: Branch, Merge und ein Konflikt in einer CSV-Datei

## Ein Fast-forward

```text
$ git add countries.csv

$ git commit -m "Add country mapping table with ISO alpha-3 codes"
[main 1624312] Add country mapping table with ISO alpha-3 codes
 1 file changed, 6 insertions(+)
 create mode 100644 labs/03/countries.csv

$ git switch -c feature/iso2
Switched to a new branch 'feature/iso2'

$ git commit -am "Add ISO alpha-2 codes to the country table"
[feature/iso2 19a7473] Add ISO alpha-2 codes to the country table
 1 file changed, 6 insertions(+), 6 deletions(-)

$ git switch main
Switched to branch 'main'

$ git merge feature/iso2
Updating 1624312..19a7473
Fast-forward
 labs/03/countries.csv | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
```

Das Wort **`Fast-forward`** in Gits Antwort zeigt, dass kein Merge-Commit entstanden ist: `main` wurde nur auf den Commit von `feature/iso2` vorgeschoben.

## Zwei Arbeitslinien

```text
$ git switch -c feature/new-names
Switched to a new branch 'feature/new-names'

$ git commit -am "Use the current short names of four countries" -m "Czechia since 2016, Eswatini since 2018, North Macedonia since 2019, Türkiye since 2022."
[feature/new-names 2bbc523] Use the current short names of four countries
 1 file changed, 4 insertions(+), 4 deletions(-)

$ git switch main
Switched to branch 'main'

$ git commit -am "Add ISO numeric codes to the country table"
[main e5f0779] Add ISO numeric codes to the country table
 1 file changed, 6 insertions(+), 6 deletions(-)

$ git log --oneline --graph --all -6
* 2bbc523 Use the current short names of four countries
| * e5f0779 Add ISO numeric codes to the country table
|/  
* 19a7473 Add ISO alpha-2 codes to the country table
* 1624312 Add country mapping table with ISO alpha-3 codes
* ac84b73 Revert "Download the school holidays for 2027"
* 05b5024 Download the school holidays for 2027
```

## Der Konflikt

```text
$ git merge feature/new-names || true
Auto-merging labs/03/countries.csv
CONFLICT (content): Merge conflict in labs/03/countries.csv
Automatic merge failed; fix conflicts and then commit the result.

$ cut -d, -f1 countries.csv
<<<<<<< HEAD
name
Czech Republic
Germany
Macedonia
Swaziland
Turkey
=======
name
Czechia
Germany
North Macedonia
Eswatini
Türkiye
>>>>>>> feature/new-names
```

So hat Git die Datei hinterlassen:

```text
<<<<<<< HEAD
name,iso3,iso2,numeric
Czech Republic,CZE,CZ,203
Germany,DEU,DE,276
Macedonia,MKD,MK,807
Swaziland,SWZ,SZ,748
Turkey,TUR,TR,792
=======
name,iso3,iso2
Czechia,CZE,CZ
Germany,DEU,DE
North Macedonia,MKD,MK
Eswatini,SWZ,SZ
Türkiye,TUR,TR
>>>>>>> feature/new-names
```

Ein Programm, das diese CSV liest, sähe die Konfliktmarker als ganz normale Zeilen: `<<<<<<< HEAD`, `=======` und `>>>>>>> feature/new-names` wären Länder, der Header stünde zweimal in der Datei, und jedes Land käme doppelt vor, einmal mit altem und einmal mit neuem Namen, mal mit drei und mal mit vier Spalten. pandas würde entweder abbrechen oder still falsche Daten einlesen.

## Gelöst

```text
$ cat countries.csv
name,iso3,iso2,numeric
Czechia,CZE,CZ,203
Germany,DEU,DE,276
North Macedonia,MKD,MK,807
Eswatini,SWZ,SZ,748
Türkiye,TUR,TR,792

$ grep -c -E "^(<<<<<<<|=======|>>>>>>>)" countries.csv || true
0

$ cut -d, -f4 countries.csv
numeric
203
276
807
748
792

$ git add countries.csv

$ git commit --no-edit
[main 6bcc26e] Merge branch 'feature/new-names'

$ git branch -d feature/iso2 feature/new-names
Deleted branch feature/iso2 (was 19a7473).
Deleted branch feature/new-names (was 2bbc523).
```

```text
$ git log --oneline --graph -8
*   6bcc26e Merge branch 'feature/new-names'
|\  
| * 2bbc523 Use the current short names of four countries
* | e5f0779 Add ISO numeric codes to the country table
|/  
* 19a7473 Add ISO alpha-2 codes to the country table
* 1624312 Add country mapping table with ISO alpha-3 codes
* ac84b73 Revert "Download the school holidays for 2027"
* 05b5024 Download the school holidays for 2027
* b506d4f Say that only the script is in the repository
```

**Beide Branches haben verschiedene Spalten geändert. Warum meldet Git trotzdem einen Konflikt?** Git vergleicht Zeilen, nicht Spalten. Für Git ist jede Zeile der CSV ein Stück Text, und beide Branches haben dieselben Zeilen geändert: `feature/new-names` den Namen am Anfang, `main` die neue Spalte am Ende.

**Warum gehören Germany und der Header dazu, obwohl nur ein Branch sie geändert hat?** Auf `main` hat jede Zeile eine neue Spalte bekommen, also auch der Header und `Germany`. Und weil die geänderten Zeilen direkt aneinander grenzen, fasst Git sie zu einem einzigen Block zusammen. Darin landen auch Zeilen, die nur auf einer Seite anders sind.

**Wie vermeidet unser Team solche Konflikte?** Kleine, kurze Branches und oft von `main` mergen. Nicht zwei Leute gleichzeitig an derselben Datendatei arbeiten lassen, sondern das im Issue absprechen. Und am besten gemeinsame Tabellen gar nicht von Hand bearbeiten, sondern von einem Skript erzeugen lassen und nur das Skript versionieren. Eine neue Spalte kommt dann als eigener Schritt im Skript dazu.
