# Lab 3 · Task 1: Commit-Graphen vorhersagen

Gespielt in [Visualizing Git](https://git-school.github.io/visualizing-git/), vier Runden ohne `clear` dazwischen. Das Tool nennt den ersten Branch `master`, ich lese ihn als `main`. Den Graphen nach Runde 4 zeigt [`git-graph.png`](git-graph.png).

<!-- ENTWURF: Die Vorhersagen und Antworten unten habe ich vorab mit echtem Git nachgestellt (gleiche Befehle, ein Startcommit). Lennart: die Runden im Visualizer selbst spielen, mit dem Bild vergleichen, die Stellen mit TODO ausfüllen und die Hashes aus dem Tool eintragen. -->

## Runde 1 · Eine gerade Linie

```text
git commit -m "Download the data"
git checkout -b clean
git commit -m "Drop empty rows"
git commit -m "Parse dates"
git checkout master
git merge clean
```

**Vorhersage:** Drei neue Commits in einer Linie. Kein Commit hat zwei Eltern. Weil `master` seit dem Abzweigen nicht weitergegangen ist, kann Git `master` einfach nach vorne schieben. Danach zeigen `master` und `clean` beide auf *Parse dates*, `HEAD` steht auf `master`.

**Ergebnis:** Stimmt. `git merge clean` hat **keinen neuen Commit** erzeugt, sondern einen *Fast-forward* gemacht. <!-- TODO: genaue Antwort des Tools hier eintragen --> `master` und `clean` zeigen auf denselben Commit (*Parse dates*).

## Runde 2 · Zwei Linien treffen sich

```text
git checkout -b plot
git commit -m "Plot cyclists per month"
git checkout master
git commit -m "Describe the data in the README"
git merge plot
git tag v1.0
```

**Vorhersage:** Zwei neue Commits auf getrennten Linien und ein Merge-Commit mit zwei Eltern. `master` und `v1.0` zeigen auf den Merge-Commit, `plot` bleibt auf *Plot cyclists per month*, `clean` auf *Parse dates*.

**Ergebnis:** Der Merge-Commit hat zwei Eltern: *Describe the data in the README* (erster Elternteil, von `master`) und *Plot cyclists per month* (zweiter Elternteil, von `plot`). Ein Fast-forward war nicht möglich, weil **beide** Branches seit dem gemeinsamen Vorgänger *Parse dates* einen eigenen Commit bekommen haben, keiner ist also ein Vorfahre des anderen. Ein Tag wie `v1.0` markiert einen festen Stand, zum Beispiel die Version des Datensatzes, die wir beim World Café zeigen, oder den Stand zur Abgabe.

## Runde 3 · Zwei Wege zurück

```text
git commit -m "Delete outliers"
git revert HEAD
git reset HEAD~2
```

**Vorhersage:** *Delete outliers* kommt dazu, dann ein neuer Commit, der ihn rückgängig macht. `git reset HEAD~2` setzt `master` zwei Commits zurück auf den Merge-Commit (`v1.0`).

**Ergebnis:** `git revert HEAD` hat einen **neuen Commit** (*Revert "Delete outliers"*) angehängt, der die Änderung umkehrt. Die Geschichte bleibt erhalten. `git reset HEAD~2` hat dagegen nichts hinzugefügt, sondern den Branch `master` auf den Merge-Commit zurückgesetzt (im Tool wie `--hard`). *Delete outliers* und der Revert sind jetzt gestrichelt. Sie sind **nicht weg**: Git hebt sie noch auf und findet sie über `git reflog`, bis sie irgendwann aufgeräumt werden. Für Commits, die schon gepusht sind, darf ich nur `git revert` nehmen, denn `reset` schreibt die Geschichte um, die meine Teammitglieder schon haben. Beim nächsten Pull gäbe es Konflikte oder die Commits kämen zurück.

## Runde 4 · Verloren und gefunden

```text
git checkout v1.0~1
git commit -m "Try a log scale"
git checkout master
git reflog
```

**Vorhersage:** `v1.0~1` ist der erste Elternteil des Merge-Commits, also *Describe the data in the README*. `HEAD` zeigt dann direkt auf einen Commit, nicht auf einen Branch (*detached HEAD*). *Try a log scale* hängt an *Describe the data in the README*. Nach `git checkout master` hält ihn kein Branch mehr.

**Ergebnis:** Über dem Graphen steht nach `git checkout v1.0~1` <!-- TODO: genauen Text aus dem Tool eintragen, z. B. "Detached HEAD" -->, also ist `HEAD` vom Branch gelöst. Nach dem Wechsel zurück auf `master` wird *Try a log scale* gestrichelt, weil kein Branch mehr auf ihn zeigt. In der Ausgabe von `git reflog` steht er in der Zeile *commit: Try a log scale*, mit dem Hash <!-- TODO: Hash aus dem Tool -->. Mit `git branch logscale <hash>` hängt wieder ein Branch daran, und er ist gerettet.

## Was ich mitnehme

- Ein Fast-forward ist kein richtiger Merge, nur ein Verschieben des Branch-Zeigers.
- Ein Merge-Commit ist der einzige Commit mit zwei Eltern. `~1` folgt immer dem ersten.
- `revert` für alles, was schon gepusht ist, `reset` nur für lokale Commits.
- Nichts ist sofort weg: Mit `git reflog` finde ich auch Commits wieder, auf die kein Branch zeigt.
