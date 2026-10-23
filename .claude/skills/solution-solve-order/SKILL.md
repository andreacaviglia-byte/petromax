---
name: solution-solve-order
description: 'Die Reihenfolge des Lösens der Epics setzen, mit dem Add-on solutioning, als erster Lauf des Solutioning: Fundament zuerst, dann Blockiertes, Riskantes schmal vorn, je Epic in solve_order, mit Grund und Stelle. Nutze das bei "in welcher Reihenfolge lösen wir die Epics", "welches Epic lösen wir zuerst", "Reihenfolge des Lösens", "solve_order neu setzen". Schneidet NICHT (epic-structure), ordnet NICHT das Bauen (solution-critical-path), entwirft KEINE Lösung (solution-design).'
---

Verträge: schreibt `datalayer-contract.md`; liest `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`.

# Die Reihenfolge des Lösens setzen

**Gelöst wird zuerst, was den größten Fehler verbergen kann** (§318). Dieser Lauf setzt je Epic
`solve_order` nach dem Schnitt und vor dem ersten `solution-design`; er ist der erste Lauf des
Solutioning und läuft nur mit dem Add-on `solutioning` (§403). Am Ende trägt **jedes Epic in
`epics/` eine Zahl in `solve_order`**, nach [ref-solve-order.md](ref-solve-order.md), und der Lead
kennt je Epic den Grund mit seiner Stelle. Die Reihenfolge ist eine Empfehlung für `solution-design`,
kein Tor (§148). Die Reihenfolge des Bauens leitet nach den Lösungen `solution-critical-path` ab.

**Du liest das ganze Vorhaben und schreibst nur `solve_order` in die Köpfe der Epics.** Ein Epic, das
fehlt, eine Anforderung ohne Epic oder eine falsche Zuordnung führt `epic-structure`; du nennst sie im
Bericht und ordnest, was steht. Gibt es neue Epics, läufst du neu; jeder Lauf prüft alle Epics.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest seine Dateien direkt, mit dem
Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` festlegt; einen Connector braucht
dieser Lauf nicht. **Scheitert ein Aufruf zweimal gleich, hältst du an** und nennst Aufruf und
Meldung. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und Begründung und suchst keinen zweiten
Weg.

### Step 1 — Das Vorhaben binden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,project_type
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. **Steht `solutioning` nicht in `add_ons`,
hältst du an** und nennst es: ohne das Add-on gibt es keine Reihenfolge des Lösens, und nach dem
Schnitt folgt `ticket-factory` (§403). Ist `project_type` leer, hältst du ebenso an und nennst
`project-setup`.

### Step 2 — Den Stand lesen

Arbeitsdateien legst du in einen eigenen Temp-Ordner außerhalb des Repos (`mktemp -d`); ins Repo
kommen nur die Köpfe der Epics (§233). Du liest jede Datei in `epics/` ohne ihren Rumpf, je
Anforderung in `requirements/` den Kopf, `## Description` und `## Approach`, die offenen Fragen in
`gaps/`, die offenen Aufgaben in `todo/` nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 1, und
`architecture.md`. **Gibt es keine Datei `epics/EP-NNN.md`, gibt es nichts zu ordnen**: du nennst
`epic-structure` und schreibst nichts.

Dann prüfst du die Zuordnung:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-repo.py . --check epic
```

`epic` hindert die Reihenfolge nicht; der Bericht nennt jede Zeile mit `epic-structure`.

### Step 3 — Die Reihenfolge ableiten

**Nach [ref-solve-order.md](ref-solve-order.md)**, über alle Epics des Vorhabens: je Epic die Stufe
der Regel, die zuerst greift, mit der Stelle, die sie belegt; daraus `solve_order`. Ein Epic, das
schon eine Lösung trägt (`draft` gesetzt oder eine Anforderung mit `solution_status: decided`),
behält seinen Platz vor den ungelösten, und du nennst es als gelöst.

### Step 4 — Die Reihenfolge zeigen und das Ja abwarten

**Aufgaben** (§359): die offenen in `todo/` zu deinem Umfang liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Zeig alle Epics in der neuen Folge, je Epic Kennung, Titel, `solve_order` heute und neu, den Grund mit
seiner Stelle und, bei einem breiten riskanten Epic, den Durchstich. Aufbau, Frage und Ja nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`; ändert der Lead die Folge, übernimmst du sie mit
seinem Wortlaut als Grund und zeigst neu.

### Step 5 — Schreiben, berichten und den nächsten Lauf nennen

Schreib in jedem Epic, dessen Zahl sich ändert, nur die Zeile `solve_order` im Kopf, die Datei direkt
davor gelesen und danach zurückgelesen. Dann endest du nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit den Teilen 1, 5 und 6: die Reihenfolge steht
in keiner Spalte des Sheets, die Teile 2 bis 4 entfallen. Die Commit-Nachricht ist
`solution-solve-order: <was>`.

Sag knapp, nach der Regel für Berichte (§397): die Folge der Epics in einem Satz je Stufe, die
vorgeschlagenen Durchstiche, was sich gegen die bisherige Folge verschoben hat, und was die Zuordnung
meldete.

Dann den nächsten Lauf, **in einer neuen Sitzung**: **`solution-design`** für das erste Epic nach
`solve_order`; `epic-structure` für Anforderungen ohne Epic oder ein fehlendes Epic. **Du stößt
keinen an**; der Lead ruft ihn auf.

## Was dieser Lauf nicht tut

Er schreibt nichts ins Sheet, in keine Anforderung, in keinen Kopf eines Epics außer `solve_order`
und nicht in `architecture.md`. Er schneidet nicht, hängt nicht um und teilt nicht; er beantwortet
keine Architekturfrage, entwirft keine Lösung und leitet keine Reihenfolge des Bauens ab. Er legt
nichts auf dem Board an.
