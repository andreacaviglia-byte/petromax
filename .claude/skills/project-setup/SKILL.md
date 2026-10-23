---
name: project-setup
description: 'Ein Projekt-Repo einrichten, den Steckbrief nach dem ersten Einlesen aus dem Material vorschlagen und die Einstellungen ändern, Sache des project_owner: Felder von project.yml, Arbeitsweise, Vorschläge dazu, Owner. Nutze das bei "Projekt aufsetzen", "Steckbrief", "Board ändern", "Arbeitsweise ändern", "Vorschlag annehmen", "Owner übertragen". Legt im Drive NICHTS an (requirements-update), nimmt KEIN Material auf (material-intake), legt KEIN Ticket an (ticket-factory).'
---

Verträge: schreibt `datalayer-contract.md`; liest `inputs-and-notes-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`.

# Das Vorhaben einrichten und seine Einstellungen ändern

**Der erste Lauf steht jedem offen** und richtet das Vorhaben ein; er setzt den `project_owner`. Er
fragt nur, **was nie im Material steht**: den Projektordner, die Sprache, Board, Confluence-Space und
das Team. **Nach dem ersten Einlesen schlägt der Lauf „Steckbrief“ den Rest aus dem Material vor**:
Kunde, Titel, Kennung, Shops, Projekttyp und Add-ons, je Feld mit Fundstelle, nach
[ref-steckbrief.md](ref-steckbrief.md). **Jeder weitere Lauf ist für die Einstellungen, Sache des
`project_owner`** (§299, §301) und eines Projekt-Admins, Admin am Repo bei GitHub (§390); wer keines
von beiden ist, bestätigt es vorher. Einstellungen sind die Felder
von `project.yml`, die Arbeitsweise und der Owner selbst, nach [ref-settings.md](ref-settings.md).

**Pflicht ist nur der Projektordner** (§229); jede andere Angabe darf „noch offen" sein, und der
Skill, der sie zuerst braucht, fragt dann danach. **Jede Angabe ist gefragt, geprüft oder mit ihrer
Fundstelle vorgeschlagen und bestätigt, keine geraten**: ein geratener Space fällt erst auf, wenn eine
Seite beim Kunden falsch steht.

**Im Drive legt dieser Lauf nichts an** (§231): fehlt der Projektordner, legt ihn ein Mensch an;
Sheet und Architektur legt `requirements-update` beim ersten Lauf an (§229).

Drive erreichst du über `Google_Drive`; den vollen Namen eines Werkzeugs und sein Schema findest du
über die Werkzeug-Suche und vergleichst die Endung.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Der erste Lauf schreibt nur
`project.yml`, die Einstellungen dazu `way-of-working/` und `todo/`, mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` festlegt. Jede Datei liest du zurück und
committest am Ende in einem Commit direkt auf `main` und pushst; wird der Push abgelehnt, holst du den
Stand und pushst erneut, nie mit Force (§233).

### Step 1 — Prüfen, dass das Repo aus dem Template stammt

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --template-only
```

Meldet es `template_version`, **halte an** und sag: „Dieses Repo stammt nicht aus dem Template
`strix-shopify-project-template`; die Datei `.claude/template-version` fehlt. Ein Projekt-Repo legt
der GitHub-Admin aus dem Template an (§225, §232)." Du legst die Datei nicht an.

### Step 2 — Erster Lauf, Steckbrief oder Einstellungen

Bevor du etwas anderes tust, prüfst du nach [ref-settings.md](ref-settings.md), „Die Prüfung: ist die
Person der `project_owner`?“. Dann:

| Lage | Weg |
|---|---|
| `project_owner` leer | der erste Lauf, weiter mit Step 3 |
| der Lead sagt „Steckbrief“, oder `customer`, `title` oder `project_type` sind leer | der Steckbrief nach [ref-steckbrief.md](ref-steckbrief.md); Steps 3 und 4 gelten dort auch |
| sonst | die Einstellungen nach [ref-settings.md](ref-settings.md) |

Steckbrief und Einstellungen laufen für den Owner ohne Rückfrage, für jeden anderen nach einem Ja
(§301); die Steps unten gelten dort nur, wo die Ref sie nennt.

### Step 3 — Die Verbindung prüfen

Prüf, dass die Werkzeuge von `Google_Drive` in der Werkzeugliste stehen, sonst über die Werkzeug-Suche.
Fehlen sie, **halte an**: „Der Google-Connector Drive ist in dieser Sitzung nicht verbunden; er wird in
claude.ai unter Einstellungen → Connectoren verbunden."

### Step 4 — Den Stand lesen

Steht `project.yml` in der Wurzel des Repos, lies sie ganz und prüf sie:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Meldet das Script einen Verstoß außer `project_folder`, zeig ihn wörtlich und frag, ob der Lead ihn in
diesem Lauf beheben will; geraten wird nichts. Angaben, die dieser Lauf nicht berührt, schreibst du
später Zeichen für Zeichen zurück.

### Step 5 — Die Fragen des ersten Laufs, alle in einer Nachricht

Frag nur, was `project.yml` noch nicht trägt, aus [ref-project-yml.md](ref-project-yml.md), „Die
Fragen des ersten Laufs“: **den Projektordner, die Sprache, das Board, den Confluence-Space und das
Team**, **alle in einer Nachricht**, und sag dazu einmal: jede Antwort außer dem Ordner darf „noch
offen" sein; dann bleibt das Feld leer, und der Skill, der es zuerst braucht, fragt wieder. Kunde,
Titel, Shops, Projekttyp und Add-ons fragst du nicht: sie stehen im Material und kommen mit dem
Steckbrief nach dem ersten Einlesen. **Übernimm keine Antwort, die du nicht bekommen hast.**

Beim Projektordner fragst du nach **dem Ordner des Vorhabens im Drive, als Link oder ID** —
ausdrücklich nicht nach dem Kundenordner (§229). Erkennen oder suchen tust du ihn nicht: die Ordner
sind ungeregelt, Erkennen hieße raten. **`project_owner` fragst du nicht**: er ist die Person, die
diesen Lauf ausführt (§289, §294), nach [ref-project-yml.md](ref-project-yml.md); den Owner trägst du
im Team mit der Rolle ein, die er nennt.

### Step 6 — Ordner, Board und Space lesend prüfen

Den Projektordner liest du nach [ref-project-yml.md](ref-project-yml.md), „Den Projektordner zeigen“:
es muss ein Ordner sein (`mimeType: application/vnd.google-apps.folder`); seinen Titel und **seine
oberste Ebene**, je Eintrag Titel und Art, zeigst du in Step 7. Eine ID, die kein Ordner ist oder
nicht erreichbar, nennst du mit der Meldung und fragst neu; ohne erreichbaren Ordner **hältst du an**:
er ist die einzige Pflicht.

Board und Space prüfst du nur, wenn der Lead sie genannt hat, nach [ref-project-yml.md](ref-project-yml.md),
„Board und Space prüfen“. Eine Angabe, deren Prüfung scheitert, bleibt leer und steht in der Vorschau
mit der Meldung; ungeprüft geht keine Adresse in den Steckbrief.

### Step 7 — Zeigen und das Ja abwarten

Vor dem Schreiben zeigst du **die Vorschau nach [ref-project-yml.md](ref-project-yml.md), „Die
Vorschau“**: eine Tabelle in Klartext mit jedem Feld des Steckbriefs, auch den leeren, dazu den
Projektordner mit seiner obersten Ebene und der Frage „Ist das der Ordner dieses Vorhabens?". **Kein
YAML in der Vorschau**; den Text von `project.yml` zeigst du nur, wenn der Lead danach fragt.
Frage und Ja nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. Verneint der Lead den Ordner, fragst du nach dem richtigen.

### Step 8 — `project.yml` schreiben, prüfen, committen

Lies `project.yml` direkt vor dem Schreiben noch einmal: hat sich seit Step 4 etwas geändert, zeig die
Änderung und frag. Dann schreibst du den Text, der der Vorschau aus Step 7 entspricht
([ref-project-yml.md](ref-project-yml.md)), liest ihn zurück und prüfst ihn:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

**Erst zurückgelesen, gleich und ohne Verstoß heißt „geschrieben".** Meldet das Script einen Verstoß,
nennst du ihn wörtlich, korrigierst den Text mit dem Lead und schreibst neu. Dann committest und pushst
du `project.yml`, Nachricht `project-setup: <was>`.

### Step 9 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397): der Projektordner mit Link; welche Angaben eingetragen
sind, in Worten (Sprache, Board, Confluence, Team) und wer Owner ist; welche noch offen sind. **Wie in diesem
Vorhaben gearbeitet wird, steht in `way-of-working.md`** (§286); ändern darf sie nur der
`project_owner`, mit diesem Skill (§299).

Dann liest du `../project-status/SKILL.md` und führst in dieser Sitzung seine Einführung aus, mit der
Umgebung zuerst (§289); sie schreibt nichts.

Dann die nächsten Läufe, als Hinweis, je in einer neuen Sitzung: `material-intake`, sobald Material im
Projektordner liegt; danach `project-setup` „Steckbrief“, das Kunde, Titel, Shops, Projekttyp und
Add-ons aus dem Material vorschlägt; dann `requirements-update`, das Sheet und Architektur beim ersten
Lauf anlegt, in jedem Vorhaben (§282). **Du stößt keinen Lauf an**; der Lead ruft ihn auf. Hatte der
Kunde schon ein Vorhaben in einem anderen Repo, sagst du: das neue bekommt eigenes Material, und was
davon noch gilt, klärt die Discovery mit dem Kunden (§224).

## Was dieser Lauf nicht tut

Er legt im Drive nichts an und schreibt nichts nach Confluence oder auf das Board. Nach dem ersten
Lauf ändert er nichts für jemanden, der nicht `project_owner` ist, ohne dessen Ja zur Rückfrage. Er legt kein Sheet,
keine Architektur, keine Kundensicht, kein Material, keine Notiz und keine ADR an. Er liest keinen anderen
Projektordner und kein anderes Projekt-Repo.
