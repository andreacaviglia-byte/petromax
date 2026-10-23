# Stand: Umgebung, Stand der Kette, Hilfe

## Umgebung

**Nötig ist, was `project.yml` verlangt** (§289). Welche Werkzeuge die Strecke braucht und wofür,
steht einmal, in `${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`; dort liest du nach, wenn
eine Zeile unklar ist. Den Namen eines Werkzeugs findest du über die Werkzeug-Suche und vergleichst
die Endung; das Schema holst du, bevor du das erste Feld setzt.

| Was | nötig | Prüfung |
|---|---|---|
| Drive | immer | `get_file_metadata` auf `project_folder`; ist er leer, nur ob das Werkzeug in der Liste steht |
| Sheets | immer | `get_spreadsheet` auf `requirements_sheet` mit `fields` = `properties.title`; ist es leer, nur ob das Werkzeug in der Liste steht |
| Docs | immer | ob `read_doc` in der Werkzeugliste steht; ohne ein Doc des Vorhabens gibt es keinen harmlosen Aufruf |
| Atlassian | mit `confluence.space` oder `board.tool: jira` | `atlassianUserInfo` |
| Asana | mit `board.tool: asana` | `get_me` |
| Figma | mit `figma` | ob ein Werkzeug des Figma-Connectors in der Liste steht; kein Lauf der Strecke ruft eines |
| Shopify-Doku | immer | die Wege aus `${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`, Abschnitt „Die Doku von Shopify“ (§340): ob `search_docs_chunks` in der Werkzeugliste steht und mit einer Frage antwortet, und ein `WebFetch` auf `https://shopify.dev/docs`; scheitert es, der `curl` auf shopify.dev von dort |
| Wissensbasis | immer | in einer Cloud-Sitzung zuerst `add_repo` mit `owner` `webweit-gmbh`, `repo` `strix-shopify-knowledge-base`, `access: read`, ohne Klon, auch wenn die Antwort einen verlangt (`kb-contract.md`); dann `get_file_contents` auf `index.md` dort (`${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`) |
| GitHub-Name | immer | `python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --whoami`; dazu, ob er der `project_owner` ist |
| Branch und Pull | immer | aus Step 1: steht die Sitzung auf `main`, lief `sync-main.py` mit Exit 0 |
| Skill-Creator | immer | ob der Skill-Creator von Anthropic in der Liste der Skills dieser Sitzung steht; `skill-create` braucht ihn |

Die Tabelle, die du zeigst:

```
| Was | da | antwortet | Meldung und Abhilfe |
|---|---|---|---|
| Drive | ja | ja | |
| Asana | nein | — | in claude.ai unter Einstellungen → Connectoren verbinden |
```

**Die Abhilfe nennt den Weg, nicht die Ursache, die du vermutest:**

- **Ein Connector fehlt:** in claude.ai unter Einstellungen → Connectoren verbinden, dann eine neue
  Sitzung.
- **Ein Connector antwortet mit einer Meldung:** die Meldung wörtlich; bei fehlendem Zugriff auf
  Ordner, Sheet, Space oder Board gibt ihn der, dem es gehört.
- **Die Shopify-Doku antwortet nicht** (§339, §340, §341): der Shopify-Connector ist ein Weg zur
  Doku-Suche, keine Voraussetzung; wer ihn will, verbindet ihn in claude.ai unter Einstellungen →
  Connectoren, ein Shop ist nicht nötig. Meldet `WebFetch` „getaddrinfo ENOTFOUND“ oder `curl`
  „CONNECT tunnel failed, response 403“, steht shopify.dev nicht in der Liste erlaubter Domains der
  Umgebung: den Block aus `network/allowlist.md` der Wissensbasis in die Umgebung kopieren. Ohne Doku laufen
  `solution-approach`, `solution-design` und `solution-review` weiter, und Plattformaussagen ohne Beleg
  stehen mit „(noch zu verifizieren)“ da.
- **Die Wissensbasis antwortet nicht:** in der Cloud ohne `add_repo` lehnt die Sitzung das Lesen ab;
  sonst fehlt dem GitHub-Konto der Zugriff auf das Repo.
- **Kein GitHub-Name:** der Hook `wow-guard` fragt dann bei jeder Änderung in `way-of-working/` nach,
  `project-setup` und `project-upgrade` fragen vorher nach. Den Account und die Cloud-Umgebung
  richtet ihr Betreuer im Team ein, nicht dieser Lauf.
- **Nicht auf `main` oder der Pull scheitert:** die Meldung wörtlich; jeder Lauf zieht zuerst `main`.
- **Der Skill-Creator fehlt:** `skill-create` läuft dann nicht; die übrigen Skills sind nicht
  betroffen.

## Stand

Du liest die Dateien selbst, nicht die `readme.md`: sie ist eine Projektion und kann hinterherhinken,
wenn ein Lauf sie nicht schrieb.

- **Stand der Kette:** je Epic in `epics/` Kennung, Titel, `status`, `information` und
  `clarification`; ob es einen Entwurf (`draft`), eine Epic Page und ein Epic-Ticket hat. Dazu je
  Snapshot in `scope/` der Anlass und das Datum, und die Zahl der Anforderungen in `requirements/`
  nach `status` und `scope`. Ohne Epics nur die Anforderungen.
- **Offene Fragen mit `blocking: yes`:** je Datei in `gaps/` mit `status: open` Kennung, erster Satz,
  `to` und `concerns`.
- **Offene Aufgaben:** je Datei in `todo/` mit `status: open` Titel und `to`; ein Vorschlag zur
  Arbeitsweise an den `project_owner` steht als solcher da.
- **Jüngste Entscheidungen:** die fünf jüngsten ADRs in `decisions/`, Kennung und Titel.

## Hilfe

**Fragen zu den Skills** („welcher Skill für …“, „was macht `solution-review`“) beantwortest du aus
den `description` der Skills unter `.claude/skills/` und aus `CLAUDE.md`, Abschnitt „Die Skills“.
**Fragen zum Stand** („warum hängt EP-003“) aus den Dateien: `clarification` des Epics, die offenen
Fragen, deren `concerns` es nennen, die Reihenfolge des Lösens in `solve_order` und die des Bauens in `epics/critical-path.md`. Jede Antwort nennt
die Stelle. Weißt du es aus dem Repo nicht, sagst du das und nennst, wo es stehen müsste.
