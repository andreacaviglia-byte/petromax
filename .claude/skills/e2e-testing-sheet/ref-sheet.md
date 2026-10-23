# Das E2E-Sheet, die Quellen und der Steckbrief: die Aufrufe dieses Laufs

Alle Aufrufe auf Drive und Sheets gehen über die Google-Connectoren `Google_Drive` und
`Google_Sheets`. Das Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt. Meldet
ein Aufruf ein Limit, wartest du eine Minute und wiederholst denselben Aufruf, ungeteilt.

## Die Sprache des Sheets

**Das E2E-Sheet steht in der Sprache aus `language` in `project.yml`** (§337): Tabs, Kopfzeile, Werte
der Dropdowns, der Wert für alle Shops, die Texte der Übersicht, der Schutztext, die Form des Datums in
`Getestet am` und das Präfix im Ablauf, alles aus dieser Tabelle. Sie ist wörtlich die in
`check-e2e.py`, das dagegen prüft; `sheet-format.py` liest dieselbe. Die deutschen Formen bleiben in
1.x, wie sie sind. Die Formeln der Übersicht sind in beiden Sprachen dieselben, mit dem Tab und den
Statuswerten der Sprache; die Funktionsnamen bleiben englisch. Ein Sheet in der einen Sprache wird nie
in die andere umgeschrieben: weicht `language` von der Kopfzeile eines bestehenden Sheets ab, lehnt
das Script mit `header` ab, und du hältst an und nennst beide.

| Art | Schlüssel | de | en |
|---|---|---|---|
| Tab | `testcases` | `Testfälle` | `Test cases` |
| Tab | `overview` | `Übersicht` | `Overview` |
| Spalte | `id` | `ID` | `ID` |
| Spalte | `testcase` | `Testfall` | `Test case` |
| Spalte | `shop` | `Shop` | `Shop` |
| Spalte | `role` | `Rolle` | `Role` |
| Spalte | `steps` | `Ablauf` | `Steps` |
| Spalte | `expected` | `Erwartetes Ergebnis` | `Expected result` |
| Spalte | `status` | `Status` | `Status` |
| Spalte | `round` | `Runde` | `Round` |
| Spalte | `result` | `Ist-Ergebnis / Beobachtung` | `Actual result / observation` |
| Spalte | `severity` | `Schweregrad` | `Severity` |
| Spalte | `tested_by` | `Getestet von` | `Tested by` |
| Spalte | `tested_on` | `Getestet am` | `Tested on` |
| Status | `open` | `Offen` | `Open` |
| Status | `passed` | `Bestanden` | `Passed` |
| Status | `failed` | `Fehlgeschlagen` | `Failed` |
| Status | `blocked` | `Blockiert` | `Blocked` |
| Status | `retest` | `Erneut testen` | `Retest` |
| Status | `not_applicable` | `Nicht anwendbar` | `Not applicable` |
| Schweregrad | `blocker` | `Blocker` | `Blocker` |
| Schweregrad | `high` | `Hoch` | `High` |
| Schweregrad | `medium` | `Mittel` | `Medium` |
| Schweregrad | `low` | `Niedrig` | `Low` |
| Shop | `all_shops` | `alle` | `all` |
| Text | `metric` | `Kennzahl` | `Metric` |
| Text | `value` | `Wert` | `Value` |
| Text | `total` | `Testfälle gesamt` | `Total test cases` |
| Text | `progress` | `Fortschritt (nicht Offen / gesamt)` | `Progress (not Open / total)` |
| Text | `pass_rate` | `Bestanden-Quote (ohne Nicht anwendbar)` | `Pass rate (excluding Not applicable)` |
| Text | `open_blockers` | `Offene Blocker (Fehlgeschlagen und Blocker)` | `Open blockers (Failed and Blocker)` |
| Text | `round_count` | `Testfälle` | `Test cases` |
| Text | `protection` | `Geschrieben vom E2E-Testlauf; Änderungen von Hand ersetzt der nächste Lauf` | `Written by the E2E test run; the next run replaces manual changes` |
| Text | `date_form` | `11.10.2026` | `11 Oct 2026` |
| Text | `precondition` | `Voraussetzung:` | `Precondition:` |

Unten stehen die Formen in `de`; in einem Projekt mit `en` gilt je Eintrag die Spalte `en`, auch in
den Bereichen der Aufrufe (`'Test cases'!A1:L1`).

## Die Spalten, wörtlich

Zwei Tabs (§256): `Testfälle` an erster Stelle, `Übersicht` an zweiter. Kopfzeile von `Testfälle`
in `'Testfälle'!A1:L1`:

| Spalte | Kopf | Wer schreibt | Werte |
|---|---|---|---|
| A | `ID` | dieser Lauf | `E2E-001`, `E2E-002` …; ein neuer Test bekommt die Nummer über der höchsten im Bestand, ein ersetzter behält seine, keine wird wiederverwendet |
| B | `Testfall` | dieser Lauf; der Text ist der Schlüssel | |
| C | `Shop` | dieser Lauf | Dropdown: mit einem Shop dessen `key`, mit mehreren jeder `key` aus `shops` und `alle` |
| D | `Rolle` | dieser Lauf | wer den Prozess durchläuft |
| E | `Ablauf` | dieser Lauf | |
| F | `Erwartetes Ergebnis` | dieser Lauf | |
| G | `Status` | wer testet | Dropdown: `Offen`, `Bestanden`, `Fehlgeschlagen`, `Blockiert`, `Erneut testen`, `Nicht anwendbar`; leer zählt als `Offen` |
| H | `Runde` | wer testet | Dropdown: `1` bis `5` |
| I | `Ist-Ergebnis / Beobachtung` | wer testet | |
| J | `Schweregrad` | wer testet | Dropdown: `Blocker` (verhindert den Go-Live), `Hoch`, `Mittel`, `Niedrig` |
| K | `Getestet von` | wer testet | |
| L | `Getestet am` | wer testet | ein Datum als Text, `TT.MM.JJJJ` (`11.10.2026`), bei `en` wie `11 Oct 2026` (§337); die Spalte ist als Text formatiert, ohne Datumsprüfung |

Keine weitere Spalte, keine Kennung einer Anforderung oder eines Epics, keine Ticket-Spalte, keine
Beispielzeile (§159). **Dieser Lauf schreibt nur A bis F**, aus `tests/`; G bis L sind Felder der
Menschen, die nur hier stehen und die kein Lauf schreibt (§280, Regel 5). Es gibt
einen Status je Testfall, und der letzte gilt; `Runde` sagt, im wievielten Durchlauf er gesetzt
wurde. Den Verlauf trägt das Repo, wenn Ergebnisse über `requirements-update` als Material
eingehen. Die Listen der Dropdowns stehen in `check-e2e.py` (`STATUS_VALUES`, `ROUNDS`,
`SEVERITY_VALUES`, `shop_values`), und `sheet-format.py` liest sie dort.

## Die Fassung des Entwurfs

Die Anforderungen und Epics liest du im Repo ([ref-testcase.md](ref-testcase.md), Quellen); aus dem
Drive brauchst du je Epic nur die Fassung seines Entwurfs, für `sources` in `tests/‹ID›.md`.

| Zweck | Aufruf |
|---|---|
| Fassung des Entwurfs | `Google_Drive.get_file_metadata` mit `fileId` = die ID aus dem Link in `draft` der Epic-Datei, vorher auf seine Eltern bis zum Projektordner. Eine Fassungsnummer liefert keiner der Google-Connectoren: die Antwort trägt kein Feld `version`, und das Werkzeug kennt keine Auswahl der Felder (gemessen am 04.10.2026). Als Fassung schreibst du deshalb `modifiedTime` aus dieser Antwort, wörtlich |

Den Inhalt des Entwurfs liest du nicht: er ist die Projektion der Epic-Datei (§302), und was der Kunde
dort kommentiert, ist Material für `solution-design`. **Scheitert der Aufruf zweimal gleich**, hältst
du an und nennst Aufruf und Meldung wörtlich: ohne Fassung trägt der Test keine Quelle.

## Den Bestand lesen

| Zweck | Aufruf |
|---|---|
| Tab-Namen | `Google_Sheets.get_spreadsheet` mit `spreadsheetId` = `e2e_sheet` und `fields: ["sheets.properties.title"]` |
| der ganze Tab `Testfälle` | `Google_Drive.download_file_content` mit `fileId` = `e2e_sheet` und `exportMimeType: text/csv`; auf die Platte wie unten, in `testcases.csv` |
| ein Rest im Ordner | erst der Unterordner `Testing` nach dem Datalayer-Vertrag (Die Ablage im Drive), ohne ihn anzulegen; dann `Google_Drive.search_files` mit `query: "parentId = '‹Testing›' and mimeType = 'application/vnd.google-apps.spreadsheet'"` und `excludeContentSnippets: true`, jede Seite über `pageToken`, bis keine mehr kommt; den Namen aus `doc-name.py . e2e` (Anlegen) vergleichst du in der Antwort. Den Papierkorb schließt diese Suche nicht aus: `search_files` kennt keinen Term dafür, und `get_file_metadata` trägt kein Feld `trashed` (gemessen am 04.10.2026); ob ein Treffer im Papierkorb erscheint, ist ungemessen. Ein Treffer gilt darum erst als Rest, wenn der Lead ihn bestätigt |

**Auf die Platte:** die Antwort von `download_file_content` trägt den Tab als Base64 in `content`. Ist
sie groß, legt die Sitzung sie als Datei ab und nennt den Pfad; dann
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py '<Pfad aus der Antwort>' testcases.csv` im Temp-Ordner des Laufs. Kommt
sie direkt in der Antwort, schreibst du den Wert von `content` in `testcases.b64` im Temp-Ordner und
dekodierst ebenso mit `python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py testcases.b64 testcases.csv`.

**Der CSV-Export liefert nur den ersten Tab.** Steht `Testfälle` dort nicht an erster Stelle, liest du
mit `get_values` und `range` = `'Testfälle'!A1:L` und schreibst die Zeilen als CSV in
`testcases.csv`. Fehlt der Tab `Testfälle`, hältst du an; du legst in einem bestehenden Sheet keinen
an. `Getestet am` ist Text und kommt im Export, wie er dasteht. Hat ein Wert nicht die Form der Sprache,
meldet das Script `DATUM ‹n› | ‹Wert›`: ein Hinweis, den der Bericht nennt; du schreibst das Feld nie.
Bei `en` heißt der Tab `Test cases`, der Bereich `'Test cases'!A1:L`.

## Abgleich

`plan.json` ist eine JSON-Liste, je Test `{"testcase": …, "shop": …, "role": …, "steps": …,
"expected": …, "requirements": […], "sources": […]}`, in der Form, die `ref-testcase.md` beschreibt;
eine `ID` trägt der Plan nicht, sie vergibt das Script. `requirements` und `sources` gehen nie ins
Sheet, nur in `tests/E2E-NNN.md` (Zuordnung, unten). `--shops` nennt die `key` aus `shops` in
`project.yml`, durch Komma getrennt, in ihrer Folge:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-e2e.py testcases.csv --plan plan.json --shops <key>,<key> --out update.json --language <language>
```

`--language` ist `language` aus `project.yml`; trägt Zeile 1 die Kopfzeile der anderen Sprache, meldet
das Script `header`.

| Zeile | heißt |
|---|---|
| `NEU E2E-‹n› \| ‹Testfall›` | kein Testfall mit diesem Text; wird mit dieser ID unten angehängt |
| `GLEICH <n> \| ‹Testfall›` | derselbe Text, `Shop`, `Rolle`, `Ablauf` und `Erwartetes Ergebnis` gleich; wird nicht geschrieben |
| `ERSETZT <n> \| ‹Testfall›` | derselbe Text, eines der vier Felder anders; in seiner Zeile ersetzt, die ID bleibt |
| `ERGEBNIS <n> \| ‹Testfall› \| ‹Status› \| ‹Ist-Ergebnis›` | eine zu ersetzende Zeile trägt schon einen Status außer `Offen` oder ein Ist-Ergebnis; du fragst für genau diese |
| `NICHT-MEHR <n> \| ‹Testfall›` | im Bestand, nicht im Plan; bleibt stehen |
| `SCHREIBEN \| ‹Bereich› \| ‹n› Zeile(n)` | der eine Aufruf, den `update.json` trägt |

`<n>` ist die Zeilennummer im Sheet. Ohne `--plan` listet das Script nur den Bestand, je Zeile
Nummer, ID, Testfall und Status. Die Prüfungen mit Exit 1: `header`, `duplicate_key` (Bestand oder
Plan), `duplicate_id` (Bestand), `forbidden_id` und `empty_field` (Plan, alle fünf Felder),
`shop_unknown` (ein `shop` außerhalb der erlaubten Werte), mit `--tests` dazu `test_file_field` und
`test_file_not_back` (Zuordnung, unten).

## Zuordnung

**Der Test steht je Test in `tests/E2E-NNN.md` im Datalayer** (§280): A bis F im Rumpf, dazu im
Kopf, welche Anforderungen er verkettet und aus welcher Quelle er stammt, was nie ins Sheet geht.
Status, Runde und Ergebnisse stehen nur im Sheet. Die Datei schreibt nur das Script, aus dem
Rücklauf in Step 9:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-e2e.py testcases.csv --plan plan.json --shops <key>,<key> --tests tests --language <language>
```

`testcases.csv` ist dabei der Export direkt nach dem Schreiben. Das Script schreibt erst, wenn jeder
geplante Test `GLEICH` meldet und im Sheet eine ID trägt; sonst lehnt es mit `test_file_not_back` ab und
lässt den Ordner, wie er ist. Je geplanten Test schreibt oder ersetzt es `tests/‹ID›.md`, Form im
Datalayer-Vertrag; die Datei eines Tests, den der Plan nicht trägt, etwa weil der Lead nur einzelne
Epics nennt, bleibt unberührt. Es liest die Dateien zurück und meldet `TESTS | tests | ‹n› Datei(en)
geschrieben, ‹m› Datei(en) anderer Tests unberührt`. Ohne `--tests` schreibt es nichts in den Datalayer.

## Anlegen

Name: `E2E-Tests ‹title› – ‹Kunde›` (§263), bei `en` `E2E tests ‹title› – ‹Kunde›` (§337), ohne
Datum. Du bildest ihn nicht selbst: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/doc-name.py . e2e` gibt ihn aus `project.yml` aus;
Exit 1 nennt das leere Feld, und dann entsteht kein Sheet. Ein bestehendes Sheet findet der Lauf über
`e2e_sheet`, nie über den Namen. Erst suchen (oben, Rest im Ordner), dann:

1. Den Unterordner `Testing` findest oder legst du an, nach dem Datalayer-Vertrag (Die Ablage im
   Drive), direkt vor dem Sheet (§231).
2. `Google_Drive.create_file` mit `title` = der Name, `parentId` = die ID von `Testing` und
   `contentMimeType: application/vnd.google-apps.spreadsheet`, immer mit `parentId`. Aus der Antwort
   nimmst du die ID der Datei; sie ist die Spreadsheet-ID.
3. `Google_Sheets.update_spreadsheet` mit `spreadsheetId` und `requests` =
   `[{updateSheetProperties: {properties: {sheetId: 0, title: "Testfälle"}, fields: "title"}},
   {addSheet: {properties: {sheetId: 1, title: "Übersicht", index: 1}}}]`, bei `en` mit `Test cases`
   und `Overview`.
4. `get_spreadsheet` mit `fields: ["sheets.properties.title", "properties.locale"]`: genau
   `Testfälle` und `Übersicht` (`Test cases`, `Overview`), in dieser Folge. Weicht es ab, bleibt `e2e_sheet` leer, und der
   Bericht nennt Link und gelesene Namen. **Erst nach diesem Zurücklesen schreibst du**: ein
   Schreibaufruf, der parallel zur Umbenennung abging, traf den alten Tab-Namen und scheiterte
   (gemessen am 04.10.2026). `locale` brauchst du in Schritt 8.
5. `Google_Sheets.update_values` mit `range` = `'Testfälle'!A1:L1` und `values` = eine Zeile mit den
   zwölf Köpfen der Sprache, jeder mit führendem Hochkomma (siehe Schreiben).
6. **Formatieren:** `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sheet-format.py --sheet Testfälle=0
   --sheet Übersicht=1 --shops <key>,<key>` (bei `en` `--sheet "Test cases=0" --sheet Overview=1`)
   gibt die `requests` in der Sprache der Tabs aus; du gibst sie unverändert an
   **einen** Aufruf von `Google_Sheets.update_spreadsheet`. Scheitert eine Anfrage, gilt keine.
   Exit 1 heißt: Script und Kopfzeile weichen ab; dann formatierst du nicht und nennst die Zeile.
   Was der Aufruf setzt:
   - Poppins, Umbruch, Breiten; Kopf A–F in Strix-Gelb, G–L heller, damit sichtbar ist, wer welche
     Spalten schreibt; fixiert Zeile 1 und Spalten A–B.
   - Zebra ab Zeile 2, ohne Kopffarbe: **die Farbe eines Zebras überdeckt die Füllung der Zelle**;
     ein Zebra mit Kopffarbe färbte G1 gelb statt heller (gemessen am 05.10.2026).
   - Dropdowns (`setDataValidation`, `ONE_OF_LIST`, `showCustomUi`, `strict`) ab Zeile 2, dazu
     `Getestet am` als Text (§337): ein Datumswert zeigte den Monat im Gebietsschema des Sheets,
     darum keine Datumsprüfung; zurückgelesen tragen die Zellen `customUiMode: ARROW` (gemessen am
     05.10.2026).
   - Bedingte Formate: Statuszelle grün, rot, orange, blau, grau je Wert; Zeile grauer Text bei
     `Nicht anwendbar`; Zeile hellrot bei `Fehlgeschlagen` und `Blocker`. **Je Zelle greift nur die
     erste passende Regel**: die Statuszelle einer roten Zeile bleibt rot, die einer grauen Zeile
     grau hinterlegt, aber ohne grauen Text (gemessen am 05.10.2026). **Die Formel einer Regel
     deutet das Sheet in seinem Gebietsschema**: `=AND($G2="…",$J2="…")` lehnt ein Sheet in `de_DE`
     mit `Invalid ConditionValue.userEnteredValue` ab, und dann gilt kein Request des Aufrufs; das
     Script schreibt die Regeln darum ohne Funktion und ohne Trenner (gemessen am 05.10.2026).
   - Ein Schutz auf A–F ab Zeile 2 mit `warningOnly`: Menschen sehen eine Warnung, `update_values`
     dieses Laufs schreibt ohne Hindernis hinein (gemessen am 05.10.2026).
   - In `Übersicht` Grundformat, die drei Köpfe gelb, Prozent in Fortschritt und Quote.

   Zebra, Regeln und Dropdowns enden an der letzten Zeile des Rasters, nicht am Ende des Tabs: ein
   neues Sheet hat 1000 Zeilen, und die Antwort trägt `endRowIndex: 1000` (gemessen am 05.10.2026).
7. **Formatierung zurücklesen:** `get_spreadsheet` mit `ranges` = `'Testfälle'!1:2` und `fields` =
   `["sheets.properties.gridProperties","sheets.data.columnMetadata.pixelSize","sheets.bandedRanges.bandedRangeId","sheets.conditionalFormats.booleanRule.condition","sheets.protectedRanges.protectedRangeId","sheets.data.rowData.values.dataValidation"]`.
   `frozenRowCount` 1 und `frozenColumnCount` 2; die `pixelSize` der Spalten sind die aus den
   `updateDimensionProperties` der Ausgabe, in derselben Folge; ein Zebra, sieben Regeln, ein Schutz;
   Zeile 2 trägt in C, G, H und J eine Validierung.
8. **Übersicht füllen:** `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sheet-format.py
   --overview-values --shops <key>,<key> --separator <Trenner> --language <language>` gibt `{"range": …, "values": …}` aus;
   du schreibst es mit **einem** Aufruf von `update_values`. Der Trenner folgt `locale` aus Schritt
   4: **`update_values` deutet eine Formel im Gebietsschema des Sheets**; in `de_DE` wird jede
   Formel mit Komma `#ERROR!` („Formula parse error.“), mit Semikolon rechnet sie, und die
   Funktionsnamen bleiben englisch (gemessen am 05.10.2026; ein neues Sheet dieses Kontos kam mit
   `de_DE`). `;` gilt für `de_DE`; für ein anderes Gebietsschema nimmst du `,` bei `en_*`, sonst
   `;`, und die Rücklesung entscheidet.
9. **Übersicht zurücklesen:** `get_values` mit dem `range` aus Schritt 8. Kein Wert ist `#ERROR!`;
   mit leerem Bestand zählt jede Formel 0 und Fortschritt und Quote stehen auf `0%`. Ein `#ERROR!`
   heißt falscher Trenner: Schritt 8 mit dem anderen, einmal; trägt auch er `#ERROR!`, nennt der
   Bericht beide Rücklesungen.

Die Formeln zählen über offene Bereiche (`'Testfälle'!G2:G`), damit neue Zeilen mitzählen; nur Zeilen
mit Text in `Testfall` zählen, ein leerer Status als `Offen`. Fortschritt ist „nicht Offen /
gesamt“, die Bestanden-Quote „Bestanden / (gesamt − Nicht anwendbar)“, offene Blocker sind Zeilen
mit `Fehlgeschlagen` und `Blocker`. Die Runde zählt eine `1` als Zahl und als Text gleich (gemessen am
05.10.2026).

**Scheitert das Formatieren oder die Übersicht, bleibt das Sheet gültig:** der Bericht nennt Aufruf
und Meldung wörtlich, und der Lauf geht weiter.

## Steckbrief: die Felder dieses Laufs

| Schritt | Weg |
|---|---|
| direkt davor lesen | lies `project.yml` |
| überschreiben und zurücklesen | überschreib `project.yml` ganz, mit dem ganzen Text; dann lies sie zurück |

Im gelesenen Text änderst du **nur die Zeilen der Felder, die dieser Lauf einträgt** (§229): den Wert
von `e2e_sheet:`, in Anführungszeichen (`e2e_sheet: "<Spreadsheet-ID>"`); `language:` und `title:`, wenn sie leer waren. Alles andere, auch Kommentare und
Reihenfolge, bleibt Zeichen für Zeichen. Nach dem Zurücklesen:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Erst zurückgelesen, gleich und ohne Verstoß heißt „eingetragen"; einen Verstoß nennst du wörtlich.

## Schreiben

`update_values` mit `range` und `values` aus `update.json`, **ein Aufruf für den Tab**. `update.json` entsteht aus dem Export direkt davor, nie aus einem früheren;
ist `range` `null`, gibt es nichts zu schreiben. **`update_values` deutet Eingaben wie getippt**:
`=…` und `+…` werden Formeln, `0042` wird `42`, ein Datum wird eine Zahl; ein führendes Hochkomma hält
den Wert als Text, und `get_values` liefert ihn ohne Hochkomma zurück (gemessen am 04.10.2026). Die
Werte in `update.json` tragen es schon; du schreibst sie, wie das Script sie ausgibt.

Mit einer ersetzten Zeile beginnt der Bereich bei `A2` und schreibt jede bestehende Zeile mit ihrem
eigenen Text zurück; darum exportierst du direkt davor, und darum trägt der Bereich nur A bis F:
`Status`, `Runde`, Ist-Ergebnis, Schweregrad, Tester und Datum bleiben unberührt (gemessen am
05.10.2026). Eine Zeile wird nicht verschoben und nicht geleert. `append_values` benutzt du hier
nicht: es hängt nach der Tabellenerkennung an („Values are appended after the last row of the
table"), und `update.json` nennt den Bereich schon genau, auch für neue Zeilen.
