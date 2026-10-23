---
name: epic-structure
description: 'Anforderungen in Epics schneiden, in jedem Projekt: fehlende Fundament-Fragen stellen, Epics anlegen, jede Anforderung genau einem Epic zuordnen, auf Wunsch umhängen, eine Teilung anstoßen. Nutze das bei "in Epics schneiden", "in Pakete gliedern", "ordne die neuen Anforderungen zu", "häng REQ-012 um", "teil REQ-020 auf zwei Epics". Setzt NICHT die Reihenfolge des Lösens (solution-solve-order) oder des Bauens (solution-critical-path), entwirft KEINE Lösung (solution-design).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`; liest `requirements-list-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-open-questions.md`.

# Die Anforderungen in Epics schneiden

Am Ende steht **in jeder Anforderung das Feld `epic` mit genau einem Epic**, auch bei `rejected` und
`duplicate`, und **je Epic eine Datei `epics/EP-NNN.md`** mit Kopf: Titel, Domäne, Kriterium des
Schnitts, Informationsstand und Klärungsbedarf (§280). **Die Fundament-Fragen sind gestellt**: was
vorgegeben ist, steht als Zeile in `architecture.md`, was offen ist, als Frage in `gaps/` an der
Anforderung, die sie treibt (§216). **Der Lauf gehört zur Discovery und läuft in jedem Projekt, mit
und ohne das Add-on `solutioning`** (§403); im Expert Service gibt es keine Epic-Dateien, dort wählt
`ticket-factory` das Epic am Board. Er nimmt auf und ordnet zu, er entscheidet nichts: die
Reihenfolge des Lösens setzt mit `solutioning` danach `solution-solve-order`, die des Bauens nach den
Lösungen `solution-critical-path`.

**Eine offene Architekturfrage hält den Schnitt nicht auf** (§216): du schneidest trotzdem, und die Epics,
deren Lösung an der Frage hängt, tragen sie in `clarification`. Ein Epic, das nur Fragen trägt, legst
du nicht an. **Ein Umfang begrenzt, was du schneidest, nicht was du liest** (§215): ein Nachschnitt für
einige Anforderungen liest alle Epics.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest seine Dateien direkt und
schreibst nur, was `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` diesem Lauf gibt: das Feld
`epic` der Anforderungen, die Epic-Dateien bis auf ihren Rumpf und `draft`, `epic_page` und
`board_key`, `architecture.md`, neue Fragen in `gaps/` und neue Aufgaben in `todo/`. **Eine
Anforderung legst du nie an und änderst an ihr nur `epic`**: Teilung, Korrektur und Ausklammerung
führt `requirements-update` (§280, Regel 3). Das Ende des Laufs, Prüfung, Projektion und Commit, steht
in `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`. **Scheitert ein Aufruf zweimal gleich, hältst
du an** und nennst Aufruf und Meldung. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und
Begründung und suchst keinen zweiten Weg.

### Step 1 — Das Vorhaben binden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,shops,project_type
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder. Dann liest
du `project.yml` ganz.

**Aus `add_ons` folgt das Design-Epic** (§303). **Ist `project_type` leer, fragst du den Lead
einmal**, welche Add-ons das unterschriebene Angebot nennt; die Antwort gilt für diesen Lauf, du trägst
sie nicht ein, und der Bericht nennt `project-setup`. Sagt er „noch offen", schneidest du ohne
Design-Epic, und der Bericht nennt es. **Ist `shops` leer, schneidest
du trotzdem**: die Fundament-Frage zu den Shops bleibt offen ([ref-frame.md](ref-frame.md)), du trägst
`shops` nicht ein, und der Bericht nennt `project-setup` für einen Lauf zum Ergänzen.

### Step 2 — Den Stand lesen

Arbeitsdateien legst du in einen eigenen Temp-Ordner außerhalb des Repos (`mktemp -d`); ins Repo
kommt nur der Datalayer (§233). Du liest je Anforderung in `requirements/` den Kopf, `## Description`
und `## Approach`, jede Datei in `epics/` ohne ihren Rumpf, die offenen Fragen in `gaps/`, die offenen
Aufgaben in `todo/` nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 1 (eine Zuordnung, die dieser Lauf
vornimmt, schließt ihre Aufgabe, §359),
`architecture.md` und `customer.md`. Aus der jüngsten Notiz `notes/JJJJ-MM-TT-solution-approach.md`
(spätestes Datum, bei gleichem Datum die höchste Endung) liest du nur `Lösungen über mehrere
Anforderungen` ([ref-cut.md](ref-cut.md)); fehlt sie, schneidest du ohne sie, und der Bericht nennt
`solution-approach`.

| Stand | Was der Lauf tut |
|---|---|
| keine Datei in `epics/` | erster Schnitt über alle Anforderungen |
| Epics stehen, Anforderungen mit leerem `epic` | Nachschnitt: nur diese, in bestehende oder neue Epics |
| der Lead nennt Anforderungen zum Umhängen oder Teilen | nur diese |
| jede Anforderung hat ein Epic, sonst nichts verlangt | kein Schnitt; nur die Fundament-Fragen, und der Bericht nennt den nächsten Lauf (Step 8) |
| der Lead verlangt einen Neuschnitt nach der Regel der Ref | alle Anforderungen, nach [ref-cut.md](ref-cut.md) (Neuschnitt) |

Ohne eine einzige Anforderung gibt es nichts zu schneiden: du nennst `requirements-update`. Fehlt
`architecture.md`, schneidest du ohne Architektur und nennst `requirements-update`, der sie anlegt (§229);
du legst sie nicht an.

### Step 3 — Die Fundament-Fragen stellen

**Nach [ref-frame.md](ref-frame.md), zu Beginn und in einem Block**: je Zeile des Fundaments, die
`offen` ist und weder eine Quelle noch eine offene Frage trägt, eine Frage, mit dem, was Repo und
Notizen schon dazu sagen. Die Antworten des Leads ordnest du ein: vorgegeben wird Zeile, offen wird
Frage in `gaps/` an der treibenden Anforderung, ohne treibende Anforderung fehlt eine Anforderung.
**Warte mit dem Schnitt nicht auf eine Antwort, die der Lead nicht geben kann**; eine offene Frage
bleibt offen. Was der Lead dabei an einer Anforderung korrigiert, ist Material für
`requirements-update` (§280, Regel 6); du nennst es im Bericht.

### Step 4 — Den Schnitt vorschlagen

**Die Regeln stehen in [ref-cut.md](ref-cut.md); lies sie, bevor du den ersten Vorschlag machst.**
Die Grenzen, die nur der Text hält:

- **Genau ein Epic je Anforderung**, auch bei `rejected` und `duplicate`. Berührt sie ein weiteres
  Epic, wird das eine Aufgabe in `todo/`. **Geteilt wird nur**, wenn sie in zwei Epics echte Arbeit
  braucht, und erst nach dem Ja des Leads; die neue Anforderung legt `requirements-update` an.
- **Umgehängt wird nur auf Wunsch**, und eine Anforderung, deren Epic `board_key` trägt, nur mit dem
  Hinweis, dass auf dem Board schon Tickets stehen: ab dem Ticket gilt das Board.
- **Ausklammern ist nicht dein Schritt.** Verlangt der Lead es, nennst du `requirements-update`; die
  Anforderung behält ihr Epic.
- **Zwei Ebenen, feste Körnung** (§252): jedes Epic trägt eine `domain` aus der Liste der Ref und
  genau eine Fähigkeit; die Storefront als ein Theme-Epic mit einer Anforderung je Seitentyp (§285),
  eine Anbindung je Datenstrom, mit dem Add-on `design` das Design-Epic. Ein Epic mit einer
  Anforderung ist erlaubt, eines mit mehr als 12 schlägst du zur Teilung vor.

### Step 5 — Den Plan zeigen und das Ja abwarten

Zeig in einem Block, **was wo entsteht oder sich ändert, im Klarnamen**:

1. **Je neues Epic die ganze Datei**, wie sie geschrieben wird, und darunter seine Anforderungen mit
   Kennung und Titel.
2. **Je Anforderung, deren `epic` sich ändert**, Kennung, Titel, heute und neu.
3. **Je bestehendes Epic, dessen Kopf sich ändert**, die Felder, heute und neu.
4. **Die neuen Fragen als Liste mit Adressat** nach `${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`,
   die neuen Dateien in `gaps/` und `todo/` je mit ganzem Text, und der Block **Aufgaben** nach `ref-tasks.md`, 5.
5. **Die Änderung an `architecture.md`**, Zeile für Zeile, gelesen gegen neu.

Darunter **„Interna: keine“**, oder die Stelle, an der etwas aus einer internen Quelle steht (§278):
Titel und Kriterium eines Epics landen im Sheet und auf dem Board. Aufbau, Frage und Ja nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`.

### Step 6 — Schreiben

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht** (§236). In dieser Folge,
jede Datei direkt davor gelesen und danach zurückgelesen:

1. die neuen Epic-Dateien, nach [ref-cut.md](ref-cut.md), „Die Datei des Epics“;
2. das Feld `epic` der Anforderungen, nur diese Zeile im Kopf;
3. die geänderten Köpfe bestehender Epics;
4. die neuen Fragen und Aufgaben;
5. `architecture.md`, die ganze Datei aus der gelesenen Fassung, geprüft nach
   [ref-frame.md](ref-frame.md), „Fortschreiben“.

### Step 7 — Prüfen

```
python3 ${CLAUDE_SKILL_DIR}/scripts/check-cut.py .
```

`domain`, `epic_size`, `add_on` und `design_qa` legst du dem Lead vor; ein Epic über 12 Anforderungen
bleibt nur mit seinem Ja und „Größe bestätigt“ (`en`: „Size confirmed“) am Ende von `summary`. Dann endest du nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`; meldet `check-repo.py` dort `epic` an einer
Anforderung dieses Laufs, ist das ein Fehler dieses Laufs, außer der Lead hat sie bewusst offen
gelassen. Die Commit-Nachricht ist `epic-structure: <was>`.

### Step 8 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397): die neuen Epics mit Kennung, Titel und Zahl ihrer Anforderungen; Umhängungen und
angestoßene Teilungen; die Fundament-Fragen mit ihrem Ergebnis, auch die ohne treibende Anforderung; die
Berührungen; was der Lead an Anforderungen korrigiert hat.

Dann den nächsten Lauf, **in einer neuen Sitzung**: mit `solutioning` in `add_ons` **`solution-solve-order`**
für die Reihenfolge des Lösens (§318, §403), ohne es **`ticket-factory`** nach der Scope-Freigabe.
`requirements-update`
für eine Teilung, eine fehlende treibende Anforderung, eine Korrektur oder eine Ausklammerung. **Du
stößt keinen an**; der Lead ruft ihn auf.

## Wann nachfragen (NICHT raten)

- Eine Anforderung passt in zwei Epics, und unklar ist, ob sie in beiden echte Arbeit braucht: frag,
  bevor du eine Teilung anstößt.
- Zwei Themen tragen vielleicht dieselbe Fähigkeit: schlag ein Epic vor und frag.
- Titel, Beschreibung und Ist-Stand reichen nicht für eine Zuordnung: das Feld bleibt leer, und du
  fragst.

## Was dieser Lauf nicht tut

Er nimmt kein Material auf, legt keine Anforderung an und ändert an ihr nur `epic`. Er setzt keine
Reihenfolge des Lösens (`solution-solve-order`) und leitet keine des Bauens ab (`solution-critical-path`), schreibt keine ADR, keinen Rumpf eines Epics, entwirft keine Lösung
und beantwortet keine Architekturfrage; die entscheidet das Projekt mit dem Kunden. Felder der Menschen
(`Cluster`, Owner, `Aufwand (h)`) schreibt er nicht (§280, Regel 5). Er legt nichts auf dem Board an
und schreibt nichts nach Confluence.
