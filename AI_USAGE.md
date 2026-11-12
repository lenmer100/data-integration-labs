# AI_USAGE

Ich habe in diesem Repository **Grok Bot** als KI-Assistenten genutzt (Modell: von der App nicht angegeben). Der Assistent hat Dateien, Skripte und Texte erstellt, Befehle auf seinem Rechner und auf meinem MacBook ausgeführt und die Ergebnisse gegen die Quellen und GitHub getestet. Ich habe die Ergebnisse geprüft und freigegeben, bevor sie committet wurden.

| Lab | Was mit KI entstanden ist | Wie geprüft |
| --- | --- | --- |
| Lab 1 | Profil-README, README und LICENSE, `cheatsheet.md`, `open-source.md` (pandas), Feiertage-Skript, CSVs und `dataset.md` | Cheatsheet mit CommonMark und der GitHub-Markdown-API gerendert; Zahlen über die GitHub-API; Feiertage gegen drei Quellen abgeglichen (NRW 37/37/37); FC-Heimspiele wegen ODbL-Lizenz entfernt |
| Lab 2 | `shell.md` und `bashcrawl.log` (in einer zsh auf meinem MacBook ausgeführt), `journals.md`, `get_data.sh`, `get_data.txt`, `approve.md` | echte Befehlsausgaben; `get_data.sh` legt `data/raw/` und `SOURCES.txt` an; `data/raw/` ist nicht committet |
| Lab 3 | `graph.md` und `git-graph.png` (lokal mit Git nachgestellt, nicht im Browser-Visualizer), `git.md`, `countries.csv` und `conflict.md`, `history.md`, `team.md`; Issue #19, PR #20 und ein Review zu PR #22 im Team-Repo (Text vom Assistenten entworfen, von mir freigegeben) | `git log` zeigt einzelne Commits pro Schritt; keine Konfliktmarken; Commits mit noreply-Adresse; Ergebnisse live auf GitHub geprüft |

Noch selbst zu prüfen: Anker im Cheatsheet im Browser anklicken, Stichprobe der Feiertage gegen das FTG NW, `get_data.sh` in einem leeren Ordner auf dem Mac laufen lassen.
