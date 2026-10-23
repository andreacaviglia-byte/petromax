---
name: project-status
description: 'Einstieg ins Projekt: Umgebung prüfen, Stand der Kette zeigen, Fragen zu Skills beantworten, Neue einführen, Neues nach dem Upgrade erklären, die Arbeitsweise zeigen, Änderungen vorschlagen, Aufgaben abhaken. Nutze das bei "ich bin neu", "wo stehen wir", "welcher Skill für", "wie arbeiten wir", "ich schlage vor", "Aufgabe … ist erledigt". Schreibt NICHTS außer Vorschlag oder Haken in todo/, ändert KEINE Einstellung (project-setup), ändert KEINE Anforderung (requirements-update).'
---

Verträge: schreibt `datalayer-contract.md`; liest `connector-contract.md`, `kb-contract.md`, `ref-projection.md`, `ref-tasks.md`.

# Stand, Guide und Arbeitsweise des Vorhabens

**Ein Skill für Stand, Einführung und Arbeitsweise** (§289), für alle im Projekt: **Stand** (Umgebung,
Stand der Kette, Hilfe), **Guide** (Einführung, Neues nach dem Upgrade, Arbeitsweise zeigen) und
**Vorschlag zur Arbeitsweise**, dazu das Abhaken einer Aufgabe. Ändern tut der `project_owner` mit `project-setup` (§299). Du antwortest
als Text. Du läufst auf Zuruf, am Ende von `project-setup` und
nach jedem `project-upgrade`.

**Du schreibst zwei Arten Änderung, beide in `todo/`:** einen Vorschlag zur Arbeitsweise an den
`project_owner` (§289) und den Haken an einer erledigten Aufgabe (§359), dazu die Zeile in `.claude/metrics/runs.md` (Wurzel-`CLAUDE.md`, §246). Alles andere liest du nur. Jede Antwort zu Skills, Stand oder Regeln nennt die Stelle, aus der sie
kommt: Datei und Abschnitt, Kennung oder Skill.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230); Pfade und Formate stehen in
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`. **Scheitert ein Aufruf zweimal gleich,
hältst du an** und nennst Aufruf und Meldung. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und
Begründung und suchst keinen zweiten Weg.

### Step 1 — Den Stand ziehen und den Teil wählen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`.
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; endet es mit
`Abgelöst` oder `Git`, nennst du die Meldung wörtlich. Beides
ist zugleich ein Befund der Umgebung (Step 2); du hältst nur an, wenn der Lead die Arbeitsweise
ändern will. Endet es mit `Template`, nennst du die Meldung wörtlich und hältst an (§338).

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Fehlt `project.yml` oder `project_folder`, ist das Repo nicht eingerichtet, und du nennst
`project-setup`; die Umgebung prüfst du trotzdem, mit Drive, Sheets und Docs. Dann wählst du den Teil nach dem, was gefragt ist:

| Anlass | Teil |
|---|---|
| ohne nähere Frage, „wo stehen wir“, „was ist offen“ | Stand: Umgebung, Stand der Kette |
| „geht mein Connector“, Probleme mit der Umgebung | Umgebung allein |
| „welcher Skill für …“, „warum hängt EP-003“ | Hilfe |
| „ich bin neu“, am Ende von `project-setup` | Einführung, mit der Umgebung zuerst |
| „was ist neu“, nach `project-upgrade` | Umgebung, dann Neues nach dem Upgrade |
| „wie arbeiten wir“, eine Frage zu einer Regel | Arbeitsweise zeigen |
| „wir machen das anders“, ein Vorschlag zur Arbeitsweise | Vorschlag zur Arbeitsweise |
| „Aufgabe … ist erledigt“, „hak … ab“ | Aufgabe abhaken |

### Step 2 — Die Umgebung prüfen

Je nötigem Connector ein harmloser lesender Aufruf, dazu Branch, Pull und Skill-Creator, nach
[ref-status.md](ref-status.md), Abschnitt „Umgebung“. Das Ergebnis ist eine Tabelle: was da ist,
was antwortet, bei Fehler die Meldung und der Weg zur Abhilfe. Eine Lücke hält dich nicht an; sie ist
die Auskunft.

### Step 3 — Den Stand zeigen

Stand der Kette, offene Fragen mit `blocking: yes`, offene Aufgaben in `todo/`, die jüngsten
Entscheidungen, nach [ref-status.md](ref-status.md), Abschnitt „Stand“. Einen nächsten Lauf
aus dem Stand empfiehlst du nicht (§306). Eine Frage zu Skills oder Stand beantwortest du nach
demselben Abschnitt, „Hilfe“.

### Step 4 — Führen

Einführung, Neues nach dem Upgrade oder die Arbeitsweise zeigen, nach [ref-guide.md](ref-guide.md).
Wo dieses Projekt vom Standard abweicht, steht in `way-of-working/`; du nennst es in jedem der drei.

### Step 5 — Einen Vorschlag zur Arbeitsweise anlegen

**Ändern darf nur der `project_owner`, mit `project-setup`** (§299). Ob die Person dieser Sitzung es
ist, sagt dieselbe Stelle, an der der Hook prüft:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --owner .
```

Exit 0 heißt: du schreibst nichts und nennst `project-setup`, „in einer neuen Sitzung“; dort ändert
der Owner die Arbeitsweise und entscheidet über offene Vorschläge. Exit 2 heißt: die Änderung wird
ein Vorschlag in `todo/` an den `project_owner`, nach [ref-way-of-working.md](ref-way-of-working.md);
die Meldung nennst du wörtlich. Ändert die Person im Auftrag des Owners, nennst du `project-setup`, das
vorher nachfragt (§301). **Was ein Prüf-Script ablehnen würde**, ist keine Abweichung, sondern
ein abgeleiteter Skill (§225): dafür nennst du `skill-create`.

Nach dem Schreiben endet der Lauf wie jeder schreibende, nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit den Teilen 1, 5 und 6: `check-repo.py`,
`readme.md` und `way-of-working.md`, Commit und Push. Ins Sheet projiziert dieser Lauf nichts, weil
`todo/` dort nicht steht; die Teile 2 bis 4 entfallen. Die Nachricht beginnt mit `project-status:`.

### Step 6 — Eine Aufgabe abhaken

**Jede Person im Projekt darf jede Aufgabe abhaken** (§359), nicht nur die, an die sie geht. Du suchst
die Datei in `todo/` mit `status: open` nach dem, was die Person nennt (Dateiname, Titel, Kennung in
`concerns`); passen mehrere, fragst du, welche. **Ein Vorschlag zur Arbeitsweise** (`todo/…-wow-…`)
ist ausgenommen: ihn schließt der `project_owner` mit `project-setup` (§299), das nennst du.

Nennt die Person nicht, was herauskam, fragst du danach; ohne Ergebnis hakst du nicht ab. Dann zeigst
du die Änderung nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 2: `status: done`, `done_by` aus
`wow-guard.py --whoami` (ohne Namen fragst du nach ihm), `done_at` von heute und die Zeile `Erledigt …`
am Ende des Rumpfs. **Geschrieben wird erst nach dem Ja**, dann zurückgelesen, und der Lauf endet wie in
Step 5.

### Step 7 — Berichten

Zum Schluss knapp, nach der Regel für Berichte (§397): was du geprüft und gezeigt hast, was offen
blieb, was du geschrieben hast, in Worten. Einen nächsten Lauf aus dem Stand empfiehlst du nicht (§306), und du stößt
keinen an.

## Was dieser Lauf nicht tut

Er ändert keine Anforderung, kein Epic, keine offene Frage und keine Entscheidung, schreibt nichts ins
Sheet, in den Drive, nach Confluence oder auf das Board, schreibt nichts in `way-of-working/` und
`way-of-working.md` und entscheidet keinen Vorschlag; das tut der `project_owner` mit `project-setup`.
Er richtet keinen GitHub-Account und keine Cloud-Umgebung ein; ohne sie läuft er nicht.
