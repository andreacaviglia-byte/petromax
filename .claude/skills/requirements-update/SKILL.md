---
name: requirements-update
description: 'Material gegen die Anforderungen im Repo abgleichen: neue Anforderungen, Korrekturen, Status und Scope, offene Fragen und Antworten, Entscheidungen, Architektur, Design-Übergaben, nach dem Ja ins Repo, dann ins Sheet projiziert; beim ersten Lauf Sheet und Architektur anlegen. Nutze das bei "pfleg das Transkript ein", "der Kunde hat geantwortet", "nimm diese Anforderung auf", "Scope ist freigegeben". Legt KEIN Material ab (material-intake), schneidet KEINE Epics (epic-structure).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`, `system-landscape-contract.md`, `requirements-list-contract.md`; liest `user-story-contract.md`, `kb-contract.md`, `ref-projection.md`, `connector-contract.md`, `ref-tasks.md`, `ref-preview.md`, `ref-open-questions.md`, `ref-run-scope.md`.

# Anforderungen fortschreiben

Am Ende steht **im Repo jede Anforderung, Korrektur, Ausklammerung, Frage und Antwort, die das
Material trägt**: je Anforderung eine Datei in `requirements/` mit dem Was, je offene Frage eine in
`gaps/`, je Entscheidung eine ADR, in `architecture.md` jede belegte Vorgabe, je Quelle **eine Notiz
zum Abgleich** (§280). Dann projiziert der Lauf ins Sheet und in `readme.md`. Du schneidest nicht,
ordnest kein Epic zu und schreibst keinen Lösungsansatz. **Beim ersten Lauf legst du das Sheet und
`architecture.md` an** (§229), in jedem Vorhaben (§282), im Unterordner `Solutioning` des
Projektordners (§231).

**Ein Kandidat verschwindet nie stumm.** Was du nicht aufnimmst, steht mit Grund in der Notiz. **Das
Was kommt nur aus Material** (§280, Regel 6): aus `inputs/`, aus dem Chat, aus einer Übergabe, nie aus
einem Eintrag im Sheet, auch nicht dem des Leads.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest und schreibst seine Dateien
direkt, mit dem Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt;
was dort „nie überschrieben" heißt, legst du nur neu an. Jede geschriebene Datei liest du zurück. Das
Ende jedes Laufs, Prüfung, Projektion und Commit, steht in
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`; ins Sheet schreibt dabei nur der Agent
`project-sheet-writer`, **nach seiner Rückmeldung geht es mit dem nächsten Satz weiter.**

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.get_file_metadata`, `Google_Drive.download_file_content`,
`Google_Sheets.get_spreadsheet` und `Google_Sheets.get_values` in der Werkzeugliste stehen. Der Name im
Aufruf trägt ein Präfix des Servers; verglichen wird die Endung. Steht eines nicht da, such es erst über
die Werkzeug-Suche. Findet auch die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets› ist in
dieser Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren
verbunden."

### Step 2 — Den Steckbrief lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,customer,title,language,shops,requirements_sheet
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder:

| leer | Folge |
|---|---|
| `title`, `language` | du fragst danach, beide in einem Aufruf; `language` ist `de` oder `en`, eine Variante nimmst du nicht an (§202). Die Antwort trägst du nach dem Vertrag ein (Abschnitt `project.yml`). Bleibt sie „noch offen", entsteht kein Sheet (§263, §295), und der Lauf schreibt nur ins Repo |
| `customer` | nur wenn auch `requirements_sheet` leer ist: ohne ihn entsteht kein Sheet, sein Name ist `Anforderungsliste ‹title› – ‹Kunde›` (bei `en` `Requirements list …`, §337; §263). Du fragst nicht danach; der Bericht nennt `project-setup` |
| `shops` | die Zeile zu den Shops in der Architektur bleibt `offen`, und eine Pflichtliste des Rechtsraums entsteht nicht; der Bericht nennt `project-setup` |
| `requirements_sheet` | du legst Sheet und Architektur an, Step 3 |

`shops[].jurisdiction` und `shops[].audience` fragst du erst, wenn die Pflichtliste des Rechtsraums
gebraucht wird ([ref-baseline-rows.md](ref-baseline-rows.md)).

**Steht `requirements_sheet`**, liest du die Elternkette des Sheets mit `get_file_metadata`
(`fileId`): erst auf das Sheet, dann auf seinen `parentId`, bis der Projektordner (`project_folder`)
erreicht ist. Einen anderen Kundenordner liest du nicht. Dann liest du `architecture.md`, listest
`requirements/`, `gaps/`, `inputs/`, `notes/` und `decisions/` und gehst zu Step 4.

### Step 3 — Beim ersten Lauf: Sheet und Architektur anlegen

Nur wenn `requirements_sheet` leer ist; ist `customer`, `title` oder `language` leer, legst du kein
Sheet an, nennst `project-setup` und gleichst trotzdem ab. Prüf dafür wie in Step 1 zusätzlich
`Google_Drive.search_files`, `Google_Drive.create_file`, `Google_Sheets.update_spreadsheet` und
`Google_Sheets.update_values`. Ob das Add-on `solutioning` verkauft ist, fragst du nicht (§229).

**Erst suchen.** Den Unterordner `Solutioning` suchst du im Projektordner, wie der Vertrag es sagt
(Abschnitt „Die Ablage im Drive"); zwei Treffer: anhalten und beide mit Link nennen. Gibt es ihn,
suchst du darin das Sheet nach [ref-create-sheet.md](ref-create-sheet.md), Schritt 0 und 1: ein Treffer
ist der Rest eines abgebrochenen Laufs, du doppelst ihn nicht. Dann liest du `architecture.md`; steht
sie, bleibt sie.

**Vormerken, nicht einzeln fragen** (§396). Was entsteht, steht oben im Block von Step 7, unter einem
Ja mit den Änderungen des Abgleichs, **im Klarnamen**: der Unterordner `Solutioning`
(neu oder vorhanden, mit Link), das Sheet mit dem Namen aus `doc-name.py . requirements` mit seinen
vier Tabs in der Sprache aus `language`, der Formel in `Aufwand (h)` und formatiert (§247), oder der
gefundene Rest mit Link, `architecture.md` mit ihrem ganzen Text, wenn sie fehlt
([ref-architecture.md](ref-architecture.md), „Anlegen"), und jede Zeile von `project.yml`, die sich
ändert.

**Anlegen**, nach dem Ja in Step 7 als Erstes in Step 8, nach
[ref-create-sheet.md](ref-create-sheet.md); erst wenn Tab-Namen und Kopfzeilen gleich zurückkommen, trägst du die ID als `requirements_sheet` ein. Scheitern nur Formel oder Formatierung,
nennt der Bericht die Meldung wörtlich, und der Lauf geht weiter. Dann legst du `architecture.md` an,
wenn sie fehlt, und liest sie zurück. Scheitert ein anderer Aufruf, bleibt stehen, was steht,
`requirements_sheet` bleibt leer, der Bericht nennt Sheet, Tab und Meldung, und der Lauf schreibt ohne
Sheet weiter ins Repo.

### Auf Wunsch: ein bestehendes Sheet nachformatieren

Sagt der Lead etwa „formatier die Anforderungsliste“, formatierst du nach Step 2 das Sheet aus
`requirements_sheet` nach [ref-create-sheet.md](ref-create-sheet.md), Abschnitt „Ein bestehendes Sheet
nachformatieren“; prüf dafür wie in Step 1 zusätzlich `Google_Sheets.update_spreadsheet`. Dann endet
der Lauf mit dem Bericht, es sei denn, der Lead hat auch Material genannt: dann Step 4.

### Step 4 — Den Anlass festlegen

| Anlass | Woher |
|---|---|
| abgelegtes Material | jede Datei in `inputs/` und jede Chat-Notiz `notes/…-chat-….md` aus `material-intake` oder einem anderen Lauf, zu der in `notes/` noch keine Notiz `…-abgleich.md` steht, oder die, die der Lead nennt |
| eine Eingabe des Leads im Chat | sein Wortlaut, auch eine Antwort, die er aus einem Gespräch kennt; die Notiz `<JJJJ-MM-TT>-chat-<thema>.md` legst du mit an, Schema nach `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md` (§282) |
| die Architektur oder eine Lösung | eine Zeile aus `architecture.md` oder ein Entwurf, aus dem eine Anforderung entsteht (§215, §216) |
| der Standard-Leistungssatz | nach [ref-baseline-rows.md](ref-baseline-rows.md), wenn `requirements/` ihn für den Rechtsraum eines Shops noch nicht trägt |
| die Add-ons | nach [ref-baseline-rows.md](ref-baseline-rows.md) (Die Standard-Anforderungen der Add-ons), wenn eine Standard-Anforderung zu einem Add-on aus `project.yml` fehlt (§303) |

**Nennt der Lead nichts, und trägt keine Zeile der Tabelle einen Anlass**, endest du nicht leer
(§398, `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`): du schreibst einen Satz, dass kein abgelegtes Material auf den Abgleich wartet und ein Link
zu Material über `material-intake` geht, und fragst „Was gleiche ich ab?“ mit den Antworten
„Text folgt“ und „Erst material-intake“. Auf „Text folgt“ wartest du und nimmst die nächste Nachricht
als Eingabe des Leads; auf „Erst material-intake“ endest du und nennst `material-intake` als nächsten Lauf, in einer neuen
Sitzung.

Liegt Material im Projektordner, das in `inputs/` fehlt, gleichst du es nicht ab: das legt
`material-intake` ab. Nenne die Quellen mit Titel und Datum und arbeite sie in der Folge ihrer Termine
ab, **eine nach der anderen, Step 5 bis 9 je Quelle**. Wird der Kontext knapp, endest du nach einer
Quelle; der Stand liegt im Repo.

### Step 5 — Den Stand lesen

Lies die Quelle in `inputs/` ganz und die Notiz, die `material-intake` zu ihr geschrieben hat; trägt
sie `Intern: ja` oder einen Abschnitt `## Intern`, gilt [ref-requirement.md](ref-requirement.md),
Interna. **Den Stand liest du aus dem Repo, nicht aus dem Sheet und nicht aus dem Kontext**:
`requirements/` und `gaps/` durchsuchst du je Kandidat mit `grep -il` nach Stichworten und liest nur
die Treffer ganz; die Kennungen und den Kopf jeder Datei liest du mit `grep -H '^id:\|^title:\|^status:'`.
Dazu die offenen Aufgaben in `todo/` zu den Treffern, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 1.

### Step 6 — Die Kandidaten schneiden, ein Verdikt je Kandidat

| Verdikt | Wann | Folge |
|---|---|---|
| Anforderung | jemand will etwas, das der Shop heute nicht tut | neue Datei in `requirements/` |
| gehört zu | dasselbe Wollen wie eine bestehende Anforderung | keine zweite Datei; schärft es den Soll-Zustand, eine Korrektur |
| Ist-Aussage | beschreibt, was der Shop heute tut oder nicht tut | `## Current state` und `live`, nur wenn das Material den Stand widerlegt |
| Korrektur | der Kunde nimmt eine Aussage zurück oder ändert sie | die Abschnitte der bestehenden Datei, `source` wächst |
| Bestätigung | der Kunde bestätigt eine Anforderung ausdrücklich | `status: confirmed` |
| Priorität | der Kunde nennt eine Anforderung ausdrücklich nachrangig („wäre schön“), oder holt sie zurück | `priority: nice-to-have` mit der Stelle in `source`, zurück `must-have`; sonst bleibt `must-have` (§327) |
| Ausklammerung | nimmt eine Anforderung zurück oder aus dem Scope, oder holt sie zurück | `status` oder `scope`, dazu eine ADR nach [ref-adr.md](ref-adr.md) |
| Duplikat | zwei Anforderungen für dasselbe Wollen | `status: duplicate` und `duplicate_of` an der jüngeren; gelöscht wird nichts |
| Scope-Freigabe | der Kunde gibt den Scope frei, im Expert Service die Ansage des Leads | `scope` je genannte Anforderung |
| Frage | eine Angabe fehlt, und ohne sie ist die Anforderung nicht zu lösen | neue Datei in `gaps/` nach [ref-questions.md](ref-questions.md) |
| Antwort | beantwortet eine offene Frage ausdrücklich | die Frage wird geschlossen, mit Antwort und Quelle |
| Aufgabe | eine Absprache oder Arbeit, die jemand bei uns tun muss, keine Frage an den Kunden | neue Datei in `todo/` nach `ref-tasks.md` und [ref-questions.md](ref-questions.md) (§359) |
| erledigt eine Aufgabe | dieser Lauf tut, was eine offene Aufgabe nennt, etwa eine Teilung | die Aufgabe wird `done`, mit dem Ergebnis, nach `ref-tasks.md` |
| Entscheidung | eine Wahl ist gefallen, mit einer Alternative, die nicht genommen wurde | ADR nach [ref-adr.md](ref-adr.md) |
| Vorgabe der Architektur | das Material legt Bauform, Theme, Stores, Integrationsschicht oder ein System fest | Zeile in `architecture.md` nach [ref-architecture.md](ref-architecture.md) |
| Seitentyp, Design-Übergabe | die UX/UI-Session legt Seitentypen fest, oder ein abgenommener Seitentyp wird übergeben | nach [ref-requirement.md](ref-requirement.md), Seitentypen, Theme und Sections |
| nicht aufgenommen | Meinung, Nebensatz, schon erledigt | eine Zeile mit Grund in der Notiz |

Wie eine Anforderung aussieht, steht in [ref-requirement.md](ref-requirement.md), wann eine Frage eine
ist, in [ref-questions.md](ref-questions.md); lies beide, bevor du die erste Datei baust. **Nur was das
Material ausdrücklich sagt, schließt eine Frage, bestätigt oder klammert aus;** eine Tendenz lässt
es offen und steht in der Notiz. **Vor jeder neuen Frage suchst du**, ob eine frühere Notiz, ADR oder
Frage sie schon beantwortet (§215); dann ist sie keine Frage, sondern eine Antwort mit dieser Quelle.
Neue Kennungen zählst du je Ordner von der höchsten weiter (§230).

### Step 7 — Vorlegen und das Ja abwarten

Zeig einen Block nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. **Kommst du direkt aus
`material-intake`**, steht zuoberst, was es abgelegt und als intern markiert hat, mit seinem Bericht
(§400); beim ersten Lauf folgt, was Step 3 anlegt. Dann **jede geplante Änderung im Repo**: je neue
Anforderung ihr Kopf und ihr Rumpf, je geänderte Datei die Felder und Abschnitte alt und neu, je
geschlossene Frage ihre Antwort; darunter jede ADR mit Titel, jede Änderung an `architecture.md` und
an einem Epic mit alter und neuer Zeile und, war die Quelle eine Pflichtliste, ihr Eintrag in
`baselines.yml` alt und neu. Eine Anforderung mit entschiedenem Lösungsansatz oder an einem Epic mit
`board_key` markierst du ([ref-requirement.md](ref-requirement.md), Korrektur). **Die neuen offenen
Fragen** stehen als Liste mit Adressat, je mit ihrer Datei, nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`; einzeln fragst du nur nach dessen fester Regel,
vor dem Block. Dann die Aufgaben und „Interna: keine“, wie die Vorschau es vorgibt.

**Gibt es einen freigegebenen Snapshot, gleichst du vor dem ersten Vorlegen des Laufs ab, Pflicht**
(§266), nach [ref-snapshot.md](ref-snapshot.md); seine Zeilen stehen über dem Block. **Nennt der Lead
das Ende der Discovery**, steht der Snapshot `discovery` als eigene Zeile darunter.

Die Frage nennt die Zahlen, etwa „Soll ich die 12 Anforderungen und 5 offenen Fragen so in die
Anforderungsliste übernehmen?“; ohne Sheet heißt das Ziel „ins Repo“.

### Step 8 — Schreiben

Beim ersten Lauf legst du zuerst Sheet und Architektur an, wie Step 3 es beschreibt.

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht**, in keine Datei
(§236; was darunter fällt, sagt der Datalayer-Vertrag). Dann, jeweils direkt davor gelesen: die
Anforderungen und Fragen nach [ref-requirement.md](ref-requirement.md) (Den Datalayer schreiben), die
ADRs nach [ref-adr.md](ref-adr.md), `architecture.md` nach [ref-architecture.md](ref-architecture.md),
`baselines.yml` nach [ref-baseline-rows.md](ref-baseline-rows.md) (§269), die Aufgaben nach `ref-tasks.md`, und je Quelle die neue Notiz
`<Name der Quelle>-abgleich.md` in `notes/` nach [ref-requirement.md](ref-requirement.md). **Die Notiz
ist das Zeichen, dass die Quelle abgeglichen ist.** Dann die nächste Quelle, zurück zu Step 5; nach
der letzten Step 9.

### Step 9 — Prüfen, projizieren, committen

Nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit `caller: requirements-update`: Prüfung mit
`check-repo.py`, Projektion ins Sheet, `readme.md` und `way-of-working.md`. Stand im Block der Snapshot
`discovery`, schreibst du ihn danach nach [ref-snapshot.md](ref-snapshot.md). Dann ein Commit, Nachricht
`requirements-update: <was>`; hat der Lauf eine Zeile in `architecture.md` ersetzt, nennt die Nachricht
die ersetzte Aussage (§231).

### Step 10 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397), nach `material-intake` für beide Läufe: neue, geänderte, bestätigte und ausgeklammerte Anforderungen mit Kennung; der Scope, wenn
er sich änderte, mit der Zahl je Wert; seit einer Freigabe die Abweichungen als mögliche Change
Requests, mit dem Snapshot; neue Fragen, davon blockierende; **jede geschlossene Frage mit ihrer
Kennung und der Quelle der Antwort**; jede geänderte Anforderung mit entschiedenem Lösungsansatz oder Ticket;
Seitentypen mit mehr Sections als angenommen; jede ungelesene Quelle, auch die Wissensbasis. Nach dem
ersten Lauf dazu: die Anforderungsliste mit Link, dass die Architektur angelegt ist, und welche
Angaben noch offen sind, in Worten.

Dann den nächsten Lauf, als Hinweis, **in einer neuen Sitzung**: `requirements-review`, wenn viele
Anforderungen dazukamen; `solution-approach` für Anforderungen ohne Lösungsansatz; `epic-structure`, wenn
Anforderungen ohne Epic warten; `solution-design` für ein Epic, dessen Anforderungen sich geändert
haben, **immer** für jedes Epic mit gesetztem `draft`, an dessen Anforderungen dieser Lauf das Was
oder die Akzeptanzkriterien geändert hat, mit Kennung des Epics; `ticket-factory` nach einer
Design-Übergabe für die Section-Subtasks. **Du stößt keinen an**;
der Lead ruft ihn auf.

## Wann nachfragen (NICHT raten)

- Unklar, ob ein Kandidat dasselbe Wollen wie eine bestehende Anforderung ist: frag, bevor du ergänzt.
- Zwei Quellen sagen Verschiedenes, und keine ist sicher die jüngere: eine Frage, keine Korrektur.
- Ein Name in der Quelle ist nicht sicher einem System oder Fachbegriff zuzuordnen: eine Frage.
- Eine Scope-Freigabe nennt Anforderungen nicht eindeutig: frag, welche gemeint sind.
