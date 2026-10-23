---
name: solution-critical-path
description: 'Die Reihenfolge des Bauens der Epics ableiten, nach den Lösungen und neu mit jeder Lösung: Kanten aus depends_on, Stufen, kritischer Pfad, Zeile im Epic-Ticket, Durchstiche, in epics/critical-path.md. Nutze das bei "in welcher Reihenfolge bauen wir die Epics", "kritischer Pfad", "welche Epics warten auf welche", "Reihenfolge neu rechnen". Setzt NICHT die Reihenfolge des Lösens (solution-solve-order), schneidet nicht (epic-structure), nichts ins Sheet, entwirft KEINE Lösung (solution-design).'
---

Verträge: schreibt `datalayer-contract.md`; liest `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`.

# Die Reihenfolge des Bauens ableiten

**Nach den Lösungen, nicht nach dem Schnitt** (§318): die Reihenfolge des Lösens setzt
`solution-solve-order` in `solve_order`; dieser Lauf ordnet nur, in welcher Folge gebaut wird, und
läuft nach `solution-design`, vor `solution-review` und neu, wenn eine Lösung hinzukommt. Seine
Kanten kommen aus `depends_on` der gelösten Anforderungen; vor den Lösungen hat er keine. Am Ende
steht **`epics/critical-path.md` mit der Reihenfolge des Bauens**, je Lauf überschrieben: Stufen, kritischer Pfad, je Epic die Zeile im Epic-Ticket,
Durchstiche, Lieferungen des Kunden, Abhängigkeiten und Zyklen, nach [ref-order.md](ref-order.md).
Aus ihr lesen `ticket-factory` und `solution-review` (§267). **Die Reihenfolge gilt als Empfehlung
für die Umsetzung; ob die Umsetzung ihr folgt, entscheiden die Fachleute** (§267).

**Du liest Epics und Zuordnung aus dem Repo und schreibst nur diese eine Datei.** Ein Epic, das fehlt,
eine Anforderung ohne Epic oder eine falsche Zuordnung führt `epic-structure`; du nennst sie im
Bericht und rechnest mit dem, was steht. Den Verlauf der Reihenfolge hält Git.

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
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen.

### Step 2 — Den Stand lesen

Arbeitsdateien legst du in einen eigenen Temp-Ordner außerhalb des Repos (`mktemp -d`); ins Repo
kommt nur `epics/critical-path.md` (§233). Du liest jede Datei in `epics/` ohne ihren Rumpf, je
Anforderung in `requirements/` den Kopf und `## Description`, die offenen Fragen in `gaps/`,
`architecture.md` und die bisherige `epics/critical-path.md`, wenn es sie gibt. **Gibt es keine Datei
`epics/EP-NNN.md`, gibt es nichts zu ordnen**: du nennst `epic-structure` und schreibst nichts.
**Trägt keine Anforderung `solution_status: decided`, gibt es keine Kante**: du nennst
`solution-design` und schreibst nichts (§318).

Dann prüfst du die Zuordnung:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-repo.py . --check epic
```

`epic` hindert die Rechnung nicht; der Bericht nennt jede Zeile mit `epic-structure`.

### Step 3 — Die Reihenfolge ableiten

**Nach [ref-order.md](ref-order.md)**, über alle Epics des Vorhabens: je gelöster Anforderung Rolle,
Abhängigkeiten aus `depends_on`, Blocker; daraus die Kanten in `deps.tsv` und die Stufen aus `order-stages.py`,
innerhalb einer Stufe die Gründe, Risiko zuerst; dazu kritischer Pfad, Durchstiche und Lieferungen
des Kunden, wo sie belegt sind. Zyklen meldest du, du löst sie nicht auf. Ist eine Fundament-Frage offen,
rechnest du je Variante.

### Step 4 — Die Datei zeigen und das Ja abwarten

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Zeig `epics/critical-path.md`, wie sie geschrieben wird, und gegen die bisherige, was sich an Stufen
und kritischem Pfad geändert hat. Aufbau, Frage und Ja nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`; ändert der
Lead etwas, rechnest du neu und zeigst neu. **Zugangsdaten, Gesundheitsdaten und Daten der Endkunden
schreibst du nicht** (§236; was darunter fällt, sagt der Datalayer-Vertrag).

### Step 5 — Schreiben, berichten und den nächsten Lauf nennen

Schreib `epics/critical-path.md` ganz neu und lies sie zurück. Dann endest du nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit den Teilen 1, 5 und 6: die Reihenfolge steht
in keiner Spalte des Sheets, die Teile 2 bis 4 entfallen. Die Commit-Nachricht ist
`solution-critical-path: <was>`.

Sag knapp, nach der Regel für Berichte (§397): die Stufen in einem Satz je Stufe, den kritischen Pfad, die vorgeschlagenen Durchstiche,
die Zyklen, was sich gegen die bisherige Fassung verschoben hat, und was die Zuordnung meldete.

Dann den nächsten Lauf, **in einer neuen Sitzung**: **`solution-review`**, wenn die Lösungen als
Ganzes geprüft werden sollen; `solution-design` für das nächste Epic nach `solve_order`;
`epic-structure` für Anforderungen ohne Epic oder ein fehlendes Epic. Mit jeder neuen Lösung
läuft dieser Lauf erneut (§318). **Du stößt keinen an**;
der Lead ruft ihn auf.

## Was dieser Lauf nicht tut

Er schreibt nichts ins Sheet, in keine Anforderung, in keinen Kopf eines Epics und nicht in
`architecture.md`. Er schneidet nicht, hängt nicht um und teilt nicht; er beantwortet keine
Architekturfrage und entwirft keine Lösung. Er legt nichts auf dem Board an und setzt dort keine
Abhängigkeit.
