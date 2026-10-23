# Der Snapshot: die vier Tabs festhalten, freigeben, abgleichen

**Der Snapshot ist Kontext, nie Wahrheit** (§266). Was gilt, steht im Repo; der Snapshot zeigt,
welchen Stand der Anforderungsliste ein Proposal vorgelegt und ein Kunde freigegeben hat, damit eine
spätere Änderung als mögliche Change Request sichtbar wird, bevor gebaut wird (§280 Regel 8). Pfad,
Umgang und das Schema des Manifests stehen im Datalayer-Vertrag
(`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt `scope/`). Snapshot und Manifest
schreibt nur das Script; du schreibst keine Datei darin von Hand und änderst keine.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py <befehl> . …
```

Arbeitsdateien liegen im Temp-Ordner des Laufs (§233). Freigaben einzelner Epics nimmt dieser Weg
nicht auf: festgehalten wird der Stand des ganzen Sheets.

## Die vier Tabs lesen

**Gelesen werden `Anforderungen`, `Solutioning`, `Epics` und `Offene Punkte`** (`en`: `Requirements`,
`Solutioning`, `Epics`, `Open items`), jeder einmal und ganz, wie für die Projektion
(`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Schritt 2), in `anforderungen.json`,
`solutioning.json`, `epics.json` und `offene-punkte.json`. Snapshot und Abgleich lesen gleich, damit
eine Abweichung aus dem Sheet kommt und nicht aus dem Weg. Nach dem Proposal sind es die Lesungen aus
Step 3; bei der Freigabe liest du sie neu und nimmst die Lesezeit direkt danach.

## Die Fassung je Epic: `pages.json`

Das Manifest nennt je Epic mit Link in `Entwurf` oder `Epic Page` dessen Fassung. Du schreibst
`pages.json` mit einem Eintrag je Epic, dessen Datei `epic_page` oder `draft` trägt, außer
`status: merged`:

| Epic trägt | `source` | `version` |
|---|---|---|
| `epic_page` | `page` | die Fassung aus `getConfluenceContent` mit `content_id` = `<pageId>` und `detail: summary`; `cloudId` aus `confluence.cloud_id`, ist es leer, die `id` des Eintrags mit Confluence-Scopes aus `getAccessibleAtlassianResources` für die Site im Link; `pageId` die Zahl nach `/pages/` im Link |
| nur `draft` | `draft` | `modifiedTime` aus `Google_Drive.get_file_metadata` mit `fileId` = die ID aus dem Link, wörtlich |

```json
{"EP-001": {"source": "page", "version": "4"}, "EP-002": {"source": "draft", "version": "2026-09-29T10:12:03.000Z"}}
```

**Die Fassung ist der Wert aus der Antwort, nie geschätzt.** Antwortet der Atlassian-Connector nicht
oder liefert ein Aufruf keinen Wert, entsteht kein Snapshot; der Bericht nennt Epic und Meldung.

## Der Snapshot nach dem Proposal

Nur nach einem gleichen Rücklauf des neuen Proposals ([ref-proposal.md](ref-proposal.md), Das Doc
anlegen, Schritt 4), nach dem Verschieben der älteren Fassungen. Das Schätzdokument ist die Fassung,
die flach in `Solutioning` liegt: **du listest den Ordner dafür jetzt neu**, nicht aus der Liste von
Schritt 1, denn ein `solution-estimate` kann während dieses Laufs eine neue Fassung angelegt und die
alte nach `Archiv` verschoben haben. Daraus die Datei mit dem Namen aus
`doc-name.py . estimate`, ihr `createdTime` aus `Google_Drive.get_file_metadata`. Liegen dort zwei,
nimmst du die mit dem jüngeren `createdTime` und nennst beide im Bericht; liegt keine, fehlen die
beiden Angaben.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py write . --occasion proposal \
  --sheet <requirements_sheet> --read-at <Lesezeit aus Step 3> --pages <temp>/pages.json \
  --tab Anforderungen=<temp>/anforderungen.json --tab Solutioning=<temp>/solutioning.json \
  --tab Epics=<temp>/epics.json --tab "Offene Punkte"=<temp>/offene-punkte.json \
  --proposal-id <ID aus Schritt 2> --proposal-created <createdTime aus Schritt 3> \
  [--estimate-id <ID> --estimate-created <createdTime>]
```

Die Tab-Namen stehen in der Sprache aus `language`. **Exit 0:** die erste Zeile ist
`SNAPSHOT scope/‹ordner›`; das Script hat jede Datei zurückgelesen. Der Ordner geht in den Commit des
Laufs. **Exit 1:** die Zeile nennt Prüfung und Stelle, und es ist nichts geschrieben. Liegt der
Fehler in deiner Datei oder einem Argument (`input`, `read_at`, `document`, `epic` aus `pages.json`),
korrigierst du ihn aus der Lesung und rufst einmal neu. Sonst bleibt es ohne Snapshot: **das Proposal
bleibt gültig**, und der Bericht nennt die Lücke mit der Zeile wörtlich. `header` heißt, eine
Kopfzeile weicht vom Vertrag ab; `epic` heißt, ein Epic mit Link im Sheet hat keine Fassung, oder der
Link im Sheet fehlt, weil die Projektion zurückliegt.

## Die Freigabe

Sagt der Lead „Kunde hat freigegeben", entsteht kein Proposal. Der Lauf hält fest, welcher Stand
freigegeben ist.

1. **Den jüngsten Snapshot finden:** `scope-snapshot.py latest .`. Exit 3 heißt, es gibt keinen:
   **du hältst an**, denn freigegeben werden kann nur ein Stand, den ein Proposal festgehalten hat;
   der nächste Lauf ist `solution-proposal` ohne Freigabe.
2. **Die vier Tabs lesen** wie oben, dann den Abgleich gegen ihn (unten).
3. **Gleich (Exit 0):** du trägst die Freigabe in sein Manifest ein:
   `scope-snapshot.py release . scope/‹ordner› --released-by "<wer>" --release-date <JJJJ-MM-TT>`.
4. **Abweichungen (Exit 3):** du nennst jede Zeile und fragst, welcher Stand freigegeben ist.
   - **Der Stand des Snapshots:** die Freigabe kommt in sein Manifest wie in 3, und die Abweichungen
     stehen im Bericht als mögliche Change Requests.
   - **Der heutige Stand:** ein neuer Snapshot mit Anlass `release`, wie oben nach dem Proposal, mit
     `--occasion release --released-by "<wer>" --release-date <JJJJ-MM-TT>` und der Lesezeit dieser
     Lesung, `pages.json` wie oben. Proposal und Schätzdokument sind die Fassungen, die flach in
     `Solutioning` liegen; das Proposal findest du dort wie das Schätzdokument, mit dem Namen aus
     `doc-name.py . proposal`.
5. **Wer freigegeben hat**, nimmst du nur aus der Angabe des Leads; fehlt sie im Aufruf, fragst du ihn
   danach. Du leitest sie nicht aus Mails, Material oder dem Sheet ab. Das Datum ist das, das der Lead
   nennt, sonst der Tag des Laufs; der Bericht sagt, welches.

`release` lehnt mit `released` ab, wenn der Snapshot schon eine Freigabe trägt: ein Snapshot wird nie
überschrieben, und welche gilt, entscheidet der Lead.

## Der Abgleich

**Pflicht bei „Kunde hat freigegeben“** gegen den jüngsten Snapshot (§266):

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py compare . scope/‹ordner› \
  --tab Anforderungen=<temp>/anforderungen.json --tab Solutioning=<temp>/solutioning.json \
  --tab Epics=<temp>/epics.json --tab "Offene Punkte"=<temp>/offene-punkte.json
```

| Zeile | heißt |
|---|---|
| `SNAPSHOT scope/‹ordner› \| gelesen ‹Lesezeit› \| freigegeben ‹Datum› durch ‹wer›` | der Stand, gegen den verglichen wird |
| `NEU ‹Tab› ‹ID› \| ‹Titel›` | die Zeile steht heute im Sheet, im Snapshot nicht |
| `ENTFERNT ‹Tab› ‹ID› \| ‹Titel›` | die Zeile stand im Snapshot, heute nicht |
| `GEÄNDERT ‹Tab› ‹ID› \| ‹Spalte›: „alt“ → „neu“` | eine Zelle ist anders; `+ „…“` heißt, an die Zelle ist etwas angehängt |
| `KOPF ‹Tab› \| Spalte „…“ neu` oder `entfernt` | die Kopfzeile ist anders |
| `ABWEICHUNGEN ‹n›` oder `GLEICH` | Exit 3 oder Exit 0 |

**Jede Zeile ist eine mögliche Change Request, keine festgestellte.** Der Abgleich entscheidet nichts
und ändert nichts: ein neuer Status oder eine neue Prüfung kann gewollt sein. Was davon eine Change
Request ist, entscheidet der Lead mit dem Kunden. Exit 1 nennt einen Snapshot, dem eine Datei fehlt
(`snapshot`); dann meldest du die Zeile wörtlich, und der Abgleich entfällt.
