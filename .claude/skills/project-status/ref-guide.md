# Guide: Einführung, Neues nach dem Upgrade, Arbeitsweise zeigen

Du schreibst in der Sprache aus `language` in `project.yml`, für das Team, nicht für das Template:
was die Person tut, nicht wie ein Skill gebaut ist.

## Einführung

Für ein neues Projektmitglied, in dieser Folge, je Punkt knapp:

1. **Die Umgebung**, nach [ref-status.md](ref-status.md), „Umgebung“. Fehlt etwas, sagst du zuerst,
   wie es dazukommt; der Rest der Einführung gilt trotzdem.
2. **Was wo liegt:** aus `way-of-working.md`, Abschnitt „Wo was liegt“, dazu die Links aus
   `project.yml` (Projektordner, Anforderungsliste, Board, Confluence, Figma), soweit gesetzt.
3. **Welche Skills es gibt und in welcher Folge:** aus `CLAUDE.md`, Abschnitt „Die Skills“, je Skill
   ein Satz aus seiner `description`.
4. **Die Regeln**, je eine Zeile: ein Lauf je Sitzung (`CLAUDE.md`, „Was immer gilt“); kein Lauf
   schreibt vor dem Ja des Leads; das Was kommt nur über Material, auch die Antwort des Leads; Stunden
   setzt nur ein Mensch, die KI schätzt die Größe (`way-of-working.md`, „Wer entscheidet“ und „Größe
   ja, Stunden nein“).
5. **Wo dieses Projekt vom Standard abweicht:** je Datei in `way-of-working/` Abschnitt und Rumpf in
   einem Satz; ohne Dateien „keine Abweichung“.
6. **Was gerade offen ist und auf die Person wartet:** offene Fragen und Aufgaben, deren `to` ihren
   GitHub-Namen oder ihre Rolle nennt; die Rolle fragst du, wenn sie nicht klar ist. Ist `team` in
   `project.yml` leer, sagst du es und nennst `project-setup`, das es einträgt (§360). Dann der Stand
   der Kette nach [ref-status.md](ref-status.md), „Stand“.

GitHub-Account und Cloud-Umgebung richtest du nicht ein; fehlen sie, sagst du, wer sie einrichtet.

## Neues nach dem Upgrade

Nach `project-upgrade`, für jedes Projektmitglied einmal.

1. Den Upgrade-Commit finden: `git log --grep '^project-upgrade:' -1 --format='%H %s'`. Seine
   Nachricht nennt `v<alt> auf v<neu>`; ohne ihn sagst du, dass das Repo noch kein Upgrade hatte, und
   nennst die Version aus `.claude/template-version`.
2. Aus `CHANGELOG.md` die Einträge nach der alten bis zur neuen Version lesen, und aus
   `git show --stat <commit>`, welche Skills dazukamen, entfielen oder sich änderten.
3. Erklären, in der Sprache des Teams: **was jetzt anders läuft**, **welche Skills neu oder
   umbenannt sind** (mit dem alten Namen) und **was von Hand nachzuziehen ist**, aus dem Abschnitt
   dafür im `CHANGELOG`. Betrifft ein Eintrag eine Abweichung in `way-of-working/`, nennst du sie.

Den `CHANGELOG` zitierst du nicht ganz; du übersetzt ihn in das, was die Person ab heute anders tut.

## Arbeitsweise zeigen

`way-of-working.md` ganz oder den Abschnitt, nach dem gefragt ist. Jede Abweichung steht darin unter
ihrem Abschnitt (§286); du sagst dazu, dass sie vom Standard abweicht, und nennst ihre Datei in
`way-of-working/`. Eine Frage zu einer Regel beantwortest du aus der Datei und nennst den Abschnitt.
Ist `way-of-working.md` nicht die Projektion (`check-repo.py --check wow` meldet `wow`), sagst du
das; gezeigt wird dann der Standard aus `.claude/way-of-working-standard.md` mit den Dateien in
`way-of-working/`.
