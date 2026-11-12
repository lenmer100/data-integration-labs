# Lab 1 · Task 4: Ein Blick in pandas

Ich habe mir **pandas** angesehen ([pandas-dev/pandas](https://github.com/pandas-dev/pandas)), weil ich es für mein Feiertags-Skript schon benutze. Alle Zahlen habe ich am **12.11.2026** abgerufen, die meisten direkt über die GitHub-API.

## Lizenz

- Die Datei [`LICENSE`](https://github.com/pandas-dev/pandas/blob/main/LICENSE) beginnt mit **BSD 3-Clause License**. Copyright: *AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team* (2008–2011) und *Open source contributors* (2011–2026).
- Sie ist **permissiv**, nicht copyleft: Ich darf den Code nutzen, verändern und auch in Software unter einer anderen Lizenz einbauen.
- Wenn ich Code aus pandas in mein Projekt kopiere, muss ich den **Copyright-Hinweis, die drei Bedingungen und den Haftungsausschluss** mitkopieren (bei Quelltext in der Datei, bei Binärdateien in der Doku). Außerdem darf ich die Namen der Urheber nicht ohne Erlaubnis zur Werbung für mein Projekt benutzen (Klausel 3).

## Was Maschinen sehen

| Repository | `license.spdx_id` | Was das heißt |
| --- | --- | --- |
| [pandas-dev/pandas](https://api.github.com/repos/pandas-dev/pandas) | `BSD-3-Clause` | GitHub hat die `LICENSE`-Datei gelesen und eindeutig als BSD 3-Clause erkannt. |
| [owid/co2-data](https://api.github.com/repos/owid/co2-data) | `null` (das ganze Feld `license` ist `null`) | Das Repo hat keine Lizenzdatei, die Dateien sind nur `.gitignore`, `README.md`, `owid-co2-codebook.csv` und `owid-co2-data.csv`. Die Lizenz (CC BY 4.0) steht nur als Satz im [README](https://github.com/owid/co2-data#license), und den kann eine Maschine nicht lesen. |
| [lenmer100/data-integration-labs](https://api.github.com/repos/lenmer100/data-integration-labs) | `MIT` | GitHub hat die `LICENSE`-Datei gelesen und als MIT erkannt (abgerufen am 12.11.2026 nach dem Veröffentlichen). |

## Community-Dateien

Laut der API ([`/community/profile`](https://api.github.com/repos/pandas-dev/pandas/community/profile), dasselbe wie Insights → Community standards, *health percentage* 87):

| Datei | vorhanden? | wo |
| --- | --- | --- |
| README | ✓ | [`README.md`](https://github.com/pandas-dev/pandas/blob/main/README.md) |
| LICENSE | ✓ | [`LICENSE`](https://github.com/pandas-dev/pandas/blob/main/LICENSE) |
| CONTRIBUTING | ✓ | nicht im Repo selbst, sondern organisationsweit in [`pandas-dev/.github`](https://github.com/pandas-dev/.github/blob/master/CONTRIBUTING.md). Sie verweist nur auf den [Contributing Guide](https://pandas.pydata.org/docs/dev/development/contributing.html) |
| CODE_OF_CONDUCT | ✓ | ebenfalls in [`pandas-dev/.github`](https://github.com/pandas-dev/.github/blob/master/CODE_OF_CONDUCT.md) |

Dazu gibt es eine [Pull-Request-Vorlage](https://github.com/pandas-dev/pandas/blob/main/.github/PULL_REQUEST_TEMPLATE.md). Eine klassische Issue-Vorlage meldet die API nicht (`issue_template: null`), der Contributing Guide spricht aber von Issue-Formularen.

## Menschen

- **Wie viele?** Die API-Liste der Contributors mit anonymen Einträgen ([`/contributors?anon=1`](https://api.github.com/repos/pandas-dev/pandas/contributors?per_page=1&anon=1)) hat 4.393 Einträge, ohne anonyme Einträge 413. Laut GitHub-Doku werden nur die ersten 500 E-Mail-Adressen einem Account zugeordnet, der Rest erscheint anonym. Eine genaue Zahl gibt es also nicht, es sind aber einige Tausend Menschen, die je etwas beigetragen haben. Die Liste steht auch unter [Insights → Contributors](https://github.com/pandas-dev/pandas/graphs/contributors).
- **Wer entscheidet, was gemergt wird?** Laut [Governance-Seite](https://pandas.pydata.org/about/governance.html) das **Core Team**: Contributors mit Commit-Rechten, die mindestens ein Jahr lang viel beigetragen haben. Sie sind *„the primary mechanism of guiding the code review process and merging pull requests“*. Darüber steht formal ein BDFL (*Benevolent Dictator for Life*, Wes McKinney), der laut der Seite aber nur selten selbst entscheidet.

## Geld

- pandas ist ein **Sponsored Project von NumFOCUS**, einer gemeinnützigen Stiftung in den USA. NumFOCUS verwaltet die Spenden und kümmert sich um Rechtliches und Finanzen ([Sponsors](https://pandas.pydata.org/about/sponsors.html)).
- **Firmen** zahlen auf zwei Wegen: Sie stellen Leute an, die an pandas arbeiten (*Institutional Partners*, im Moment Nvidia), oder sie geben Geld (*Sponsors*: Tidelift und Bodo). Indeed hat das Logo gestaltet (*in-kind*).
- Einen Sponsor-Button gibt es ebenfalls: Die organisationsweite [`FUNDING.yml`](https://github.com/pandas-dev/.github/blob/master/FUNDING.yml) verweist auf `open_collective: pandas`.
- Daneben arbeiten viele **Freiwillige** mit, die Governance-Seite sagt ausdrücklich, dass Contributors mit jeder oder keiner Organisation verbunden sein können.

## Aktivität

| Was | Wert am 12.11.2026 | Quelle |
| --- | --- | --- |
| letztes Release | **v3.1.1** vom 04.11.2026 | [`/releases/latest`](https://github.com/pandas-dev/pandas/releases/tag/v3.1.1) |
| offene Issues | 1.633 | Suche `repo:pandas-dev/pandas is:issue is:open` |
| offene Pull Requests | 271 | Suche `repo:pandas-dev/pandas is:pr is:open` |
| `open_issues_count` der API | 1.905 | zählt Issues **und** PRs zusammen, deshalb ≈ 1.633 + 271 (die Zahlen kamen aus zwei Abfragen kurz nacheinander) |
| letzter Push | 12.11.2026 | `pushed_at` in der API |

## Mein Weg hinein

Laut [Contributing Guide](https://pandas.pydata.org/docs/dev/development/contributing.html):

1. Ein Issue suchen, das nicht `Needs Triage`, `Needs Discussion`, `Needs Info` oder `Closing Candidate` heißt und noch niemandem zugewiesen ist.
2. Mit dem Kommentar `/take` übernehmen, dann weist ein Bot es mir zu (höchstens zwei gleichzeitig).
3. pandas forken, klonen, `upstream` hinzufügen und einen Feature-Branch anlegen.
4. Änderung mit Tests committen, auf den eigenen Fork pushen und einen Pull Request mit Präfix im Titel (`BUG:`, `DOC:`, `ENH:` …) und `closes #1234` öffnen.
5. Ein Core-Team-Mitglied reviewt. Wer 14 Tage nicht auf ein Review reagiert, bekommt das Label `Stale`, nach weiteren 7 Tagen wird der PR geschlossen.

**Good first issue?** Nein. Ein Label `good first issue` gibt es in pandas nicht (die API antwortet auf `/labels/good%20first%20issue` mit `Not Found`, und die Suche nach offenen Issues mit diesem Label findet 0). Der Guide verweist stattdessen auf einen Text mit dem Titel *Don't start with good first issues*.

Interessant für den Kurs: Der Guide hat einen Abschnitt *Automated contributions policy*. KI-Werkzeuge sind erlaubt, man muss aber angeben, welches Werkzeug und Modell man benutzt hat, das Ergebnis selbst prüfen und darf in Diskussionen nicht die KI für sich sprechen lassen. Das ist ziemlich genau die Regel mit `AI_USAGE.md` aus diesem Kurs.
