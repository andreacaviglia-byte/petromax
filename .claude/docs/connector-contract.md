# Der Connector-Vertrag — welche fremden Werkzeuge diese Strecke braucht

**Diese Tabelle ist die einzige Stelle, an der der Bedarf steht.** `dev/tests/check-connectors.py` liest
sie; nennt ein Skill ein Werkzeug daraus, ohne hier als Bedarf zu stehen, scheitert der Prüflauf.
Nennt ein Skill einen Composio-Slug (`GOOGLESHEETS_…`, `GOOGLEDRIVE_…`, `GOOGLEDOCS_…`, `COMPOSIO_…`),
scheitert er auch: Composio entfällt (§226).

Ein **Bedarf** ist ein Paar aus Connector und Lauf, nicht ein Connector allein: derselbe Connector
ist für einen Lauf unverzichtbar und für den nächsten ein Zusatz. **Der Bedarf steht je Lauf, nicht
je Skill**; die Zeile nennt den Zweck, nicht eine Schrittnummer. Die Läufe sind die Skills aus
§274 und §275 und der Agent `project-sheet-writer` aus §215.
`project-upgrade` holt das Template mit git, ohne Connector (§237); es steht nur bei `add_repo`
und `get_session`.

**Drive, Sheets und Docs erreicht die Strecke über die Google-Connectoren von claude.ai** (§226):
`Google_Drive`, `Google_Sheets`, `Google_Docs`. Sie handeln mit dem Google-Konto des Leads; was er im
Drive nicht sieht, sieht auch die Sitzung nicht. **Composio entfällt** (§226).

**Gelesen und geschrieben wird im Projektordner** (`project_folder` in `project.yml`, §229), in den
Unterordnern, die die Skills selbst anlegen (§231), auch `Epics` und `Archiv` in `Solutioning` (§260). Eine Sperre, die ein Schreiben außerhalb
verhindert, gibt es nicht (§226, §227); die Skills suchen nur in der Liste des Projektordners und
seiner Unterordner, nie über das ganze Drive.

**Der Datalayer liegt im Projekt-Repo der Sitzung** (§230); die Skills lesen und schreiben ihn
direkt, ohne Connector. `dev/tests/check-connectors.py` lehnt einen Skill ab, der in einem Absatz oder
einer Tabellenzeile einen Drive- oder GitHub-Befehl zusammen mit einem Pfad des Datalayers nennt.

**Die Anforderungsliste schreibt nur der Agent `project-sheet-writer`** (§230, §220): die Skills
lesen das Sheet selbst und übergeben ihm die Stellen `changes` aus `project-sheet.py`, nach
[`ref-projection.md`](ref-projection.md) (§280). Ein Skill, der über
den Agent schreibt, braucht dafür kein Schreibwerkzeug des Connectors; der Bedarf steht beim Agent.
Angelegt wird das Sheet von `requirements-update` beim ersten Lauf (§229). Das E2E-Sheet schreibt
`e2e-testing-sheet` selbst (§220).

## Die Doku von Shopify

**Die Doku ist im Solutioning eine Quelle, keine Voraussetzung** (§339), die von Shopify ebenso wie
die der Apps und Systeme des Kunden; diese Stelle ist die einzige, die ihre Wege beschreibt. Kein Lauf
hält an, weil sie fehlt.

**Vier Wege, ohne feste Reihenfolge** (§340): welcher trägt, hängt am Host (in der Liste erlaubter
Domains der Umgebung oder nicht, mit Bot-Schutz oder ohne) und daran, ob der Connector verbunden ist.

| Weg | leistet |
|---|---|
| `WebSearch` | findet die richtige Seite, auch beim Hersteller einer App oder eines Systems; liefert Links mit Zusammenfassung. Gelesen wird danach mit einem der anderen Wege |
| `WebFetch` | liest eine ganze Seite, nur Hosts aus der Liste erlaubter Domains der Umgebung. `.claude/settings.json` erlaubt es ohne Rückfrage für `shopify.dev`, `help.shopify.com` und `apps.shopify.com`; ein anderer Host fragt nach. Steht der Host nicht in der Liste, meldet es „getaddrinfo ENOTFOUND“ |
| `curl` | der Rückfall: liest eine Seite über den Proxy der Umgebung, nur Hosts aus ihrer Liste erlaubter Domains. `curl -sS https://shopify.dev/<Pfad>` auf die Referenz, versioniert wie `docs/api/admin-graphql/2026-10/objects/Product` oder als `latest`, erlaubt `.claude/settings.json` ohne Rückfrage; eine andere Form fragt nach. Ohne `-L`: auf eine Umleitung rufst du die Zieladresse in derselben Form, wenn sie auf `https://shopify.dev/` liegt, sonst nicht. Das Help Center von Shopify antwortet auf `curl` mit einer Bot-Prüfung |
| Shopify-Connector, `search_docs_chunks` | die Doku-Suche für shopify.dev, wenn der Connector verbunden ist; ein Shop ist nicht nötig |

- **Jeder Beleg nennt die URL, die gelesen wurde, das Datum und die Stufe** (§320, §340). Trägt ein Weg
  in der Sitzung nicht, versuchst du einen anderen und nennst den Fehlschlag mit Meldung im Bericht,
  bevor eine Aussage „(noch zu verifizieren)“ wird, bei `language: en` „(to be verified)“ (§337).
- **Ein Muss-Kriterium des gewählten Lösungsansatzes ohne Beleg bleibt eine blockierende offene Frage** (§326).
- **`validate_graphql_codeblocks` und `graphql_schema` sind weder Pflicht noch Beleg.** Das
  Solutioning nennt für Custom App und Schnittstelle Objekte, Operationen, Scopes, Plan und Grenzen,
  keine fertigen Abfragen.
- **Ein gesperrter Host** (§341): meldet `WebFetch` „getaddrinfo ENOTFOUND“ oder `curl` „CONNECT tunnel
  failed, response 403“, steht der Host nicht in der Liste erlaubter Domains der Umgebung. Du schlägst
  ihn in der Allowlist der Knowledge Base nach (`network/allowlist.md`, gelesen nach
  [`kb-contract.md`](kb-contract.md)) und nennst im Bericht, steht er dort: „Die Umgebung ist nicht auf
  dem Stand der Allowlist vom ‹Datum›; den Block aus network/allowlist.md der Knowledge Base in die
  Umgebung kopieren.“, steht er nicht dort: „‹Host› fehlt in der Allowlist der Knowledge Base; an den
  Kurator.“ Danach ein anderer Weg, sonst „(noch zu verifizieren)“; kein Lauf hält deswegen an. Ein
  403 vom Ziel selbst (Bot-Schutz, etwa `help.shopify.com`) ist kein fehlender Eintrag. `WebSearch`
  findet auch außerhalb der Liste, gelesen wird nur, was sie zulässt (§321).
- **Eine Ablehnung durch den Klassifizierer des Auto-Modus ist kein Weg, der nicht trägt:** der Lauf
  nennt sie wörtlich und sucht keinen zweiten Weg (Wurzel-`CLAUDE.md`).
- `requirements-update` lässt die Einordnung offen, wenn kein Weg trägt. `project-status` prüft die
  Wege in der Umgebung und sagt, was zu tun ist.

| Connector | Werkzeuge | Wer | Härte | Ausfall heißt |
|---|---|---|---|---|
| Drive | `search_files`, `get_file_metadata` | `project-setup`, `material-intake`, `requirements-update`, `requirements-review`, `solution-approach`, `epic-structure`, `solution-design`, `solution-review`, `solution-estimate`, `solution-proposal`, `solution-epic-page`, `e2e-testing-sheet`, `ticket-factory`, `project-sheet-writer` — den Projektordner und seine Unterordner auflisten, eine Datei darin finden, die Eltern einer verlinkten Datei lesen | hart | Anhalten. Ohne den gelesenen Projektordner hat der Lauf keinen Ort; ein Name, über das ganze Drive gesucht, ist geraten |
| Drive | `create_file` | `requirements-update`, `solution-design`, `solution-estimate`, `solution-proposal`, `e2e-testing-sheet` — beim ersten Schreiben den eigenen Unterordner im Projektordner anlegen (§231), in Solutioning die Unterordner Epics und Archiv (§260), darin Sheet, Entwurf, Schätzdokument und Proposal anlegen; ein Doc entsteht aus Markdown, der Entwurf einmal je Epic (§302) | hart | Anhalten. Ein Dokument, das nicht angelegt ist, wird nicht als angelegt berichtet |
| Drive | `update_file` | `solution-estimate`, `solution-proposal` — ältere Fassungen der eigenen Dokumentart, die flach in Solutioning liegen, nach dem gleichen Rücklauf der neuen nach Archiv verschieben (§260) | weich | Die ältere Fassung bleibt in `Solutioning` liegen, und der Bericht nennt sie mit Link |
| Drive | `trash_file` | `solution-design`, `solution-estimate`, `solution-proposal`, `e2e-testing-sheet` — ein Doc oder Sheet, das der Lauf selbst kaputt angelegt hat, in den Papierkorb legen, sobald es für die Neuerstellung nichts mehr trägt (§259) | weich | Das kaputte Dokument bleibt liegen, und der Bericht nennt es mit Link |
| Drive | `download_file_content`, `read_file_content` | `material-intake`, `requirements-update`, `requirements-review`, `solution-approach`, `epic-structure`, `solution-design`, `solution-review`, `solution-estimate`, `solution-proposal`, `solution-epic-page`, `e2e-testing-sheet`, `ticket-factory` — den Tab Anforderungen als CSV und einen Entwurf als HTML exportieren, Material und Entwürfe als Text lesen, mit Kommentaren | hart | Anhalten, **bevor** etwas aus dem Gelesenen geschrieben wird |
| Google Sheets | `get_spreadsheet`, `get_values` | `requirements-update`, `requirements-review`, `solution-approach`, `epic-structure`, `solution-design`, `solution-review`, `solution-estimate`, `solution-proposal`, `solution-epic-page`, `e2e-testing-sheet`, `ticket-factory`, `project-sheet-writer` — Tab-Namen und Kopfzeilen prüfen, schmale Bereiche lesen, jede Stelle direkt vor dem Schreiben lesen | hart | Anhalten. Ohne gelesenen Stand hat die Tabelle keine Spalte `heute` |
| Google Sheets | `update_values`, `append_values`, `update_spreadsheet` | `project-sheet-writer` die bestätigte Tabelle an genau ihre Stellen; `requirements-update` Tabs, Kopfzeilen und Formatierung beim Anlegen des Sheets, die Formatierung auch auf Wunsch des Leads (§247); `e2e-testing-sheet` das E2E-Sheet, mit derselben Formatierung beim Anlegen (§248), dazu Dropdowns, bedingte Formate, Schutz und den Tab Übersicht mit Formeln (§256) | hart | Anhalten. Eine Stelle ohne gleichen Rücklauf gilt nicht als geschrieben |
| Google Docs | `read_doc`, `update_doc` | `solution-design` den Entwurf lesen und gezielt fortschreiben (§302); `solution-estimate`, `solution-proposal` das Doc füllen | hart | Anhalten. Ohne gelesenen Entwurf schreibt kein Lauf ihn fort |
| Atlassian | `getJiraIssue` | `material-intake`, ein verlinktes Jira-Ticket als Material lesen (§212) | weich | Das Ticket bleibt ungelesen, und der Lauf nennt den Link als ungelesene Quelle |
| Slack | `slack_read_channel`, `slack_read_thread` | `material-intake`, Material aus einem Kanal | weich | Der Kanal bleibt ungelesen, und der Lauf nennt ihn als ungenutzte Quelle |
| Claap | `search_recording_transcripts`, `get_recording_transcript` | `material-intake`, Transkript eines Termins | weich | Das Transkript bleibt ungelesen, und der Lauf nennt den Termin als ungenutzte Quelle |
| GitHub | `get_file_contents` | `requirements-update`, Abgleich gegen index.md der Wissensbasis und den Standard-Leistungssatz des Rechtsraums | weich | Der Abgleich entfällt; der Lauf nennt die Wissensbasis als ungelesene Quelle, und aus der ungelesenen Pflichtliste wird eine Frage an den Lead statt einer Anforderung |
| Doku | die Wege oben (`WebSearch`, `WebFetch`, `curl`, `search_docs_chunks`) | `requirements-update`, Einordnung einer Anforderung (§340) | weich | Die Einordnung bleibt offen, und die Anforderung bekommt eine offene Frage in `gaps/` |
| GitHub | `get_file_contents` | `solution-approach`, je Lösungsansatz der passende Stamp der Wissensbasis: erst index.md, dann nur die Stamps, die passen (§275); bei einem gesperrten Host die Allowlist network/allowlist.md (§341) | weich | Der Lauf arbeitet weiter (§268): jeder Lösungsansatz trägt `KB: nicht gelesen`, und Notiz und Bericht nennen die Wissensbasis als ungelesene Quelle |
| Doku | die Wege oben (`WebSearch`, `WebFetch`, `curl`, `search_docs_chunks`) | `solution-approach`, der Fit eines Lösungsansatzes, dessen Fit unklar ist (§275, §340) | weich | Die Aussage steht mit „(noch zu verifizieren)“ da; die blockierende Frage für ein Muss-Kriterium ohne Beleg legt erst `solution-design` an (§326) |
| Atlassian | `atlassianUserInfo`, `getAccessibleAtlassianResources`, `executeRead`, `getConfluenceSpace`, `getContentFormatGuide`, `searchConfluence`, `getConfluenceContent`, `createConfluenceContent`, `updateConfluenceContent` | `solution-epic-page`, mit dem Add-on solutioning Pflicht vor den Tickets (§313): ein geprüftes, freigegebenes Epic als Epic Page übertragen, fortschreiben und zurücklesen, Space und Elternseite prüfen, den Owner als Mention setzen (§218, §277); getConfluenceSpace und getContentFormatGuide laufen über executeRead, atlassianUserInfo liefert nur die Konto-ID (gemessen am 10.10.2026) | hart | Anhalten. Ohne Seite bleibt der Entwurf der einzige Stand, und der Lauf nennt die Übertragung als nicht erfolgt |
| GitHub | `get_file_contents` | `solution-design`, kb_match gegen die Wissensbasis: erst index.md, dann die Stempel; bei einem gesperrten Host die Allowlist network/allowlist.md (§341) | weich | Der Lauf arbeitet weiter (§268): jeder Lösungsansatz, den er schreibt, trägt `KB: nicht gelesen` statt `KB: keiner`, weil „kein Fund in der Wissensbasis" und „nicht nachgesehen" verschiedene Auskünfte sind; Bericht und Entwurf nennen die Wissensbasis als ungelesene Quelle, und `solution-review` meldet die Lösungsansätze vor dem Proposal |
| GitHub | `get_file_contents` | `solution-review`, bei einem gesperrten Host die Allowlist network/allowlist.md der Wissensbasis (§341) | weich | Der Bericht nennt den Host als gesperrt, ohne den Abgleich mit der Allowlist |
| Claude Code Remote | `add_repo` | `requirements-update`, `solution-approach`, `solution-design`, `solution-review`, `project-status`: die Wissensbasis, `project-upgrade`: das Template an die Cloud-Sitzung hängen, nur lesend, ohne Klon | weich | Auf dem Rechner eines Leads gibt es das Werkzeug nicht und es braucht es nicht; in der Cloud bleibt sonst die Quelle ungelesen, und der Lauf nennt sie so |
| Claude Code Remote | `get_session` | `project-setup`, `material-intake`, `requirements-update`, `requirements-review`, `solution-approach`, `epic-structure`, `solution-critical-path`, `solution-design`, `solution-review`, `solution-estimate`, `solution-proposal`, `solution-epic-page`, `e2e-testing-sheet`, `ticket-factory`, `project-upgrade`, `project-status`, `skill-create` — am Ende des Laufs ohne session_id cost_usd und ID der eigenen Sitzung, mit session_id die genauen Kosten früherer Sitzungen, die run-metrics.py mit --open nennt, als Kosten für .claude/metrics/runs.md (§246); die Regel steht in der Wurzel-CLAUDE.md, nicht im Skill | weich | Auf dem Rechner eines Leads gibt es das Werkzeug nicht; die Kosten kommen dann aus dem Kostenstand im Protokoll oder stehen „ungemessen“. Geraten oder aus Tokens gerechnet wird nicht |
| Doku | die Wege oben (`WebSearch`, `WebFetch`, `curl`, `search_docs_chunks`) | `solution-design`, jede Plattformaussage und die Muss-Kriterien einer Public App beim Hersteller, im App Store und im Help Center (§320, §340) | weich | Die Aussage steht mit „(noch zu verifizieren)“ da; ein Muss-Kriterium des gewählten Lösungsansatzes ohne Beleg wird eine blockierende Frage (§326) |
| Doku | die Wege oben (`WebSearch`, `WebFetch`, `curl`, `search_docs_chunks`) | `solution-review`, Grenzen je Shop gegen die Summe der Lösungen (§216, §340) | weich | Die Summe steht mit „Grenze nicht gefunden“ als Beobachtung, nicht als Befund; eine Summe gegen eine erinnerte Grenze ist keine Prüfung |
| Atlassian | `getAccessibleAtlassianResources`, `getConfluenceContent` | `solution-proposal`, nur für den Snapshot: die Fassung einer Epic Page (aus der Lesung), cloudId aus dem Link ableiten, wenn cloud_id in project.yml leer ist; gerechnet wird das Proposal aus dem Repo (§280) | weich | Der Snapshot entsteht nicht; das Proposal bleibt gültig, und der Bericht nennt Epic und Meldung |
| Atlassian | `getConfluenceContent` | `ticket-factory`, die Epic Page als freigegebenen Stand lesen und gegen das Repo abgleichen (§219); nach Confluence schreibt der Lauf nichts (§328), das Ticket verlinkt die Epic Page als Kontext | hart | Kein Ticket für ein Epic mit Epic Page; der Bericht nennt die Seite als ungelesen. Die übrigen Epics laufen weiter |
| Atlassian | `createJiraIssue`, `searchJiraIssuesUsingJql`, `getJiraIssue`, `executeRead`, `getJiraIssueTypeMetaWithFields`, `editJiraIssue`, `listJiraIssueTransitions`, `transitionJiraIssue` | `ticket-factory`, Kanal Jira: Pflichtfelder je Lauf lesen („Get field metadata"), Bestand über die Zeile Schlüssel abgleichen, Epic, Story und Subtask anlegen und zurücklesen (§281); ein bestehendes Ticket vor jeder Änderung lesen und nur Titel und Beschreibung ändern (§280, Regel 7); eine Story mit Out of Scope in den Status Wunschliste überführen (§284) | hart | Kein Ticket entsteht |
| Atlassian | `getAccessibleAtlassianResources`, `executeRead`, `listJiraProjects`, `listJiraProjectIssueTypesMetadata`, `atlassianUserInfo` | `ticket-factory`, Kanal Jira binden: Klarname des Projekts und seine Vorgangstypen zurücklesen; listJiraProjects, listJiraProjectIssueTypesMetadata, getJiraIssueTypeMetaWithFields und listJiraIssueTransitions laufen über executeRead (gemessen am 11.10.2026), die Person des Laufs für das Feld Eigentümer (§281) | hart | Anhalten. Eine Kennung wird nie geraten; ist `board.*` leer, trägt der Lauf das geprüfte Projekt in project.yml ein (§229) |
| Asana | `get_project`, `get_tasks`, `create_tasks`, `update_tasks`, `get_me` | `ticket-factory`, Kanal Asana: Ziel, Sections („include_sections") samt Wunschliste und Feldwerte lesen, die Person des Laufs für das Feld Owner (§281), Bestand und offen oder geschlossen (completed) über die Liste abgleichen, anlegen, ein gelesenes Ticket ändern (§280, Regel 7), das erste Epic-Ticket, die erste Story und den ersten Subtask über die Liste ihrer Section zurücklesen. nie über die Suche: sie ist laut Schema „Premium accounts only … Use get_tasks for non-Premium workspaces" und fand am 25.09.2026 einen frisch angelegten Task erst nach etwa 31 s | hart | Kein Ticket entsteht |
| Atlassian | `getAccessibleAtlassianResources`, `executeRead`, `getConfluenceSpace`, `listJiraProjects` | `project-setup`, Confluence-Space und Jira-Projekt prüfen, die der Lead im Onboarding nennt (§229) | weich | Das Feld bleibt leer, der Bericht nennt die Meldung, und der Skill, der es zuerst braucht, fragt wieder. Eine ungeprüfte Adresse wird nicht in den Steckbrief geschrieben |
| Asana | `get_project` | `project-setup`, Board-Projekt prüfen, wenn der Lead im Onboarding ein Asana-Board nennt (§229) | weich | Das Feld bleibt leer, der Bericht nennt die Meldung. Eine ungeprüfte Projekt-GID wird nicht in den Steckbrief geschrieben |
| Drive | `get_file_metadata` | `project-status`, Umgebung: den Projektordner lesen (§289) | weich | Die Zeile Drive in der Tabelle der Umgebung nennt die Meldung und den Weg zur Abhilfe |
| Google Sheets | `get_spreadsheet` | `project-status`, Umgebung: den Titel der Anforderungsliste lesen (§289) | weich | Die Zeile Sheets nennt die Meldung und den Weg zur Abhilfe |
| Google Docs | `read_doc` | `project-status`, Umgebung: nur ob das Werkzeug in der Liste steht (§289) | weich | Die Zeile Docs nennt es als fehlend und den Weg zur Abhilfe |
| Atlassian | `atlassianUserInfo` | `project-status`, Umgebung, wenn der Steckbrief Confluence oder Jira nennt (§289) | weich | Die Zeile Atlassian nennt die Meldung und den Weg zur Abhilfe |
| Asana | `get_me` | `project-status`, Umgebung, wenn das Board in Asana liegt (§289) | weich | Die Zeile Asana nennt die Meldung und den Weg zur Abhilfe |
| GitHub | `get_file_contents` | `project-status`, Umgebung: index.md der Wissensbasis lesen (§289) | weich | Die Zeile Wissensbasis nennt die Meldung; in der Cloud zuerst `add_repo` |
| Doku | `search_docs_chunks`, `WebFetch` | `project-status`, Umgebung: ob der Shopify-Connector die Doku-Suche trägt und ob WebFetch shopify.dev liest (§340) | weich | Die Zeile Shopify-Doku nennt Meldung und Rückfall: `curl` auf shopify.dev; der Connector ist ein Weg, keine Voraussetzung; ein gesperrter Host: den Block aus `network/allowlist.md` der Wissensbasis in die Umgebung kopieren (§341) |

**Härte ist `hart` oder `weich`, ein drittes Wort gibt es nicht.** `hart` heißt: der Lauf hält an und
nennt Connector, Werkzeug und die Frage, die offen bleibt. `weich` heißt: der Lauf läuft weiter und
nennt den Ausfall in seiner Rückgabe — nie still.

## Google-Connectoren: die Aufrufe auf Ordner, Sheet und Doc

Die Sätze in Anführungszeichen sind die Werkzeugbeschreibungen aus der Werkzeugliste einer
Cloud-Sitzung, gelesen am 03.10.2026.

| Werkzeug | Beschreibung sagt | Wofür hier |
|---|---|---|
| `Google_Drive.search_files` | Suche mit `parentId`, `title`, `mimeType`, `modifiedTime`; „Use `'root'` for the user's \"My Drive\"" | die Liste eines Ordners: `parentId = '<Ordner>'`; nie ohne `parentId` |
| `Google_Drive.get_file_metadata` | „find general metadata about a user's Drive file" | Titel, `parentId`, `canAddChildren` einer Datei oder eines Ordners |
| `Google_Drive.create_file` | „Folders can be created by setting the mime type to `application/vnd.google-apps.folder`"; Docs, Sheets und Slides „can be created without providing content"; „By default, supported content will be converted to Google first-party mime types" | Unterordner und Sheet anlegen; ein Doc mit `textContent` und `contentMimeType: text/markdown`; immer mit `parentId` |
| `Google_Drive.update_file` | „currently only title and parent_id are supported“; zu `parentId`: „If the file has an existing parent, it will be replaced, resulting in a folder move.“ (gelesen am 08.10.2026) | ältere Fassungen von Schätzung und Proposal nach `Archiv` verschieben (§260) |
| `Google_Drive.copy_file` | „If the parent folder is not specified, the copy will be created in the same folder as the original file" | eine Vorlage in den Projektordner kopieren, immer mit `parentId` |
| `Google_Drive.download_file_content` | „download the content of a Drive file as a base64 encoded string"; für native Dateien setzt `exportMimeType` das Format | den Tab Anforderungen als `text/csv`, einen Entwurf als `text/html` |
| `Google_Drive.read_file_content` | „a natural language representation of a known Drive file, and if specified, its comments" | Material und Entwurf lesen, mit `includeComments` |
| `Google_Sheets.get_spreadsheet` | „Returns titles, sheet names, grid properties" | Tab-Namen, `sheetId`, vorhandenes Zebra (`sheets.bandedRanges`), Fixierung und Spaltenbreiten zurücklesen; mit `fields` schmal halten |
| `Google_Sheets.get_values` | „Returns a range of values from a spreadsheet" | Kopfzeilen, Spalten, einzelne Stellen |
| `Google_Sheets.update_values` | „Sets values in a range of a spreadsheet" | eine Stelle oder ein Bereich, Zeile für Zeile bestätigt |
| `Google_Sheets.append_values` | „Values are appended after the last row of the table" | neue Zeilen unter der zuletzt belegten |
| `Google_Sheets.update_spreadsheet` | „Applies one or more updates to the spreadsheet", u. a. `updateSheetProperties` | Tabs anlegen und benennen beim Anlegen des Sheets; formatieren mit `repeatCell`, `updateSheetProperties`, `updateDimensionProperties`, `addBanding` (§247) |
| `Google_Docs.read_doc` | „a JSON representation of the Google Doc" mit Struktur und Indizes | den Entwurf vor jedem gezielten Schreiben; in Schätzung und Proposal das Ende des Body für die Schrift |
| `Google_Docs.update_doc` | `documents.batchUpdate`, u. a. `insertText`, `replaceAllText`, `updateTextStyle`, `updateDocumentStyle`, `createFooter` | gezielt in den Entwurf schreiben; in Schätzung und Proposal A4, Ränder, Fußzeile und Schrift setzen (§248) |

**Gemessen am 03.10.2026 in einer Cloud-Sitzung**, in der eigenen Ablage des Nutzers: `create_file`
legt Ordner, Doc und Sheet an; `copy_file` kopiert in einen Zielordner; `update_doc` mit `insertText`
und `replaceAllText` und `update_values` ändern einzelne Stellen in derselben Datei, und das
Zurücklesen zeigt genau die geschriebenen Werte; `download_file_content` liefert ein Sheet als CSV
(nur den ersten Tab) und ein Doc als HTML, beide als Base64 in der Antwort, ohne Link. Im geteilten
Drive ist bisher nur gelesen worden; schreibend ist es ungemessen (M2 im Umbauplan).

**Gemessen am 04.10.2026 für §248**, im Projektordner des Test-Repos: `create_file` mit
`contentMimeType: text/html` legt ein Google-Doc an; Inline-Stile tragen (`font-family:'Poppins'` ohne
Fallback-Liste, Gewicht, Farbe, Zellhintergrund, Rahmen, Innenabstand, Hervorhebung, Linkfarbe), Stile
nur im `<style>`-Block tragen die Schrift nicht (Arial). Die Seite kommt als US Letter.
`update_doc` nimmt danach `updateDocumentStyle` (A4, Ränder) und `createFooter` an, die Antwort trägt
die `footerId`; ein zweiter Aufruf setzt mit `insertText` und `updateTextStyle` den Text der Fußzeile.
`read_file_content` gibt Überschriften fett umschlossen, eine leere Kopfzeile je Tabelle und maskierte
Zeichen in Zellen zurück; `check-solution-doc.py readback` gleicht das aus.
**Gemessen am 08.10.2026:** dasselbe HTML-Muster kam als Proposal in Poppins an, als Schätzdokument
(rund 130 KB HTML, 1.934 Inline-Stile mit `font-family:'Poppins'`) in Arial; Größe, Farbe und
Hintergrund kamen in beiden an. Ein `updateTextStyle` mit `weightedFontFamily` über den Body, von
Index 1 bis vor das Ende aus `read_doc`, setzt die Schrift danach und nimmt die Fettung mit: aus `bold:
true` wurde nicht fett, und Überschriften, die ihr Fett aus der Vorlage erbten, bekamen `bold: false`.
`check-solution-doc.py font` setzt darum nach der Schrift die Fettung je Abschnitt wieder; der Text
blieb zeichengleich, Fußzeile und Seite unverändert.
Ein `<img>` mit einer PNG als data-URI, `width="110" height="35"`, in einem Absatz mit
`margin:0 0 18pt 0` kommt als eingebettetes Bild von 82,5 × 26,25 pt an, der Absatz mit 18 pt Abstand
unten; `read_file_content` gibt das Bild nicht zurück, der Text beginnt mit dem Absatz danach. Aus
`font-weight:600` macht das Doc fett, `letter-spacing` fällt weg.

**Gemessen am 08.10.2026, die Abstände**, an einem Probe-Doc im Projektordner des Test-Repos:
`margin-top` und `margin-bottom` an `<h2>`, `<h3>` und `<p>` kommen als `spaceAbove` und `spaceBelow`
in derselben Größe an; `padding` addiert sich zum `margin` und ohne `margin` zum Standard des Docs
(24 pt werden 35,25 pt). Folgt eine Überschrift auf einen Absatz, wandert ihr `margin-top` in den
`spaceBelow` dieses Absatzes, ihr `spaceAbove` wird 0; `padding-top` bei `margin-top:0` bleibt an der
Überschrift. Direkt unter einer Tabelle zeigt das Doc den `spaceAbove` eines Absatzes nur, solange
sein `spaceBelow` 0 ist (12 pt mit 22 pt darunter: kein Abstand; 12 pt mit 0: Abstand);
`margin` an `<table>` fällt weg, den Abstand zur Tabelle trägt der Absatz davor oder danach.
`border-bottom` an einer Überschrift wird ein eigener leerer Absatz mit einer grauen Linie, die Farbe
fällt weg. Ein leerer Absatz als Abstandhalter bleibt als Leerzeile stehen. `updateParagraphStyle`
mit `spaceAbove` und `spaceBelow` nach dem Anlegen wirkt gleich wie `margin`. `read_file_content`
gibt die Abstände nicht zurück; die Rücklesung eines Docs aus dem HTML der Fixture ist ohne Linie
`GLEICH`. Ein Doc aus Markdown (der Entwurf) trägt die Standard-Abstände des Docs, Überschrift 2
18 pt davor und 6 pt danach.
Tabellen aus HTML kommen mit festen Spaltenbreiten an, zusammen 468 pt, die Satzbreite von US
Letter, auch nach dem Wechsel auf A4 (Satzbreite 481,9 pt); ohne Angabe sind die Spalten gleich breit.
`width` in pt oder % an der Zelle nimmt das Doc als Verhältnis und skaliert auf 468 pt, `width` an
`<table>` ändert nichts. `updateTableColumnProperties` setzt danach jede Breite, auch bis 481,9 pt.
Ein Entwurf aus Markdown trägt `EVENLY_DISTRIBUTED` über die ganze Satzbreite.

**Gemessen am 04.10.2026**, ebenfalls in der eigenen Ablage: `create_file` mit `textContent` in
Markdown und `contentMimeType: text/markdown` legt ein Google-Doc an, mit Überschriften, Tabelle,
fett, kursiv und Liste als Formatierung des Docs. `update_spreadsheet` benennt den ersten Tab um und
legt weitere an; ein Schreibaufruf, der parallel zur Umbenennung abging, traf den alten Tab-Namen
und scheiterte, deshalb erst umbenennen, zurücklesen, dann schreiben. `append_values` auf
`'<Tab>'!A1` hängt unter die zuletzt belegte Zeile. **Eine große Antwort legt die Sitzung als Datei
ab**: der CSV-Export eines Tabs mit 1.500 Zeilen (280.691 Zeichen) kam als Pfad, und
`jq -r .content <datei> | base64 -d` ergab genau die 1.500 Zeilen; die Skills dekodieren mit `.claude/scripts/decode-export.py`, weil jq nicht auf jedem Rechner liegt. Eine kleine Antwort steht direkt
in der Antwort; dann wird `content` in eine Datei geschrieben und ebenso dekodiert. Der Export eines
Docs als PDF kommt als Base64 in die Antwort, rund 21 KB je Seite; ein PDF des Proposals gibt es
nicht mehr (§235).

**Gemessen am 04.10.2026 an einer Kopie eines Test-Sheets:** ein `update_spreadsheet` mit
`repeatCell` (Schrift, Umbruch, Ausrichtung, Kopfzeile mit Hintergrund), `updateSheetProperties`
(Fixierung), `updateDimensionProperties` (Breite) und `addBanding` lief in einem Aufruf durch, und
zurückgelesen standen Farbe, Schrift, Fixierung und Breiten. **Feldmasken gehen nur als volle Pfade
mit Komma**; die Form `userEnteredFormat(textFormat,…)` lehnte der Connector mit `Invalid field` ab,
und dann galt kein Request des Aufrufs. `addBanding` ohne `endRowIndex` deckt das ganze Gitter (zurückgelesen `endRowIndex` 1000
bei 1000 Zeilen); ein zweites `addBanding` auf einen gebänderten Bereich lehnt er ab („Einem benannten
Bereich, der bereits abwechselnde Hintergrundfarben aufweist, können keine weiteren abwechselnden
Hintergrundfarben hinzugefügt werden.“), und der ganze Aufruf gilt nicht. Die volle Ausgabe von
`sheet-format.py` für drei Tabs (52 Requests) lief an einer Kopie in einem Aufruf durch; `get_spreadsheet`
mit `ranges` `'Epics'!1:1` und `fields` auf `gridProperties` und `columnMetadata.pixelSize` las
Fixierung und Breiten zurück.

**Der Klassifizierer des Auto-Modus kann das Lesen eines Kundendokuments ablehnen**; gemessen am
03.10.2026 an `read_doc` auf ein Doc in einem Kundenordner („PII Data Handling"). Der Lauf nennt die
Ablehnung wie jede andere und sucht keinen zweiten Weg.

## Der Preflight — bevor der erste Aufruf rausgeht

1. **Such das Werkzeug über die Werkzeug-Suche, nicht über den Namen hier.** Der Name im Aufruf trägt
   ein Präfix aus dem Server, unter dem der Connector angebunden ist; die Endung ist der Name in
   dieser Tabelle. Verglichen wird die **Endung**, nie der ganze Name.
2. **Hol das Schema, bevor du das erste Feld setzt**, über die Werkzeug-Suche.
   Ein geratenes Feld sieht wie ein Aufruf aus und ist keiner.
3. **Fehlt ein Name, such das Werkzeug nach seinem Zweck.** Die Namen in dieser Tabelle und in den
   Refs sind die eines gemessenen Stands; derselbe Connector kommt in mehreren Fassungen, und die
   Namen wechseln (gemessen am 11.10.2026: Atlassian bot `getVisibleJiraProjects` nicht mehr an, nur
   `listJiraProjects` über `executeRead`). Steht der Name nicht in der Werkzeugliste, suchst du über
   die Werkzeug-Suche mit dem Zweck der Zeile; bietet der Connector eine eigene Suche an, wie
   Atlassian mit `discover`, nimmst du sie und rufst die Operation mit dem Werkzeug, das sie nennt
   (`executeRead`, `executeWrite`). Ein anderer Name für denselben Zweck ist kein Ausfall; der
   Bericht nennt ihn. **Nie mit einem Werkzeug, das einen anderen Zweck hat**: was löscht, teilt
   oder unter dem Namen des Leads schreibt, ersetzt kein Werkzeug, das liest.
4. **Fehlt ein Werkzeug für den Zweck, entscheidet die Härte**, und beides steht in der Rückgabe des Laufs.

**Was unter dem Namen des Leads nach außen geht oder löscht, fragt die Sitzung vorher** (§227). Die
Einträge in `.claude/settings.json` greifen nur auf den genauen Namen; heißt ein Werkzeug neu, kommt
der neue Name dazu, und der alte bleibt für ältere Fassungen des Connectors;
was ein Mensch bestätigen soll, fragt der Skill außerdem im Dialog, vor dem Aufruf und mit dem Ziel
im Klarnamen. Lehnt die Sitzung einen Aufruf ab, nennt der Lauf Aufruf und Begründung.

**Der stille Rückfall ist der Fehler, den dieser Vertrag verhindert.** Ein Lauf, der ohne Beleg aus dem
Gedächtnis antwortet, liefert eine plausible Auskunft, die niemand als
ungemessen erkennt. Deshalb ist der Ausfall eine **Auskunft des Laufs**, keine Fußnote im Log.

**Nach Slack wird nicht geschrieben, von keinem Lauf.** Der Kanal ist Material, kein Ziel.

**GitHub hängt an zwei Instanzen, und angesprochen wird die Endung.** Dieselbe Sitzung kann den
Connector zweimal gebunden haben; welche antwortet, entscheidet sie, nicht der Lauf. Die
Wissensbasis wird nur mit `get_file_contents` gelesen, erst `index.md`, dann die Stempel.

**In einer Cloud-Sitzung liest GitHub nur Repos, die an der Sitzung hängen.** Gemessen am
04.10.2026 in einer Sitzung mit nur dem Projekt-Repo: `get_file_contents` auf die Wissensbasis wurde
abgelehnt („is not configured for this session“), `git ls-remote` auf das Template scheiterte an
der Anmeldung. Nach `add_repo` mit `access: read`, ohne Klon, ging `git ls-remote`, und `deny` aus der
`settings.json` des Projekt-Repos griff weiter. Die Läufe, die Wissensbasis oder Template lesen,
hängen sie deshalb zuerst an; auf dem Rechner eines Leads fällt der Schritt weg.

## Was hier nicht steht

- **Kein Zugang, kein Ort, kein Schlüssel.** Was ein Connector braucht, um zu antworten, ist Sache
  der Sitzung, nicht dieses Repos.
- **Kein anderer Server einer Sitzung.** Was hier nicht als Bedarf steht, ist für diese Strecke keine
  Quelle; sein Fehlen ist kein Befund und gehört in keinen Bericht.
- **Die Werkzeugnamen der Kanäle nicht doppelt.** Welcher Aufruf welche Rolle am Board bedient, steht
  je Kanal in `.claude/skills/ticket-factory/ref-<tool>.md` und nur dort. Hier steht, **dass** der Lauf sie braucht.
