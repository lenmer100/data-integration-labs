# Lab 2 · Tasks 1–2: Meine Shell und bashcrawl

Ausgeführt auf meinem MacBook (zsh) am 12.11.2026, Zeiten in Europe/Berlin. Benutzernamen in Pfaden habe ich durch `<user>` ersetzt.

## Task 1 · Meine Shell

### Welche Shell?

```text
$ echo $0
/bin/zsh
$ zsh --version
zsh 5.9 (arm64-apple-darwin25.0)
$ echo $SHELL
/bin/zsh
```

Antwort: Es läuft **zsh 5.9** (arm64, Apple Darwin). `$SHELL` ist `/bin/zsh`. `echo $0` in einer interaktiven zsh hat `/bin/zsh` ausgegeben.

### Wo bin ich?

```text
$ cd ~ && pwd
/Users/<user>
$ cd ~/Downloads && pwd
/Users/<user>/Downloads
```

Antwort: Das Home-Verzeichnis ist `/Users/<user>`, der Downloads-Ordner liegt direkt darunter als `/Users/<user>/Downloads`.

### Woher kommen die Befehle?

```text
$ echo $PATH | tr ':' '\n'
/Users/<user>/.openclaw/bin
/Users/<user>/.npm-global/bin
/opt/homebrew/bin
/opt/homebrew/sbin
/Library/Frameworks/Python.framework/Versions/3.14/bin
/usr/local/bin
/System/Cryptexes/App/usr/bin
/usr/bin
/bin
/usr/sbin
/sbin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin
/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
/pkg/env/global/bin
$ echo $PATH | tr ':' '\n' | wc -l
15
$ which curl python3 git
/usr/bin/curl
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
/usr/bin/git
$ git --version
git version 2.50.1 (Apple Git-155)
```

Antwort: Im `PATH` stehen **15 Verzeichnisse**; zuerst wird `/Users/<user>/.openclaw/bin` durchsucht. `curl` und `git` liegen unter `/usr/bin`, `python3` in der Python-3.14-Installation unter `/Library/Frameworks`. Git 2.50.1 (Apple Git-155) ist bereits installiert.

### Wie voll ist meine Festplatte?

```text
$ df -h ~
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   187Gi    19Gi    91%    1.5M  200M    1%   /System/Volumes/Data
$ du -sh ~/Downloads
5.0G	/Users/<user>/Downloads
```

Antwort: Auf der Datensplatte sind noch **19 GiB** von 228 GiB frei (91 % belegt). Der Ordner Downloads belegt **5,0 GB**.

### Einen hängenden Prozess stoppen

Ich habe `sleep 600` in derselben Sitzung im Hintergrund gestartet (PID 21321, 19:33 Europe/Berlin) und ihn in derselben Sitzung gesucht und beendet. Ein zweites Terminal-Fenster stand in dieser entfernten Sitzung nicht zur Verfügung.

```text
$ sleep 600 &
$ ps aux | grep sleep
<user>  21321   0.1  0.0 435300272   1152   ??  SN    7:33PM   0:00.00 sleep 600
<user>  21327   0.0  0.0 435300400   1360   ??  S     7:33PM   0:00.00 grep sleep
$ kill 21321
```

Antwort: Der Prozess 21321 wurde mit `SIGTERM` beendet (exit-Status 143, also 128+15). In einem zweiten Fenster, in dem `sleep 600` im Vordergrund liefe, würde zsh typischerweise `zsh: terminated  sleep 600` anzeigen; diese Meldung habe ich hier nicht gesehen, weil der Befehl im Hintergrund lief. `ps aux | grep sleep` listet **zwei** Prozesse, weil der `grep sleep`-Prozess selbst das Wort `sleep` in seiner Befehlszeile trägt.

## bashcrawl

Inventar am Ende, direkt nach `cat end` in derselben Sitzung:

```text
$ echo $I
armour,sword,amulet,
```

(Das Komma am Ende kommt daher, dass `$I` beim ersten `export I=amulet,$I` noch leer war.)

Drei Befehle aus dem Spiel, die nicht in der Vorlesung vorkamen:

1. `alias ls='ls -F'`: legt eine Abkürzung an, sodass `ls` immer Verzeichnisse mit `/` und ausführbare Dateien mit `*` kennzeichnet.
2. `export I=sword,$I`: schreibt das Inventar in eine Umgebungsvariable, die Kindprozesse (Schatz- und Monster-Skripte) lesen können. Ebenso `export HP=15` für die Lebenspunkte.
3. `ls -a` (bzw. `cd .rift`): zeigt auch versteckte Einträge, deren Namen mit einem Punkt beginnen. So wird die versteckte Tür `.rift` sichtbar.

`ls -l` in einem Raum mit Monster (Kammer `cellar/armoury/chamber`; wegen des Alias war das wirksam `ls -F -l`):

```text
total 32
-rw-r--r--@ 1 <user>  staff   282 May 24 00:21 scroll
-rwxr-xr-x@ 1 <user>  staff  1852 May 24 00:21 spell*
-rwxr-xr-x@ 1 <user>  staff  2730 May 24 00:21 statue*
-rwxr-xr-x@ 1 <user>  staff  1288 May 24 00:21 treasure*
```

Was ein Monster von einer Schriftrolle unterscheidet: Die Schriftrolle `scroll` hat keine Ausführungsrechte (`-rw-r--r--`). Monster und andere Begegnungen (`statue`, `spell`, `treasure`) sind ausführbare Skripte (`-rwxr-xr-x` und das `*` von `ls -F`). Man startet sie mit `./statue`, eine Schriftrolle liest man mit `cat scroll`.

Das Spiellog steht in [`bashcrawl.log`](bashcrawl.log): es beginnt mit `cd bashcrawl-master/entrance` und enthält `cat end`. Den letzten Gegner (Nyarlathotep) habe ich mit Schwert, Rüstung und dem POSIX-Bonus aus der Box im ersten Kampf besiegt.
