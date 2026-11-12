# Lab 3 · Task 1: Commit-Graphen vorhersagen

Die vier Runden habe ich **nicht** im Browser-Tool [Visualizing Git](https://git-school.github.io/visualizing-git/) getippt, sondern am 12.11.2026 (Europe/Berlin) in einem Wegwerf-Repository mit denselben Befehlen nachgestellt. Wie im Tool heißt der erste Branch `master` (ich lese ihn als `main`), ich habe `git checkout` statt `git switch` benutzt, und `git reset` als `--hard`. Die Commits sind mit `--allow-empty` entstanden, außer *Delete outliers* und dem anschließenden Revert: die brauchten eine echte Dateiänderung, damit `git revert` einen Commit anlegen kann. Die Hashes und der Graph in [`git-graph.png`](git-graph.png) stammen aus diesem lokalen Nachspielen, nicht aus einem Screenshot des Visualizers.

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

**Ergebnis:** Stimmt. `git merge clean` hat **keinen neuen Commit** erzeugt, sondern einen Fast-forward gemacht. Lokales Git hat geantwortet: `Updating a68d765..5ac23e2` und `Fast-forward`. `master` und `clean` zeigen beide auf *Parse dates* (`5ac23e2`), `HEAD` steht auf `master`.

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

**Ergebnis:** Der Merge-Commit `c7df293` (*Merge branch 'plot'*) hat zwei Eltern: *Describe the data in the README* (`a213ef6`, erster Elternteil, von `master`) und *Plot cyclists per month* (`b74cabe`, zweiter Elternteil, von `plot`). Ein Fast-forward war nicht möglich, weil **beide** Branches seit dem gemeinsamen Vorgänger *Parse dates* (`5ac23e2`) einen eigenen Commit bekommen haben, keiner ist also ein Vorfahre des anderen. Ein Tag wie `v1.0` markiert einen festen Stand, zum Beispiel die Version des Datensatzes, die wir beim World Café zeigen, oder den Stand zur Abgabe. Hier zeigt `v1.0` auf denselben Merge-Commit wie `master`.

## Runde 3 · Zwei Wege zurück

```text
git commit -m "Delete outliers"
git revert HEAD
git reset HEAD~2
```

**Vorhersage:** *Delete outliers* kommt dazu, dann ein neuer Commit, der ihn rückgängig macht. `git reset HEAD~2` setzt `master` zwei Commits zurück auf den Merge-Commit (`v1.0`).

**Ergebnis:** `git revert HEAD` hat einen **neuen Commit** (`6843a7c`, *Revert "Delete outliers"*) angehängt, der die Änderung umkehrt. Die Geschichte bleibt erhalten. `git reset --hard HEAD~2` (so arbeitet `git reset` im Visualizer) hat dagegen nichts hinzugefügt, sondern den Branch `master` auf den Merge-Commit `c7df293` (`v1.0`) zurückgesetzt. *Delete outliers* (`f6d7c3f`) und der Revert (`6843a7c`) sind danach von keinem Branch mehr erreichbar; im Bild sind sie gestrichelt. Sie sind **nicht weg**: Git hebt sie noch auf und findet sie über `git reflog`, bis sie irgendwann aufgeräumt werden. Für Commits, die schon gepusht sind, darf ich nur `git revert` nehmen, denn `reset` schreibt die Geschichte um, die meine Teammitglieder schon haben. Beim nächsten Pull gäbe es Konflikte oder die Commits kämen zurück.

## Runde 4 · Verloren und gefunden

```text
git checkout v1.0~1
git commit -m "Try a log scale"
git checkout master
git reflog
```

**Vorhersage:** `v1.0~1` ist der erste Elternteil des Merge-Commits, also *Describe the data in the README*. `HEAD` zeigt dann direkt auf einen Commit, nicht auf einen Branch (*detached HEAD*). *Try a log scale* hängt an *Describe the data in the README*. Nach `git checkout master` hält ihn kein Branch mehr.

**Ergebnis:** Nach `git checkout v1.0~1` stand ich wirklich auf *Describe the data in the README* (`a213ef6`). Lokales Git hat gemeldet: *You are in 'detached HEAD' state* und *HEAD is now at a213ef6 Describe the data in the README*. (Den genauen Satz über dem Graphen im Browser-Tool habe ich nicht, weil ich das Tool nicht benutzt habe.) Nach dem Wechsel zurück auf `master` warnt Git: *you are leaving 1 commit behind, not connected to any of your branches: 5ee3ed9 Try a log scale*. Im Reflog steht er in der Zeile `5ee3ed9 HEAD@{1}: commit: Try a log scale`. Mit `git branch logscale 5ee3ed9` hängt wieder ein Branch daran, und er ist gerettet. So zeigt ihn [`git-graph.png`](git-graph.png).

## Was ich mitnehme

- Ein Fast-forward ist kein richtiger Merge, nur ein Verschieben des Branch-Zeigers.
- Ein Merge-Commit ist der einzige Commit mit zwei Eltern. `~1` folgt immer dem ersten.
- `revert` für alles, was schon gepusht ist, `reset` nur für lokale Commits.
- Nichts ist sofort weg: Mit `git reflog` finde ich auch Commits wieder, auf die kein Branch zeigt.
