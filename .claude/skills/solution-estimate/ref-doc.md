# Das Schätzdokument anlegen

Ein Google-Doc im Unterordner `Solutioning` des Projektordners (`project_folder` aus `project.yml`),
**je Lauf eine neue Fassung** (§220 W13). Eine neue Fassung ist ein neues Doc. Flach in `Solutioning`
liegt nur die aktuelle; die vorigen verschiebt der Lauf in den Unterordner `Archiv` (§260).

## Name

`Aufwandsschätzung ‹title› – ‹Kunde›` (§263), ohne Datum und Uhrzeit, die Art in jeder Sprache deutsch, denn das Dokument ist intern (§337). Den
Namen bildest du nicht selbst, das Script bildet ihn aus `project.yml`:
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/doc-name.py . estimate`. Exit 1 nennt das leere Feld;
dann hältst du an und nennst `project-setup`. **Jede Fassung trägt denselben Namen**; welche die
aktuelle ist, sagt der Ort (flach in `Solutioning`), und das Datum der Lesezeit steht im Dokument
selbst („Stand: ‹TT.MM.JJJJ›“, bei `en` „As of: 11 Oct 2026“; Uhrzeit und gelesene Stunden im Commit des Laufs, §264).

## Die Aufrufe, in dieser Folge

| # | Zweck | Aufruf |
|---|---|---|
| 0 | den Unterordner finden oder anlegen | `Google_Drive.search_files` mit `query` = `parentId = '‹project_folder›' and title = 'Solutioning' and mimeType = 'application/vnd.google-apps.folder'`. Ein Treffer: seine ID ist `‹solutioning›`. Keiner: `Google_Drive.create_file` mit `title: Solutioning`, `contentMimeType: application/vnd.google-apps.folder`, `parentId` = `project_folder`, die zurückgegebene ID ist `‹solutioning›`. Zwei: anhalten und beide mit Link nennen; welcher gilt, entscheidet der Lead (§231) |
| 1 | die vorige Fassung finden | `Google_Drive.search_files` mit `query: "parentId = '‹solutioning›'"` und `excludeContentSnippets: true`, jede Seite über `pageToken`, bis kein `nextPageToken` mehr kommt; den Namen vergleichst du in der Antwort. Jeder Treffer mit dem Namen ist eine vorige Fassung (§262): du merkst dir ID und Namen und legst trotzdem an |
| 2 | das Doc anlegen, mit Inhalt | `Google_Drive.create_file` mit `title` = Name, `parentId` = `‹solutioning›`, `contentMimeType: text/html`, `textContent` = die Ausgabe des Scripts (HTML), Zeichen für Zeichen |
| 3 | Ort prüfen | `Google_Drive.get_file_metadata` mit `fileId` = ID aus Schritt 2; die Antwort nennt `‹solutioning›` als `parentId` und den Typ Google-Doc |
| 4 | zurücklesen und vergleichen | `Google_Drive.read_file_content` mit der ID; den Text der Antwort schreibst du in eine Datei im Temp-Ordner und vergleichst: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py readback estimate <ordner> <datei>`. `GLEICH` heißt: der Text des Docs ist der des Scripts |
| 5 | Seite, Fußzeile und Schrift | `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py layout` gibt die `requests` für `Google_Docs.update_doc` mit `documentId` = ID aus Schritt 2 aus: A4, Ränder, eine leere Fußzeile. Die Antwort trägt unter `createFooter` die `footerId`. Dann `check-solution-doc.py footer estimate <ordner> <footerId>` und dessen Ausgabe als `requests` an einen zweiten `update_doc`: Text und Stil der Fußzeile. Dann `Google_Docs.read_doc` mit `documentId` = ID aus Schritt 2; die Antwort (JSON) liegt in einer Datei im Temp-Ordner, und hat die Sitzung sie schon selbst als Datei abgelegt, nimmst du diese. `check-solution-doc.py font <datei>` gibt die `requests` für einen dritten `update_doc` aus: Poppins auf den ganzen Body, Fließtext, Tabellen und Überschriften, danach die Fettung, wie sie vorher stand. Die `requests` gehen unverändert und vollständig in diesen einen Aufruf. Der Schritt läuft immer, auch wenn das Doc schon Poppins zeigt |
| 6 | ältere Fassungen nach `Archiv` (§260, §262) | Nur wenn Schritt 4 `GLEICH` meldete, nach Schritt 5. Ältere Fassung ist jede Datei aus der Liste von Schritt 1 mit dem Namen aus `doc-name.py`, deren ID nicht die aus Schritt 2 ist und deren `createdTime` vor der des neuen Doc liegt; `createdTime` liest du je Datei mit `Google_Drive.get_file_metadata`, für das neue Doc aus Schritt 3. Trägt eine Antwort kein `createdTime`, verschiebst du diese Datei nicht und nennst sie. Gibt es keine ältere Fassung, entfällt der Schritt. Sonst `Archiv` finden oder anlegen: `Google_Drive.search_files` mit `query` = `parentId = '‹solutioning›' and title = 'Archiv' and mimeType = 'application/vnd.google-apps.folder'`. Ein Treffer: seine ID ist `‹archiv›`. Keiner: `Google_Drive.create_file` mit `title: Archiv`, `contentMimeType: application/vnd.google-apps.folder`, `parentId` = `‹solutioning›`. Zwei: nichts verschieben, beide mit Link nennen. Dann je ältere Fassung `Google_Drive.update_file` mit `fileId` = ihre ID und `parentId` = `‹archiv›` |

- **Gesucht wird über die Liste des Ordners, nicht über den Namen** im ganzen Drive.
- **Der Inhalt geht in Schritt 2 als HTML mit Inline-Stilen** (§248): `create_file` mit
  `contentMimeType: text/html` legt ein Google-Doc an und behält Farben, Tabellenköpfe und
  Rahmen (gemessen am 04.10.2026), dazu die Abstände um Überschriften und Tabellen, die das Script als
  `margin` setzt (gemessen am 08.10.2026); einen eigenen Aufruf dafür gibt es nicht. Die Schrift behält
  es nicht bei jedem Doc: am 08.10.2026 kam das Schätzdokument in Arial an, das Proposal desselben
  Stands in Poppins, aus demselben HTML-Aufbau. Deshalb setzt Schritt 5 sie nach. Die Seite kommt als
  US Letter; A4 und die Fußzeile setzt Schritt 5.
- **Scheitert Schritt 5, bleibt das Doc gültig**: der Inhalt steht, nur Seite, Fußzeile oder Schrift fehlen;
  der Bericht nennt Aufruf und Meldung wörtlich.
- Ein Doc, das es schon gibt, schreibt dieser Weg nie, auch keine frühere Fassung.
- **Angelegt ist das Doc erst**, wenn Schritt 3 den Unterordner `Solutioning` nennt und Schritt 4
  `GLEICH` meldet; damit stehen auch „Intern — nicht für den Kunden." und die Zeile `Gesamt` wie in der
  Ausgabe des Scripts da. Sonst nennt der Bericht das Doc als nicht bestätigt, mit der Zeile, die
  `readback` als erste abweichende nennt.
- **Ein kaputt angelegtes neues Doc kommt weg** (§259), **erkannt an der ID aus Schritt 2, nie am
  Namen**: die vorige Fassung trägt denselben Namen (§262) und bleibt dann flach liegen, wie sie ist.
- **Scheitert Schritt 6, bleibt die ältere Fassung in `Solutioning` liegen** (weich); der Bericht
  nennt sie mit Name und Link. Verschoben wird nur, was dieser Weg als ältere Fassung erkennt, kein
  Proposal und kein anderes Doc.

## Was dieser Weg nicht tut

Er löscht nichts und verschiebt nichts in den Papierkorb außer einem Doc, das er selbst kaputt angelegt
hat (§259), auch keine ältere Fassung; die geht nach
`Archiv` (Schritt 6) und bleibt dort, wie sie ist. Er teilt das Doc
nicht; angelegte Dateien sind privat, bis ein Mensch sie teilt.
