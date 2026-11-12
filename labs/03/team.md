# Lab 3 · Task 7: Unsere Roadmap über Pull Requests

Stand: 12.11.2026, 21:25 Europe/Berlin, im Team-Repository [dis-bahn-wetter/bahn-wetter](https://github.com/dis-bahn-wetter/bahn-wetter).

| Was | Link |
| --- | --- |
| mein Issue | https://github.com/dis-bahn-wetter/bahn-wetter/issues/19 |
| mein Pull Request | https://github.com/dis-bahn-wetter/bahn-wetter/pull/20 (offen, noch nicht gemergt: wartet auf das Review von @paulews und @robelmihretab; `main` ist geschützt) |
| der PR, den ich reviewt habe | https://github.com/dis-bahn-wetter/bahn-wetter/pull/22 (Änderungswünsche: https://github.com/dis-bahn-wetter/bahn-wetter/pull/22#pullrequestreview-5881482890) |

`git log --oneline --graph -15` im Team-Repo (Klon von `main` auf meinem Mac, 12.11.2026):

```text
*   2fa4cf3 Merge pull request #17 from dis-bahn-wetter/feature/15-ai-usage
|\  
| * 08c8bdd Sort AI_USAGE entries by date and unify tool name
| * 6ec57ef Fill AI_USAGE.md with AI use so far
| * da92372 Add AI_USAGE.md to document AI tool use
* |   5ea7844 Merge pull request #18 from dis-bahn-wetter/feature/16-dwd-wind-temp
|\ \  
| |/  
|/|   
| * b7f50a0 Add wind and air temperature to the DWD data row (closes #16)
|/  
*   e8292a4 Merge pull request #14 from dis-bahn-wetter/feature/11-team
|\  
| * 279615d Add team members and responsibilities (closes #11)
* |   00385fb Merge pull request #13 from dis-bahn-wetter/feature/12-thema
|\ \  
| |/  
|/|   
| * 4cc97be Add topic description to README
|/  
*   89cd12b Merge pull request #10 from dis-bahn-wetter/feature/7-forschungsfragen
|\  
| * d731484 Add research questions to README
* |   f787351 Merge pull request #9 from dis-bahn-wetter/feature/8-plan
|\ \  
| |/  
|/|   
| * 946322a Add project plan until the final presentation (closes #8)
|/  
*   97738aa Merge pull request #4 from dis-bahn-wetter/feature/3-db-verspaetungen
|\
```

Zu Robels PR #22 (der neuere von zwei inhaltlich gleichen PRs) habe ich am 12.11.2026 um 21:25 Europe/Berlin ein Review mit Änderungswünschen geschrieben: die Lizenz in der Tabelle soll „Datenlizenz Deutschland Namensnennung 2.0“ heißen (so steht es im Open.NRW-Datensatz), dazu ein Link zum Datensatz, `Closes #5` in der PR-Beschreibung, und das Duplikat #21 soll geschlossen werden. Meinen eigenen PR #20 habe ich nicht gemergt; er bleibt offen, bis ein Teammitglied (aktuell angefragt: Paul und Robel) ihn freigibt. Einen Merge-Konflikt gab es bisher nicht, weil weder meine Feiertags-Zeile noch Robels Schulferien-Zeile schon auf `main` liegt — sobald einer der PRs gemergt ist, entsteht an derselben Stelle der Tabelle typischerweise ein Konflikt, den ich dann lokal löse. Als Regel haben wir uns geeinigt (und GitHub setzt sie auf `main` durch): niemand pusht direkt auf `main`; jede Änderung kommt über einen Branch und einen Pull Request, den ein Teammitglied reviewt.
