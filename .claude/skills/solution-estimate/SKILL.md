---
name: solution-estimate
description: 'Das interne Schätzdokument als Google-Doc in Solutioning, aus dem Repo: Stunden aus Aufwand (h) je Position mit Bullets in Kundensprache, Projektmanagement und Testing als Satz, Gesamt, je Epic Größe und Lücken. Nutze das bei "Schätzdokument", "was kostet das", "Stunden insgesamt". Schätzt KEINE Stunden (solution-design), KEIN Budget und kein Abgleich damit, NICHTS ins Sheet, KEIN Proposal (solution-proposal).'
---

Verträge: liest `datalayer-contract.md`, `requirements-list-contract.md`, `ref-projection.md`, `ref-preview.md`.

# Das Schätzdokument eines Vorhabens

Am Ende liegt **ein Google-Doc im Unterordner `Solutioning` des Projektordners**, intern, mit dem Datum
des Stands, aus dem es gerechnet ist: oben der Aufwand je Position mit ihren Stunden, „Summe
Umsetzung“, Projektmanagement und Testing als Satz auf die Umsetzung (§258), die Zusatzpositionen,
und das Gesamt (§355); darunter je Position Bullets in
Kundensprache; dann die Übersicht je Epic mit `Aufwand (h)` und einem Hinweis, wenn Anforderungen ohne
Größe oder ohne Stunden sind (§265); je Epic die Anforderungen mit Größe, Stunden, Stand der Lösung und
offenen Fragen, beim Seitentyp dazu die Annahme zu den eigenen Sections (§285); die Lücken (§212).
**Jeder Lauf legt eine neue Fassung an**; eine frühere bleibt, wie sie ist, und liegt danach im
Unterordner `Archiv` (§260).

**Das Dokument ist eine Projektion des Repos** (§280): Anforderungen, Epics und offene Fragen kommen
aus `requirements/`, `epics/` und `gaps/`, Kunde, Titel, Sprache und `add_ons` aus `project.yml`. Aus
dem Sheet liest du nur die schmale Spalte `Aufwand (h)` im Tab `Solutioning` (§280 Regel 5, §283).

**Die Positionen, in dieser Folge** (§355), je mit ihrem Namen in der Sprache des Projekts:

| Position (`de`) | Position (`en`) | was hineinzählt |
|---|---|---|
| Shop-Setup | Shop setup | Lösungsansatz `shop` |
| Erweiterte Shop-Features | Extended shop features | Lösungsansatz `app` |
| UX/UI | UX/UI | das Design-Epic (Domäne `design`) und die Lösungsansätze `theme_native` und `theme` |
| Custom-Erweiterungen | Custom extensions | Lösungsansatz `custom_app` |
| Schnittstellen | Interfaces | Lösungsansätze `integration_connector`, `integration_middleware`, `integration_custom` |
| Daten-Migration | Data migration | Epics der Domäne `data_migration`, gleich welcher Lösungsansatz |
| Content-Migration | Content migration | Epics der Domäne `content_migration`, gleich welcher Lösungsansatz |
| Lösungsansatz offen | Approach open | Anforderungen ohne Lösungsansatz, die keine Domäne oben zuordnet |

Der Lösungsansatz ist `classification` in der Datei der Anforderung. Die Domänen `design`,
`data_migration` und `content_migration` gehen vor ihm; trägt eine Anforderung zwei Werte, zählt der
erste, außer eine Schnittstelle (`integration_*`): sie zählt immer zu Schnittstellen. Eine Position ohne Anforderung entfällt. **Trägt eine gezählte Anforderung noch keinen
Lösungsansatz** (`classification` leer) und gehört sie über ihre Domäne zu keiner Position, steht sie in der letzten
Position „Lösungsansatz offen“, mit ihren Stunden; ihre Bullets nennen, was offen ist, und die Lücken
nennen die Anforderung. So zeigt die Schätzung den offenen Teil, statt
anzuhalten, bis jede Frage an den Kunden beantwortet ist.

**Du schätzt keine Stunde** (§280 Regel 10). Stunden je Anforderung setzt ein Mensch in `Aufwand (h)`;
eine Position und ein Epic tragen ihre Summe. Größe `S` bis `XL` und die Annahme zu den eigenen
Sections schreibt `solution-design` in die Datei der Anforderung. Fehlt eine Zahl, steht die Lücke im
Dokument; du leitest keine aus einer Größe ab und schlägst keine vor, auch nicht als Hinweis. Ob eine
Stundenzahl zur Größe passt, prüft kein Lauf, auch du nicht; das zeigt der Kalibrierungsbericht
einem Menschen (§357). **Die Modellschätzung `effort_estimate_model` liest du nicht** (§357): sie ist keine Zusage, und das
Dokument rechnet nur mit `Aufwand (h)`.

**Mit dem Add-on `design`** trägt das Design-Epic die Stunden des Designers, darin die UX/UI-QA vor
dem Go-Live; sie zählen zur Position UX/UI (§285, §303, §355). Fehlt ein Epic der Domäne `design` oder
darin die Anforderung mit `standard: design-qa` (§303), steht das unter den Lücken.

**Was der Lead im Aufruf nennt, gilt für diesen Lauf** (§258, §355): die Sätze für Projektmanagement
und Testing und Zusatzpositionen. Fehlt ein Satz, rechnest du ihn nicht ein, und
Dokument und Bericht nennen ihn. Du fragst nicht danach und schlägst keinen vor.

**Ein Budget kennt das Schätzdokument nicht** (§355): den Abgleich mit dem verkauften Budget machen
PM oder Sponsor außerhalb der Strecke. Nennt der Lead eines, nimmst du es nicht auf, und der Bericht
sagt das einmal. Ins Repo kommt es nie (§352), auch nicht in eine Notiz, einen Commit oder
`.claude/metrics/runs.md`.

**Das Dokument ist intern** (§355): es trägt im Kopf „Intern — nicht für den Kunden.“ und geht nicht
nach außen; das Proposal nennt keine Stunden. Die Bullets stehen trotzdem in Kundensprache: ohne
Stunden, ohne „Aufschlag“ und „Budget“, ohne Kennungen und ohne Werkzeugsprache.

Drive, Sheets und Docs erreichst du nur über die Google-Connectoren `Google_Drive` und
`Google_Sheets` (ein Doc legt Drive aus HTML an, Seite, Fußzeile und Schrift setzt
`Google_Docs.update_doc`). Das Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt.
Die Aufrufe zum Lesen stehen in [ref-read.md](ref-read.md), das Anlegen in [ref-doc.md](ref-doc.md).
**Scheitert ein Aufruf zweimal gleich, hältst du an** und nennst Aufruf und Meldung wörtlich; einen
zweiten Weg suchst du nicht. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und Begründung.

**Ein Doc, das dieser Lauf kaputt angelegt hat, kommt weg** (§259): abgebrochen, unvollständig oder im
Rücklauf ungleich. Du legst es mit `Google_Drive.trash_file` in den Papierkorb, sobald es für die
Neuerstellung nichts mehr trägt: nachdem die neue Fassung angelegt und gleich zurückgelesen ist, und
entsteht in diesem Lauf keine, am Ende des Laufs. Nur was dieser Lauf selbst angelegt hat, erkannt an
der ID aus dem Anlegen, nie am Namen: die vorige Fassung heißt gleich (§262). Ohne Rückfrage; der
Bericht nennt Name und Link.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230): `project.yml` liegt in seiner Wurzel.
Du liest es direkt; **im Datalayer schreibst du nur die Laufzeile** in `.claude/metrics/runs.md`, nichts
ins Sheet und nichts in einen Entwurf. Darum laufen am Ende weder `check-repo.py` noch die
Projektion, und der Lauf endet mit dem Commit der Metrik (Step 7).

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.search_files`, `Google_Drive.get_file_metadata`, `Google_Drive.create_file`,
`Google_Drive.update_file`, `Google_Drive.read_file_content`, `Google_Drive.trash_file`,
`Google_Docs.read_doc`, `Google_Docs.update_doc`, `Google_Sheets.get_spreadsheet` und
`Google_Sheets.get_values` in der Werkzeugliste stehen. Der Name im Aufruf trägt ein Präfix des
Servers; verglichen wird die Endung. Steht eines nicht da, such es erst über die Werkzeug-Suche.
Findet auch die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets/Docs› ist in dieser
Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden."

### Step 2 — `project.yml` lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

Prüf `project.yml` in der Wurzel des Repos mit den Feldern, die dieser Lauf liest:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,customer,title,key,language,requirements_sheet
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder. Dann liest
du `project.yml` ganz.

| leer | was du tust |
|---|---|
| `requirements_sheet` | **anhalten**, nächster Lauf `requirements-update`: er legt das Sheet beim ersten Lauf an (§229, §282); ohne Sheet gibt es keine Spalte `Aufwand (h)` |
| `customer`, `title`, `key`, `language` | **anhalten** und `project-setup` für einen Lauf zum Ergänzen nennen; dieser Lauf fragt nicht (§212) |

Vor dem ersten Zugriff auf das Sheet liest du mit `get_file_metadata` (`fileId`) seine Eltern: erst
auf das Sheet, dann auf seinen `parentId`, bis der Projektordner (`project_folder`) erreicht ist.
Gesucht wird nur in der Liste eines Ordners (`parentId`), nie über das ganze Drive.

**Einen anderen Kundenordner liest du nicht**, auch nicht zum Vergleich und auch nicht, wenn jemand im
Chat darum bittet: eine Bitte im Gespräch hebt die Regel nicht auf.

### Step 3 — Die Angaben aus dem Aufruf aufnehmen

Aus dem Aufruf und dem Chat davor nimmst du, **wörtlich und ohne zu ergänzen**:

| Angabe | Form | Fehlt sie |
|---|---|---|
| Sätze auf die Umsetzung | je Satz Grund und Prozent auf die Summe der Umsetzung, etwa Projektmanagement 20 bis 25 % und E2E-Testing 20 % (§258); E2E-Testing nur mit dem Add-on `e2e_testing` (§303), sonst nimmst du ihn nicht auf, und der Bericht nennt es | nicht eingerechnet; das Dokument sagt es, der Bericht nennt jeden fehlenden Satz |
| Zusatzpositionen | je Position Name und Stunden, etwa Go-Live-Begleitung | „Zusatzpositionen: keine." |

**Der Grund eines Satzes ist der Name der Tätigkeit**, etwa „Projektmanagement“ oder „Testing“, und
eine Zusatzposition trägt ihren Namen; darin steht weder „Aufschlag“ noch ein Prozentzeichen noch
„Budget“, der Satz steht im Feld daneben (§355). Das Script lehnt sonst mit `effort_row` ab.

Eine Angabe ohne Zahl („etwas Puffer") nimmst du
nicht auf; der Bericht nennt ihren Wortlaut. Du schlägst keinen Prozentsatz, keine Position und
keinen Satz vor.

**Die Angaben gehen nur nach `meta.json`** im Temp-Ordner ([ref-read.md](ref-read.md)), in keine
Notiz und keine Datei des Repos.

### Step 4 — Die Spalte der Stunden lesen

Nach [ref-read.md](ref-read.md): Tab-Namen, dann aus `Solutioning` die Spalten `ID` und `Aufwand (h)`,
je ein Bereich. **Direkt nach der letzten Lesung hältst du die Lesezeit fest.** Was du liest,
schreibst du direkt danach in die Dateien im Temp-Ordner des Laufs (`mktemp -d`, außerhalb des Repos,
§233), wie die Ref sie beschreibt; gerechnet wird aus den Dateien und dem Repo, nicht aus dem
Gedächtnis. Die Dateien des Repos holst du nicht in den Kontext: das Script liest sie.

### Step 5 — Die Positionen, die Bullets und die Vorschau

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py positions <temp-ordner des laufs>
```

**Exit 0:** je Position eine Zeile `POSITION ‹schlüssel› ‹Name› | ‹Stunden› | ‹Anforderungen mit
Titel›`, in der Folge der Positionen. **Exit 1:** eine Zeile, die Prüfung und Stelle nennt (Tabelle
unten).

**Daraus fasst du je Position die Bullets** nach [ref-read.md](ref-read.md), „Die Bullets“: in
Kundensprache, so viele wie nötig, so wenige wie möglich, keine feste Zahl (§355). Bei UX/UI die
Bullets „Designkonzept und Design-System“, „UX/UI-QA vor dem Go-Live“ und „Theme-Anpassungen“, soweit
die Position das trägt; bei Daten-Migration je migriertem Objekt ein Bullet, etwa Produkte, Kunden,
Bestellungen, Gutscheine und Rabattcodes. Du liest dafür die Titel aus der Zeile `POSITION`, und wo sie
nicht reichen, Beschreibung und Lösungsansatz der Anforderung in ihrer Datei. Sie gehen nach `bullets.json`.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py estimate <temp-ordner des laufs>
```

**Exit 0:** die Ausgabe ist das Dokument, Zeichen für Zeichen; du formulierst nichts um und fügst
nichts hinzu. Oben trägt es nur „Stand: ‹Datum›“; die Zeile `STAND ‹Lesezeit› UTC; Aufwand (h): ‹je
Anforderung die gelesenen Stunden›` auf stderr ist für Bericht und Commit (Step 7); sie trägt kein
Budget. **Exit 1:** stdout trägt dann kein Dokument, sondern eine Zeile, die Prüfung und Stelle nennt.
Liegt der Fehler in deiner Datei, korrigierst du sie aus der Lesung und rechnest neu; sonst **hältst du
an** und nennst die Zeile wörtlich mit dem, der sie behebt:

| Prüfung | behebt |
|---|---|
| `bullet` (Position ohne Bullet, Bullet ohne Position, Bullet mit Stunden, „Aufschlag“, „Budget“, Kennung oder Werkzeugsprache) | du, in `bullets.json` |
| `hours` (keine Zahl in `Aufwand (h)`) | ein Mensch im Sheet |
| `header` (Kopfzeile von `Solutioning` weicht ab) | ein Mensch stellt das Sheet um (`../../docs/ref-projection.md`) |
| `size` (Stunden statt einer Größe) | `solution-design` |
| `domain` (Domäne fehlt oder nicht in der Liste) | `epic-structure` |
| `object` (Datei ohne lesbaren Kopf) | der Lauf, der die Datei schreibt; `check-repo.py .` nennt die Stelle |
| `meta` aus `project.yml` | `project-setup` |
| `budget` (`meta.json` trägt ein Budget) | du nimmst es aus `meta.json`; der Bericht sagt, dass der Abgleich außerhalb der Strecke liegt |
| `effort_row`, `surcharge`, `extra` (Grund oder Name mit „Aufschlag“, Prozent oder „Budget“, oder ohne Zahl) | du, in `meta.json`, aus dem Wortlaut des Aufrufs |

**Fehlen Stunden, ist das kein Befund:** Position und Gesamtzeile heißen dann „unvollständig", und trägt keine Anforderung Stunden, steht dort „offen". Gezählt wird eine
Anforderung mit `status` `open` oder `confirmed`, deren `scope` nicht `out_of_scope` ist, in einem Epic,
das nicht zusammengeführt oder aufgelöst ist.

**Dann die Vorschau, vor dem ersten schreibenden Aufruf** in Drive oder Repo: der Name des Doc aus
`doc-name.py . estimate` und der Unterordner `Solutioning`; die Tabelle „Aufwand je Position“ wörtlich
aus der Ausgabe; je Position die Bullets; die Angaben aus Step 3, welche
fehlen und welche du nicht aufgenommen hast. Aufbau, Frage und Ja nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`; das Ja deckt Doc und Commit dieses Laufs. Korrigiert der Lead einen Bullet, rechnest du neu und zeigst den Block neu.

### Step 6 — Das Schätzdokument anlegen

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht** ins Schätzdokument
(§236; was darunter fällt, sagt der Datalayer-Vertrag).

Nach [ref-doc.md](ref-doc.md): zuerst den Unterordner `Solutioning` im Projektordner finden oder
anlegen, wie der Datalayer-Vertrag es festlegt (Abschnitt „Die Ablage im Drive“, §231); dann den
Namen aus `doc-name.py . estimate`, `Aufwandsschätzung ‹title› – ‹Kunde›` ohne Datum und Uhrzeit (§263),
im Unterordner, als Google-Doc aus genau der HTML-Ausgabe aus Step 5 (§248), dann A4, Fußzeile und
Schrift, zurückgelesen und mit `readback` verglichen. **Jede Fassung trägt denselben Namen** (§262):
ein Doc mit diesem Namen flach in `Solutioning` ist die vorige Fassung, und du legst die neue trotzdem
an. Erst ein gleicher Rücklauf heißt „angelegt".

**Danach verschiebst du die älteren Fassungen nach `Archiv`** (§260), nach [ref-doc.md](ref-doc.md)
Schritt 6: jedes Schätzdokument, das flach in `Solutioning` liegt, den Namen des neuen trägt und nach
ID und `createdTime` eine ältere Datei ist (§262), mit `Google_Drive.update_file` (`fileId`,
`parentId` = die ID von `Archiv`); `Archiv` findest oder legst du in `Solutioning` an, erst wenn es
etwas zu verschieben gibt. Nur nach einem gleichen Rücklauf. Scheitert das Verschieben, bleibt die
Fassung liegen, und der Bericht nennt sie; du hältst nicht an.

### Step 7 — Berichten, committen und die nächsten Läufe nennen

Sag knapp, nach der Regel für Berichte (§397): den Link des Dokuments; ob der Unterordner
`Solutioning` neu angelegt wurde; welche älteren Fassungen nach `Archiv` verschoben wurden, ob
`Archiv` dafür neu angelegt wurde und welche liegen blieben; die Lesezeit; die Gesamtsumme, mit
„unvollständig", wenn das Dokument es sagt; welche Sätze fehlten und nicht eingerechnet sind; wie viele Anforderungen ohne `Aufwand (h)`,
wie viele ohne Größe, welche Seitentypen ohne Annahme zu den eigenen Sections, ob das Design-Epic
fehlt; die Angaben, die ohne Zahl waren oder nicht aufgenommen wurden.

**Der Stand geht in den Commit des Laufs** (§264): Lesezeit und gelesene Stunden stehen nicht im
Dokument, sondern in der Zeile `STAND` aus Step 5. Seine Zeile in `.claude/metrics/runs.md` geht in
einen Commit `metrics: solution-estimate`, direkt auf `main`, dann pushen (§233, §246). In seinen
Rumpf schreibst du die Zeile `STAND` wörtlich: das Sheet hält keinen Revisionsschutz, und erst Commit
und Zeile zusammen machen das Dokument später nachrechenbar. **Das Budget steht weder im Commit noch
in der Laufzeile** (§352).

Dann, was Menschen tun: ein Mensch setzt die fehlenden Stunden je Anforderung in `Aufwand (h)` im Tab
`Solutioning`. Die Läufe, die Grundlage liefern: `solution-approach` für Anforderungen ohne
Lösungsansatz, `solution-design` für Anforderungen ohne Größe, ohne Annahme zu den eigenen Sections
oder ohne entschiedene Lösung, `epic-structure` für Anforderungen ohne Epic und ein fehlendes
Design-Epic, `solution-review` vor der Zusage, und `solution-proposal` für das Dokument an den Kunden.
**Du rufst keinen auf**; der Lead ruft ihn.

## Was dieser Lauf nicht tut

Er schreibt nur nach dem Ja zur Vorschau, nur sein Dokument, in den Unterordner `Solutioning`,
verschiebt frühere Schätzdokumente nach `Archiv` und committet seine Metrik: kein Sheet, keine Notiz,
keine andere Datei des Datalayers, nichts in `project.yml`, kein Entwurf, kein Board. Das Budget
schreibt er nie ins Repo (§352). Er setzt kein `Aufwand (h)`, schlägt keine Stundenzahl vor und hält
keine Stunden gegen Größe oder Kalibrierung (§357). Er löscht und überschreibt keine
frühere Fassung. Stunden stehen auf keiner Kundenfläche; das Dokument trägt im Kopf „Intern — nicht
für den Kunden.“
