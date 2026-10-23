# In die Anforderungsliste schreiben: die Befehle

Geschrieben wird die Projektion des Repos (`requirements-list-contract.md`, „Die Projektion“): nur
Spalten, deren Eigentümer das Repo ist, und nur, was in `changes` steht.

Alle Aufrufe gehen über die Google-Connectoren von claude.ai, `Google_Drive` und `Google_Sheets`. Der
volle Name eines Werkzeugs trägt ein Präfix des Servers; du findest es über die Werkzeug-Suche und
vergleichst die Endung. Das Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt.
Stehen die Werkzeuge nicht in der Werkzeugliste, suchst du sie erst über die Werkzeug-Suche; findet
auch die eines nicht, endest du mit `FEHLER` „Der Google-Connector ‹Drive/Sheets› ist in dieser
Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden."

## Die Kette schließen

Dein erster Aufruf liest die Elternkette des Sheets: `Google_Drive.get_file_metadata` mit `fileId` =
`spreadsheet_id`; die Antwort trägt `parentId` und `title`. Dann dasselbe auf ihren `parentId`, bis du
beim Projektordner (`project_folder`) bist. Führt die Kette nicht dorthin, endest du mit `FEHLER` „das Sheet liegt nicht im
Projektordner".

## Lesen

| Zweck | Aufruf |
|---|---|
| Tab-Namen | `Google_Sheets.get_spreadsheet` mit `spreadsheetId` und `fields: ["sheets.properties.title"]` |
| Kopfzeile eines Tabs | `Google_Sheets.get_values` mit `range` = `'‹Tab›'!1:1` |
| der Tab vor dem Schreiben | `get_values`, ein Aufruf je Tab aus `changes`, mit `range` = `'‹Tab›'!A1:‹letzte Spalte›` (§280, Regel 7: eine Lesung je Tab) |
| Rücklauf | dieselben Aufrufe wie vor dem Schreiben |

`get_values` liest einen Bereich je Aufruf; mehrere Bereiche sind mehrere Aufrufe. Die Antwort trägt
`values` als Liste von Zeilen. Darin fehlen leere Zellen am Zeilenende; eine Zeile kann also
weniger Werte haben als Spalten, und eine fehlende Zelle ist `leer`. Die Zeilennummer im Sheet ist die
Stelle in `values` plus eins, weil die Kopfzeile Zeile 1 ist. Aus der einen Lesung je Tab nimmst du
jede Stelle, die ID ihrer Zeile, die letzte belegte Zeile und die Dubletten; einzelne Zellen liest du
nicht nach.

## Die Kopfzeilen prüfen

Die gelesenen Kopfzeilen schreibst du je Tab als eine Zeile CSV in eine Datei im Temp-Ordner des Laufs (`mktemp -d`, außerhalb des Repos) und prüfst
sie mit dem Script des Repos, je Tab mit seinem Namen im Sheet und mit `language` aus `project.yml`:

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/check-sheet.py --check header --language de --header Anforderungen kopf-anforderungen.csv --header Solutioning kopf-solutioning.csv
```

Bei `language: en` heißen die Tabs anders, etwa `--language en --header Requirements kopf-anforderungen.csv`;
die Namen je Sprache stehen in `requirements-list-contract.md`.

Nur die Tabs, die `changes` anfasst. Exit 0 ohne Befund, 1 mit einer Zeile `header …` je Befund; bei 1
schreibst du in den Tab nichts und nennst die Zeile wörtlich.

## Vor dem Schreiben prüfen

- **Keine Spalte der Menschen und keine Formel.** Liegt eine Stelle in einer Spalte, deren
  Eigentümer die Menschen sind oder die eine Formel trägt (der Vertrag, je Tab), schreibst du keine
  Zeile des Auftrags.
- **`heute` gegen das Gelesene**, Zeichen für Zeichen, nach Entfernen von Leerzeichen am Zellenende.
- **Die Kennung der Zeile** gegen die Kennung in `Stelle`: `ID`, `Epic-ID` oder `GAP-ID`, in `en`
  `ID`, `Epic ID` oder `GAP ID`.
- **Neue Zeilen:** die erste liegt auf der Zeile nach der letzten belegten der Spalte der Kennung,
  die weiteren direkt darunter, und keine ihrer Kennungen steht schon in dieser Spalte.

## Schreiben

Alles mit `Google_Sheets.update_values` (`range`, `values`), ein Bereich je Aufruf.

| Was | Bereich | `values` |
|---|---|---|
| eine Zelle | `'‹Tab›'!‹Spalte›‹r›` | `[[‹neu›]]` |
| benachbarte Zellen einer Zeile | `'‹Tab›'!‹Spalte›‹r›:‹Spalte›‹r›` | `[[‹neu›, ‹neu›, …]]` |
| benachbarte Zellen einer Spalte | `'‹Tab›'!‹Spalte›‹r›:‹Spalte›‹s›` | `[[‹neu›], [‹neu›], …]` |
| neue Zeilen | `'‹Tab›'!‹erste Spalte›‹n›:‹letzte Spalte›‹m›` | eine Zeile je Kennung, die Spalten in der Reihenfolge der Kopfzeile |

**Benachbarte Zellen gehen in einen Aufruf.** Liegen Stellen in derselben Zeile in Spalten ohne
Lücke nebeneinander, oder in derselben Spalte in Zeilen ohne Lücke untereinander, schreibst du sie
als einen Bereich. Im Bereich liegt nur, was eine Stelle aus `changes` ist: eine Zelle dazwischen,
die keine Stelle ist, trennt ihn, auch wenn ihr Wert gleich bliebe. Jede Zelle gehört zu genau einem
Aufruf; nimm je Zeile die Läufe nebeneinander, die übrigen Zellen je Spalte untereinander. In der
Probe am 10.10.2026 kosteten 56 Stellen 54 Aufrufe und rund 8 Minuten, weil jede Zelle einzeln ging.

Die neuen Zeilen eines Tabs gehen **je Bereich aus `changes` in einen** Aufruf, nicht Zeile für Zeile.
Nennt `changes` für dieselben Zeilen zwei Bereiche, etwa
`A:D` und `H:L` neuer Anforderungen, weil die Spalten dazwischen den Menschen gehören, sind es zwei Aufrufe;
die Lücke füllst du nicht. `Google_Sheets.append_values` benutzt du nicht: es schreibt nicht in einen
genannten Bereich, sondern „after the last row of the table", also an eine Zeile, die das Werkzeug
bestimmt und nicht die bestätigte `Stelle`, und zwei Bereiche derselben Zeilen trifft es nicht. Dass
es auf `'‹Tab›'!A1` unter die zuletzt belegte Zeile hängt, ist gemessen (04.10.2026); dass diese Zeile
immer die aus `Stelle` ist, nicht.

**`update_values` deutet Eingaben wie getippt**: `=…` und `+…` werden Formeln (`+49 170 …` zeigt
`#ERROR!`), `0042` wird `42`, `03.10.2026` wird ein Datumswert. **Deshalb geht jeder nicht leere Wert
mit einem führenden Hochkomma** in `values` (`'0042`); das Sheet hält ihn als Text, und `get_values`
liefert ihn ohne Hochkomma zurück (gemessen am 04.10.2026). Verglichen wird im Rücklauf mit `neu`
ohne Hochkomma.

**Eine Zelle leeren** (`neu` leer, etwa wenn die letzte offene Frage einer Zeile geschlossen ist):
`update_values` auf die Zelle mit `[[""]]`, ohne Hochkomma. Ungemessen ist, ob der Connector einen
leeren Wert als Leeren der Zelle annimmt; gemessen wird es in der ersten Probe.

**Eine Zeile löschen**, nur im Tab `Offene Punkte` und nur für eine Stelle `Zeile ‹n› (GAP-…,
löschen)`: die `sheetId` des Tabs aus `Google_Sheets.get_spreadsheet` mit `fields:
["sheets.properties"]`, dann ein Aufruf `Google_Sheets.update_spreadsheet` mit
`{"deleteDimension": {"range": {"sheetId": ‹id›, "dimension": "ROWS", "startIndex": ‹n-1›,
"endIndex": ‹n›}}}`. Die Felder der Menschen derselben Zeile fallen mit ihr. Gelöscht wird nach allen
anderen Stellen und von unten nach oben, damit die Zeilennummern der übrigen Stellen stimmen; vorher
liest du die Zeile und prüfst, dass in Spalte A die Kennung aus `Stelle` steht. Dass
`update_spreadsheet` Anfragen für Format, Fixierung und Zebra annimmt, ist gemessen (§247); dass es
`deleteDimension` annimmt, nicht: gemessen wird es in der ersten Probe.

## Zurücklesen

Dieselben `get_values` wie vor dem Schreiben, ein Aufruf je Tab. Du vergleichst jede Stelle mit
`neu`. Dass keine ID doppelt steht, prüfst du im Tab `Anforderungen` an der Spalte
`ID`, als TSV mit der Kopfzeile `ID`:

```
python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/check-sheet.py ids.tsv --check duplicate_id
```

## Was kein Befehl dieses Agents ist

Ein Sheet anlegen, einen Tab anlegen oder umbenennen, eine Zeile außerhalb von `Offene Punkte`
löschen, Zellen formatieren, ein anderes Sheet beschreiben: das gehört `requirements-update` oder dem Menschen, nicht dem Writer.
