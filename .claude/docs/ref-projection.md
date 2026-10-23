# Das Ende jedes schreibenden Laufs: prüfen, projizieren, committen

**Jeder schreibende Lauf endet gleich** (§280, Regel 4): `check-repo.py` prüft die Objekte
gegeneinander, dann projiziert der Lauf in eine Richtung, ins Sheet und in `readme.md` und
`way-of-working.md`, dann committet und pusht er. Die Projektion schreibt nur Spalten des Repos und
übernimmt nichts aus dem Sheet ([`requirements-list-contract.md`](requirements-list-contract.md),
„Die Projektion“). Arbeitsdateien liegen im Temp-Ordner des Laufs (`mktemp -d`), außerhalb des
Repos (§233). Die Schritte laufen, nachdem die Dateien des Laufs geschrieben und zurückgelesen sind,
**vor** dem Commit.

## 1. Die Objekte prüfen

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/check-repo.py .
```

Exit 0 ohne Verstoß. Je Verstoß eine Zeile `<prüfung> <Datei oder Kennung> <Satz>`, Exit 1:

- **`page_type` und `sections`** sind Befunde über den Scope, keine kaputte Datei: ein Seitentyp ohne
  Größe oder Annahme, mehr Sections als angenommen (§285). Die Projektion läuft weiter; der Bericht
  nennt jede Zeile und die offene Frage in `gaps/`, die sie klärt, oder dass sie fehlt.
- **`app_evaluation`** ist ein Befund über den Stand der Lösung, keine kaputte Datei: eine Anforderung
  mit `app` ohne belegte Evaluierung (§320), etwa während ein anderes Epic gelöst
  wird. Die Projektion läuft weiter; der Bericht nennt jede Zeile mit `solution-design` für das
  Epic der Anforderung.
- **`epic` mit „steht in keinem Epic“** ist ein Befund über den Schnitt, keine kaputte Datei: eine
  Anforderung, die nach dem Schnitt neu dazukam. Zuordnen tut nur `epic-structure`. Die
  Projektion läuft weiter; der Bericht nennt jede Zeile mit `epic-structure` als nächstem
  Lauf (§330). `epic` mit einem Epic, das es nicht gibt, bleibt ein Verstoß.
- **jede andere Prüfung an einer Datei dieses Laufs:** du berichtigst sie, legst die Berichtigung vor
  und prüfst neu;
- **jede andere Prüfung nur an fremden Dateien:** die Projektion unterbleibt in diesem Lauf, der
  Commit nimmt die Dateien des Laufs mit, und der Bericht nennt jede Zeile wörtlich mit dem Lauf, dem
  sie gehört.

## 2. Kennungen prüfen und das Sheet lesen, wenn sich eine Stelle ändert

Zuerst, ohne Sheet, in einem Befehl:

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/sync-main.py . --ids && python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/project-sheet.py . --base refs/strix/run-start --repo-only
```

`sync-main.py --ids` zieht den Stand von `main` und prüft die neuen Kennungen des Laufs (`REQ`, `GAP`,
`ADR`, Aufgaben in `todo/`) gegen ihn (§309): trägt `main` dieselbe Kennung aus einem anderen Lauf,
bekommt die Datei dieses Laufs die nächste freie Nummer, und die Verweise in den Dateien des Laufs
werden umgeschrieben. **Jede Zeile `Kennung … → …` nennt der Bericht wörtlich.** Endet es nicht mit
Exit 0, hält der Lauf vor dem Schreiben ins Sheet an und nennt die Meldung wörtlich (§308).

`project-sheet.py --repo-only` vergleicht die Spalten des Repos zwischen dem Startcommit und den
Dateien des Laufs (§311, §319). **`KEINE`:** du liest das Sheet nicht und schreibst nichts hinein, es geht mit 5
weiter, und der Bericht sagt „Sheet: keine Stelle geändert“. **`GEÄNDERT`:** weiter wie unten.

Ist `requirements_sheet` in `project.yml` leer, gibt es kein Sheet, und es geht mit 5 weiter; der
Bericht nennt `requirements-update`, der es beim ersten Lauf anlegt. Sonst liest du jeden der vier Tabs
einmal, mit seinem Namen in der Sprache aus `language` (`en`: `Requirements`, `Solutioning`, `Epics`,
`Open items`):

| Tab | Aufruf | Datei |
|---|---|---|
| `Anforderungen` | `Google_Sheets.get_values` mit `range` = `'Anforderungen'!A1:R` | `anforderungen.json` |
| `Solutioning` | `Google_Sheets.get_values` mit `range` = `'Solutioning'!A1:L` | `solutioning.json` |
| `Epics` | `Google_Sheets.get_values` mit `range` = `'Epics'!A1:P` | `epics.json` |
| `Offene Punkte` | `Google_Sheets.get_values` mit `range` = `'Offene Punkte'!A1:H` | `offene-punkte.json` |

Die Antwort von `get_values` schreibst du, wie sie kommt, als JSON in ihre Datei; legt die Sitzung
sie als Datei ab, nimmst du diese. Sie kommt als Text, nicht als Base64: am Testprojekt kam der Tab
`Anforderungen` mit 44 Zeilen und 16 Spalten vollständig zurück (gemessen am 10.10.2026).

**Ist eine Antwort gekappt**, lehnt `project-sheet.py` die Datei in 3 mit `input` ab, weil sie kein
lesbares JSON ist; fehlen ganze Zeilen, hält der Writer an der ersten neuen Zeile an, deren Kennung
schon im Sheet steht (§309). Dann liest du nur diesen Tab neu, `Anforderungen` als Export: Bei 279 Zeilen mal 11
Spalten kam ein Tab an einem früheren Lese-Weg nicht mehr in den Kontext zurück (gemessen am
25.09.2026). `Google_Drive.download_file_content` mit `fileId` = Spreadsheet-ID und
`exportMimeType: text/csv` liefert nur den ersten Tab, und der ist `Anforderungen`; die Antwort trägt
ihn als Base64 in `content`. Legt die Sitzung sie als Datei ab, dekodierst du von dort, sonst
schreibst du `content` in `anforderungen.b64`, und in 3 nennst du `anforderungen.csv` statt
`anforderungen.json`:

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/decode-export.py '<Pfad oder anforderungen.b64>' anforderungen.csv
```

## 3. Die Stellen berechnen

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/sync-main.py . --ids && python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/project-sheet.py . --tab Anforderungen=anforderungen.json --tab Solutioning=solutioning.json --tab Epics=epics.json --tab "Offene Punkte"=offene-punkte.json --base refs/strix/run-start --out changes.json
```

Der Pull steht im selben Befehl direkt davor (§308), damit ein paralleler Lauf seine eben
projizierten Zellen nicht als `ABWEICHUNG` sieht; für ihn und die Kennungen gilt dasselbe wie in 2.
Die Tab-Namen stehen in der Sprache aus `language`. `--base refs/strix/run-start` ist der
Startcommit: der Stand von `main`, auf dem der Lauf begann, den `sync-main.py` in Step 1 ohne `--ids`
gemerkt hat (§319). Nicht `HEAD`: hat der Lauf schon committet, etwa weil der Stop-Hook der
Cloud-Sitzung beim Warten auf das Ja Commit und Push verlangt, trägt `HEAD` die Werte des Laufs, und
die alten Werte im Sheet erschienen als `ABWEICHUNG`. Fehlt die Ref, endet `project-sheet.py` mit
`base` und nennt `sync-main.py` als Abhilfe für den nächsten Lauf; dann rufst du `sync-main.py` ohne `--ids` nicht neu auf, sondern nennst die Meldung wörtlich,
und die Projektion unterbleibt. Die Ausgabe nennt je Stelle `ÄNDERN`, `ABWEICHUNG`, `NEU` oder `LÖSCHEN`, am Ende
`STELLEN <n>` oder `GLEICH`. Exit 1 nennt eine Prüfung (`header`, `duplicate_id`, `input`, `value`,
`object`, `base`): die Projektion unterbleibt, und der Bericht nennt die Zeile wörtlich. Umgestellt
wird ein Sheet mit anderen Kopfzeilen von Hand; eine dabei neu angelegte Spalte formatiert
`sheet-format.py` mit `--no-banding` und `--no-protect` je Tab, der schon ein Zebra und Schutzbereiche
trägt (`requirements-update/ref-create-sheet.md`, „Ein bestehendes Sheet nachformatieren“). Ihre leeren
Zellen legt die Projektion danach als `ÄNDERN` vor, nicht als `ABWEICHUNG`.

## 4. Vorlegen und schreiben lassen

**Vorgelegt wird die Änderung im Repo, nicht die Projektion**: das Ja des Leads zu den Dateien des
Laufs gilt auch für die Stellen, die aus ihnen folgen. Du nennst die Zahl der Stellen je Tab.

**Jede `ABWEICHUNG` legst du einzeln vor**: eine Zelle des Repos, die ein Mensch im Sheet geändert hat
(§280, Regel 7). Die Projektion überschreibt sie mit dem Stand des Repos; was bleiben soll, kommt als
Material ins Repo, über `requirements-update`. Der Lead sagt je Abweichung, ob die Projektion sie
überschreibt; verneint er eine, unterbleibt die Projektion in diesem Lauf, und der Bericht nennt die
Abweichung.

Bei `GLEICH` rufst du keinen Agent. Sonst rufst du `project-sheet-writer` über das Agent-Werkzeug mit
`spreadsheet_id` und `project_folder` aus `project.yml`, `language`, `changes` = `changes.json`,
`confirmed: ja` mit dem Wortlaut des Ja und `caller` = der Name deines Skills. Nach seiner Rückmeldung
geht es mit dem nächsten Satz weiter. `FEHLER … Stand geändert` heißt: jemand hat das Sheet seit der
Lesung geändert; du liest nach 2 neu, berechnest nach 3 neu und legst die geänderten Stellen vor.
Ein anderes `FEHLER` beendet die Projektion; der Bericht nennt die Meldung wörtlich.

## 5. `readme.md` und `way-of-working.md`

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/project-readme.py .
```

Das Script schreibt beide Dateien neu und liest sie zurück (§286, §288); eine Änderung von Hand an
ihnen ersetzt es. Exit 1 nennt die Prüfung (`object`, `wow_section`, `readback`); dann bleibt die
Datei, wie sie war, und der Bericht nennt die Zeile.

## 6. Committen und pushen

Ein Commit je Lauf mit allen Dateien, die der Lauf geschrieben hat, dazu `readme.md` und
`way-of-working.md`, wenn sie sich geändert haben, direkt auf `main`, dann pushen; wird der Push
abgelehnt, holst du den Stand und pushst erneut, nie mit Force (§233). Die Nachricht beginnt mit dem
Namen des Skills.
