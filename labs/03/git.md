# Lab 3 · Git auf meinem Rechner (Tasks 2–4)

Die Abschnitte *Step by step* und *Undo* stammen aus den echten Befehlen, mit denen die Dateien in `labs/03` entstanden sind (siehe `AI_USAGE.md`). Den Abschnitt *Setup* habe ich am 12.11.2026 (Europe/Berlin) nach `git clone` auf meinem MacBook ausgefüllt. Die Ausgaben von `git status` vor und nach dem ersten Push von diesem Rechner stehen am Ende von *Setup* und stammen aus genau diesem Push.

## Setup

Zuerst die fünf Einstellungen aus der Aufgabe, weil `~/.gitconfig` auf diesem Mac noch nicht existierte:

```text
$ git config --global user.name "Lennart Merschel"
$ git config --global user.email "248039784+lenmer100@users.noreply.github.com"
$ git config --global init.defaultBranch main
$ git config --global pull.rebase false
$ git config --global core.editor "code --wait"
$ git config --global --list
user.name=Lennart Merschel
user.email=248039784+lenmer100@users.noreply.github.com
init.defaultbranch=main
pull.rebase=false
core.editor=code --wait
```

`gh auth status` zeigte, dass ich bereits als `lenmer100` per HTTPS (keyring, Scope `repo`) angemeldet war. Danach der Klon:

```text
$ cd ~
$ git clone https://github.com/lenmer100/data-integration-labs.git Documents/data-integration-labs
$ cd Documents/data-integration-labs
```

```text
$ ls -a
.
..
.git
.gitignore
AI_USAGE.md
LICENSE
README.md
labs

$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

$ git remote -v
origin	https://github.com/lenmer100/data-integration-labs.git (fetch)
origin	https://github.com/lenmer100/data-integration-labs.git (push)

$ git log --oneline
59a6ad0 Record the GitHub licence API value MIT for this repository
ef57fa1 Remove FC home matches from the Feiertage data because of the ODbL licence
d19b87b Lab 3: read the history of datasets/co2-ppm (Task 6)
bd2fb93 Lab 3: document step-by-step commits and the undo commands (Tasks 3-4)
87ae13b Lab 3: document the merge conflict in countries.csv (Task 5)
6bcc26e Merge branch 'feature/new-names'
e5f0779 Add ISO numeric codes to the country table
2bbc523 Use the current short names of four countries
19a7473 Add ISO alpha-2 codes to the country table
1624312 Add country mapping table with ISO alpha-3 codes
ac84b73 Revert "Download the school holidays for 2027"
05b5024 Download the school holidays for 2027
b506d4f Say that only the script is in the repository
68dc856 Explain how to rebuild data/raw/ in labs/03
4aa39a3 Print a checksum of each download
709c282 Explain how to run the script and save its output
3593005 Keep raw downloads out of Git
c257cfd Copy the download script from lab 2
4c80b82 Lab 3: add predictions and answers for the commit graph (Task 1)
6b1ece6 Lab 2: decide which agent commands to approve (Task 5)
2362a41 Lab 2: add download script for the Feiertage raw data and its output (Task 4)
31246aa Lab 2: mine the journal articles with pipes (Task 3)
c0c376f Log where an AI assistant helped (draft to confirm)
9734c86 Expand README with links, table of labs and licence section
d3f1102 Lab 1: profile the Feiertage dataset (Tasks 5-8)
185043f Lab 1: add Feiertage script and derived tables
0addfc3 Lab 1: look inside pandas (Task 4)
f0ecf10 Lab 1: add Markdown cheat sheet (Task 3)
e32a10e Ignore virtual environments, raw data and macOS files
c7a0ce0 Add MIT licence so that others may reuse my code
abc6834 Create README with a one-sentence description
```

**Wie viele Commits, und wo sind sie entstanden?** 31 Commits, alle schon auf `origin/main`, alle mit der noreply-Adresse. Diesen Klon habe ich am 12.11.2026 zum ersten Mal auf diesem MacBook angelegt; die früheren Commits entstanden nicht in dieser Arbeitskopie, sondern wurden zuvor nach GitHub gepusht.

**Welche Messages hat GitHub geschrieben?** Typische GitHub-UI-Messages wie *Add files via upload* oder *Create README.md* kommen in diesem Log **nicht** vor. Die frühen Messages sind schon formuliert, zwei davon würde ich heute so umschreiben (nur hier, die Geschichte bleibt unverändert):

| Commit | aktuelle Message | bessere Message |
| --- | --- | --- |
| `abc6834` | Create README with a one-sentence description | Add a short README that states this repository collects the Data Integration labs. |
| `c0c376f` | Log where an AI assistant helped (draft to confirm) | Start AI_USAGE.md so later labs can record where an assistant helped. |

**Welche E-Mail tragen die Commits?**

```text
$ git log --format="%h %ae %s" | head
59a6ad0 248039784+lenmer100@users.noreply.github.com Record the GitHub licence API value MIT for this repository
ef57fa1 248039784+lenmer100@users.noreply.github.com Remove FC home matches from the Feiertage data because of the ODbL licence
d19b87b 248039784+lenmer100@users.noreply.github.com Lab 3: read the history of datasets/co2-ppm (Task 6)
bd2fb93 248039784+lenmer100@users.noreply.github.com Lab 3: document step-by-step commits and the undo commands (Tasks 3-4)
87ae13b 248039784+lenmer100@users.noreply.github.com Lab 3: document the merge conflict in countries.csv (Task 5)
6bcc26e 248039784+lenmer100@users.noreply.github.com Merge branch 'feature/new-names'
e5f0779 248039784+lenmer100@users.noreply.github.com Add ISO numeric codes to the country table
2bbc523 248039784+lenmer100@users.noreply.github.com Use the current short names of four countries
19a7473 248039784+lenmer100@users.noreply.github.com Add ISO alpha-2 codes to the country table
1624312 248039784+lenmer100@users.noreply.github.com Add country mapping table with ISO alpha-3 codes
```

Alle 31 Commits tragen `248039784+lenmer100@users.noreply.github.com`. Schritt 1 (E-Mail privat halten und Pushes blocken, die eine private Adresse veröffentlichen) sorgt dafür, dass neue Commits mit dem Profil verknüpft werden, ohne eine private Adresse zu zeigen, und dass GitHub einen Push mit einer gesperrten privaten Adresse ablehnt. Es **ändert nicht** die E-Mail-Adressen, die schon in der veröffentlichten Geschichte stehen.

**Welche Dateien habe ich am häufigsten geändert?**

```text
$ git log --name-only --format="" | sort | uniq -c | sort -rn | head
   5 labs/03/get_data.sh
   4 labs/03/countries.csv
   3 README.md
   2 labs/03/README.md
   2 labs/01/open-source.md
   2 labs/01/feiertage/run_log.txt
   2 labs/01/feiertage/kalender_koeln_2024-07-01_2027-12-31.csv
   2 labs/01/feiertage/get_feiertage.py
   2 labs/01/feiertage/events_koeln_2024-2027.csv
   2 labs/01/feiertage/README.md
```

Am häufigsten geändert: das Download-Skript in Lab 3 und die Ländertabelle, danach das README.

### Erster Commit und Push von diesem Rechner

Zuerst habe ich `labs/02/shell.md` und `labs/02/bashcrawl.log` als eigenen Commit (`7813dd7`) gepusht. Der erste Lab-3-Commit von diesem Rechner ist `6f55183` (*Lab 3: add the commit graph image and answers from a local Git replay (Task 1)*), mit `graph.md` und `git-graph.png`. `git.md`, `team.md` und `AI_USAGE.md` waren zu diesem Zeitpunkt noch nicht mit committed, deshalb erscheinen sie unten noch als uncommitted.

Vor dem Push von `6f55183`:

```text
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   AI_USAGE.md
	modified:   labs/03/git.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	labs/03/team.md

no changes added to commit (use "git add" and/or "git commit -a")

$ git push
```

Nach dem Push:

```text
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   AI_USAGE.md
	modified:   labs/03/git.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	labs/03/team.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**Ist mein Avatar neben dem Commit auf GitHub?** Ja: Der Commit `6f55183` ist über die noreply-Adresse mit dem Konto [lenmer100](https://github.com/lenmer100) verknüpft (`author.login` in der GitHub-API). Damit erscheint der Avatar des Profils neben dem Commit.

## Step by step

Erst ohne, dann mit `.gitignore` (Task 3):

```text
$ cp labs/02/get_data.sh labs/03/

$ chmod +x get_data.sh

$ git add get_data.sh

$ git commit -m "Copy the download script from lab 2"
[main c257cfd] Copy the download script from lab 2
 1 file changed, 56 insertions(+)
 create mode 100755 labs/03/get_data.sh

$ ./get_data.sh > /dev/null

$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	data/

nothing added to commit but untracked files present (use "git add" to track)

$ cat .gitignore
data/raw/

$ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore

nothing added to commit but untracked files present (use "git add" to track)

$ git status --ignored
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore

Ignored files:
  (use "git add -f <file>..." to include in what will be committed)
	data/

nothing added to commit but untracked files present (use "git add" to track)

$ git check-ignore -v data/raw/*
labs/03/.gitignore:1:data/raw/	data/raw/SOURCES.txt
labs/03/.gitignore:1:data/raw/	data/raw/schulferien_nrw.csv
labs/03/.gitignore:1:data/raw/	data/raw/wikipedia_feiertage.html

$ git add .gitignore

$ git commit -m "Keep raw downloads out of Git" -m "data/raw/ is rebuilt by get_data.sh, so only the script and this rule belong in the repository."
[main 3593005] Keep raw downloads out of Git
 1 file changed, 1 insertion(+)
 create mode 100644 labs/03/.gitignore
```

Zwei Änderungen, zwei Commits mit `git add -p`:

```text
$ ./get_data.sh | tail -n 4
== Checksum data/raw/wikipedia_feiertage.html
16d35d7879918a620acb240b3c6e85eba3d4a01c
== Checksum data/raw/schulferien_nrw.csv
6c511bec43183cb5766b1a6920b0a9b4e0194917

$ git diff
diff --git a/labs/03/get_data.sh b/labs/03/get_data.sh
index 9e8d2a6..e359cdd 100755
--- a/labs/03/get_data.sh
+++ b/labs/03/get_data.sh
@@ -2,7 +2,8 @@
 # get_data.sh: lädt die Rohdaten für mein Feiertags-Profil (Lab 1, dataset.md)
 # herunter und zeigt einen ersten Blick darauf.
 #
-# Aufruf:  ./get_data.sh          (legt data/raw/ an, falls es fehlt)
+# Aufruf:  ./get_data.sh          (im Ordner des Skripts; legt data/raw/ an, falls es fehlt)
+#          ./get_data.sh > get_data.txt   speichert den ersten Blick in einer Datei
 #
 # Quelle 1 (Hauptquelle):
 #   "Feiertag (Deutschland)", Version 271794065 vom 01.11.2026, Autor:innen der
@@ -40,6 +41,11 @@ echo "===== $out2"
 echo "== Columns";     sed -n 2p "$out2" | tr ';' '\n' | wc -l
 echo "== First lines"; head -n 3 "$out2"
 
+# Prüfsumme jeder Datei: ändert sich, sobald sich der Inhalt der Quelle ändert
+for f in "$out" "$out2"; do
+  echo "== Checksum $f"; git hash-object --no-filters "$f"
+done
+
 # Abgleich mit labs/01/dataset.md (Stand 12.11.2026):
 # - Die Wikipedia-Seite ist hier HTML (action=render). In dataset.md stehen 75.783 Bytes
 #   Wikitext, das ist die Größe des Quelltexts, nicht des gerenderten HTML. Die Zahl der

$ git add -p get_data.sh
diff --git a/labs/03/get_data.sh b/labs/03/get_data.sh
index 9e8d2a6..e359cdd 100755
--- a/labs/03/get_data.sh
+++ b/labs/03/get_data.sh
@@ -2,7 +2,8 @@
 # get_data.sh: lädt die Rohdaten für mein Feiertags-Profil (Lab 1, dataset.md)
 # herunter und zeigt einen ersten Blick darauf.
 #
-# Aufruf:  ./get_data.sh          (legt data/raw/ an, falls es fehlt)
+# Aufruf:  ./get_data.sh          (im Ordner des Skripts; legt data/raw/ an, falls es fehlt)
+#          ./get_data.sh > get_data.txt   speichert den ersten Blick in einer Datei
 #
 # Quelle 1 (Hauptquelle):
 #   "Feiertag (Deutschland)", Version 271794065 vom 01.11.2026, Autor:innen der
(1/2) Stage this hunk [y,n,q,a,d,j,J,g,/,e,p,?]? @@ -40,6 +41,11 @@ echo "===== $out2"
 echo "== Columns";     sed -n 2p "$out2" | tr ';' '\n' | wc -l
 echo "== First lines"; head -n 3 "$out2"
 
+# Prüfsumme jeder Datei: ändert sich, sobald sich der Inhalt der Quelle ändert
+for f in "$out" "$out2"; do
+  echo "== Checksum $f"; git hash-object --no-filters "$f"
+done
+
 # Abgleich mit labs/01/dataset.md (Stand 12.11.2026):
 # - Die Wikipedia-Seite ist hier HTML (action=render). In dataset.md stehen 75.783 Bytes
 #   Wikitext, das ist die Größe des Quelltexts, nicht des gerenderten HTML. Die Zahl der
(2/2) Stage this hunk [y,n,q,a,d,K,g,/,e,p,?]? 

(Antworten: y für den Kommentar, n für die Prüfsumme)

$ git diff --staged
diff --git a/labs/03/get_data.sh b/labs/03/get_data.sh
index 9e8d2a6..57e23fd 100755
--- a/labs/03/get_data.sh
+++ b/labs/03/get_data.sh
@@ -2,7 +2,8 @@
 # get_data.sh: lädt die Rohdaten für mein Feiertags-Profil (Lab 1, dataset.md)
 # herunter und zeigt einen ersten Blick darauf.
 #
-# Aufruf:  ./get_data.sh          (legt data/raw/ an, falls es fehlt)
+# Aufruf:  ./get_data.sh          (im Ordner des Skripts; legt data/raw/ an, falls es fehlt)
+#          ./get_data.sh > get_data.txt   speichert den ersten Blick in einer Datei
 #
 # Quelle 1 (Hauptquelle):
 #   "Feiertag (Deutschland)", Version 271794065 vom 01.11.2026, Autor:innen der

$ git commit -m "Explain how to run the script and save its output"
[main 709c282] Explain how to run the script and save its output
 1 file changed, 2 insertions(+), 1 deletion(-)

$ git add get_data.sh

$ git commit -m "Print a checksum of each download" -m "git hash-object changes whenever the content changes, so I can tell whether a source has changed since my last download."
[main 4aa39a3] Print a checksum of each download
 1 file changed, 5 insertions(+)
```

```text
$ git add README.md

$ git commit -m "Explain how to rebuild data/raw/ in labs/03" -m "Lists the command, both sources and their licences, so that a teammate can get the raw data without me."
[main 68dc856] Explain how to rebuild data/raw/ in labs/03
 1 file changed, 32 insertions(+)
 create mode 100644 labs/03/README.md
```

`git log --oneline -- .` und `git status --ignored` in `labs/03`:

```text
$ git log --oneline -- .
68dc856 Explain how to rebuild data/raw/ in labs/03
4aa39a3 Print a checksum of each download
709c282 Explain how to run the script and save its output
3593005 Keep raw downloads out of Git
c257cfd Copy the download script from lab 2
4c80b82 Lab 3: add predictions and answers for the commit graph (Task 1)

$ git status --ignored
On branch main
Ignored files:
  (use "git add -f <file>..." to include in what will be committed)
	data/

nothing to commit, working tree clean
```

**Warum gehört die `.gitignore` ins Repository, `data/raw/` aber nicht?** Die `.gitignore` ist eine Regel für alle, die das Repo klonen: Wer `get_data.sh` ausführt, soll die heruntergeladenen Dateien nicht aus Versehen committen. `data/raw/` dagegen kann jede:r jederzeit neu bauen. Rohdaten sind groß, ändern sich an der Quelle und haben eine eigene Lizenz, und Git ist für Text gemacht, den wir selbst schreiben. Mein Skript hatte übrigens schon die Ausführungsrechte (`create mode 100755`), weil es nicht über den Browser hochgeladen wurde. `chmod +x` hat deshalb nichts geändert.

**Was braucht ein Teammitglied für meine Rohdaten?** Nur das Repo, `curl` und eine Shell: `cd labs/03 && ./get_data.sh`. Woher die Daten kommen und unter welcher Lizenz sie stehen, steht in [`README.md`](README.md). Die Prüfsummen am Ende zeigen, ob es dieselben Dateien bekommen hat wie ich.

## Undo

### Aus Versehen gelöscht

```text
$ rm get_data.sh

$ git status
On branch main
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	deleted:    get_data.sh

no changes added to commit (use "git add" and/or "git commit -a")

$ git restore get_data.sh

$ git status && ls -l get_data.sh
On branch main
nothing to commit, working tree clean
-rwxr-xr-x 1 <user> <user> 3133 Nov 12 12:22 get_data.sh
```

`git restore` hat das Skript aus dem letzten Commit zurückgeholt. Nicht zurückholen könnte Git alles, was nie committet wurde: Dateien in `data/raw/` (ignoriert) und Änderungen, die ich seit dem letzten Commit noch nicht committet hatte.

### Aus Versehen gestaged

```text
$ echo "Ein Satz Notizen" > notes.txt

$ git add .

$ git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   notes.txt


$ git restore --staged notes.txt

$ git status && ls notes.txt
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt

nothing added to commit but untracked files present (use "git add" to track)
notes.txt

$ rm notes.txt

$ git status
On branch main
nothing to commit, working tree clean
```

`git restore --staged` nimmt die Datei nur aus der Staging Area. Sie ist danach noch da, als untracked file, und erst `rm` löscht sie.

### Tippfehler in der Message

```text
$ git diff --stat
 labs/03/README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git commit -am "Say that only the scirpt is in the repository"
[main 73fb3c4] Say that only the scirpt is in the repository
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git log --oneline -1
73fb3c4 Say that only the scirpt is in the repository

$ git commit --amend -m "Say that only the script is in the repository"
[main b506d4f] Say that only the script is in the repository
 Date: Thu Nov 12 12:22:58 2026 +0100
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git log --oneline -1
b506d4f Say that only the script is in the repository
```

Der Hash hat sich von `73fb3c4` zu `b506d4f` geändert. Ein Commit-Hash berechnet sich aus dem ganzen Commit, also auch aus der Message. Eine neue Message ergibt einen neuen Commit, der den alten ersetzt. Deshalb ist `--amend` nur sicher, bevor ich pushe: Wer den alten Commit schon hat, hätte danach eine andere Geschichte als ich.

### Ein kaputter Commit, der schon draußen ist

```text
$ git diff | grep "^[-+]url2"
-url2="https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/Schulferien/OpenData_Ferientermine.csv"
+url2="https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/Schulferien/OpenData_Ferientermine_2027.csv"

$ git commit -am "Download the school holidays for 2027"
[main 05b5024] Download the school holidays for 2027
 1 file changed, 1 insertion(+), 1 deletion(-)

$ ./get_data.sh > /dev/null; echo "exit code: $?"
curl: (22) The requested URL returned error: 404
exit code: 1

$ git revert --no-edit HEAD
[main ac84b73] Revert "Download the school holidays for 2027"
 Date: Thu Nov 12 12:23:00 2026 +0100
 1 file changed, 1 insertion(+), 1 deletion(-)

$ ./get_data.sh > /dev/null; echo "exit code: $?"
exit code: 0

$ git log --oneline -3
ac84b73 Revert "Download the school holidays for 2027"
05b5024 Download the school holidays for 2027
b506d4f Say that only the script is in the repository

$ git status
On branch main
nothing to commit, working tree clean
```

`git log --oneline -3` zeigt jetzt den kaputten Commit `05b5024` **und** darüber den Revert `ac84b73`. Die Geschichte bleibt vollständig, der Revert ist ein neuer Commit, der die Änderung umkehrt. Das ist der richtige Weg, sobald ein Commit gepusht ist, denn andere haben ihn vielleicht schon gepullt. `git reset --hard HEAD~1` würde den Commit nur bei mir löschen. Beim nächsten Push müsste ich die Geschichte mit `--force` überschreiben, und beim Pull der anderen käme er zurück. Hinweis: Weil das Repo zu diesem Zeitpunkt noch nicht auf GitHub lag, war der kaputte Commit beim Revert nur lokal. Am Ablauf ändert das nichts.

Nebenbei gelernt: Bei Wikipedia hätte dieser Test nicht funktioniert. Eine nicht vorhandene `oldid` liefert dort trotzdem HTTP 200 mit einer Fehlerseite, `curl -f` merkt davon nichts. Beim Schulministerium kommt ein echtes 404.
