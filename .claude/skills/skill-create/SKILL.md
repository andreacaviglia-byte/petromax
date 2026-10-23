---
name: skill-create
description: 'Einen eigenen Skill fürs Projekt anlegen oder einen Standard-Skill abwandeln: erst mit grill-me in Runden klären (wozu, was nicht, Abgrenzung, Beispiele), dann mit dem Skill-Creator von Anthropic schreiben, nach den Regeln des Templates prüfen, als Abweichung eintragen. Nutze das bei "eigener Skill", "Skill bauen", "Skill abwandeln", "das soll bei uns anders laufen als der Standard". Ändert KEINEN Standard-Skill und ändert die Arbeitsweise NICHT ohne den project_owner (project-setup).'
---

Verträge: schreibt `datalayer-contract.md`; liest `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`.

# Einen eigenen Skill anlegen

Am Ende liegt ein eigener Skill unter `.claude/skills/<name>/`, mit eigenem Namen, den drei
Kopfzeilen und höchstens 300 Zeilen, und **eine Abweichung in `way-of-working/` nennt ihn** (§225,
§286, §290). Abwandeln läuft genauso: der abgeleitete Skill ist eine Kopie unter eigenem Namen und
nennt den Standard in `abgeleitet von:`. **Ein Standard-Skill wird nie geändert**; seinen neuen Stand
bringt `project-upgrade`, und eine Änderung daran überschriebe das nächste Upgrade.

Die Reihenfolge ist fest: **erst klären, dann schreiben, dann prüfen.** Ohne die Befragung fehlen die
Abgrenzung zu den Standard-Skills und die Kopfzeilen, und das fällt erst auf, wenn der Skill steht.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230); Formate in
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`. **Scheitert ein Aufruf zweimal gleich,
hältst du an** und nennst Aufruf und Meldung. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und
Begründung und suchst keinen zweiten Weg.

### Step 1 — Stand ziehen und den Skill-Creator finden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`.
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Exit 1 heißt anhalten, mit der Meldung. Dann prüfst du, ob **der Skill-Creator von Anthropic** in der
Liste der Skills dieser Sitzung steht. Fehlt er, **halte an** und sag: „Der Skill-Creator von Anthropic
lädt in dieser Sitzung nicht; ohne ihn legt dieser Lauf keinen Skill an. `project-status` prüft die
Umgebung und nennt den Weg."

### Step 2 — Neu oder abgewandelt

Frag: ein neuer Skill, oder ein Standard-Skill, der in diesem Projekt anders laufen soll? Die
Standard-Skills nennt `CLAUDE.md`, Abschnitt „Die Skills“. **Beim Abwandeln** liest du die
`SKILL.md` des Standards und seine Refs ganz; sie sind die Vorlage, und was gleich bleibt, bleibt
wörtlich.

**Würde nur eine Regel der Arbeitsweise anders**, ohne dass ein Prüf-Script oder ein Skill-Text sie
anders verlangt, braucht es keinen Skill: das ist eine Abweichung über `project-setup` (§299); du sagst das
und endest.

### Step 3 — Klären, mit `grill-me` in Runden

Du liest `../grill-me/SKILL.md` und rufst ihn in **vier Runden**, je mit einer Liste von Befunden,
die du vorher selbst schreibst: je Punkt die Frage, deine Empfehlung mit Grund und was die Antwort
ändert. Was der Lead schon gesagt hat, kommt nicht auf die Liste.

1. **Wozu:** wer ruft den Skill, bei welchen Worten, was liegt am Ende vor, und wer ist
   `verantwortlich:` (der Solution Owner, wenn er nur einen Workstream betrifft).
2. **Was nicht:** was er ausdrücklich nicht tut, nicht liest und nicht schreibt.
3. **Abgrenzung:** je Standard-Skill, dessen `description` nahe liegt, wo die Grenze verläuft; und
   `gilt für:` (das ganze Vorhaben, ein Workstream, ein Epic).
4. **Beispiele:** zwei oder drei Aufrufe mit dem, was danach im Repo oder im Chat steht.

`grill-me` gibt je Runde eine Tabelle zurück. Ein Punkt `an den Kunden` gehört nicht in einen Skill;
du nennst ihn als offene Frage, die über `requirements-update` ins Repo kommt. Bleibt ein Punkt `offen`,
schreibt der Skill-Creator ihn nicht; du nennst ihn im Bericht.

### Step 4 — Schreiben, mit dem Skill-Creator

Du rufst den Skill-Creator von Anthropic mit den vier Tabellen als Auftrag und den Regeln aus
[ref-rules.md](ref-rules.md) als Vorgabe. Das Ziel ist `.claude/skills/<name>/`; Evals und
Arbeitsdateien des Skill-Creators legst du in einen Temp-Ordner außerhalb des Repos (`mktemp -d`),
nicht ins Repo (§233).

### Step 5 — Nach den Regeln des Templates prüfen

Jede Regel aus [ref-rules.md](ref-rules.md) gegen den Entwurf; was sie verletzt, berichtigst du und
zeigst die Berichtigung. Dann:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Eine Zeile `skill_header` zu deinem Skill heißt: eine Kopfzeile fehlt; du ergänzt sie. Gibt es zu
einer Regel keinen Fund im Entwurf, sagst du das je Regel in einem Satz.

### Step 6 — Die Abweichung in `way-of-working/`

Die Datei mit `skill:` = der Name des Skills, `section:` = der Abschnitt des Standards, dessen Ablauf
der Skill ändert oder ergänzt, und im Rumpf, wann er statt oder neben welchem Standard-Skill läuft. Ob
du sie schreibst oder als Vorschlag in `todo/` anlegst, sagt:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --owner .
```

Exit 0: die Abweichung in der Form des Datalayer-Vertrags
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt `way-of-working/JJJJ-MM-TT-<slug>.md`,
mit seinem Pfad (§299); lehnt der Hook `wow-guard` das Schreiben trotzdem ab, nennst du seine Meldung
wörtlich und hältst an. Exit 2: der Skill entsteht trotzdem, und die Abweichung wird ein Vorschlag an
den `project_owner`, in der Form des Datalayer-Vertrags, Abschnitt `todo/JJJJ-MM-TT-<slug>.md`, „Ein
Vorschlag zur Arbeitsweise“, mit seinem Pfad; er nimmt ihn mit `project-setup` an, und bis dahin
sagt der Bericht, dass der Skill nicht in der Arbeitsweise steht.

### Step 7 — Zeigen, schreiben, committen

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Du zeigst die ganze `SKILL.md`, jede Ref und die Datei aus Step 6, mit Frage und Ja nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. Dann schreibst du, liest zurück und endest nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Teile 1, 5 und 6; ins Sheet projiziert dieser
Lauf nichts. Ein Commit `skill-create: <name>` mit dem Skill, der Datei aus Step 6 und
`way-of-working.md`, dann pushen.

### Step 8 — Berichten

Knapp, nach der Regel für Berichte (§397): der Name, der Aufruf `/<name>`, für wen er gilt und wer
ihn verantwortet, die Abweichung oder der Vorschlag in Worten, offene Punkte aus Step 3. Ob der neue Skill in dieser Sitzung schon lädt, ist
ungemessen; sicher ist eine neue Sitzung. Du stößt keinen Lauf an.

## Was dieser Lauf nicht tut

Er ändert keinen Standard-Skill, kein Script und keinen Vertrag unter `.claude/`, schreibt
`way-of-working.md` nie von Hand und nichts in den Drive, nach Confluence oder auf das Board. Der
Rücklauf eines eigenen Skills in den Standard ist nicht sein Teil; er läuft über das Team, das das
Template pflegt.
