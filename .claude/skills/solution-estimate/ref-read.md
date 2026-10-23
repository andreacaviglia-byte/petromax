# Lesen: das Repo, die Spalte der Stunden, und die Arbeitsdateien

Das Script liest das Projekt-Repo selbst und aus dem Temp-Ordner des Laufs drei Dateien:
`hours.json` und `meta.json`, die du direkt nach der Lesung schreibst, und `bullets.json`, die du
nach `positions` schreibst.

## Das Repo

**Die Dateien des Repos sind die Quelle** (§280). Das Script liest sie über `repo` in `meta.json`;
du holst sie nicht in den Kontext und schreibst nichts davon ab. Es nimmt:

| Datei | Felder |
|---|---|
| `requirements/REQ-NNN.md` | `title`, `shops`, `status`, `scope`, `epic`, `size`, `classification`, `own_sections`, `solution_status`, `standard`; der Titel steht mit dem Shop-Bezug hinten wie im Proposal, `Staffelpreise (B2B)` (§307) |
| `epics/EP-NNN.md` | `title`, `domain`, `status` |
| `gaps/GAP-NNN.md` | `status`, `concerns`, `blocking` |
| `project.yml` | `customer`, `title`, `language`, `add_ons`, die `key` aus `shops` |

Ein Seitentyp ist eine Anforderung in einem Epic der Domäne `storefront`; sein Feld `own_sections`
ist die Annahme zu den eigenen Sections (§285). Ein Epic der Domäne `design` ist das Design-Epic
(§303). Die Feldnamen und Werte stehen in `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
die Anzeige in der Sprache des Projekts in `${CLAUDE_SKILL_DIR}/../../docs/requirements-list-contract.md`.

## Die Spalte der Stunden

**`Aufwand (h)` ist ein Feld der Menschen** (§280 Regel 5, §283): seine Quelle ist das Sheet, und es
steht in keiner Datei des Repos. Du liest nur die schmale Spalte, mit der Kennung daneben:

| Zweck | Aufruf |
|---|---|
| Tab-Namen | `Google_Sheets.get_spreadsheet` mit `spreadsheetId` = `requirements_sheet` und `fields: ["sheets.properties.title"]`; `Solutioning` muss dastehen, sonst hältst du an |
| Kennung | `Google_Sheets.get_values`, `range` = `'Solutioning'!A1:A` |
| Stunden | `Google_Sheets.get_values`, `range` = `'Solutioning'!E1:E` |

**`hours.json` trägt die beiden Antworten von `get_values`, wie sie kamen**, als
`{"valueRanges": [‹Antwort A›, ‹Antwort E›]}`; jede Antwort trägt `values` als Liste von Zeilen. Das
Script legt die Bereiche nebeneinander und nimmt die Spalten an ihrer Kopfzeile, `ID` und
`Aufwand (h)` (`en`: `Effort (h)`); eine leere Zelle fehlt in der Antwort, und das Script füllt sie
auf. Steht in Zeile 1 etwas anderes, lehnt es mit `header` ab: das Sheet hat nicht die Spalten des
Vertrags, und ein Mensch stellt es um.

**Die Lesezeit** nimmst du direkt nach der zweiten Lesung: `date -u +%Y-%m-%dT%H:%MZ`.

## `meta.json`

```json
{"repo": "‹Wurzel des Projekt-Repos›", "read_at": "2026-09-30T14:05Z",
 "surcharges": [{"reason": "Projektmanagement", "percent": "20"}, {"reason": "Testing", "percent": "20"}],
 "extras": [{"name": "Go-Live-Begleitung", "hours": "8"}]}
```

`repo` ist die Ausgabe von `git rev-parse --show-toplevel`, `read_at` die Lesezeit. `surcharges` und
`extras` sind die Angaben aus dem Aufruf (Step 3); was dort fehlt, lässt du weg, und das
Dokument sagt es. `reason` und `name` sind der Name der Tätigkeit oder Position, ohne „Aufschlag“,
Prozent und „Budget“ (§355; sonst `effort_row`). Ein Budget steht nicht darin; das Script lehnt es mit `budget` ab.
Kunde, Titel und Sprache stehen hier nicht: das Script
liest sie aus `project.yml`.

**`meta.json` liegt im Temp-Ordner des Laufs, außerhalb des Repos** (§233), und landet nie im Repo.

## Die Bullets

**`bullets.json` trägt je Position, die `positions` nennt, eine Liste von Bullets** in Kundensprache,
der Schlüssel ist der aus der Zeile `POSITION` (§355):

```json
{"shop_setup": ["Märkte, Währungen und Versandzonen einrichten", "Zahlungsarten und Steuern"],
 "ux_ui": ["Designkonzept und Design-System", "UX/UI-QA vor dem Go-Live", "Theme-Anpassungen"],
 "data_migration": ["Produkte", "Kunden", "Bestellungen", "Gutscheine und Rabattcodes"]}
```

- **So viele wie nötig, so wenige wie möglich**: ein Bullet fasst zusammen, was der Kunde unter der
  Position wiedererkennt, nicht je Anforderung eine Zeile. Eine feste Zahl gibt es nicht.
- **UX/UI** trägt „Designkonzept und Design-System“ (mit dem Design-Epic), „UX/UI-QA vor dem Go-Live“
  (mit `standard: design-qa`) und „Theme-Anpassungen“ (mit `theme` oder `theme_native`), soweit
  vorhanden, und nur, was die Position trägt.
- **Daten-Migration** trägt je migriertem Objekt einen Bullet, etwa Produkte, Kunden, Bestellungen,
  Gutscheine und Rabattcodes.
- **Kein Bullet trägt** Stunden, „Aufschlag“ oder „Budget“, eine Kennung (`REQ-012`, `EP-003`), einen
  Wert des Repos (`custom_app`), einen Pfad, einen Skill-Namen oder eine Adresse aus dem Drive; sonst
  lehnt das Script mit `bullet` ab.
- Eine Position ohne Bullet und ein Schlüssel ohne Position lehnt es ebenfalls mit `bullet` ab.

## Der Stand

**Die Zeile `STAND` auf stderr nennt die Lesezeit und je gezählte Anforderung die gelesenen
Stunden**. Das Sheet hält keinen Revisionsschutz; mit dem Commit des Repos, auf dem
der Lauf steht, und dieser Zeile ist das Dokument nachzurechnen. Sie steht nicht im Dokument, sondern
im Rumpf des Commits des Laufs (§264, Step 7 der SKILL.md).
