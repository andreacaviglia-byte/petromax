# Der Datalayer — was vom Vorhaben maschinenlesbar ist

**Die Einheit ist das Vorhaben** (§224): ein Projekt und, wenn der Lead es so will, der Expert
Service danach. **Der Datalayer ist das Projekt-Repo**, das aus dem Template entsteht; es gibt keinen
zweiten Speicherort und keine Ebene darüber. Zwischen Projekt-Repos gibt es keine Verbindung.

**Das Projekt-Repo ist die Quelle der Wahrheit** (§280) für Anforderungen, Lösungen, Epics, offene
Fragen, Entscheidungen, Kontext und offene Arbeit, **ein Objekt je Datei** mit Kopfzeilen (Form
unten). Drive trägt Ein- und Ausgabedokumente und die Projektionen aus dem Repo: die Anforderungsliste,
Schätzung, Proposal, den Entwurf je Epic und das E2E-Sheet. Confluence trägt nur Freigegebenes,
mit `solutioning` jedes freigegebene Epic (§313); das Board trägt die Umsetzung.

**Die Skills lesen und schreiben die Dateien des Datalayers direkt** (§230) und committen je Lauf
einmal, **direkt auf `main`, und pushen**, auch wenn die Sitzung einen Branch zuweist (§233). Ein
abgelehnter Push heißt: holen, erneut pushen, nie mit Force. Den Umgang je Pfad legt die Tabelle
unten fest; was dort „nie überschrieben" heißt, wird nur neu angelegt. Jede geschriebene Datei wird
zurückgelesen. **Den Verlauf hält Git**; einen eigenen daneben gibt es nicht.

**Jeder schreibende Lauf endet gleich** (§280): `check-repo.py` prüft die Objekte gegeneinander,
dann projiziert der Lauf, in eine Richtung, ins Sheet
([`requirements-list-contract.md`](requirements-list-contract.md)), in die `readme.md` (§288) und in
`way-of-working.md` (§286). Die Projektion schreibt nur, was ein Skill im Repo führt. Zurück ins Repo
kommt nichts aus einer Projektion: Antworten kommen als Material, auch die des Leads; der Kommentar
des Kunden im Entwurf eines Epics ist Material für den nächsten Lauf. **Die Felder der Menschen**
haben ihre Quelle im Sheet und stehen in keiner Datei des Repos (§280, Regel 5); ein Lauf liest sie
dort nur, wenn er den Wert braucht, und nur die schmale Spalte.

**Arbeitsdateien eines Laufs liegen außerhalb des Repos**, in einem eigenen Temp-Ordner je Lauf
(`mktemp -d`, §233): Exporte des Sheets, Ticket-Bodies, Rechenstände. Im Repo steht nur, was die
Tabelle unten nennt.

**Nicht zum Datalayer gehören** das Sheet der Anforderungsliste, das E2E-Sheet, Entwürfe,
Schätzung und Proposal im Drive, die Epic Page in Confluence und ein Ticket auf dem Board. Sie sind
Projektionen oder Umsetzung; was dort anders steht als im Repo, ist eine Abweichung, die der nächste
Lauf vorlegt, keine Wahrheit (§280, Regel 7).

## Die Pfade

Pfade sind relativ zur Wurzel des Projekt-Repos.

| Pfad | Inhalt | Schreiber | Umgang |
|---|---|---|---|
| `project.yml` | der Steckbrief des Vorhabens, Schema unten | kommt als leeres Gerüst aus dem Template, `project-setup` füllt ihn; jeder Skill trägt den Wert ein, den er als erster braucht (§229) | wird überschrieben |
| `baselines.yml` | je Rechtsraum der geltende Stand seiner Pflichtliste aus der Wissensbasis: Pfad, `sha` und Lesedatum, Schema unten (§269) | `requirements-update`, wenn es `minimum-standard/<kennung>.md` liest | wird überschrieben, der Eintrag eines Rechtsraums mit jedem neuen Lesestand |
| `customer.md` | die Sicht auf den Kunden aus dem Material dieses Vorhabens, mit dem Kopf „Stand ‹Datum›. Arbeitsstand, keine Faktenquelle. Massgeblich sind `notes/` und `decisions/`.", solange es kein Sheet gibt „… Massgeblich ist `notes/`." | `material-intake` | wird überschrieben |
| `architecture.md` | die Architektur des Vorhabens, eine Aussage je Zeile, Form unten (§216, §230) | `requirements-update` legt sie mit dem Sheet an; `requirements-update`, `epic-structure`, `solution-design` schreiben sie fort | fortgeschrieben; eine überholte Zeile wird ersetzt (§231) |
| `inputs/` | Material als Text, Transkripte im Zeilenformat mit Zeitstempel, so wie es ist, Namen beim Auftraggeber eingeschlossen (§228); Zugangsdaten, Gesundheitsdaten und Daten der Endkunden ersetzt (§236) | `material-intake`; `requirements-update` für Material aus dem Chat (§282) | nie überschrieben |
| `notes/` | nur Material, Abgleiche und Übergaben: je Quelle und Termin eine Notiz, der Abgleich eines Laufs, die Übergabe an den nächsten | die Skills; `requirements-update` für Material aus dem Chat (§282) | nie überschrieben |
| `requirements/` | je Anforderung eine Datei `REQ-NNN.md`, zugleich die Story (§280, §281), Form unten | `requirements-update` legt sie an und schreibt das Was; `epic-structure` das Feld `epic`; `solution-approach` und `solution-design` die Abschnitte des Wie und `size`; `ticket-factory` nichts | fortgeschrieben; nie gelöscht, eine Kennung wird nie umgewidmet |
| `epics/` | je Epic eine Datei `EP-NNN.md`, Form unten; dazu `critical-path.md`, die Reihenfolge des Bauens (§318) | `epic-structure` legt sie an und schreibt den Kopf bis auf `solve_order`; `solution-solve-order` nur `solve_order`; `solution-design` die Lösung; `requirements-update` nur `clarification`, wenn es eine Zeile in `architecture.md` ersetzt, auf der das Epic baut; `ticket-factory` nur `board_key`; `solution-epic-page` nur `epic_page`; `critical-path.md` schreibt `solution-critical-path` | `EP-NNN.md` fortgeschrieben, nie gelöscht; `critical-path.md` je Lauf überschrieben |
| `gaps/` | je offene Frage eine Datei `GAP-NNN.md`, Form unten (§279) | `requirements-update` schreibt und schließt sie; eine Frage, die im Lauf eines anderen Skills entsteht, legt dieser Lauf an, geschlossen wird sie nur über `requirements-update` | fortgeschrieben; nie gelöscht, eine beantwortete Frage wird geschlossen |
| `todo/` | je interne Aufgabe eine Datei `JJJJ-MM-TT-<slug>.md`, auch der Vorschlag an den `project_owner`, die Arbeitsweise zu ändern (§279, §289), Form unten | jeder schreibende Lauf legt an und schließt, was er erledigt (§359); den Vorschlag legt `project-status` an und schließt nur `project-setup`; abhaken darf jede Person über `project-status` | fortgeschrieben; nie gelöscht, eine erledigte wird `done` |
| `decisions/` | ADRs, flach, Form unten; eine je Entscheidung, auch je Ausklammerung und je Wahl in einer Lösung (§181, §220); der Ordner entsteht mit der ersten ADR | `solution-design`, `requirements-update` | nie überschrieben |
| `tests/` | je E2E-Test eine Datei `E2E-NNN.md`: die Anforderungen, die der Test verkettet, und die Quellen, aus denen er abgeleitet ist, Form unten (§280) | `e2e-testing-sheet` nach dem gleichen Rücklauf des E2E-Sheets | je Test ersetzt, wenn ein Lauf ihn plant; die Datei eines anderen Tests bleibt |
| `way-of-working.md` | wie in diesem Vorhaben gearbeitet wird: der Standard aus `.claude/way-of-working-standard.md`, jede Abweichung sichtbar unter ihrem Abschnitt (§286) | die Projektion am Ende jedes schreibenden Laufs (`project-readme.py`) | wird überschrieben, nie von Hand |
| `way-of-working/` | je Abweichung vom Standard eine Datei `JJJJ-MM-TT-<slug>.md`, auch für eigene Skills, Form unten (§286) | `project-setup`, nur für den `project_owner` (§299) | nie überschrieben |
| `readme.md` | der Überblick über das Vorhaben aus `project.yml`, `gaps/`, `todo/`, `decisions/` und `epics/`, ohne Interna (§278, §288) | die Projektion am Ende jedes schreibenden Laufs (`project-readme.py`) | wird überschrieben, nie von Hand |
| `scope/` | je Snapshot ein Ordner `JJJJ-MM-TT-<anlass>/` mit den vier Tabs des Sheets als TSV (`anforderungen.tsv`, `solutioning.tsv`, `epics.tsv`, `offene-punkte.tsv`) und `manifest.yml`, Form unten: der Stand am Ende der Discovery, den ein Proposal vorlegt und den ein Kunde freigibt (§266, §280 Regel 8) | `requirements-update` am Ende der Discovery (Anlass `discovery`); `solution-proposal` nach dem gleichen Rücklauf des Proposals (Anlass `proposal`) und bei „Kunde hat freigegeben“ (die Freigabe im Manifest, oder ein Snapshot mit Anlass `release`); alle nur über `.claude/scripts/scope-snapshot.py`; `requirements-update` liest | nie überschrieben; an das Manifest wird nur der Eintrag unter `releases` angehängt |

**Ordner entstehen mit ihrer ersten Datei**; einen leeren Ordner gibt es im Repo nicht. Jeder Ordner
außer `scope/` ist flach, ohne Unterordner je Beauftragung (§233). In `inputs/`, `notes/`, `todo/`
und `way-of-working/` beginnt ein Dateiname mit dem Datum, `JJJJ-MM-TT-<slug>.md`; in
`requirements/`, `epics/`, `gaps/` und `tests/` ist er die Kennung. `scope/` trägt genau eine Ebene,
einen Ordner je Snapshot.

**Eine Notiz, die falsch ist, wird zum Wegweiser** auf die gültige: über ihre erste Zeile kommt genau
eine Zeile, die auf die gültige zeigt, der alte Text folgt Zeichen für Zeichen. Die gültige trägt die
Korrekturkette. Gelöscht wird sie nicht.

**Das Material bleibt, wie es ist, bis auf drei Sorten Daten** (§228, §236). Daten über den
Auftraggeber und das Projekt bleiben, auch Namen, Rollen und Mail-Adressen der Menschen beim
Auftraggeber. **Drei Sorten stehen in keiner Datei, die ein Skill schreibt**, weder im Repo noch im
Sheet, in einem Doc, einem Ticket oder auf einer Seite:

| Sorte | Platzhalter (Die festen Wendungen) |
|---|---|
| Zugangsdaten jeder Art: Passwörter, API-Keys, Secrets, Tokens, Schlüssel, ein Endpunkt, der eines trägt (§227) | „‹Zugangsdatum entfernt›", bei `en` „‹credential removed›" |
| Gesundheitsdaten und die übrigen Daten nach Art. 9 DSGVO über erkennbare Menschen | „‹Gesundheitsdaten entfernt›", bei `en` „‹health data removed›" |
| Daten der Endkunden des Auftraggebers, der Menschen, die in seinem Shop kaufen: Namen, Adressen, Mail-Adressen, Telefonnummern, Bestellungen und Kundenkonten, die einem Menschen zuzuordnen sind | „‹Endkundendaten entfernt›", bei `en` „‹end-customer data removed›" |

`material-intake` ersetzt sie vor der Ablage durch den Platzhalter, sagt an, was ersetzt wurde, und
lässt Struktur und Zweck stehen: Spaltenköpfe, Anzahl der Zeilen, was eine Angabe belegen sollte.
Eine Anforderung über eine Produktgruppe, etwa rezeptpflichtige Artikel, ist keine Angabe über einen
Menschen und bleibt. Aus dem Projekt-Repo geht nichts in die Knowledge Base oder ein anderes
übergeordnetes Wissen.

## `project.yml`

**Das Schema steht nur hier;** `project-setup` verweist darauf. Jede Angabe ist gefragt, geprüft,
gemessen oder mit ihrer Fundstelle aus dem Material vorgeschlagen und bestätigt, keine geraten. **Ein Feld, das noch niemand weiß, bleibt leer** (§229); der Skill, der
es zuerst braucht, fragt danach, prüft die Antwort und trägt sie ein.

```yaml
customer: <Name des Kunden>   # ohne Rechtsform im Namen der Hauptdokumente (§263)
key: relaunch               # Kennung des Vorhabens, klein, a-z, 0-9, - und _; steht an jedem Epic-Ticket
title: <Titel des Vorhabens>  # steht im Namen der Hauptdokumente (§263)
language: de                # de | en, keine Variante (§202)
project_folder: <Drive-ID des Projektordners>   # Pflicht; fragt project-setup (§229)
project_owner: <GitHub-Name>   # die Person, die project-setup ausgeführt hat (§289, §294)
project_type: project       # project | expert_service; fragt project-setup aus dem Angebot (§303)
add_ons: [solutioning, design]   # vorab verkaufte Add-ons: solutioning | design | content_migration | e2e_testing (§303)
shops:                      # ein Eintrag je Shop, auch je Expansion Store (§231)
  - key: main
    domain: <domain>
    plan: plus              # der Plan, wie der Admin ihn nennt
    markets: [DE, AT]
    jurisdiction: de        # Kennung des Rechtsraums in minimum-standard/ der Wissensbasis
    audience: b2c           # b2c | b2b | both: an wen der Shop verkauft (§249)
team:                       # das Team der Agentur in diesem Vorhaben, optional (§360); Menschen beim Kunden stehen nicht hier
  - name: <Name, wie er im Material steht>
    role: lead              # die Projektrolle; empfohlen: sponsor | lead | solution_owner | associate | specialist
    github: <GitHub-Name>
    workstream: ""          # optional, beim solution_owner: der Workstream, den er verantwortet
requirements_sheet: ""      # Spreadsheet-ID; legt requirements-update beim ersten Lauf an
e2e_sheet: ""               # Spreadsheet-ID; legt e2e-testing-sheet beim ersten Lauf an (§159)
figma: ""                   # Link zur Figma-Datei (§231)
confluence:                 # trägt der Skill ein, der ihn zuerst braucht, und prüft den Space
  cloud_id: ""
  space: ""                 # immer gequotet: ein persönlicher Space beginnt mit ~
  parent_page: ""
board:                      # trägt der Skill ein, der es zuerst braucht, und prüft es
  tool: ""                  # jira | asana
  project: ""               # Jira-Schlüssel oder Asana-Projekt-GID
```

**`key` steht an jedem Epic-Ticket in der Zeile `Beauftragung:`** (§233): an ihr findet
`ticket-factory` ohne Sheet sein Epic auf einem Board wieder, das mehrere Vorhaben teilen. Der Name
der Zeile bleibt, damit Epics, die schon so auf einem Board stehen, wiedergefunden werden.
`project-setup` schlägt `key` aus dem Titel vor und ändert ihn nicht.

**`project_owner` ist der GitHub-Name der Person, die `project-setup` ausgeführt hat** (§289), bis sie
das Projekt mit `project-setup` an eine andere überträgt (§299). Sie ändert die Einstellungen und die
Arbeitsweise in `way-of-working/`; wer es nicht ist, bestätigt vorher eine Rückfrage, in
`project-setup` und, in Claude Code, beim Hook `.claude/scripts/wow-guard.py` (§301). Ebenso führt sie
`project-upgrade` aus, und nur sie: jeden anderen verweist das Upgrade an sie und endet (§294, §350).
Fehlt das Feld, fragt der Hook bei jeder Änderung in `way-of-working/` nach, und `project-upgrade`
verweist auf `project-setup`.

**Ein Projekt-Admin hat die Rechte des `project_owner`** (§390): wer bei GitHub Admin-Rechte am
Projekt-Repo hat, gilt bei jeder Prüfung von `wow-guard.py` als Owner, ohne Eintrag in `project.yml`
und ohne Anzeige im Dashboard. Owner wird ein Admin dadurch nicht: das Feld setzt und überträgt
weiter nur `project-setup`, und ist es leer, ist es auch für einen Admin der erste Lauf.

**`team` nennt, wer bei uns im Vorhaben arbeitet** (§360): je Person der Name, wie er im Material
steht, die Projektrolle, der GitHub-Name und beim Solution Owner der Workstream. Ein Lauf löst damit
`to` einer Aufgabe in `todo/` auf ([`ref-tasks.md`](ref-tasks.md)). `check-project.py` prüft nur die
Form: eine Liste, jede Person mit `name`; die Rollen im Schema sind eine Empfehlung.

**Projekttyp und Add-ons stehen in `project.yml`, so wie das unterschriebene Angebot sie nennt**
(§303). `project_type` sagt, ob das Vorhaben ein Projekt oder ein Expert Service ist; er wechselt
höchstens einmal, nach dem Go-Live, vom Projekt zum Expert Service im selben Repo (§224), als
Einstellung über `project-setup` (§299). Die Skills lesen ihn hier, statt den Lead zu fragen; ist er
leer, fragt der Skill einmal und nennt `project-setup` (Tabelle unten). `add_ons` nennt die vorab verkauften
Zusatzmodule, jedes optional; eine leere Liste heißt: keines verkauft.

| Add-on | was es schaltet |
|---|---|
| `solutioning` | die Solutioning-Phase und die `solution-*`-Skills |
| `design` | das Design-Epic; `requirements-update` legt seine Standard-Anforderungen an: das Designkonzept (`standard: design-concept`) und die UX/UI-QA vor dem Go-Live (`standard: design-qa`) |
| `content_migration` | die Standard-Anforderung `standard: content-migration`, angelegt von `requirements-update` |
| `e2e_testing` | die Testing-Phase mit `e2e-testing-sheet`; nur damit rechnet die Schätzung den Aufwand für E2E-Testing ein, als Satz auf die Umsetzung (§258); das Proposal nennt keinen Aufwand (§355) |

**Alles andere ist ein normales Thema:** Setup, Datenmigration, Theme-Arbeit und jedes weitere kommen
als Anforderungen aus dem Material, ohne automatisch angelegte Anforderung. Ziele und Themen des
Vorhabens stehen in `customer.md`, nicht hier. Das Solution Proposal ist kein Angebot (§189).
**Die Anforderungsliste gibt es in jedem Vorhaben** (§282): `requirements-update` legt sie beim ersten
Lauf an und trägt `requirements_sheet` ein; ohne das Add-on `solutioning` bleiben ihre Spalten des
Solutionings leer (§283). Ohne das Add-on `design` legt `ticket-factory` keine UX/UI-Story und keinen
UX/UI-Subtask an (§209, §285).

**Jeder Skill prüft `project.yml` zu Beginn** mit
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs <die Felder, die er liest>`.
Exit 1 heißt anhalten: das Script nennt den Verstoß, und ohne `project.yml` oder `project_folder` ist
`project-setup` der nächste Lauf. Exit 3 nennt die leeren Felder. Eine Zeile `skill_header` ist eine
Warnung, kein Verstoß: ein eigener Skill ohne die drei Kopfzeilen aus der `CLAUDE.md` (§225, §271);
der Lauf geht weiter und nennt sie im Bericht.

**Ein leeres Feld trägt der Skill ein, den die Tabelle unten nennt** (§229): er fragt den Lead, prüft die
Antwort, wo es eine Prüfung gibt (Board erreichbar, Space vorhanden), und schreibt sie so ein: `project.yml`
direkt davor lesen, nur die Zeile des Feldes ändern, die ganze Datei schreiben, zurücklesen,
`check-project.py .` laufen lassen, im Commit des Laufs mitnehmen. Sagt der Lead „noch offen", bleibt
das Feld leer, und der Lauf geht so weit, wie er ohne es kommt. Welcher Skill welches Feld einträgt:

| Feld | trägt ein |
|---|---|
| `project_owner` | `project-setup` setzt ihn beim ersten Lauf auf die Person, die es ausführt; danach überträgt ihn nur der `project_owner` mit `project-setup` (§299); kein anderer Skill trägt ihn ein |
| `team` | `project-setup`, beim ersten Lauf und in einem Lauf zum Ergänzen (§360); „noch offen“ ist erlaubt. Kein anderer Skill trägt ein, jeder Lauf, der eine Aufgabe anlegt, liest |
| `customer`, `shops` | `project-setup`, auch in einem Lauf zum Ergänzen. Wer ohne das Feld weiterkommt, arbeitet weiter und nennt `project-setup` im Bericht; sonst hält er an |
| `title`, `language` | `project-setup`; ist es leer, fragen `requirements-update` und `e2e-testing-sheet` beide, `material-intake` und `solution-design` nur `language`. Die übrigen halten an und nennen `project-setup`. Ohne `title` oder `customer` entsteht kein Hauptdokument (§263): `requirements-update` und `e2e-testing-sheet` legen kein Sheet an, Schätzung und Proposal halten an; alle nennen `project-setup` |
| `key` | `project-setup`; ist es leer, fragt `ticket-factory` vor dem ersten Epic-Ticket |
| `project_type`, `add_ons` | nur `project-setup`, aus dem unterschriebenen Angebot (§299, §303). Ist `project_type` leer, fragt der Skill, der ihn liest, den Lead einmal für seinen Lauf, trägt nichts ein und nennt `project-setup` im Bericht |
| `shops[].jurisdiction` | `requirements-update` für die Pflichtliste des Rechtsraums |
| `shops[].audience` | `project-setup` mit den Shops; ist es leer, `requirements-update` zusammen mit `jurisdiction`. Es lesen `requirements-update`, für welchen Shop eine Zeile der Pflichtliste entsteht, und `requirements-review`, ob es den Shop-Bezug dieser Zeilen prüft (§249) |
| `requirements_sheet` | `requirements-update`, indem es das Sheet anlegt |
| `e2e_sheet` | `e2e-testing-sheet`, indem es das E2E-Sheet anlegt |
| `figma` | `ticket-factory`, eine Frage beim ersten Lauf |
| `board.*` | `project-setup`; ist es leer, `ticket-factory` |
| `confluence.*` | `project-setup` (`cloud_id`, `space`); ist es leer, `solution-epic-page` vor der ersten Übertragung, die Elternseite immer dort. Lesende Skills leiten `cloud_id` aus dem Link einer Seite ab, nur für ihren Lauf |

**Fehlt `project.yml`, hält jeder Skill an** und verweist auf `project-setup`. **Fehlt
`.claude/template-version`, hält `project-setup` an**: das Repo stammt nicht aus dem Template (§232).

## `baselines.yml`

**Die Datei trägt je Rechtsraum den geltenden Lesestand seiner Pflichtliste** (§269), die Notiz zum
Abgleich den Stand ihres Laufs; die Notiz bleibt. Sie entsteht mit dem ersten Lesen einer Liste;
fehlt sie, ist noch keine gelesen.

```yaml
de:                              # Kennung des Rechtsraums, wie in shops[].jurisdiction
  path: minimum-standard/de.md   # immer minimum-standard/<Kennung>.md der Wissensbasis
  sha: <sha aus get_file_contents>
  read_on: 2026-10-08            # Lesedatum, JJJJ-MM-TT
```

**Geschrieben wird je Rechtsraum, den der Lauf gelesen hat:** direkt davor lesen, den Eintrag des
Rechtsraums mit allen drei Feldern ersetzen oder anhängen, die übrigen Einträge Zeichen für Zeichen
lassen, die ganze Datei schreiben, zurücklesen, `check-project.py .` laufen lassen, im Commit des
Laufs mitnehmen. `check-project.py` prüft die Datei, wenn es sie gibt, mit `baselines`: je Rechtsraum
genau `path`, `sha` und `read_on`, `path` passend zur Kennung.

## Die Ablage im Drive

**Der Projektordner ist `project_folder`** (§229), nicht der Kundenordner; den legt in der Regel Sales
an, und kein Skill liest oder schreibt in ihm außerhalb des Projektordners. **Eine feste
Ordnerstruktur gibt es nicht** (§231): `project-setup` legt im Drive nichts an; fehlt der
Projektordner, legt ihn ein Mensch an.

**Jeder Skill legt beim ersten Schreiben seinen Unterordner im Projektordner an** und findet ihn
danach über die Liste des Projektordners, nicht über einen Namen im ganzen Drive:

| Unterordner | was dort liegt | wer ihn anlegt |
|---|---|---|
| `Solutioning` | flach nur die Hauptdokumente: das Sheet der Anforderungsliste, die aktuelle Schätzung, das aktuelle Proposal | der erste Skill, der dort schreibt |
| `Solutioning/Epics` | die Entwürfe der Epics, flach (§260) | `solution-design`, direkt vor dem ersten Entwurf |
| `Solutioning/Archiv` | die vorigen Fassungen von Schätzung und Proposal (§260) | `solution-estimate` oder `solution-proposal`, erst wenn es etwas zu verschieben gibt |
| `Testing` | das E2E-Sheet | `e2e-testing-sheet` |

**Den eigenen Unterordner findet oder legt ein Skill so an**, direkt vor seinem ersten Schreiben im
Drive: `Google_Drive.search_files` mit `query` = `parentId = '<project_folder>' and title =
'<Unterordner>' and mimeType = 'application/vnd.google-apps.folder'`. Ein Treffer: seine ID nehmen.
Keiner: `Google_Drive.create_file` mit `title` = der Name, `contentMimeType:
application/vnd.google-apps.folder` und `parentId` = `project_folder`, dann die zurückgegebene ID
nehmen. Zwei: anhalten und beide mit Link nennen; welcher gilt, entscheidet der Lead. Die ID des
Unterordners steht nicht in `project.yml`; jeder Lauf findet ihn neu.

**Die Hauptdokumente heißen `‹Art› ‹title› – ‹Kunde›`** (§263), in natürlicher Schreibweise mit
Groß- und Kleinschreibung, Umlauten und Leerzeichen, ohne Datum und Uhrzeit; die Art steht in der
Sprache aus `language` (§337), das interne Schätzdokument heißt in jeder Sprache deutsch:

| Dokument | Name | Name bei `en` | Art im Script |
|---|---|---|---|
| das Sheet der Anforderungsliste | `Anforderungsliste ‹title› – ‹Kunde›` | `Requirements list ‹title› – ‹Kunde›` | `requirements` |
| das Schätzdokument | `Aufwandsschätzung ‹title› – ‹Kunde›` | `Aufwandsschätzung ‹title› – ‹Kunde›` | `estimate` |
| das Solution Proposal | `Solution Proposal ‹title› – ‹Kunde›` | `Solution Proposal ‹title› – ‹Kunde›` | `proposal` |
| das E2E-Sheet | `E2E-Tests ‹title› – ‹Kunde›` | `E2E tests ‹title› – ‹Kunde›` | `e2e` |

`‹title›` ist `title` aus `project.yml`, wie er dort steht; ein `/` wird `-`. `‹Kunde›` ist
`customer` ohne die Rechtsform am Ende (GmbH, GmbH & Co. KG, AG, KG, OHG, UG, UG
(haftungsbeschränkt), SE, e.K., e. K., Ltd., Inc., LLC, BV, B.V.), sonst unverändert: Groß- und
Kleinschreibung und Umlaute bleiben, überzählige Leerzeichen und ein übrig bleibendes Komma oder `&`
am Ende fallen weg. Dazwischen steht ein Halbgeviertstrich mit Leerzeichen davor und danach. Aus
„Nordlicht Tee GmbH“ und `title: Relaunch Onlineshop` wird „Aufwandsschätzung Relaunch Onlineshop –
Nordlicht Tee“. **Den Namen bildet kein Lauf von Hand**, sondern
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/doc-name.py . <art>`; Exit 1 nennt das leere Feld.
Ein Sheet findet ein Lauf über seine ID in `project.yml`, nicht über den Namen. Schätzung und Proposal
tragen bei jeder Fassung denselben Namen: welche die aktuelle ist, sagt der Ort, und das Datum der
Lesezeit steht im Dokument („Stand: ‹TT.MM.JJJJ›“, bei `en` „As of: 11 Oct 2026“, §264, §337).

**`Epics` und `Archiv` liegen in `Solutioning`** (§260) und werden ebenso gefunden oder angelegt,
mit `parentId` = die ID von `Solutioning` statt `project_folder`. Ein Entwurf, den ein Epic schon über
`Entwurf: ‹Link›` trägt, wird über den Link gefunden, wo er auch liegt. Ist eine neue Fassung von Schätzung oder Proposal angelegt und
zurückgelesen, verschiebt ihr Skill jede ältere Fassung seiner Dokumentart, die flach in
`Solutioning` liegt, nach `Archiv`: derselbe Name, eine andere ID und ein früheres `createdTime`
(§262); scheitert das, bleibt sie liegen, und der Bericht nennt sie.

Alle übrigen Ordner legen Menschen an, nach der Praxis des Teams. Material liest `material-intake`, wo
der Lead es nennt.

## `scope/`: der Stand am Ende der Discovery, bei Proposal und Freigabe

**Der Snapshot hält fest, wogegen ein Kunde freigegeben hat** (§266), und den Stand, mit dem die
Discovery endet (§280, Regel 8).
Ohne ihn ist eine Änderung nach der Freigabe nicht von einer davor zu unterscheiden, und eine Change
Request zeigt sich erst beim Bauen.

**Ein Snapshot entsteht in drei Fällen:** wenn der Lead das Ende der Discovery nennt (Anlass
`discovery`), nach dem gleichen Rücklauf eines Proposals (Anlass `proposal`), und wenn der Lead
bei „Kunde hat freigegeben“ den heutigen Stand statt des letzten Snapshots als freigegeben nennt
(Anlass `release`). Der Ordner heißt `JJJJ-MM-TT-<anlass>`, das
Datum aus der Lesezeit; gibt es ihn schon, bekommt der neue `-2`, `-3` angehängt. **Freigaben
einzelner Epics nimmt er nicht auf.**

**Die vier Tabs** stehen als TSV mit Kopfzeile, so wie gelesen, auf die Breite der Kopfzeile des
Vertrags aufgefüllt, alle vier in derselben Sprache: `Anforderungen` aus dem CSV-Export,
`Solutioning`, `Epics` und `Offene Punkte` über `get_values` über den ganzen Tab, weil der Export
nur den ersten Tab liefert. Wie gelesen wird, steht in der Ref von `solution-proposal`
(`ref-scope.md`).

**Das Manifest** schreibt nur das Script, jeden Wert als String in doppelten Anführungszeichen:

```yaml
date: "2026-10-08"                # das Datum der Lesezeit
occasion: "proposal"              # discovery | proposal | release
language: "de"                    # die Sprache der Kopfzeilen, de | en
read_at: "2026-10-08T14:05Z"      # die Lesezeit des Sheets, UTC
sheet: "<Spreadsheet-ID>"         # requirements_sheet
tabs:                             # je Tab Datei und Zahl der Zeilen unter der Kopfzeile
  - tab: "Anforderungen"
    file: "anforderungen.tsv"
    rows: 280
epics:                            # je Epic des Tabs Epics
  - id: "EP-001"
    source: "page"                # page | draft | none
    link: "<Link der Req Page oder des Entwurfs>"
    version: "4"                  # Req Page: metadata.version; Entwurf: modifiedTime; leer bei none und bei Zusammengeführt
documents:                        # bei discovery: proposal und estimate null
  proposal:
    file_id: "<Datei-ID>"
    created_time: "<createdTime>"
  estimate: null                  # oder file_id und created_time des Schätzdokuments in Solutioning
baselines: null                   # oder der Inhalt von baselines.yml, Zeichen für Zeichen, wenn es die Datei gibt
releases:                         # leer, bis der Lead die Freigabe nennt; immer der letzte Schlüssel
  - date: "2026-10-20"            # der Tag der Freigabe
    released_by: "<wer>"          # nur aus der Angabe des Leads
```

**Die Freigabe** trägt `solution-proposal` bei „Kunde hat freigegeben“ ein: angehängt an das
Manifest des jüngsten Snapshots, wenn das Sheet ihm gleicht oder der Lead dessen Stand nennt; sonst
in einem neuen Snapshot mit Anlass `release`. Ein Snapshot mit Freigabe bekommt keine zweite.

**Der Abgleich ist Pflicht und entscheidet nichts.** `scope-snapshot.py compare` listet je Tab neue,
entfernte und geänderte Zeilen gegen einen Snapshot als mögliche Change Requests. Ihn rufen
`solution-proposal` bei „Kunde hat freigegeben“ und `requirements-update` vor dem Vorlegen, wenn es
einen freigegebenen Snapshot gibt.

## Die festen Wendungen

**Was ein Lauf als feste Wendung in ein Feld des Repos schreibt und was von dort in ein Dokument
wandert, das der Kunde sieht** (Anforderungsliste, Entwurf, Epic Page, Proposal, Ticket), steht in der
Sprache aus `language` in `project.yml` (§337), aus dieser Tabelle. Inhalt, den ein Mensch formuliert
hat, bleibt in seiner Sprache; die feste Wendung um ihn herum folgt dem Projekt. `‹…›` ist die Stelle,
die der Lauf füllt, in der Spalte `en` englisch benannt; ein Datum steht in der Form aus `date`. Die Scripts, die eine Wendung erkennen
oder ausgeben, kennen beide Sprachen; `order-stages.py` liest sie hier (`repo_objects.phrases()`), die
übrigen tragen Kopien, die die Tests des Templates gleich halten. Kein Skill-Name
und kein Dateiname des Repos steht in einer Wendung: der Kunde liest sie ohne das Repo. Ab 1.0.0
bleibt jede Wendung in 1.x, wie sie hier steht.

| Schlüssel | de | en |
|---|---|---|
| `date` | `11.10.2026` | `11 Oct 2026` |
| `source_workshop` | `Workshop ‹Titel› vom ‹Datum›` | `Workshop ‹title› on ‹date›` |
| `source_chat` | `Chat mit dem Lead vom ‹Datum›` | `Chat with the lead on ‹date›` |
| `source_corrected` | `; korrigiert: ‹Quelle›` | `; corrected: ‹source›` |
| `source_added` | `; ergänzt: ‹Quelle›` | `; added: ‹source›` |
| `source_confirmed` | `; bestätigt: ‹Quelle›` | `; confirmed: ‹source›` |
| `source_split` | `; aufgeteilt aus ‹ID›` | `; split from ‹ID›` |
| `source_offer` | `Angebot` | `Offer` |
| `current_unchecked` | `ungeprüft` | `unchecked` |
| `current_standard` | `Leistung dieses Vorhabens, im Shop noch nicht vorhanden.` | `A deliverable of this project, not yet in the shop.` |
| `kb_line_none` | `KB: keiner` | `KB: none` |
| `kb_line_unread` | `KB: nicht gelesen` | `KB: not read` |
| `to_customer` | `Kunde` | `Customer` |
| `question_current_state` | `Wie ist das heute im Shop gelöst?` | `How is this solved in the shop today?` |
| `question_way` | `Welcher Lösungsansatz für ‹Gegenstand›? ‹Lösungsansätze›, Empfehlung ‹Lösungsansatz›` | `Which approach for ‹subject›? ‹options›, recommendation ‹option›` |
| `question_frame` | `Architektur: ‹Frage›` | `Architecture: ‹question›` |
| `clar_gap_open` | `‹GAP› offen` | `‹GAP› open` |
| `clar_gap_blocks` | `‹GAP› blockiert ‹REQ›` | `‹GAP› blocks ‹REQ›` |
| `clar_customer_decides` | `Kunde entscheidet den Lösungsansatz für ‹REQ›` | `Customer decides the approach for ‹REQ›` |
| `clar_solution_open` | `Lösung offen` | `Solution open` |
| `clar_reviewed` | `geprüft; bereit für Tickets` | `reviewed; ready for tickets` |
| `clar_recheck` | `Nachprüfen: ‹Datum›, Architektur „‹Aussage›“` | `Recheck: ‹date›, architecture “‹statement›”` |
| `clar_rechecked_holds` | `Nachgeprüft: ‹Datum›, trägt` | `Rechecked: ‹date›, holds` |
| `clar_rechecked_changed` | `Nachgeprüft: ‹Datum›, geändert` | `Rechecked: ‹date›, changed` |
| `clar_dissolved` | `Aufgelöst am ‹Datum›: ‹Zuordnung›` | `Dissolved on ‹date›: ‹mapping›` |
| `size_confirmed` | `Größe bestätigt` | `Size confirmed` |
| `evidence_measured` | `gemessen am ‹Datum› an ‹Shop›` | `measured on ‹date› at ‹shop›` |
| `evidence_community` | `(noch zu verifizieren)` | `(to be verified)` |
| `stage` | `Stufe ‹n›` | `Stage ‹n›` |
| `stage_waits` | `Stufe ‹n› · wartet auf ‹EPs›` | `Stage ‹n› · waits for ‹EPs›` |
| `stage_none` | `keine Stufe` | `no stage` |
| `page_type` | `Seitentyp: ‹Seitentyp›` | `Page type: ‹page type›` |
| `removed_credential` | `‹Zugangsdatum entfernt›` | `‹credential removed›` |
| `removed_health` | `‹Gesundheitsdaten entfernt›` | `‹health data removed›` |
| `removed_end_customer` | `‹Endkundendaten entfernt›` | `‹end-customer data removed›` |

`date` ist bei `de` `TT.MM.JJJJ`, bei `en` Tag ohne führende Null, Monat in drei Buchstaben, Jahr
(`Jan` … `Dec`); `repo_objects.date_text()` bildet beide. `to_customer` ist der Anfang von `to`
einer Frage an den Kunden („Kunde, ERP-Betreuung“, „Customer, ERP support“); daran erkennt das Proposal
sie. Die Ersatzmarken sind die Platzhalter des Abschnitts „Die Pfade“, in der Sprache des Projekts.

## Die Objekte: eine Datei je Objekt

**Jede Datei beginnt mit einem Kopf in YAML zwischen zwei Zeilen `---`**, darunter steht der Rumpf in
Markdown. **Feldnamen, Werte und die Überschriften des Rumpfs sind englisch** (§12, §295); der Titel
einer Anforderung und jede offene Frage in `gaps/`, Musterfragen eingeschlossen, stehen in der Sprache
aus `language` (§337), die wörtliche Formulierung bleibt im Material; was ein Mensch sonst geschrieben
hat, Beschreibung und Kriterien, bleibt in der Sprache, in der es erfasst wurde. Sheet, Ticket und Seite zeigen die Werte in der Sprache des Projekts; die Zuordnung
steht in [`requirements-list-contract.md`](requirements-list-contract.md). Ein Feld, das noch niemand
weiß, bleibt leer (`""`). **Die Felder der Menschen stehen in keiner Datei** (§280, Regel 5): Cluster
(der Workstream, §336), Owner, Stunden, Kommentar, der Prüfpunkt eines Epics, Verantwortlich und Bis
einer Frage.

### `requirements/REQ-NNN.md`: die Anforderung, zugleich die Story

**Sie trägt das Was, den Lösungsansatz und die Angaben, die er braucht, ohne Gewerk** (§280, Regel 2). Das
Gewerk entsteht erst beim Anlegen der Tickets (§281); ein Board-Schlüssel steht nicht in der Datei.

```yaml
---
id: REQ-012
title: <der Bedarf in wenigen Worten>   # in der Sprache aus language (§337); ohne Schlüssel eines Shops (§307)
shops: []                  # die `key` aus shops in project.yml, für die sie gilt; leer: alle Shops (§307)
status: open               # open | confirmed | rejected | duplicate (§283)
duplicate_of: ""           # nur bei duplicate: die Kennung, die gilt
priority: must-have        # must-have | nice-to-have; nice-to-have nur, wenn der Kunde es ausdrücklich sagt, mit der Stelle in source (§327)
scope: ""                  # "" | in_scope | out_of_scope; gesetzt mit der Scope-Freigabe (§283)
epic: ""                   # EP-NNN; setzt epic-structure, genau ein Epic (§150)
design_needed: open        # yes | no | open
interface_needed: open     # yes | no | open (§205)
live: ""                   # "" | yes | no | partial | verify: tut der Shop es heute (§283)
source: <Quelle>           # Termin, Notiz, Chat mit dem Lead, Zeile aus architecture.md; bei einer Teilung dazu "; aufgeteilt aus REQ-NNN" (en "; split from REQ-NNN"); feste Wendungen in der Sprache aus language (§337)
size: ""                   # "" | S | M | L | XL; nie Stunden (§280, Regel 10); Vorschlag von solution-approach, endgültig solution-design (§326)
size_estimate_approach: "" # "" | S | M | L | XL; die Größe aus solution-approach, mit size geschrieben, danach unverändert (§357)
effort_estimate_model: ""  # "" | Stunden als Zahl, Dezimalpunkt erlaubt; nur mit solutioning, gesetzt von solution-design (§357)
classification: []         # die Art des gewählten Lösungsansatzes, eine oder zwei, Werte unten in „Die Klassifizierung“ (§314, §324)
depends_on: []             # die Kennungen von Anforderungen, Epics und ADRs, auf denen der Lösungsansatz aufbaut
solution_status: ""        # "" | proposed | decided | blocked
own_sections: ""           # nur bei einem Seitentyp: die Annahme als Zahl, höchstens so viele eigene Sections (§285)
design_reference: ""       # optional: Link auf das Design (§285)
standard: ""               # nur bei einer Standard-Anforderung eines Add-ons: design-concept | design-qa | content-migration (§303)
---
```

| Abschnitt im Rumpf | Inhalt | schreibt |
|---|---|---|
| `## Description` | der Soll-Zustand: was gelten soll, nicht womit | `requirements-update` |
| `## Acceptance criteria` | ein Kriterium je Listenpunkt, an dem die Story abgenommen wird (§281) | `requirements-update` |
| `## Current state` | der Ist-Zustand, wie die Aufnahme ihn vorfindet; „ungeprüft“ (`current_unchecked`, `en`: „unchecked“, §337), wenn das Material ihn nicht nennt | `requirements-update` |
| `## Approach` | die Lösungsansätze, ohne Gewerk, höchstens drei; je Lösungsansatz ein Unterabschnitt `### <Name>` mit einem Satz und den Zeilen `Fit:`, `Größe:` und `KB:` (§268, §326), der empfohlene oder gewählte zuerst, unter ihm bei mehreren `Empfehlung:` und im Expert Service `Gewählt:` (§401); hinter `Größe:` in Klammern Bau, Konfiguration und Pflege. Eine Datei mit einem Lösungsansatz ohne diese Zeilen und ohne Klammer bleibt gültig (§338) | `solution-approach` mit `solution_status: proposed`, `solution-design` mit `decided` |
| `## Details` | die Angaben, die der Lösungsansatz braucht, ohne Gewerk | `solution-design` |
| `## Sections` | nur bei einem Seitentyp, nach der Übergabe des Designs: je angepasste oder neue Section ein Listenpunkt mit Frame-Link; `check-repo.py` zählt sie gegen `own_sections` (§285) | `requirements-update` |

**`size_estimate_approach` und `effort_estimate_model` sind die Schätzungen des Modells** (§357),
zur Kalibrierung gegen die Schätzung des Menschen und den Ist-Aufwand, keine Zusage:

- **`size_estimate_approach`** schreibt `solution-approach` mit demselben Wert wie `size`, auch wenn
  es einen Vorschlag auf Ansage des Leads ersetzt; sonst fasst es kein Lauf an. So bleibt die frühe Größe stehen, wenn `solution-design` `size` entscheidet.
- **`effort_estimate_model`** sind Stunden, die das Modell schätzt, **nur in einem Vorhaben mit dem
  Add-on `solutioning`** und nur für eine Anforderung mit `solution_status: decided`. Nur
  `solution-design` setzt sie, mit der Wahl, bevor der Lead schätzt, und neu, wenn sich die Lösung
  ändert; kein anderer Lauf trägt sie nach. Die Zahl ist die Rohschätzung des Modells, ohne
  Korrektur und ohne Spanne; ihre Zerlegung je Teil mit Begründung steht in
  `.claude/metrics/estimates/REQ-NNN.md`, versteckt und von keinem Skill gelesen. Wie sie entsteht, legt
  `solution-design` fest. Den Faktor je Bereich, mit dem sie korrigiert wird, trägt
  [`calibration.md`](calibration.md); die kalibrierte Zahl wird gerechnet, nie gespeichert. Ohne
  `solutioning` schreibt kein Lauf eine Stundenzahl, auch nicht im Expert Service.

**Beide gehen in kein Dokument, das der Kunde liest** (Anforderungsliste, Entwurf, Epic Page,
Proposal, E2E-Sheet, Ticket), und die interne Schätzung rechnet nur mit `Aufwand (h)`. Die Zahl des
Menschen bleibt in 1.x `Aufwand (h)` im Tab `Solutioning` (§280, Regel 5); im Repo kommt sie erst mit
2.0 als `effort_estimate_human`, der Ist-Aufwand als `effort_actual_hours` mit einem eigenen Vorhaben.
Fehlt ein Feld, ist es leer. `check-repo.py` prüft `size_estimate_approach` als `value` und
`effort_estimate_model` als `effort_estimate`: eine Zahl oder leer, gesetzt nur mit `solutioning` und
bei `decided`.

**Eine User Story trägt die Anforderung nicht** (§323): sie ist eine Ableitung aus Ist, Soll, FC und
UC und steht im Entwurf, auf der Epic Page und im Ticket, nach
[`user-story-contract.md`](user-story-contract.md).

**`standard` markiert die Standard-Anforderungen, die `requirements-update` aus den Add-ons in
`project.yml` anlegt** (§303): mit `design` das Designkonzept (`design-concept`) und die UX/UI-QA vor
dem Go-Live (`design-qa`, §285), mit `content_migration` die Content-Migration (`content-migration`).
Fehlt das Feld, ist es leer. Daran erkennen der Schnitt (`check-cut.py`) und die Schätzung die
UX/UI-QA, und `requirements-review`, ob eine Standard-Anforderung fehlt.

**Ein Lösungsansatz mit `solution_status: proposed` ist ungeprüft** (§275): er erscheint nicht im Sheet,
in keinem Entwurf, auf keiner Seite und keinem Board. `blocked` heißt, der Lösungsansatz hängt an einer offenen Frage mit
`blocking: yes`.

### Die Klassifizierung

**Die Art eines Lösungsansatzes hat acht Werte, und dieser Vertrag ist ihr einziger Besitzer** (§324): Wert,
Anzeige, Gewerk und Größe nach der Größentabelle stehen nur hier. Anforderungsliste, Ticket, Entwurf,
Skills und Scripts zeigen und prüfen dieselben acht; ein anderer Wert, auch `integration` oder `data`,
ist ungültig, und `check-repo.py` meldet ihn als `value`.

| Wert | Anzeige `de` | Anzeige `en` | Gewerk | Größe nach Tabelle |
|---|---|---|---|---|
| `shop` | Shopify-nativ | Shopify native | Konfig | S |
| `theme_native` | Theme-nativ | Theme native | Konfig | S |
| `app` | Public App | Public app | Konfig | S bis M |
| `theme` | Theme-Anpassung | Theme customization | DEV | M bis L |
| `custom_app` | Custom App | Custom app | DEV | L bis XL |
| `integration_connector` | Standard-Konnektor | Standard connector | Schnittstelle | M bis L |
| `integration_middleware` | Middleware | Middleware | Schnittstelle | L |
| `integration_custom` | Custom Schnittstelle | Custom integration | Schnittstelle | XL |

| Wert | heißt |
|---|---|
| `shop` | eine native Funktion von Shopify, Konfiguration im Admin |
| `theme_native` | was das Theme schon kann, eingestellt im Theme Editor: vorhandene Sections, Blocks, Einstellungen, ohne Code (§314) |
| `app` | eine öffentliche App aus dem App Store, eingerichtet in der App |
| `theme` | eine Anpassung an der Storefront, mit Code im Theme |
| `custom_app` | eine eigene App, Function oder Extension |
| `integration_connector` | ein fertiger Konnektor zu einem System der Systemlandschaft in `architecture.md`: Warenwirtschaft, ERP, PIM, Fulfillment |
| `integration_middleware` | eine Middleware zwischen Shopify und einem System der Systemlandschaft |
| `integration_custom` | eigener Code, der Daten zwischen Systemen bewegt, laufend oder einmalig |

**Die Abgrenzung:** ein Standard-Konnektor verbindet mit einem System der Systemlandschaft. Ein
Dienst, der als App kommt und in der App eingerichtet wird, etwa E-Mail-Marketing oder Bewertungen,
ist `app`, auch wenn er Daten synchronisiert. Ein Feed ist keine Schnittstelle, sondern `shop` oder
`app`.

**Welche Middleware, sagen die Best Practices der Knowledge Base** ([`kb-contract.md`](kb-contract.md));
im Template steht kein Name. Die Wahl ist eine Entscheidung des Projekts mit ADR und der Zeile
`Integrationsschicht` in `architecture.md` (§216).

**Datenmigration ist ein Thema, keine Klassifizierung**: das Thema trägt die Domäne des Epics,
`data_migration` oder `content_migration` (§252). Eine Migration wird über einen der Lösungsansätze gelöst: der
CSV-Import im Admin ist `shop`, eine Import-App aus dem App Store `app`, eine Middleware
`integration_middleware`, ein eigenes Skript `integration_custom`.

**Das Gewerk folgt der Klassifizierung, bei einer Migration der Domäne** (§281): in einem Epic der
Domäne `data_migration` ist es `Schnittstelle`, gleich über welchen Lösungsansatz; in einem Epic der Domäne
`content_migration` `Konfig`. Ein Feed bleibt `Konfig`; eine Anforderung im Epic der Domäne `design`
trägt keine Klassifizierung und das Gewerk `UX/UI` (§297). Die Datei der Anforderung trägt das Gewerk
nie; es entsteht beim Anlegen der Tickets (§280, Regel 2).

**Die Anzeige mit Namen:** im Block `Lösungsansatz` des Tickets (§312) steht je Klassifizierung ihre
Anzeige mit dem Namen dessen, was den Lösungsansatz trägt, darunter die Kurzbeschreibung: `Public App: ‹Name der
App›`, `Standard-Konnektor: ‹Name› an ‹System›`, `Middleware: ‹Name› an ‹System›`, `Custom
Schnittstelle: an ‹System›`; bei `en` steht statt „an“ „to“ (§337). Bei diesen vier ist der Name Pflicht. Im Sheet zeigt `Klassifizierung`
nur die Anzeige; der Name steht in der Lösungsoption. Wie groß ein Lösungsansatz ist und welcher gewinnt, sagt
[`solution-choice-contract.md`](solution-choice-contract.md).

### `epics/EP-NNN.md`: das Epic und seine Lösung

```yaml
---
id: EP-003
title: <Titel>
domain: <aus der festen Liste>   # Werte in requirements-list-contract.md (§252)
summary: <das Kriterium des Schnitts in einem Satz, ohne Lösungsansatz>
status: open               # Werte in requirements-list-contract.md
information: thin          # thin | partial | solid
clarification: ""          # was das Epic aufhält, oder dass es bereit ist: eine Wendung clar_… aus „Die festen Wendungen“, in der Sprache aus language, ohne Skill- und Dateinamen (§337)
draft: ""                  # Link zum Entwurf im Drive
solve_order: ""            # die Reihenfolge des Lösens, 1 zuerst, gleiche Zahl gleichrangig; setzt solution-solve-order, nur mit solutioning; sonst leer (§318, §403)
epic_page: ""              # Link zur Epic Page in Confluence; mit solutioning Pflicht nach der Freigabe, vor den Tickets; schreibt solution-epic-page (§313)
board_key: ""              # der Schlüssel des Epic-Tickets; den Schlüssel einer Story trägt keine Datei
---
```

**Welche Anforderungen zum Epic gehören, steht nur in deren Feld `epic`**, nicht hier; die Liste im
Sheet entsteht daraus. Der Rumpf ist die Lösung des Epics in der Gliederung des Entwurfs
([`draft-and-epic-page-contract.md`](draft-and-epic-page-contract.md)); der Entwurf im Drive ist ihre Projektion, ein Google-Doc, das
`solution-design` einmal anlegt und gezielt fortschreibt (§302).
**Die Reihenfolge des Lösens steht in `solve_order` der Epics**, gesetzt von `solution-solve-order`
nach dem Schnitt, nur mit dem Add-on `solutioning` (§318, §403); `solution-design` schlägt danach das
nächste Epic vor. Ist `solve_order` leer, gilt die Nummer des Epics. **`epics/critical-path.md`** trägt die
Reihenfolge des Bauens in der Form unten, aus `depends_on` der gelösten Anforderungen, und wird je
Lauf überschrieben.

### `epics/critical-path.md`: die Reihenfolge des Bauens

`solution-critical-path` schreibt die Datei je Lauf ganz neu, auch wenn sich nichts geändert hat;
`solution-review` und `ticket-factory` lesen sie:

```markdown
# Reihenfolge der Epics, ‹TT.MM.JJJJ›

Vorhaben ‹key›, gelesen ‹TT.MM.JJJJ HH:MM› auf Commit ‹kurzer Hash›.

## Fundament-Fragen
‹je Zeile des Fundaments in `architecture.md`, die `offen` oder `widersprüchlich` ist: die Frage, ihre treibende Anforderung, ob die Antwort die Kanten ändert; sonst „Keine offen.“›

## Stufen
| Stufe | Epic | Titel | wartet auf | wartende Epics | Grund der Folge | parallel möglich mit |

## Zeile im Epic-Ticket
‹je Epic eine Zeile `- ‹Epic-ID›: ‹Zeile aus order-stages.py›`, etwa `- EP-004: Stufe 2 · wartet auf EP-001, EP-002`›

## Kritischer Pfad
‹die Ketten aus order-stages.py, `EP-001 → EP-002 → EP-005`; ohne Kante „keiner“›

## Durchstiche
| Epic | Anforderung | Risiko, das er prüft | was er umfasst | was er auslässt | Beleg |

## Lieferungen des Kunden
| Lieferung | Epic | gebraucht ab Stufe | Beleg |

## Abhängigkeiten
| ID | Epic | Rolle | hängt ab von | wird gebraucht von | Blocker (Adressat, Belegstand) | Beleg |
‹nur Anforderungen mit Rolle, Kante oder Blocker; darunter ein Satz: „‹Zahl› weitere Anforderungen ohne Abhängigkeit.“›

## Zyklen
## Früh an Dritte
‹Fragen, deren Antwort lange Vorlauf hat, mit Adressat und den Epics, die warten›
```

`wartet auf` sind die Epics der Kanten dieses Epics, leer ohne Kante. Varianten
stehen als eigene Tabellen `Stufen (‹Variante›)` und `Zeile im Epic-Ticket (‹Variante›)` darunter.

**Ohne Beleg keine Aussage.** Ein Durchstich steht nur mit einem Risiko, das eine Stelle im Repo
oder in einer Notiz trägt; eine Lieferung des Kunden nur, wenn eine Anforderung, eine Frage oder eine
Notiz sie nennt (Daten, Texte, Bilder, Zugänge, eine Entscheidung), und `gebraucht ab Stufe` ist die
Stufe des ersten Epics, das sie braucht. Ein Abschnitt ohne Beleg trägt den Satz „Nicht belegt.“

### `gaps/GAP-NNN.md`: eine offene Frage

```yaml
---
id: GAP-007
kind: discovery            # discovery | solutioning | decision (§279)
to: <Rolle oder Person>    # an wen die Frage geht
concerns: [REQ-012]        # die Anforderungen und Epics, die sie betrifft
blocking: no               # yes | no: hängt eine Anforderung oder Lösung an der Antwort
status: open               # open | closed
opened: 2026-10-10         # JJJJ-MM-TT
---
```

**Eine Frage anlegen**, für jeden Lauf, der eine stellt (§279): je Frage eine Datei, die Kennung
fortgezählt von der höchsten in `gaps/`.

| Teil | Was der Lauf schreibt |
|---|---|
| `kind` | `discovery` für eine Frage zum Was; `decision`, wenn eine Wahl beim Kunden oder Lead liegt, etwa ein Widerspruch in der Architektur oder eine Änderung des Scopes; `solutioning` für eine Frage zur Lösung, gestellt von den Läufen des Solutionings |
| `to` | eine Rolle („Kunde, ERP-Betreuung“, bei `en` „Customer, ERP support“; `to_customer`, §337), keine Person, wenn das Material keine nennt |
| `concerns` | jede Anforderung, die an der Antwort hängt; eine Frage, die mehrere betrifft, steht **einmal** mit allen. Betrifft sie keine, weil die Anforderung erst mit der Antwort entsteht, steht sie in der Notiz und im Bericht, nicht in `gaps/`: eine Frage ohne Ziel lehnt `check-repo.py` ab |
| `blocking` | `yes` nur, wenn ohne die Antwort kein Lösungsansatz für die Anforderung zu wählen ist |
| `opened` | das Datum des Laufs |
| der Rumpf | die Frage, so wie sie gestellt wird, in der Sprache des Vorhabens; **ihr erster Satz ist der Kurztext**, den das Sheet zeigt, darum steht die Frage selbst vorn. Nennt das Material eine Frist, steht sie hier als Satz; `Verantwortlich` und `Bis` setzen Menschen im Tab `Offene Punkte` (§280, Regel 5) |

**Im Zweifel nicht blockierend.** Eine blockierende Frage hält in `solution-design` die Wahl an; eine zu
viel hält die Arbeit ohne Grund auf, eine zu wenig bleibt trotzdem als Frage stehen.

Der Rumpf trägt die Frage; ihr erster Satz ist der Kurztext, den das Sheet zeigt. **Der ganze Text geht
wörtlich zum Kunden** (Anforderungsliste, Proposal) und ist deshalb, wie der Titel (§137), einer, den
er ohne das Repo versteht: kein Werkzeug-Jargon („laut Arbeitsweise“, „Annahme des Leads“), keine
Dateinamen, keine Namen von Skills, keine Quelle als Laufwort. Was der Lead zur Frage weiß, steht
nicht im Text, sondern als Material in `notes/` (§287). **Geschlossen wird
eine Frage mit der Antwort und ihrer Quelle** unter `## Answer`, aus Material, nie durch einen Eintrag
im Sheet (§276); beantwortet eine ADR sie, nennt die Antwort sie. Verantwortlich und Bis sind Felder
der Menschen im Tab `Offene Punkte` und stehen nicht in der Datei.

### `tests/E2E-NNN.md`: woraus ein E2E-Test stammt

**Das E2E-Sheet bleibt der Ort für Status, Runde und Ergebnisse** (§256, §280, Regel 5): sie sind Felder der
Menschen. Die Datei hält fest, welche Anforderungen der Test verkettet und aus welcher Fassung welcher
Quelle er abgeleitet ist, damit ein Lauf nach einer geänderten Seite den betroffenen Test findet.

```yaml
---
id: E2E-001
testcase: <der Text in Testfall>   # der Schlüssel im Sheet
requirements: [REQ-001, REQ-002]   # in der Folge des Ablaufs
sources:
  - epic: EP-001
    kind: draft                    # page | draft
    version: <Fassung>             # Epic Page: metadata.version; Entwurf: modifiedTime
    link: <Link der Epic Page oder des Entwurfs>
---
```

Der Rumpf trägt, was `e2e-testing-sheet` je Test ins Sheet projiziert, in der Form seiner Ref.

### `todo/JJJJ-MM-TT-<slug>.md`: eine interne Aufgabe

```yaml
---
title: <was zu tun ist>
to: <GitHub-Name aus team, sonst die Projektrolle>
status: open               # open | done
concerns: []               # optional: Kennungen oder der Abschnitt von way-of-working.md
done_by: ""                # optional, nur bei done: der GitHub-Name dessen, der abhakt (§359)
done_at: ""                # optional, nur bei done: JJJJ-MM-TT
---
```

Der Rumpf sagt, was zu tun ist und warum. **Wer eine Aufgabe auf `done` setzt, schreibt das Ergebnis
dazu** (§359): `done_by`, `done_at` und am Ende des Rumpfs eine Zeile `Erledigt <TT.MM.JJJJ>: <was
herauskam>`; die Datei wird nie gelöscht. Auf `done` setzen darf der Lauf, der ihre Arbeit tut, und
jede Person im Projekt über `project-status`; den Vorschlag zur Arbeitsweise schließt nur
`project-setup` (§299). Wann ein Lauf anlegt, schließt oder offen lässt und wie er `to` auflöst, sagt
[`ref-tasks.md`](ref-tasks.md). **Ein Vorschlag zur Arbeitsweise** geht an den
`project_owner` und nennt Abschnitt, gewünschte Änderung, Grund und wer vorschlägt (§289), in dieser
Form, Pfad `todo/<Datum>-wow-<slug>.md`:

```
---
title: "Arbeitsweise: <Abschnitt> – <was in drei Worten>"
to: <project_owner>
status: open
concerns: ["<Abschnitt>"]
---

Abschnitt: <Abschnitt>
Gewünschte Änderung: <was anders sein soll>
Grund: <warum>
Vorgeschlagen von: <GitHub-Name aus --whoami, sonst der Name, den die Person nennt>
```

### `way-of-working/JJJJ-MM-TT-<slug>.md`: eine Abweichung vom Standard

```yaml
---
date: 2026-10-10
section: <die Überschrift des Abschnitts im Standard>
reason: <warum dieses Vorhaben abweicht>
by: <GitHub-Name des project_owner>
proposed_by: ""            # nur, wenn sie aus einem Vorschlag in todo/ kommt
skill: ""                  # nur bei einem eigenen Skill: sein Name
---
```

Der Rumpf sagt, was in diesem Vorhaben anders ist; die Projektion setzt ihn unter seinen Abschnitt
in `way-of-working.md` (§286). Pfad `way-of-working/<Datum>-<slug>.md`, das Datum von heute
(`date +%F`), der Slug kurz, klein, mit `-`.

## `architecture.md`

**Die Datei trägt den geltenden Stand der Architektur, die ADRs tragen das Warum** (§216). Eine Zeile
trägt eine Aussage und keine Begründung. Oben steht das Fundament, darunter stehen die Festlegungen,
die mehrere Epics betreffen (§230).

```markdown
# Architektur

| Aussage | Status | Quelle/ADR | gestützt von |
|---|---|---|---|
| Shops, Pläne, Markets oder Expansion Stores: stehen in `project.yml`, `shops` | offen | | |
| Bauform der Storefront: Theme, headless oder gemischt | offen | | |
| Integrationsschicht: ob, welche, wer betreibt | offen | | |
| Systemlandschaft: welche Systeme angebunden sind und welches führt | offen | | |
```

| Status | `Quelle/ADR` verweist auf |
|---|---|
| `belegt` | die Quelle |
| `entschieden` | die ADR in `decisions/` |
| `offen` | die offene Frage in `gaps/`, `GAP-NNN` (§279) |
| `widersprüchlich` | beide Aussagen und die offene Frage in `gaps/` |

`gestützt von` nennt die Epics, deren Lösung auf der Zeile baut, `EP-003, EP-007`; `solution-design`
trägt sein Epic ein.

**Das Fundament steht in jeder Datei:** die vier Zeilen oben. `requirements-update` legt die Datei mit
ihnen an, wenn er das Sheet anlegt (§229); jede Fundament-Frage, zu der `project.yml` keinen Wert trägt,
steht dort als `offen`. **Die Zeile zu den Shops verweist auf `project.yml` und schreibt die Werte
nicht ab** (§180). Weitere Zeilen entstehen nur, wo eine Lösung etwas festlegt, das andere Epics
betrifft: ein Master, ein Muster, eine App, eine Function, ein Schlüssel.

**Baut ein Vorhaben mehrere Shops, trägt eine Zeile, die nur für einen gilt, seinen Schlüssel vorne
in der Aussage**, `b2b: Preise kommen aus dem ERP` (§231). Eine Zeile ohne Schlüssel gilt für alle
Shops. Hier bleibt die Form, anders als bei Anforderung und ADR: eine Zeile ist kein YAML (§307).

**Fortgeschrieben wird so, und nur so:**

- Eine neue Aussage ist eine neue Zeile am Ende der Tabelle.
- An einer bestehenden Zeile ändern sich `Status` und `Quelle/ADR`; `gestützt von` wächst und
  verliert nichts.
- **Eine überholte Zeile wird ersetzt, nicht durchgestrichen** (§231): an ihrer Stelle steht die neue
  Aussage mit ihrem Status und ihrer Quelle, `gestützt von` bleibt. Den alten Stand hält Git. Der
  Lauf, der ersetzt, markiert die Epics unter `gestützt von` im Tab `Epics` als nachzuprüfen
  ([`requirements-list-contract.md`](requirements-list-contract.md)) und nennt im Commit die ersetzte
  Aussage.
- Einen Widerspruch überschreibt kein Lauf: die Zeile wird `widersprüchlich`, und der Lauf, der ihn
  findet, legt die Frage in `gaps/` an (§279).
- **Keine Zeile wird gelöscht, keine umsortiert**, die Kopfzeile bleibt, wie sie ist.

**Geprüft wird vor jedem Schreiben gegen die gelesene Fassung:** Kopf und Kopfzeile unverändert;
jede gelesene Zeile steht noch an ihrer Stelle, neue nur am Ende; ein Status ist einer der vier oben;
in `gestützt von` fehlt kein Eintrag, der dastand. Hält die neue Fassung das nicht, wird sie nicht
geschrieben.

## Der Shop-Bezug

**Für welche Shops eine Anforderung oder eine ADR gilt, sagt ihr Feld `shops`** (§307): die `key` aus
`shops` in `project.yml`, als Liste in eckigen Klammern; leer heißt, sie gilt für alle Shops (§231).
**Der Titel trägt keinen Schlüssel.**

**Angezeigt wird der Bezug hinten am Titel**, erzeugt aus dem Feld, in Anforderungsliste, Ticket,
Entwurf, Epic Page, Proposal und Schätzung, mit dem Schlüssel in Großbuchstaben:

| gilt für | Anzeige `de` | Anzeige `en` |
|---|---|---|
| einen Shop | `Staffelpreise (B2B)` | `Tier pricing (B2B)` |
| zwei Shops | `Staffelpreise (B2B & B2C)` | `Tier pricing (B2B & B2C)` |
| drei oder mehr, nicht alle | `Staffelpreise (3 Shops)` | `Tier pricing (3 shops)` |
| alle Shops, auch bei leerem Feld | `Staffelpreise (alle Shops)`; in der Anforderungsliste keine Klammer | `Tier pricing (all shops)`; in der Anforderungsliste keine Klammer |
| ein Projekt mit nur einem Shop | keine Klammer | keine Klammer |

Die Schlüssel stehen in der Folge von `shops` in `project.yml`. In der Anforderungsliste sagt die
Spalte `Shops`, für welche Shops eine Anforderung gilt; deshalb trägt dort eine Anforderung für alle
Shops keine Klammer. `repo_objects.shops_title()` erzeugt die Anzeige für die Scripts;
`python3 .claude/scripts/repo_objects.py <repo> REQ-012` gibt sie für einen Lauf aus, der sie von Hand
schreibt (Ticket, Entwurf, Epic Page).

## Die Kennungen

**Eine Anforderung trägt `REQ-` und drei Ziffern: `REQ-001`**, fortgezählt über die Anforderungen
dieses Vorhabens (§230). Die Kennung ist im Repo eindeutig, wird nie neu vergeben und nie
umgewidmet; eine falsch geschnittene Anforderung geht auf `rejected` oder `duplicate`. **Eine neue
Kennung zählt vom Maximum in `requirements/` und am Board dieses Vorhabens weiter** (§230); Repos
anderer Vorhaben zählen nicht mit. Ein Board, das zwei Vorhaben teilen, bleibt abgedeckt, weil die
Kennung vom Maximum am Board weiterzählt. **Sie sagt nichts über Thema, Workstream oder
Lösungsansatz**: eine Anforderung, die beim Schnitt in ein anderes Epic wandert, behält sie. Epics
tragen `EP-001`, offene Fragen `GAP-001` (§279), E2E-Tests `E2E-001`, Entscheidungen `ADR-001`; jede
Kennung zählt von der höchsten in ihrem Ordner weiter.

## Die ADR in `decisions/`

Eine Datei je Entscheidung, `ADR-001-<slug>.md`: drei Ziffern, `<slug>` englisch, klein, kebab-case;
die Nummer zählt von der höchsten im Ordner weiter.

```yaml
---
id: ADR-001
title: <Titel>
status: accepted            # proposed | accepted | superseded
supersedes: ADR-000         # nur, wenn sie eine frühere ablöst
shops: [b2b]                # die `key` aus shops in project.yml, für die sie gilt; leer: alle Shops (§307)
---
```

Der Rumpf trägt die Entscheidung mit Begründung und die verworfenen Lösungsansätze mit ihrem Grund; die
stehen nicht auf der Req Page (§153). Zwei Läufe legen ADRs an, je in ihrer Form:
`requirements-update` hält eine Entscheidung aus dem Material fest, auch jede Ausklammerung, mit den
Zeilen `Frage:`, `Entscheidung: … (‹Quelle›)`, `Verworfen: …` und `Betrifft: ‹Kennungen›`;
`solution-design` hält die Wahl eines Lösungsansatzes fest, mit den Abschnitten `## Entscheidung`,
`## Begründung`, `## Verworfene Optionen` und `## Betroffene Anforderungen`. Den Grund einer
Ausklammerung liest `solution-proposal` aus der Zeile `Entscheidung:`. Bei einer Public App trägt die ADR aus `solution-design` die Evaluierung unter
`## Evaluation`, eine Tabelle Kandidat × Muss-Kriterium mit Ergebnis und Beleg (§320,
`solution-design/ref-adr.md`); sie entsteht auf `proposed` vor der Wahl und bleibt dort, solange ein
Kriterium des gewählten Kandidaten unbelegt ist. **Kippt eine Entscheidung auf `accepted`, entsteht eine neue
mit `supersedes`**, und in der alten ändert sich nur die Zeile `status:` auf `superseded`. Eine ADR
auf `proposed` ist ein Entwurf und wird umgeschrieben.

## Was hier nicht steht

- **Geprüft wird der Datalayer im Lauf**, von `check-repo.py` vor jeder Projektion (§280); das
  Gelesene einer Projektion prüft `.claude/scripts/check-sheet.py`, und auch der Abgleich
  gegen einen Snapshot läuft im Lauf.
- **Kein Zustand des Shops.** Der Datalayer trägt, was wir entschieden haben.
