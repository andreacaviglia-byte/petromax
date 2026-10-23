---
name: solution-approach
description: 'Je Anforderung bis zu drei Lösungsansätze vorschlagen, vor dem Schnitt: Fit gegen den Standard, grobe Größe aus Bau, Konfiguration und Pflege, Stamps der Wissensbasis, Empfehlung, ungeprüft in die Anforderung; im Expert Service wählt der Lead hier. Nutze das bei "Standard, App oder Custom?", "grober Lösungsansatz je Anforderung", "geht das mit Bordmitteln". Löst KEIN Epic (solution-design), schneidet KEINE Epics (epic-structure), legt KEINE Tickets an (ticket-factory).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`; liest `solution-choice-contract.md`, `kb-contract.md`, `shopify-limits.md`, `connector-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-run-scope.md`.

# Die Lösungsansätze je Anforderung vorschlagen

Am Ende stehen **in jeder Anforderung im Umfang bis zu drei Lösungsansätze**, ungeprüft, unter
`## Approach` ihrer Datei in `requirements/`, je mit einem Satz, seiner Größe aus Bau, Konfiguration
und Pflege, seinem Fit gegen die Grenzen von Shopify und dem passenden Stamp der Wissensbasis, der
empfohlene zuerst (§275, §280, §326, §401). Dazu **eine Notiz `notes/JJJJ-MM-TT-solution-approach.md`**
mit den Lösungen, die mehrere Anforderungen zugleich tragen, den Grenzen und, **im Expert Service,
einem Projekt-Hinweis** mit Begründung. `epic-structure` schneidet danach entlang dieser
Lösungen, `solution-design` belegt die Lösungsansätze und wählt, `ticket-factory` im Expert Service
nimmt den gewählten.

**Jede Anforderung bearbeitest du für sich, im Projekt wie im Expert Service gleich** (§401): der Fit
gegen den Standard, bis zu drei Lösungsansätze und eine Empfehlung, ohne Belege. **Mit dem Add-on
`solutioning` wählt hier niemand**: gewählt wird in `solution-design` mit Beleg und ADR. **Im Expert
Service wählt der Lead hier**, vor der Vorschau. **Deshalb trägt die Anforderung `solution_status:
proposed`** und ihre Lösungsansätze erscheinen nicht im Sheet, in keinem Entwurf, auf keiner Seite
und auf keinem Board: ein Lösungsansatz, den der Kunde liest, gilt ihm als zugesagt. Den
Projekt-Hinweis entscheidet der Lead; du empfiehlst nur. `grill-me` ruft dieser Lauf nicht (§287).
**Kein Skill ruft einen anderen**; du nennst den nächsten Lauf.

**Kontext ist knapp, weil der Lauf über viele Anforderungen geht:** je Anforderung ein Satz je
Lösungsansatz, aus der Wissensbasis nur `index.md` und die Stamps, die passen, aus der Dokumentation
nur, was einen unklaren Fit klärt ([ref-approach.md](ref-approach.md), Der Fit).

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest seine Dateien direkt und
schreibst nur `## Approach`, `classification`, `size`, `size_estimate_approach` und `solution_status`
der Anforderungen, die Notiz und die Notiz einer Runde, mit dem Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` und `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md` festlegen. Die Werte
der Klassifizierung stehen dort, die Auswahl und die Größentabelle in
`${CLAUDE_SKILL_DIR}/../../docs/solution-choice-contract.md`, was aus der Wissensbasis gilt, in
`${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`. Das Ende des
Laufs, Prüfung, Projektion und Commit, steht in `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`.
**Scheitert ein Aufruf zweimal gleich, hältst du an** und nennst Aufruf und Meldung. Lehnt die Sitzung
einen Aufruf ab, nennst du Aufruf und Begründung und suchst keinen zweiten Weg.

### Step 1 — Den Steckbrief lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,shops,requirements_sheet,project_type
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen; ohne `project.yml` oder `project_folder`
ist `project-setup` der nächste Lauf. Exit 3 nennt die leeren Felder. Dann liest du `project.yml`
ganz. **Ein leeres `requirements_sheet`** hält nicht an: es fehlt nur die Projektion, und der Bericht
nennt `requirements-update`. **Leere `shops` oder ein leeres `plan`** halten nicht an: eine Grenze, die
am Plan hängt, wird eine Frage, keine Annahme, und der Bericht nennt `project-setup`. **Liegt in
`requirements/` keine Anforderung**, ist das kein Stand: verweise auf `requirements-update`; Material
aus dem Chat nimmt er an, nicht dieser Lauf (§282).

Ob das Vorhaben ein Expert Service ist, liest du aus `project_type` (§303); ist das Feld leer, fragst du einmal und nennst `project-setup` im Bericht. Daran hängen der Projekt-Hinweis und der nächste Lauf.

### Step 2 — Die Verbindungen prüfen

**Die Doku ist eine Quelle, keine Voraussetzung** (§339, §340): du liest sie über die Wege aus
`${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`, Abschnitt „Die Doku von Shopify“, wo sie eine
Plattformaussage belegt, nennst je Beleg URL, Datum und Stufe, und hältst nicht an, wenn sie fehlt. Die Wissensbasis (`get_file_contents`, in der Cloud vorher `add_repo`) ist **weich**: fehlt
sie, arbeitest du weiter, und Notiz und Bericht sagen es an jeder betroffenen Stelle
([ref-approach.md](ref-approach.md), Wenn eine Quelle fehlt).

**Für einen Umfang nach Workstream (Spalte `Cluster`) und für die Projektion am Ende** prüfst du, dass
`Google_Drive.get_file_metadata`, `Google_Drive.download_file_content`, `Google_Sheets.get_spreadsheet`
und `Google_Sheets.get_values` in der Werkzeugliste stehen; der Name im Aufruf trägt ein Präfix des
Servers, verglichen wird die Endung. Steht eines nicht da, such es über die Werkzeug-Suche. Findet auch
die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets› ist in dieser Sitzung nicht
verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden." Vor dem ersten
Zugriff auf das Sheet liest du mit `get_file_metadata` (`fileId`) seine Eltern, bis der Projektordner
(`project_folder`) erreicht ist. **Einen anderen Kundenordner liest du nicht**, auch nicht auf Bitte
im Chat.

### Step 3 — Die Anforderungen lesen

Nach [ref-read.md](ref-read.md): die Liste aus dem Script, für einen Workstream vorher die schmale
Spalte. **Die Dateien holst du nicht alle zugleich in den Kontext**, sondern die Liste: je
Anforderung eine Zeile; jede Anforderung im Umfang öffnest du erst in Step 5, für sich.

**Den Umfang nennt der Aufruf**: eine oder mehrere IDs, der Regelfall; ein Workstream wörtlich; alle
nur, wenn er „alle“ sagt. **Nennt er keinen, läufst du nicht los** (§398, `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`): du nennst in einem Satz die
Zahl der Anforderungen ohne Lösungsansatz je Workstream und dass einzelne Anforderungen ins freie Feld
gehören, und fragst „Für welche Anforderungen schlage ich den Lösungsansatz vor?“, mit Mehrfachauswahl,
ohne Empfehlung. Die Antworten sind bis zu drei Workstreams mit ihrer Zahl, die mit den meisten
zuerst, etwa „SHOP (12 ohne Lösungsansatz)“, und „Alle ohne Lösungsansatz“. Die Zahl je Workstream holst du
mit der schmalen Spalte `Cluster` wie für einen Umfang nach Workstream ([ref-read.md](ref-read.md));
fehlt das Sheet oder trägt keine Anforderung einen Cluster, ist „Alle ohne Lösungsansatz“ die einzige
Antwort neben dem freien Feld.

**Der Umfang begrenzt, wo du schreibst, nicht was du liest** (§215, §398): die Liste holst du immer
mit `--umfang alle`, damit jeder Lösungsansatz im Umfang zu den Lösungsansätzen der übrigen Anforderungen passt.

**Trägt eine Anforderung schon einen Lösungsansatz, schlägst du für sie nichts Neues vor**:
`entschieden:` oder `blockiert:` hat `solution-design` gesetzt, `vorgeschlagen:` ein früherer Lauf
([ref-approach.md](ref-approach.md), Die Lösungsansätze in der Datei); einen Vorschlag ersetzt du nur,
wenn der Lead es für diese Anforderung sagt. Die Notiz zählt ihn mit; widerspricht er einer Grenze,
die du findest, ist das ein Befund im Bericht, keine neue Wahl.

**Designkonzept und UX/UI-QA bekommen keinen Lösungsansatz** (§297): eine Anforderung mit `standard:
design-concept` oder `design-qa` ist Arbeit des UX/UI-Designers im Design-Epic, keine Lösung im Shop.
Das Script nimmt sie aus dem Umfang und nennt sie in der Zeile „ohne Lösungsansatz (Design-Epic,
§297)“; du schreibst in ihre Dateien nichts, und Notiz und Bericht nennen sie mit diesem Wortlaut.

**Eine abgebrochene Sitzung**: steht in `notes/` eine Notiz einer Runde dieses Laufs mit `Stand:
offen`, liest du sie nach `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Die Notiz
einer Runde, nennst ihr Datum und `Lead:` und übernimmst ihre Antworten in Step 6.

### Step 4 — Die Architektur lesen

Lies `customer.md`, `architecture.md` und die ADRs in `decisions/` mit `status: accepted`. **Eine
`entschieden`e oder `belegt`e Zeile und eine akzeptierte ADR gelten**: ein Lösungsansatz, der eine
bricht, steht mit dem, was er bricht. Eine `offen`e Zeile ist keine Annahme: ein Lösungsansatz, der
sie voraussetzt, nennt sie in seinem Satz `Offen:`.

### Step 5 — Die Lösungsansätze je Anforderung vorschlagen

**Nach [ref-approach.md](ref-approach.md); lies sie, bevor du den ersten Lösungsansatz schreibst.**
Je Anforderung, eine nach der anderen: du öffnest sie mit `--zeile` ([ref-read.md](ref-read.md)),
prüfst den Fit gegen den Standard, streichst harte Grenzen, nimmst bis zu drei Lösungsansätze auf,
je mit grober Größe aus Bau, Konfiguration und Pflege, wägst nach dem Vertrag der Wahl und gibst die
Empfehlung. Die Wissensbasis liest du einmal über ihren `index.md`, dann die Stamps, deren Eintrag zu
einem Lösungsansatz passt, jeden ganz, und die Best Practices für seine Art; die `source_url` eines
Stamps öffnest du nie. **Ist keiner zu empfehlen**, stehen die Kandidaten mit der Frage, an der es
hängt; an einer kaufmännischen Präferenz wählst du keine Seite.

Danach fasst du zusammen, **welche Lösung mehrere Anforderungen trägt**: dieselbe App, dieselbe
Custom App, dieselbe Schnittstelle je Datenstrom, über alle Anforderungen der Liste, auch außerhalb
des Umfangs. **Widerspricht ein Lösungsansatz im Umfang dem Lösungsansatz einer Anforderung außerhalb**, etwa zwei Apps
für denselben Zweck, änderst du den anderen nicht: der Widerspruch steht mit beiden IDs in der Notiz
und im Bericht. Im Expert Service prüfst du dann den
**Projekt-Hinweis** nach [ref-approach.md](ref-approach.md), Projekt-Hinweis.

### Step 6 — Im Expert Service wählen, vorlegen und das Ja abwarten

**Im Expert Service wählt der Lead zuerst** nach [ref-approach.md](ref-approach.md), Die Wahl im
Expert Service: je Anforderung mit mehr als einem Lösungsansatz eine Frage, bis zu vier in einem
Aufruf (§396). **Nach jeder Runde** schreibst du seine Antworten in die Notiz einer Runde, committest
und pushst sie allein (`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Die Notiz einer
Runde); die Anforderungen schreibst du erst nach dem Ja. Mit dem Add-on `solutioning` entfällt die
Wahl.

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Zeig je Anforderung den Abschnitt `## Approach`, `classification`, `size` (und mit ihr
`size_estimate_approach`) und `solution_status`, wie sie in die Datei gehen, als Tabelle mit ID, je
Lösungsansatz Name, Größe, Fit und KB, und der Empfehlung oder der Wahl des Leads, und darunter die
Notiz in der Form aus [ref-approach.md](ref-approach.md), Die Notiz, mit ihrem Dateinamen. Aufbau,
Frage und Ja nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. Korrigiert der Lead einen
Lösungsansatz, ist das eine Runde wie oben: sein Wortlaut geht in die Notiz einer Runde, sein
Lösungsansatz steht mit „Chat mit dem Lead vom ‹Datum›“ im Satz des Lösungsansatzes, in der Sprache
aus `language` (`source_chat` in `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
„Die festen Wendungen“, §337), und du zeigst den Block neu.

### Step 7 — Schreiben, prüfen, projizieren, committen

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht** (§236; was darunter
fällt, sagt der Datalayer-Vertrag). Je Anforderung liest du die Datei direkt davor, setzt nur
`## Approach` an das Ende des Rumpfs, `classification`, `size`, `size_estimate_approach` mit demselben
Wert wie `size` (§357) und `solution_status: proposed`, schreibst die
ganze Datei und liest sie zurück. Dann legst du `notes/JJJJ-MM-TT-solution-approach.md` an; steht der
Name schon, hängst du `-2` an. Eine Notiz einer Runde setzt du auf `Stand: abgeschlossen`. Die Metrik-Zeile schreibst du nach der Wurzel-`CLAUDE.md` (§246).
Dann endest du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md` mit
`caller: solution-approach`: ein vorgeschlagener Lösungsansatz ändert im Sheet nichts, `project-sheet.py
--repo-only` meldet dann `KEINE`, und das Sheet wird nicht gelesen. Commit-Nachricht `solution-approach: <Umfang>`.

### Step 8 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397): Umfang und Zahl der Anforderungen; je Art und je Größe des ersten Lösungsansatzes die Zahl, und wie viele mehr als einen tragen; die IDs „ohne Lösungsansatz (Design-Epic,
§297)“; die ohne Empfehlung mit ihrer Frage; im Expert Service die Wahl des Leads, wo sie von der
Empfehlung abweicht; die Lösungen über mehrere Anforderungen; die harten Grenzen, die einen
Lösungsansatz gestrichen haben; im Expert
Service den Projekt-Hinweis mit Empfehlung und Gründen; was ungelesen blieb, mit Grund. Dann den nächsten Lauf, **„in einer
neuen Sitzung“**: im Projekt `epic-structure`, mit und ohne `solutioning` (§403); im Expert Service `ticket-factory`, und
empfiehlt der Hinweis ein Projekt, entscheidet der Lead. **Du stößt keinen an**; der Lead ruft ihn auf.

## Wann nachfragen (NICHT raten)

- Der Aufruf nennt einen Workstream, den es in der Spalte `Cluster` nicht gibt: nenne die vorhandenen und frag.
- Eine Anforderung betrifft einen von mehreren Shops, und weder `title` noch Material sagen, welchen.
- Im Expert Service die Wahl zwischen mehreren Lösungsansätzen, nach Step 6.

Sonst fragst du nicht: eine Anforderung ohne Empfehlung steht in der Datei mit ihrer Frage.

## Was dieser Lauf nicht tut

Er schreibt nichts ins Sheet außer über die Projektion, in keinen Entwurf, auf keine Seite und auf kein
Board, legt keine ADR und keine Frage in `gaps/` an und ändert das Was einer Anforderung,
`architecture.md` und `project.yml` nicht. Er sammelt keine Belege, wählt mit dem Add-on
`solutioning` keinen Lösungsansatz, schneidet keine Epics, setzt keine Größe endgültig, schätzt keine
Stunden und vergibt keine Kennung: die Modellschätzung in Stunden setzt nur `solution-design` mit dem
Add-on `solutioning` (§357).
