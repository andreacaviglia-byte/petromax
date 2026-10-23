# Die Anforderungsliste anlegen

Ein natives Google Sheet je Vorhaben, mit und ohne das Add-on `solutioning` (§282), vier Tabs, je eine
Kopfzeile (§283). Es entsteht beim ersten Lauf von `requirements-update` (§229), **im Unterordner
`Solutioning` des Projektordners** (§231); dessen ID hat der Lauf vorher gefunden oder angelegt, wie
es `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` im Abschnitt „Die Ablage im Drive" sagt.
Was in den Spalten steht, sagt der Vertrag, `${CLAUDE_SKILL_DIR}/../../docs/requirements-list-contract.md`;
beim Anlegen schreibt der Lauf nur die Kopfzeilen und die Formel in `Aufwand (h)`. Die Zeilen schreibt
danach die Projektion über `project-sheet-writer`. Alle Aufrufe gehen über die Google-Connectoren
`Google_Drive` und `Google_Sheets` von claude.ai. Das Schema holst du über die Werkzeug-Suche, bevor
du das erste Feld setzt.

## Tabs und Kopfzeilen

**Tab-Namen und Kopfzeilen stehen in der Sprache aus `language`** (§295), wörtlich wie im Vertrag,
Abschnitt „Die Kopfzeilen“ und je Tab die Zeile `de` oder `en`. Die Folge der Tabs ist fest, der erste
ist `Anforderungen`, denn der CSV-Export liefert nur ihn:

| Tab `de` | Tab `en` | Bereich der Kopfzeile |
|---|---|---|
| `Anforderungen` | `Requirements` | `A1:R1` |
| `Solutioning` | `Solutioning` | `A1:L1` |
| `Epics` | `Epics` | `A1:P1` |
| `Offene Punkte` | `Open items` | `A1:H1` |

Keine weitere Spalte, kein weiterer Tab, keine Beispielzeile. Ist `language` leer, entsteht kein
Sheet: Kopfzeilen und Tab-Namen hängen an ihr.

## Die Folge der Aufrufe

0. **Den Namen bilden** (§263): `python3 ${CLAUDE_SKILL_DIR}/../../scripts/doc-name.py . requirements`
   gibt `Anforderungsliste ‹title› – ‹Kunde›` (bei `en` `Requirements list ‹title› – ‹Kunde›`, §337) aus `project.yml` aus, ohne Datum. Du bildest ihn
   nicht selbst. Exit 1 nennt das leere Feld; dann legst du nichts an und nennst `project-setup`.
1. **Suchen.** `Google_Drive.search_files` im Unterordner `Solutioning` mit `excludeContentSnippets: true` und
   `query` = `parentId = '<Unterordner>' and title = '‹Name›' and mimeType = 'application/vnd.google-apps.spreadsheet'`,
   `‹Name›` aus Schritt 0, Zeichen für Zeichen: Leerzeichen, Umlaute und der Halbgeviertstrich `–`
   bleiben, wie sie sind; vor jedes `'` und jeden `\` im Namen setzt du einen `\`, damit die
   einfachen Anführungszeichen der Query den Namen umschließen. Ein bestehendes Sheet findet der
   Lauf über `requirements_sheet`, nie über den Namen; diese Suche gilt nur dem Rest eines
   abgebrochenen ersten Laufs.
   Ein Treffer: nicht neu anlegen, sondern mit Schritt 7 prüfen und dem Lead mit Link zeigen. Ob
   `search_files` Dateien im Papierkorb mitliefert, ist ungemessen; die Suche kennt keinen Filter dafür.
   Die ID eines Treffers geht deshalb erst in `project.yml`, wenn der Lead ihn als das Sheet bestätigt.
2. **Anlegen.** `Google_Drive.create_file` mit `title` = der Name aus Schritt 0,
   `contentMimeType: application/vnd.google-apps.spreadsheet` und `parentId` = die ID des Unterordners
   `Solutioning`, immer mit `parentId`. Aus der Antwort nimmst du die ID des Sheets. Der erste Tab eines neuen Sheets hat die
   `sheetId` 0.
3. **Ersten Tab umbenennen.** `Google_Sheets.update_spreadsheet` mit `spreadsheetId` und `requests` =
   `[{updateSheetProperties: {properties: {sheetId: 0, title: "‹erster Tab›"}, fields: "title"}}]`.
4. **Drei Tabs anlegen, nacheinander.** `update_spreadsheet` mit `requests` =
   `[{addSheet: {properties: {title: "Solutioning"}}}]`, dann in je einem eigenen Aufruf dasselbe mit
   `Epics` und mit dem vierten Tab.
5. **Tab-Namen zurücklesen, bevor geschrieben wird.** `Google_Sheets.get_spreadsheet` mit
   `spreadsheetId` und `fields: ["sheets.properties.title"]`: genau die vier Tabs der Tabelle oben in
   der Sprache aus `language`, in dieser Reihenfolge, sonst nichts. Erst danach schreibst du: ein
   Schreibaufruf parallel zur Umbenennung traf den alten Tab-Namen (gemessen am 04.10.2026).
6. **Kopfzeilen.** `Google_Sheets.update_values` je Tab mit `range` = `'‹Tab›'!‹Bereich›` aus der
   Tabelle oben und `values` = eine Zeile, jeder Kopf mit führendem Hochkomma: `update_values` deutet
   Eingaben wie getippt, das Hochkomma hält sie als Text (gemessen am 04.10.2026).
7. **Zurücklesen.** Die Tab-Namen wie in Schritt 5. Dann `Google_Sheets.get_values` je Kopfzeile, ein
   Aufruf je Bereich; die Antwort trägt `values` als Liste von Zeilen. Jede gelesene Kopfzeile
   schreibst du als eine Zeile CSV in eine Datei im Temp-Ordner des Laufs (`mktemp -d`, außerhalb des
   Repos, §233) und prüfst sie mit dem Script des Repos, je Tab mit seinem Namen im Sheet:

   ```
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-sheet.py --check header --language ‹language› --header Anforderungen kopf-a.csv --header Solutioning kopf-s.csv --header Epics kopf-e.csv --header "Offene Punkte" kopf-o.csv
   ```

   Exit 0 heißt gleich. Stimmen Namen und Kopfzeilen, trägst du die ID als `requirements_sheet` in
   `project.yml` ein, wie der Datalayer-Vertrag es im Abschnitt `project.yml` sagt, und liest zurück.
   Weicht etwas ab, bleibt `requirements_sheet` leer, und der Bericht nennt Sheet-Link, gelesene
   Namen und die abweichenden Zellen. Einen fehlenden Tab legst du in einem bestehenden Sheet nur
   nach Rückfrage an.
8. **Die Formel in `Aufwand (h)`** des Tabs `Epics`, erst nach Schritt 7. Das Gebietsschema liest du
   mit `get_spreadsheet` und `fields: ["properties.locale"]`: `de_DE` trennt die Argumente mit `;`,
   `en_US` mit `,`. Dann gibt
   `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sheet-format.py --epic-hours --language ‹language› --separator ‹;|,›`
   `{"range": …, "values": …}` aus, und du schreibst genau das mit einem Aufruf von `update_values`.
   Zurück liest du die Zelle mit `get_values`: ein Fehlerwert wie `#ERROR!` oder `#NAME?` heißt, die
   Formel gilt nicht; dann leerst du die Zelle mit `update_values` und `[[""]]`, und der Bericht nennt
   die Meldung. Ungemessen ist, ob `update_values` die Formel in einem Sheet in `de_DE` und `en_US`
   annimmt (Vertrag, Tab `Epics`).
9. **Formatieren** (§247). Die `sheetId` je Tab liest du mit
   `Google_Sheets.get_spreadsheet` und `fields: ["sheets.properties.sheetId","sheets.properties.title"]`.
   Die Anfragen erzeugt das Script aus den Kopfzeilen und Eigentümern des Vertrags:
   `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sheet-format.py --sheet Anforderungen=<id> --sheet Solutioning=<id> --sheet Epics=<id> --sheet "Offene Punkte"=<id>`,
   die Tabs mit ihren Namen im Sheet. Seine Ausgabe gibst du unverändert als `requests` an **einen**
   Aufruf von `Google_Sheets.update_spreadsheet`; scheitert eine Anfrage, gilt keine. Exit 1 heißt:
   Script und Vertrag weichen ab; dann formatierst du nicht und nennst die Zeile.
10. **Formatierung zurücklesen.** `get_spreadsheet` mit `ranges` = je Tab die Zeile 1
    (`'‹Tab›'!1:1`) und `fields` =
    `["sheets.properties.title","sheets.properties.gridProperties","sheets.data.columnMetadata.pixelSize"]`.
    Je Tab stehen `frozenRowCount` und `frozenColumnCount` auf 1, und die `pixelSize` der Spalten
    sind die aus den `updateDimensionProperties` der Ausgabe, in derselben Folge.

**Scheitert das Formatieren, bleibt das Sheet gültig:** `requirements_sheet` steht schon aus
Schritt 7, und der Bericht nennt den Fehler wörtlich, mit Aufruf und Tab. Die Formatierung holt der
Lead später mit „formatier die Anforderungsliste“ nach.

## Ein bestehendes Sheet nachformatieren

Nur auf Wunsch des Leads (§247), an dem Sheet aus `requirements_sheet`. Zuerst
`get_spreadsheet` mit `fields: ["sheets.properties.sheetId","sheets.properties.title","sheets.bandedRanges","sheets.protectedRanges"]`:
ein Tab, der schon ein Zebra trägt, bekommt `--no-banding <Tab>`: ein zweites `addBanding` auf
denselben Bereich lehnt der Connector ab, und dann gilt kein Request des Aufrufs (gemessen am 04.10.2026).
Ein Tab, der schon Schutzbereiche trägt, bekommt `--no-protect <Tab>`: sonst legt der Aufruf jeden
Bereich ein zweites Mal an (am Testprojekt 9 Bereiche, 10.10.2026). So formatierst du auch
eine neue Spalte an einem bestehenden Sheet; die bestehenden Schutzbereiche bleiben, wie sie sind. Vor dem Aufruf sagst du dem Lead, dass Schrift, Umbruch, Kopfzeile,
Fixierung und Breiten das überschreiben, was Menschen gesetzt haben; Farben einzelner Zellen
bleiben. Nach seinem Ja Schritt 9 und 10 wie oben.
