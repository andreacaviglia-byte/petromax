# Die Regeln des Templates für einen eigenen Skill

Jede Regel hat einen Grund im Template; der Skill-Creator kennt sie nicht und bekommt sie als Vorgabe.

| Regel | Grund |
|---|---|
| **Eigener Name:** kebab-case, höchstens 64 Zeichen, ohne `claude` und `anthropic`, und keiner der Namen aus `CLAUDE.md`, Abschnitt „Die Skills“. Ein Präfix aus `key` in `project.yml` macht ihn als eigenen kenntlich (`relaunch-content-check`) | ein Standard-Name würde beim nächsten `project-upgrade` überschrieben oder führt zum Konflikt; die Plattform liest den Namen |
| **Ablage** unter `.claude/skills/<name>/`, der Ordner heißt wie `name` im Frontmatter | so lädt Claude Code ihn |
| **Frontmatter** nur `name` und `description`; die `description` englisch oder in der Sprache des Projekts, mit den Worten, bei denen er läuft („Nutze das bei …“), und mit dem, was er nicht tut, in Großbuchstaben (`KEIN`, `NICHT`); höchstens 1024 Zeichen, besser unter 500 | die `description` ist das Einzige, was vor dem Laden gelesen wird; ohne Abgrenzung greift das Routing daneben |
| **Die drei Kopfzeilen** direkt unter dem Frontmatter, je eine Zeile: `abgeleitet von: <Standard-Skill oder „keinem“>`, `gilt für: <Vorhaben, Workstream oder Epic>`, `verantwortlich: <Rolle oder GitHub-Name>` (§225) | ohne sie meldet `check-project.py` den Skill als `skill_header`; sie sagen, wem er gehört |
| **Länge:** die `SKILL.md` höchstens 300 Zeilen, besser unter 150; was nur in einem Fall gebraucht wird, steht in einer Ref daneben (§238) | hinter 300 Zeilen wird ein Skill nicht mehr verlässlich gelesen |
| **Steps** als `### Step N — <Name>`; Step 1 zieht den Stand von `main` mit `sync-main.py` und hält an, wenn es nicht mit Exit 0 endet | jede Sitzung startet sonst auf einem veralteten Stand |
| **Anrede Du**, Sätze in der Gegenwart | wie jeder Skill des Templates |
| **Kein Lauf schreibt vor dem Ja des Leads**; was er schreibt, liest er zurück | `way-of-working.md`, „Wer entscheidet“ |
| **Schreibt er in den Datalayer**, endet er nach `.claude/docs/ref-projection.md` und hält die Schreiber je Pfad aus `.claude/docs/datalayer-contract.md` ein; ein Feld, das dort einem anderen Skill gehört, schreibt er nicht | die Projektion zeigt sonst einen Stand, den kein Script geprüft hat |
| **Scripts** des Templates ruft er über `${CLAUDE_SKILL_DIR}/../../scripts/`; eigene liegen in seinem `scripts/` | die Pfade bleiben gültig, wenn das Repo woanders liegt |
| **Kein Skill ruft einen anderen**, außer `grill-me` über `../grill-me/SKILL.md`; er nennt am Ende den nächsten Lauf „in einer neuen Sitzung“ | §215; jeder Lauf zahlt den ganzen Kontext neu (§244) |
| **Interna und Daten:** nichts aus internen Quellen nach außen (`way-of-working.md`, „Interna“), keine Zugangsdaten, keine Daten der Endkunden (`CLAUDE.md`, „Was immer gilt“) | §278, §227, §236 |
