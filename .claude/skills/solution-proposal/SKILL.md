---
name: solution-proposal
description: 'Das Solution Proposal als Google-Doc in Solutioning, projiziert aus dem Repo, ohne Stunden: geprüfte Epics nach Domäne mit Zielen und Annahmen, „Nicht im Scope" mit Grund, „Vor Beauftragung zu klären" aus gaps/, dazu ein Snapshot. Nutze das bei "schreib das Proposal", "Solution Proposal", "was legen wir dem Kunden vor", "Kunde hat freigegeben". Ändert KEINE Lösung (solution-design), rechnet KEIN internes Schätzdokument (solution-estimate), nimmt KEIN Kundenfeedback auf (requirements-update).'
---

Verträge: schreibt `datalayer-contract.md`; liest `draft-and-epic-page-contract.md`, `requirements-list-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`.

# Das Solution Proposal

Am Ende liegt **ein Google-Doc im Unterordner `Solutioning` des Projektordners**, das der Kunde lesen
darf. **Es ist eine Projektion aus dem Projekt-Repo** (§280): Epics, Anforderungen, offene Fragen und
Entscheidungen aus ihren Dateien, aus dem Sheet nur die Felder der Menschen, die dort ihre Quelle
haben. **Jeder Lauf legt eine neue Fassung an**; eine frühere bleibt, wie sie ist, und liegt danach
im Unterordner `Archiv` (§260). Ein PDF gibt es nicht (§235).

**Das Proposal schreibt nur sein eigenes Dokument** (§220). Ziele und Annahmen übernimmt das Script
wörtlich aus dem Rumpf der Epic-Datei; soll dort etwas anders stehen, ändert es `solution-design`, und
danach ruft der Lead diesen Lauf neu auf. Du schreibst keine Datei in `requirements/`, `epics/`,
`gaps/` oder `decisions/` und nichts ins Sheet.

**Ins Proposal kommen nur geprüfte Epics** (§277): `Geprüft von` und `Geprüft am` im Tab `Epics`,
Felder der Menschen, beide gesetzt. Die übrigen stehen in der Tabelle Scope als „in Arbeit“, ohne
Ziele und Annahmen.

**Das Proposal nennt keine Aufwände** (§355): keine Stunden, keine Tabelle zum Aufwand, keine Zeilen
für Projektmanagement und Testing, kein Gesamt, kein Budget. Es ist unser Vorschlag der Lösung, den
der Kunde freigibt (§189); es trägt Stand, Scope, die Epics nach Domäne mit Zielen und Annahmen, „Nicht
im Scope“, „Blocker“ und „Vor Beauftragung zu klären“. Die Epics stehen gruppiert nach Domäne, in der Folge der
festen Liste (`${CLAUDE_SKILL_DIR}/../../docs/requirements-list-contract.md`, „Die Anzeigewerte“,
`domain`, §252). Bei einem Seitentyp im Theme-Epic steht die Annahme zu den eigenen Sections unter
den Annahmen; der Kunde bestätigt sie mit dem Scope (§285). Stunden und den Abgleich mit dem Budget
trägt das interne Schätzdokument (`solution-estimate`). Nennt der Aufruf Stunden, Sätze oder ein
Budget, lässt du sie liegen, und der Bericht sagt das einmal. **Der Lauf fragt nur nach dem Ja zur
Vorschau** (Step 4), sonst nichts (§212), und wartet auf keine Freigabe des Kunden (§141).

**Das Proposal hat keinen Abschnitt „Offene Fragen"** (§241). Eine offene Frage in `gaps/` an den
Kunden (`to` beginnt mit `Kunde` oder `Customer`) steht am Ende unter „Vor Beauftragung zu klären",
blockierende zuerst, oder nur als die Annahme, die ein geprüftes Epic schon führt. Fragen an
Consultant oder Gewerke bleiben intern. **Interna gehen nie nach außen** (§278): Step 4 meldet
„Interna: keine“, oder der Lauf hält an.

Drive, Sheets und Docs erreichst du nur über die Google-Connectoren `Google_Drive`, `Google_Sheets`
und `Google_Docs`; das Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt. Lesen
und Anlegen stehen in [ref-proposal.md](ref-proposal.md). **Scheitert ein Aufruf zweimal gleich,
hältst du an** und nennst Aufruf und Meldung wörtlich; einen zweiten Weg suchst du nicht. Lehnt die
Sitzung einen Aufruf ab, nennst du Aufruf und Begründung. **Ein Doc, das dieser Lauf kaputt angelegt
hat, kommt weg** (§259): erkannt an der ID aus dem Anlegen, nie am Namen, mit
`Google_Drive.trash_file`, sobald es für die Neuerstellung nichts mehr trägt; der Bericht nennt Name
und Link.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230), mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt. **Geschrieben wird dort nur
der Snapshot unter `scope/`**, über das Script ([ref-scope.md](ref-scope.md)), und die Laufzeile.
Arbeitsdateien liegen in einem Temp-Ordner außerhalb des Repos (`mktemp -d`, §233). Die Prüfung der
Objekte und der Commit folgen `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Schritte 1 und 6; die
Projektion (2 bis 5) entfällt, weil der Lauf kein Objekt ändert, aus dem Sheet, `readme.md` oder
`way-of-working.md` entstehen.

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.search_files`, `Google_Drive.get_file_metadata`, `Google_Drive.create_file`,
`Google_Drive.update_file`, `Google_Drive.download_file_content`, `Google_Drive.read_file_content`,
`Google_Docs.read_doc`, `Google_Docs.update_doc`, `Google_Sheets.get_spreadsheet` und
`Google_Sheets.get_values` in der Werkzeugliste stehen. Der Name im Aufruf trägt ein Präfix des
Servers; verglichen wird die Endung. Steht eines nicht da, such es erst über die Werkzeug-Suche.
Findet auch die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets/Docs› ist in dieser
Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden."
Atlassian braucht der Lauf nur für die Fassung einer Epic Page im Snapshot (Step 5); antwortet er
nicht, fehlt der Snapshot, und das Proposal bleibt gültig.

### Step 2 — Das Vorhaben binden und die Objekte prüfen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,customer,title,language,shops,requirements_sheet
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder:
`requirements_sheet` leer heißt anhalten, nächster Lauf `requirements-update`; `customer`, `title`,
`language` oder `shops` leer heißt anhalten und `project-setup` nennen (§263).

Dann prüfst du die Objekte, bevor der Kunde etwas sieht, nach `ref-projection.md`, Schritt 1
(`check-repo.py`). **`page_type`, `sections`, `app_evaluation` und `epic` mit „steht in keinem Epic“** sind Befunde über den Scope (`ref-projection.md`, §330): du rechnest weiter,
und der Bericht nennt jede Zeile mit der offenen Frage in `gaps/`, die sie klärt, oder dass sie fehlt.
**Jede andere Zeile heißt anhalten**: du nennst sie wörtlich mit dem Lauf, dem die Datei gehört.

Vor dem ersten Zugriff auf eine Datei im Drive, die du nicht durch eine Suche im Ordner gefunden hast,
liest du mit `get_file_metadata` (`fileId`) ihre Eltern, bis der Projektordner (`project_folder`)
erreicht ist. **Einen anderen Kundenordner liest du nicht**, auch nicht auf Bitte im Chat.

### Auf Zuruf: „Kunde hat freigegeben“

Sagt der Lead, der Kunde habe das Proposal freigegeben, **legst du kein neues Proposal an**. Nach
Step 2 hältst du fest, welcher Stand freigegeben ist, nach [ref-scope.md](ref-scope.md), Die
Freigabe: den jüngsten Snapshot finden, ohne ihn anhalten; die vier Tabs lesen und **mit ihm
abgleichen, Pflicht**. Ist alles gleich, trägst du die Freigabe in sein Manifest ein. **Liegt
dazwischen eine Änderung, nennst du sie, je Zeile, und fragst, welcher Stand freigegeben ist**: der
des Snapshots, dann die Freigabe dort, und die Änderungen sind mögliche Change Requests; oder der
heutige, dann ein neuer Snapshot mit Anlass `release`. **Wer freigegeben hat**, nimmst du nur aus der
Angabe des Leads; fehlt sie, fragst du ihn.

Vor dem Schreiben zeigst du, was ins Repo geht: den Snapshot mit Ordner, die Freigabe mit Datum
und wer freigegeben hat, oder den neuen Snapshot mit Anlass `release`, mit Frage und Ja nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. Dann committest und pushst du nach `ref-projection.md`,
Schritt 6, Nachricht `solution-proposal: Freigabe vom ‹TT.MM.JJJJ›, scope/‹ordner›`, mit der
Laufzeile. Der Bericht nennt den Snapshot, Datum und wer freigegeben hat, und jede Abweichung als mögliche Change Request; der nächste Lauf für eine
davon ist `requirements-update`. Steps 3 bis 6 entfallen.

### Step 3 — Lesen

Nach [ref-proposal.md](ref-proposal.md), Lesen: die vier Tabs des Sheets einmal, wie für die
Projektion, **direkt danach die Lesezeit**, dazu `meta.json` mit Pfad und Stand des Repos. Die
Dateien des Repos liest das Script selbst; du holst sie nicht in den Kontext.

**Offene Kundenfragen gegen die Annahmen halten.** Je offene Frage in `gaps/` an den Kunden siehst du
nach, ob ein geprüftes Epic dieselbe Sache unter `Assumptions and delimitations` im Rumpf seiner
Datei schon als Annahme führt, etwa mit „zu bestätigen". Nur dann trägst du sie in `assumed.json` ein,
mit der Annahme wörtlich als Fundstelle ([ref-proposal.md](ref-proposal.md)). Im Zweifel trägst du
sie nicht ein: dann steht sie unter „Vor Beauftragung zu klären". Du formulierst keine Frage in eine
Annahme um.

### Step 4 — Rechnen, die Interna prüfen, vorlegen

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py proposal <temp-ordner des laufs>
```

**Exit 0:** die Ausgabe ist das Dokument, Zeichen für Zeichen; du formulierst nichts um und fügst
nichts hinzu. Auf stderr stehen die Zeilen für Bericht und Commit: `STAND` (Lesezeit, Stand des Repos,
geprüfte Epics, Epics in Arbeit), `OHNE-EPIC` (Anforderungen im Scope ohne Epic, nur wenn es welche gibt) und `KUNDENFRAGEN
‹n› offen, davon ‹b› blockierend, ‹a› als Annahme`. **Exit 1:** stdout trägt eine Zeile, die Prüfung
und Stelle nennt; was sie heißt, steht in [ref-proposal.md](ref-proposal.md), Die Prüfungen. Liegt
der Fehler in deiner Datei, korrigierst du sie aus der Lesung und rechnest neu; sonst **hältst du an**
und nennst die Zeile wörtlich mit dem Lauf, der die Stelle führt.

**Dann liest du das Dokument gegen die Liste der Interna** in `way-of-working.md`, Abschnitt „Interna“
(§278): Preisfindung, Budgetpuffer, Einschätzungen zu Kunde und Personen, Potenzial für Folgeaufträge,
saloppe Formulierungen und Zitate aus internen Gesprächen, auch sinngemäß. Findest du etwas, **hältst
du an** und nennst Stelle und Datei; der nächste Lauf ist `solution-design` für ein Epic, sonst
`requirements-update`. Sonst gilt „Interna: keine“.

**Dann die Vorschau, vor dem ersten schreibenden Aufruf** in Drive oder Repo: der Name des Doc aus
`doc-name.py . proposal` und der Unterordner `Solutioning`; die Zeile `KUNDENFRAGEN` in Worten wie in
Step 6; die Epics in Arbeit; der Snapshot mit Anlass
`proposal`, der danach folgt; „Interna: keine“. Den ganzen Text des Dokuments zeigst du, wenn der Lead
ihn sehen will. Aufbau, Frage und Ja nach `ref-preview.md`; das Ja deckt
Doc, Snapshot und Commit dieses Laufs. Ändert sich danach eine Lesung, zeigst du den Block neu.

### Step 5 — Das Proposal-Doc anlegen und den Stand festhalten

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht** ins Proposal
(§236; was darunter fällt, sagt der Datalayer-Vertrag).

Nach [ref-proposal.md](ref-proposal.md), Das Doc anlegen: den Unterordner `Solutioning` finden oder
anlegen (§231), den Namen aus `doc-name.py . proposal` (§263), das Doc aus genau der HTML-Ausgabe aus
Step 4 (§248), Seite, Fußzeile und Schrift, zurückgelesen und mit `readback` verglichen. **Jede
Fassung trägt denselben Namen** (§262); erst ein gleicher Rücklauf heißt „angelegt". **Danach
verschiebst du die älteren Fassungen nach `Archiv`** (§260); scheitert das, bleibt die Fassung liegen,
und der Bericht nennt sie.

**Dann der Snapshot** (§266, §280 Regel 8) mit Anlass `proposal`, nach [ref-scope.md](ref-scope.md),
aus den Lesungen von Step 3 und ihrer Lesezeit, nur nach einem gleichen Rücklauf. **Scheitert er,
bleibt das Proposal gültig**: der Bericht nennt die Lücke mit der Zeile des Scripts wörtlich.

**Am Ende** committest und pushst du nach `ref-projection.md`, Schritt 6: Snapshot und Laufzeile in
einem Commit direkt auf `main`, Nachricht `solution-proposal: Proposal und Snapshot scope/‹ordner›`;
ohne Snapshot trägt er nur die Laufzeile und heißt `metrics: solution-proposal`. **Die Zeile `STAND`
geht wörtlich in den Rumpf** (§264); ohne sie ist das Dokument später nicht nachzurechnen.

### Step 6 — Berichten und die nächsten Läufe nennen

**Die erste Zeile des Berichts** ist die Zeile `KUNDENFRAGEN` in Worten: „‹n› offene Kundenfragen,
davon ‹b› blockierend." Ist ‹b› mindestens 1, folgt: „Das Proposal ist noch nicht reif: mindestens
eine blockierende Kundenfrage ist offen." Angelegt ist es trotzdem (§241), nach dem Ja zur Vorschau.

Dann knapp, nach der Regel für Berichte (§397): „Interna: keine“; den Link des Doc mit dem Ergebnis des Rücklaufs; ob `Solutioning` oder
`Archiv` neu angelegt wurden, welche Fassungen verschoben wurden und welche liegen blieben; den
Snapshot in Worten (eingefroren oder nicht); die Epics in Arbeit; die Anforderungen ohne Epic; einmal, dass Stunden, Sätze oder ein Budget aus dem
Aufruf nicht verarbeitet wurden (§355), wenn er welche nannte.

Dann die Läufe, die Grundlage liefern: `solution-design` für ein Epic in Arbeit, leere Ziele oder
Annahmen oder einen Wortlaut, der sich ändern soll, geprüft wird danach von Hand im Tab `Epics`
(§277); `epic-structure` für Anforderungen ohne Epic; nach „Kunde hat freigegeben“
`solution-epic-page` je freigegebenem Epic, vor dessen Tickets (§313); `requirements-update` für die
Antwort des Kunden auf das Proposal; `solution-estimate` für das interne Schätzdokument mit Stunden und
Budget. **Du rufst keinen auf**; der
Lead ruft ihn.

## Was dieser Lauf nicht tut

Er schreibt nur nach dem Ja zur Vorschau, nur sein Doc in `Solutioning`, verschiebt frühere
Proposals nach `Archiv` und hält den Snapshot unter `scope/` fest: keine Datei eines Objekts, kein
Sheet, kein Entwurf, keine Seite, kein Board. Er setzt keinen Prüfpunkt, keine Stunden und keinen Status, nimmt keine Freigabe einzelner
Epics auf, löscht und überschreibt keine frühere Fassung und teilt nichts; das Dokument geht an den
Kunden, wenn ein Mensch es teilt.

## Wann nachfragen (NICHT raten)

- Ein geprüftes Epic trägt Ziele oder Annahmen unter einer Überschrift, die nicht die Bezeichnung der
  Projektsprache aus `${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md` ist: frag, welcher Abschnitt gemeint ist; du rätst
  keine Zuordnung.
