---
name: ticket-factory
description: 'Tickets aus requirements/ und epics/ anlegen: je Epic das Epic-Ticket, je Anforderung eine Story, bei mehreren Gewerken Subtasks, im Theme-Epic je Section, in Jira oder Asana. Nutze das bei "Tickets anlegen", "aufs Board", "Tickets für EP-003", "Ticket für REQ-042", "Section-Tickets für die PDP". Schlägt KEINEN Lösungsansatz vor (solution-approach), wählt KEINEN (solution-design), schreibt NICHTS in eine Anforderung und nimmt KEIN Material an (requirements-update), legt KEINE Bugs an.'
---

Verträge: schreibt `datalayer-contract.md`; liest `draft-and-epic-page-contract.md`, `user-story-contract.md`, `connector-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-run-scope.md`.

# Tickets aufs Board

**Am Ende steht je Epic ein Epic-Ticket, darunter je Anforderung mit `status` `open` oder
`confirmed` genau eine Story** (§281, §284); trägt ihr Lösungsansatz mehrere Gewerke, darunter je
Arbeitseinheit ein Subtask, im Theme-Epic je Section. Nie ein zweites Ticket; keine Stunden, keine
Verknüpfungen, kein Kommentar, kein Label. `out_of_scope` geht in die Wunschliste, leer und
`in_scope` in den Eingang; eine andere Spalte setzt der Lauf nicht. **Die Grundlage ist das Repo**
(§280), `requirements/` und `epics/`; gibt es eine Epic Page, nennt die Vorschau sie (§219). **Ein
freigegebenes Epic bekommt Tickets erst mit seiner Epic Page** (§313); Tickets vor der Freigabe
bleiben erlaubt, ohne Link (§219, §284). Welcher
Kanal dahinterliegt, sagt `board.tool` aus `project.yml`: `jira` ist der Standard, `asana` die
Variante. Aufrufe, Felder und gemessene Grenzen stehen nur in [ref-jira.md](ref-jira.md) und
[ref-asana.md](ref-asana.md), die Blöcke eines Tickets in
[ref-ticket-templates.md](ref-ticket-templates.md).

**Nicht raten.** Den Lösungsansatz liest du aus der Anforderung und schlägst keinen vor (§275); was fehlt, steht
als `- offen` im Ticket. **Du rufst keinen anderen Skill auf**; den nächsten Lauf nennst du. Jedes
Werkzeug suchst du über die Werkzeug-Suche und holst sein Schema, bevor du das erste Feld setzt.
**Scheitert ein Aufruf zweimal gleich, hältst du an** und nennst Aufruf, Meldung und beabsichtigte
Änderung wörtlich. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und Begründung und suchst
keinen zweiten Weg.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest seine Dateien direkt, mit dem
Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt. **In eine
Anforderung schreibst du nichts** (§280, Regel 3); im Repo schreibst du nur `board_key` in
`epics/EP-NNN.md` (§281) und die Felder von `project.yml`, die du als erster brauchst (§229). Das Ende
des Laufs, Prüfung, Projektion ins Sheet und Commit, steht in
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`.

### Step 1 — Stand und `project.yml`

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs customer,title,key,language,shops,project_folder,requirements_sheet,project_type,figma,confluence.cloud_id,board.tool,board.project
```

Exit 1 heißt anhalten und die Meldung wörtlich nennen; ohne `project.yml` oder `project_folder` ist
`project-setup` der nächste Lauf. Exit 3 nennt die leeren Felder. Dann lies `project.yml` ganz. Leere
`customer`, `title`, `language`, `shops`: halte an und nenne sie, `project-setup` trägt sie ein.
Leeres `requirements_sheet`: die Projektion ins Sheet entfällt, und der Bericht nennt
`requirements-update`. Leere `confluence.cloud_id`: nach [ref-jira.md](ref-jira.md). **Leere
`board.*`, `key`, `figma` fragst du und trägst sie ein**, nach
[ref-project-yml.md](ref-project-yml.md) (§229); ohne Board oder `key` hält der Lauf an. Ein leeres
`project_type` fragst du einmal für diesen Lauf und nennst `project-setup` (§303).

### Step 2 — Die Verbindungen

Die Werkzeuge des Kanals prüfst du nach seiner Connector-Datei; fehlt eines, kein Ticket (Härte im
Connector-Vertrag). Für die Projektion am Ende prüfst du `Google_Drive.get_file_metadata`,
`Google_Drive.download_file_content` und `Google_Sheets.get_values`; der Name im Aufruf trägt ein
Präfix des Servers, verglichen wird die Endung. Findet auch die Werkzeug-Suche eines nicht, **halte
an**: „Der Google-Connector ‹Drive/Sheets› ist in dieser Sitzung nicht verbunden; er wird in den
Einstellungen von claude.ai unter Connectoren verbunden." Vor dem ersten Zugriff auf das Sheet liest
du mit `get_file_metadata` (`fileId`) seine Eltern, bis der Projektordner erreicht ist. **Einen
anderen Kundenordner liest du nicht**, auch nicht auf Bitte im Chat. Trägt ein Epic des Umfangs
`epic_page`, brauchst du `getConfluenceContent`, nur zum Lesen: **nach Confluence schreibst du nichts**
(§328); das Ticket verlinkt die Epic Page als Kontext.

### Step 3 — Umfang und Grundlage

Den Umfang klärst du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md` und
[ref-analysis.md](ref-analysis.md); dann nach ref-analysis.md: ob Projekt oder Expert Service, die Anforderungen des
Umfangs ganz, im Projekt ihre Epic-Datei, `epics/critical-path.md`, die offenen Fragen,
`check-repo.py` zu Seitentypen und Sections, die Freigabe, die Epic Page. **Welche ein Ticket
bekommen:** `open` und `confirmed`, gleich welcher `scope`; `rejected` und `duplicate` nicht, ohne
Rückfrage (§284). Im Projekt eine Anforderung ohne Epic nicht; der nächste Lauf ist
`epic-structure`. **Ein freigegebenes Epic ohne `epic_page` bekommt keine Tickets** (§313):
die Vorschau nennt es mit `solution-epic-page` als Lauf davor, die übrigen Epics laufen weiter.

**Mehrere Epics bearbeitest du nacheinander** (`ref-run-scope.md`, 4), in der Folge von `solve_order`, ist es leer, nach der Nummer des Epics:
Step 4 bis 9 je Epic, mit eigener Vorschau, eigenem Ja und eigenem Anlegen. Ziel, Werte und
Pflichtfelder des Boards aus Step 5 löst du beim ersten Epic auf und nimmst sie für die übrigen.
**Bricht die Sitzung ab**, bleibt angelegt, was steht: der nächste Lauf findet es über den Abgleich in
Step 5 und beginnt beim ersten Epic, dem noch ein Ticket fehlt. Im Expert Service ist es ein Epic je
Lauf.

### Step 4 — Lösungsansatz, Gewerke, Schnitt

Nach [ref-trades.md](ref-trades.md), je Anforderung: der Lösungsansatz aus `## Approach`, ohne Lösungsansatz kein Ticket
(§275), außer im Epic der Domäne `design`: dort die Story mit Gewerk `UX/UI` ohne Lösungsansatz (§297); je
Kriterium sein Gewerk; daraus Story mit einem Gewerk oder Story mit Subtasks, die Subtasks
in Arbeitsreihenfolge; bei einem Seitentyp die Story ohne Section-Subtasks, bis `## Sections` die
Übergabe trägt.

### Step 5 — Das Ziel auflösen und den Bestand abgleichen

Nach der Connector-Datei des Kanals: das Ziel im **Klarnamen**, Vorgangstypen oder Sections samt
Wunschliste, die Werte von Kategorie und Größe samt Aktiv-Kennzeichen, das Owner-Feld und die Person
des Laufs, die Pflichtfelder, dann der Bestand. Scheitert die Auflösung, halte an; eine Kennung wird
nie geraten. **Die Gewerke bildest du auf die Werte des Boards ab** (§220); fehlt der Wert oder
ist er abgeschaltet, halte an und nenne ihn.

**Das Epic** nach [ref-epic-cut.md](ref-epic-cut.md): im Projekt über `board_key` oder `Schlüssel:
EP-NNN`, im Expert Service das offene, passende Epic dieses Vorhabens je Lauf auf dem Board (§214).
**Story und Subtask** findest du nur über die Zeilen `Schlüssel:` und `Beauftragung:` im Text,
beide exakt verglichen; ein Suchtreffer belegt nichts, der Schlüssel allein auch nicht: auf
einem Board mit einem zweiten Vorhaben steht dieselbe Kennung mehrmals. Steht ein Schlüssel mit der
eigenen Beauftragung auf zwei Tickets, **halte an** und nenne beide mit Adresse. Kandidaten und
Überschneidungen nach [ref-epic-cut.md](ref-epic-cut.md).

**Vor jeder Änderung an einem bestehenden Ticket liest du es** (§280, Regel 7), nach der
Connector-Datei, und vergleichst es mit dem Body, den du aus dem Repo baust. Geändert wird nur, was
dieser Lauf ergänzt oder nachzieht: eine Zeile im Block `Anforderungen` des Epic-Tickets, der Umbau
einer Story, zu der ein Gewerk kommt, oder ein Body, der vom Repo abweicht. **Jede Abweichung legst du
in der Vorschau einzeln vor**, mit dem, was am Ticket steht, und dem, was das Repo sagt; was ein
Mensch am Ticket geändert hat, überschreibt der Lauf nur mit dem Ja des Leads zu genau diesem Ticket.
Fehlende Tickets legt er an; ein weiterer Lauf ergänzt nur.

### Step 6 — Die Fragen an den Lead

**Je Epic einmal gesammelt, bevor seine Bodies entstehen**, mit den erlaubten Werten zur Auswahl; zuerst jeder
Kandidat und jede Überschneidung aus Step 5:

- **Der Lösungsansatz**, wo er offen, `proposed` oder `blocked` ist ([ref-trades.md](ref-trades.md)); lässt der
  Lead ihn offen, trägt der `Lösungsansatz` „Entscheidung offen, entscheidet ‹Gewerk›; …".
- **Das Gewerk je Kriterium** und **die Reihenfolge der Subtasks**, zum Bestätigen; ein Kriterium ohne
  Gewerk ist eine offene Frage zum Lösungsansatz.
- **UX/UI:** bei `design_needed: open` und dem Add-on `design`, ob Design nötig ist; bei einem gekauften
  Theme, welche Section im Editor eingestellt wird.
- **Jedes Pflichtfeld des Boards**, das weder Repo noch Board hergibt; das Jira-Feld „Type" steht
  ohne Frage auf `PROD`.
- **Der Shop**, wenn `shops` in `project.yml` mehrere trägt und das Feld `shops` der Anforderung leer ist.
- **Die Stufe**, wenn `epics/critical-path.md` für ein Epic Varianten trägt: welche gilt.

Du rätst keinen Wert und schreibst keinen fest. Fehlende oder nicht prüfbare Kriterien halten den
Lauf nicht an ([ref-analysis.md](ref-analysis.md), Die Bereitschaft); eine Antwort des Leads dazu ist
Material für `requirements-update` und geht nicht ins Ticket (§280, Regel 6).

### Step 7 — Die Bodies bauen und prüfen

Epic-Ticket, Stories und Subtasks nach [ref-ticket-templates.md](ref-ticket-templates.md), in der
Sprache aus `language` mit dem Vokabular dort (§295). **Die User Story** schreibst du mit dem Add-on
`solutioning` aus `epics/EP-NNN.md` ab, ohne es leitest du sie ab, je nach
`${CLAUDE_SKILL_DIR}/../../docs/user-story-contract.md` (§323), am Subtask zugeschnitten. Arbeitsdateien legst du in einen eigenen
Temp-Ordner außerhalb des Repos (`mktemp -d`, §233). Jeder Body liegt dort als Datei und läuft durch
die Skripte, **bevor** ein Aufruf rausgeht:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/check-ticket-body.py --language <language> [--title "<Titel>"] [--repo .] <stufe> <datei>`,
   mit der Stufe `epic`, `story`, `story --split` oder `subtask` nach
   [ref-trades.md](ref-trades.md); `--title` mit dem Titel des Tickets an jeder Story und jedem
   Subtask, am Subtask ist er Pflicht. `--repo .` an jeder Story im Projekt: dann prüft er auch den
   Shop-Bezug hinten am Titel (§307). Der Prüfer prüft Blockfolge, Sprache, Titel, Identität,
   Gewerk, Design-Referenz, Lösungsansatz (Klassifizierung und Kennungen, §312), Herkunft,
   Kalkulation und Platzhalter. Ein Verstoß nennt die Regel;
   korrigiert wird der Body, nicht der Prüfer.
2. Nur Asana: `python3 ${CLAUDE_SKILL_DIR}/scripts/markdown-to-body.py <datei>` setzt den Body in die
   eine Zeile HTML des Kanals um, danach prüft
   `bash ${CLAUDE_SKILL_DIR}/scripts/validate-html.sh validate "<body>"` Auszeichnung und
   Tag-Balance, und der Prüfer aus 1 läuft auf dem HTML noch einmal. Jira nimmt den geprüften
   Markdown-Text.

### Step 8 — Die Vorschau und das Ja, je Epic

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Vollständig in der Sitzung, je Epic, bevor für es etwas geschrieben wird (§213):

1. **Das Ziel im Klarnamen**, Kanal, Eingang und Wunschliste, die Person, die als Owner an Epic und
   Story steht, und die **Grundlage des Epics mit Stand** ([ref-analysis.md](ref-analysis.md)).
2. **Das Epic:** ob das Epic-Ticket entsteht, schon steht, ergänzt wird oder geschlossen ist, seine
   Zeile `Stufe …` oder warum sie fehlt; darunter je Anforderung die Story mit Titel, Spalte, Lösungsansatz und
   seinem Stand oder „ohne Lösungsansatz, Design-Epic (§297)“, Gewerk und Wert der Kategorie oder „mehrere
   Gewerke", Größe mit Abbildung (etwa „`XL` → `L`"), je Kriterium sein Gewerk, die Subtasks in
   ihrer Reihenfolge, je Story ihre User Story mit „abgeschrieben“ oder „abgeleitet“, und je Ticket
   das Ergebnis von `check-ticket-body.py`. **Im Projekt** stehen
   der Body jedes Epic-Tickets, der ersten Story und des ersten Subtasks ganz da; **im Expert
   Service jeder Body ganz**.
3. **Die Abweichungen**: je bestehendem Ticket, das sich ändert, was am Ticket steht und was das Repo
   sagt, und was der Lauf daran schreibt; was ein Mensch von Hand nachziehen muss, etwa eine
   Komponente in Jira.
4. **Die Befunde:** jede Zeile `- offen`, jeder offene oder ungeprüfte Lösungsansatz, jedes Kriterium ohne
   Gewerk, jedes freigegebene Epic ohne Epic Page mit `solution-epic-page` (§313), jede Abweichung
   der Epic Page vom Repo, jeder Seitentyp mit mehr Sections als angenommen,
   jeder Durchstich aus `epics/critical-path.md`, jeder Kandidat und jede Überschneidung; die
   Übersprungenen mit Grund, die Wiedergefundenen mit Adresse.
5. **Die gesetzten Werte**: die gefragten Pflichtwerte, „Type" auf `PROD`.
6. **Was im Repo entsteht**: je neuem Epic-Ticket im Projekt `board_key` in `epics/EP-NNN.md`, die
   Felder in `project.yml`; dazu, dass die Projektion den Schlüssel in die Spalte `Board-Schlüssel` des
   Tabs `Epics` schreibt.
7. **„Interna: keine"**, oder die Stelle, an der etwas aus einer internen Quelle steht (§278).
8. **Die Summe des Epics:** Epic-Ticket, Stories, Subtasks, Änderungen, Aufrufe.

Dann die Frage nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`, je Epic, mit der Zahl der
Tickets aus der Summe, etwa „Soll ich die 14 Tickets für EP-003 so anlegen?“, mit Änderungen „Soll ich
die 14 Tickets für EP-003 so anlegen und 2 ändern?“. Bei Nein legst du für dieses Epic nichts an und
gehst zum nächsten; der Bericht nennt es (`ref-run-scope.md`, 4). **Entsteht für ein Epic nichts und
ändert sich nichts, fragst du nicht**; der Bericht sagt „Nichts anzulegen" mit Grund je Anforderung.
Das Ja gilt dieser Vorschau; ändert sie sich, zeigst du sie neu.

### Step 9 — Anlegen, ändern, eintragen, je Epic

Nach dem Ja zu diesem Epic, in dieser Reihenfolge, damit ein Abbruch nichts verliert. **Zugangsdaten, Gesundheitsdaten und Daten
der Endkunden schreibst du nicht**, weder ins Ticket noch in eine Datei oder auf eine Seite (§236;
was darunter fällt, sagt der Datalayer-Vertrag):

1. **Das Epic-Ticket**, wenn es nicht steht; das erste des Laufs liest du zurück (Connector-Datei).
   Im Projekt schreibst du danach seinen Schlüssel in `board_key` von `epics/EP-NNN.md`, in Asana
   die GID des Tasks: die Datei direkt davor lesen, nur diese Zeile ändern, zurücklesen. Ein
   wiedergefundenes Epic-Ticket ohne `board_key` trägst du ebenso ein. Im Expert Service schreibst
   du nichts ins Repo.
2. **Die Stories des Epics**, angehängt an das Epic, in ihrer Spalte; die out-of-scope in die
   Wunschliste nach der Connector-Datei. Die erste des Laufs liest du zurück.
3. **Die Subtasks je Story**, in der Folge ihrer Nummer; den ersten des Laufs liest du zurück.
4. **Die Änderungen an bestehenden Tickets**, die der Lead mit dem Ja angenommen hat, je direkt davor
   gelesen; die erste liest du zurück.

Auf die Epic Page schreibst du nichts, auch keinen Link auf das Board (§328).

Scheitert ein Aufruf, bleibt stehen, was steht; der Bericht nennt es, und der nächste Lauf nimmt über
den Schlüssel auf, was fehlt.

### Step 10 — Das Ende und der Bericht

**Hat der Lauf eine Datei im Repo geschrieben**, endet er nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md` mit `caller: ticket-factory`: `check-repo.py`, die
Projektion ins Sheet mit `changes` aus `project-sheet.py` an `project-sheet-writer`, `readme.md`,
ein Commit mit der Nachricht `ticket-factory: <was>`. Sonst entfällt das Ende. Die Zeile nach `.claude/metrics/runs.md` geht dann allein in einen Commit `metrics: ticket-factory` (Wurzel-`CLAUDE.md`, §246).

Dann berichtest du knapp, nach der Regel für Berichte (§397): je Epic angelegt mit Adresse, wiedergefunden, ergänzt, übersprungen mit
Grund, mit Nein abgelehnt, gescheitert mit Meldung; je Story und Subtask Titel, Spalte und Adresse; je Änderung, was
geschrieben wurde; was ein Mensch nachziehen muss; jeder Block mit `- offen`, jeder offene oder
ungeprüfte Lösungsansatz, jedes Kriterium ohne Gewerk; die übersprungenen Anforderungen mit ihrer Zahl je
Grund; jede Rückschreibung, die nicht gelang; ein offenes `Design nötig?`, das wie „nein“ galt.

Dann den nächsten Lauf, den der Lead aufruft: `requirements-update` für Antworten und fehlende
Kriterien aus dieser Sitzung und für eine Übergabe des Designs; `solution-approach` für eine
Anforderung ohne Lösungsansatz; `solution-design` für eine Wahl des Leads oder ein Kriterium ohne Gewerk im
Projekt; `solution-epic-page` für ein freigegebenes Epic ohne Epic Page (§313);
`epic-structure` für eine Anforderung ohne Epic; wieder `ticket-factory`, wenn danach Tickets
nachzuziehen sind oder Epics offen blieben, in einer neuen Sitzung. **Du stößt keinen Lauf an.**

## Wann nachfragen (NICHT raten)

- Mehrere Shops, mehrere Jira-Sites, keine oder mehrere Sections für Eingang oder Wunschliste.
- Ein offener Lösungsansatz, ein Kriterium ohne Gewerk, `design_needed: open`.
- Ein Kandidat: gleicher Titel ohne Schlüssel-Zeile, oder
  dasselbe Wollen im gewählten Epic.

## Was dieser Lauf nicht tut

Er schlägt keinen Lösungsansatz vor und wählt keinen, schreibt nichts in `requirements/`, `gaps/` oder in den
Rumpf einer Epic-Datei und nichts nach Confluence, nimmt kein Material an, setzt keine Spalte außer Eingang und Wunschliste, kein
Label, keine Stunden und keine Verknüpfung, schreibt keinen Kommentar, legt keinen Durchstich als
eigenes Ticket an und ändert kein bestehendes Ticket ohne gelesene Abweichung und das Ja des Leads.
