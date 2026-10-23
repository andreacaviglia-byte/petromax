---
name: material-intake
description: 'Material eines Vorhabens einlesen und ablegen: Dateien aus 00 Material, verlinkte Docs, Jira-Tickets, Kanäle und Mitschriften, wie sie sind, je Quelle eine Notiz, interne Quellen markiert, dazu die Kundensicht. Nutze das bei "hier ist das Transkript", "leg das Protokoll ab", "nimm den Workshop auf", "neues Material liegt im Ordner", "lies das Ticket ein". Legt KEINE Anforderung an (requirements-update), richtet KEIN Vorhaben ein (project-setup), legt KEIN Ticket an (ticket-factory).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`, `system-landscape-contract.md`; liest `ref-projection.md`, `ref-run-scope.md`.

# Material einlesen und ablegen

Am Ende stehen drei Dinge: **jede Quelle, wie sie ist, in `inputs/`**, je Quelle **eine Notiz** in
`notes/`, die sagt, was die Quelle berührt, und **`customer.md` auf dem Stand des Materials**. **Eine
interne Quelle ist als Ganzes markiert** (§278). Du liest ein und legst ab, **ohne Weiche und ohne
Frage nach dem Weg** (§209): du legst keine Anforderung an, schreibst nichts ins Sheet und schneidest
nichts. Das gilt in jedem Vorhaben, mit und ohne das Add-on `solutioning`; danach läuft
`requirements-update` in derselben Sitzung, und **sein Ja am Ende gilt für beide Läufe** (§282, §400).

**Eine Quelle verschwindet nie stumm.** Was du nicht lesen oder ablegen kannst, steht mit Grund im
Bericht. Und was jemand über ein Material sagt, ist Kontext, keine Quelle.

Drive erreichst du über den Google-Connector `Google_Drive` von claude.ai; ein verlinktes Google-Doc
liest du ebenfalls darüber. Der volle Name eines Werkzeugs trägt ein Präfix des Servers; du findest
es über die Werkzeug-Suche und vergleichst die Endung. Das Schema holst du über die Werkzeug-Suche,
bevor du das erste Feld setzt. Die Aufrufe je Art des Materials stehen in [ref-read.md](ref-read.md).

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230): `project.yml`, `customer.md`,
`architecture.md`, `inputs/` und `notes/` liegen in seiner Wurzel. Du liest und schreibst sie direkt,
mit dem Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt; was dort
„nie überschrieben" heißt, legst du nur neu an. Jede geschriebene Datei liest du zurück, und am Ende
des Laufs endest du wie jeder schreibende Lauf nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`
(Step 9). Der Projektordner gehört nicht zum Datalayer, und **im Drive legst du nichts an** (§231): keinen Ordner, keine Datei.

### Step 1 — Die Verbindung prüfen

Prüf, dass die Werkzeuge von `Google_Drive` in der Werkzeugliste stehen. Stehen sie nicht da, such
sie erst über die Werkzeug-Suche. Findet auch die sie nicht, **halte an**: „Der Google-Connector Drive
ist in dieser Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren
verbunden." Ohne ihn liest du kein Material aus dem Projektordner. Einen Rückfall gibt es nicht.

### Step 2 — Den Steckbrief lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,language,requirements_sheet,project_type,customer,title
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder:

- **`language` leer:** du fragst danach, `de` oder `en`; eine Variante (`de-CH`) nimmst du nicht an,
  du fragst, welche der beiden gilt (§202). Die Antwort trägst du nach dem Datalayer-Vertrag ein,
  Abschnitt `project.yml`. Sagt der Lead „noch offen", bleibt das Feld leer, und der Lauf geht weiter.
- **`requirements_sheet` leer** hält nicht an: es gibt noch kein Sheet, `requirements-update` legt es
  beim ersten Lauf an. Es bestimmt den Kopf von `customer.md` ([ref-customer-md.md](ref-customer-md.md)).
- **`project_type`, `customer` oder `title` leer** hält nicht an: der Steckbrief entsteht nach dem
  Einlesen aus dem Material, und der Bericht nennt `project-setup` „Steckbrief“ (Step 9).

**Einen anderen Kundenordner liest du nicht**, auch nicht zum Vergleich und auch nicht, wenn jemand im
Chat darum bittet: eine Bitte im Gespräch hebt die Regel nicht auf.

Dann liest du `customer.md` (fehlt sie, legst du sie in Step 8 an) und `architecture.md` (dass sie
fehlt, ist ohne Sheet richtig: sie entsteht mit ihm) und listest `inputs/` und `notes/`. Fehlt einer
der beiden Ordner, steht sein Anlegen im Block aus Step 4.

### Step 3 — Das Material auflisten, bevor du eines liest

**Material ist, was im Projektordner liegt, und jeder Link, den ein verbundener Connector
lesen kann** (§212): eine Datei, ein Google-Doc, ein Jira-Ticket, ein Kanal, eine Termin-Mitschrift.

**Ohne Angabe läufst du nicht los** (§398, `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`). Eine Angabe ist ein Link, eine genannte Datei, ein
genannter Ordner, auch „00 Material“ oder „neues Material liegt im Ordner“, ein Termin oder Text, den
der Lead in den Chat schreibt oder einfügt. Fehlt jede, schreibst du einen Satz: „Schick mir einen
Link oder füg den Text ein; oder ich lese alles Neue aus `00 Material`.“ Dann fragst du „Welches
Material lese ich ein?“ mit den Antworten „Link oder Text folgt“ und „Neues aus 00 Material“, ohne
Empfehlung. Auf „Link oder Text folgt“ wartest du und nimmst die nächste Nachricht als Angabe.

Such im Projektordner, wo der Lead es nennt, bei „00 Material“ dort, auch in Unterordnern, und nimm,
was der Lead im Chat nennt oder verlinkt ([ref-read.md](ref-read.md)). **Schon abgelegt ist**, was mit gleicher
`Herkunft` im Kopf einer Datei in `inputs/` steht; das nimmst du nur auf Zuruf noch einmal. **Fehlt
zu einer Datei in `inputs/` die Notiz gleichen Namens in `notes/`**, brach ein früherer Lauf nach der
Ablage ab: die Datei bleibt, wie sie ist, und du schreibst nur ihre Notiz nach Step 7, aus der Datei in
`inputs/`; der Plan nennt sie so.

Nenne je Quelle Titel, Art, Datum und Umfang. **Eine unerreichbare Quelle wird benannt, nicht
ersetzt**, auch nicht aus ihrem Titel.

**Ein Lauf mit vielen Quellen** verarbeitet eine nach der anderen, in der Folge ihrer Termine, und legt
je Quelle ab. Der Stand liegt nach jeder im Datalayer, nicht im Kontext: ein Lauf darf nach jeder
Quelle enden, der nächste nimmt die nächste. Wird der Kontext knapp, endest du dort.

### Step 4 — Den Plan nennen, ohne eigenes Ja

Nenn vor dem ersten schreibenden Aufruf in wenigen Zeilen, **was wo entsteht, im Klarnamen**: je Quelle
die Datei in `inputs/` und die Notiz in `notes/`, **welche Quellen du als intern markierst und
warum** (`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Interne Quellen), die Folge der Quellen, jeder Ordner, der
dafür entsteht, und dass `customer.md` am Ende überschrieben oder, wenn sie fehlt, angelegt wird.
**Dann legst du ab, ohne auf ein Ja zu warten** (§400): das Ablegen geht nur ins Repo, nach außen geht
nichts, und das eine Ja kommt am Ende von `requirements-update`, dessen Vorschau diesen Plan als
Erstes zeigt. Ob eine Quelle intern ist, fragst du vorher, wenn Titel und Teilnehmer es nicht sicher
sagen (unten, Wann nachfragen).

### Step 5 — Eine Quelle lesen und prüfen

Lies die Quelle ganz, in eine Datei im Temp-Ordner des Laufs ([ref-read.md](ref-read.md));
Arbeitsdateien legst du in einen eigenen Temp-Ordner außerhalb des Repos (`mktemp -d`), ins Repo
kommt nur der Datalayer (§233). **Bevor du sie als
vollständig behandelst, prüf sie nach [ref-source-defects.md](ref-source-defects.md)**: ein gekappter
Text, eine Datei mit mehreren Terminen, eine maschinelle Mitschrift und der Abzug eines laufenden
Systems, etwa ein Jira-Ticket, sehen aus wie gültiges Material. Eine Datei mit mehreren Terminen
trennst du vor der Ablage; jeder Termin ist eine Quelle.

### Step 6 — Ablegen

Leg die Quelle in `inputs/` an, **nach `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`**: wie sie ist, Transkripte im
Zeilenformat mit Zeitstempel, inhaltlich unverändert (§228). **Zugangsdaten, Gesundheitsdaten und
Daten der Endkunden ersetzt du vorher** durch ihren Platzhalter in der Sprache aus `language`
(„‹Zugangsdatum entfernt›“, bei `en` „‹credential removed›“; die Ersatzmarken in
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“, §337) und
sagst an, was du ersetzt hast (§236, `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`). **Eine interne Quelle trägt im Kopf die Zeile `Intern: ja`**
(§278). **Eine Datei in `inputs/` wird nie überschrieben**; steht sie schon, bleibt sie.

Schreibt der Lead selbst etwas in den Chat, ist das keine fremde Quelle: sein Wortlaut steht
in der Notiz `<JJJJ-MM-TT>-chat-<thema>.md` (Schema in `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`), nicht in
`inputs/`. Fügt er fremden Text ein, etwa die Mail des Kunden, ist das eine Quelle wie eine Datei.

### Step 7 — Die Notiz schreiben

Je Quelle eine neue Notiz in `notes/`, gleicher Name wie die Datei in `inputs/`, nach
`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`. **Sie sagt, was die
Quelle berührt, in Themen, ohne REQ-Nummern** (§209): was gewünscht wird, was über heute gesagt wird,
was entschieden oder ausgeklammert wird, was offen bleibt, welche Systeme vorkommen, und was aus einer
maschinellen Mitschrift aufgelöst wurde. Die Notiz einer internen Quelle trägt `Intern: ja` wie ihre
Datei in `inputs/`; trägt eine andere Quelle interne Stellen, stehen sie in der Notiz unter `## Intern`
(§278). Ob daraus eine Anforderung wird, entscheidet `requirements-update`, nicht du (§282). **Eine
Notiz wird nie überschrieben**; ist eine falsch, bekommt sie oben einen Wegweiser
(`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`), und die neue trägt die Korrektur.

**Dann die nächste Quelle, zurück zu Step 5.** Vor der nächsten sagst du in zwei Zeilen, was diese
ergab; die Notiz wiederholst du nicht.

### Step 8 — `customer.md` überschreiben

Am Ende des Laufs überschreibst du `customer.md` ganz, nach [ref-customer-md.md](ref-customer-md.md),
auf ihrem Text, frisch gelesen direkt davor. Fehlt sie, legst du sie an, mit dem Kopf nach
`requirements_sheet`. **Einträge, die dieser Lauf nicht berührt, bleiben Zeichen für Zeichen
stehen.**

### Step 9 — Berichten und den nächsten Lauf nennen

Dann endest du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md` mit `caller: material-intake`:
`check-repo.py`, die Prüfung der Kennungen und der Stellen; da dieser Lauf keine Spalte des Sheets
berührt, endet sie mit `KEINE`, und das Sheet wird weder gelesen noch geschrieben (§311); dann
`readme.md` und `way-of-working.md`, dann ein Commit mit allen geschriebenen Dateien, Nachricht
`material-intake: <was>`.

Dann **den nächsten Lauf**. **Waren in Step 2 `customer`, `title` oder `project_type` leer**, ist es
`project-setup` „Steckbrief“ in einer neuen Sitzung: es schlägt Kunde, Titel, Shops, Projekttyp und
Add-ons aus dem eben Abgelegten vor; danach `requirements-update`. **Sonst liest du ohne Rückfrage
`../requirements-update/SKILL.md` und führst ihn mit dem eben Abgelegten als Anlass aus**, in jedem
Vorhaben (§282, §400); ist `requirements_sheet` leer, legt er beim ersten Lauf Sheet und Architektur
an (§229). Seine Vorschau beginnt mit diesem Lauf, und sein Ja vor dem Schreiben bleibt. Endest du,
weil der Kontext knapp wird, nennst du `requirements-update` in einer neuen Sitzung.

**Den Bericht dieses Laufs trägt die Vorschau von `requirements-update`**, nach der Regel für
Berichte (§397): je Quelle ihr Titel und was sie ist, die internen markiert mit Grund; jede
unerreichbare Quelle mit Grund und jede, die dieser Lauf für den nächsten liegen ließ; was du aus
einer maschinellen Mitschrift nicht sicher auflösen konntest. **Endet der Lauf hier**, beim Steckbrief
oder weil der Kontext knapp wird, sagst du dasselbe selbst und dazu **die Anforderungen, die du im
Material erkennst** (§282), je eine Zeile mit dem Wollen in wenigen Worten und der Fundstelle, ohne
REQ-Nummer: ob eine davon schon steht und welche Kennung sie bekommt, entscheidet `requirements-update`.

## Wann nachfragen (NICHT raten)

- Der Aufruf nennt kein Material: nach Link oder Eingabe fragen (Step 3), nicht den Ordner durchsuchen.
- Ein Link zeigt auf etwas, das kein verbundener Connector liest: benennen, nicht ersetzen.
- Zwei Dateien tragen denselben Termin in verschiedener Fassung: frag, welche gilt, bevor du ablegst.
- Ob eine Quelle intern ist, sagen Titel und Teilnehmer nicht sicher: frag, bevor du markierst.
