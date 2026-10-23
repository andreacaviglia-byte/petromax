# Repo und Sheet: was dieser Lauf liest und schreibt

**Die Lösung steht im Repo** (§280): das Epic in `epics/EP-NNN.md`, seine Anforderungen in
`requirements/`, je mit `epic` = die Kennung des Epics, die offenen Fragen in `gaps/`, die
Entscheidungen in `decisions/`, die Architektur in `architecture.md`. Form und Felder setzt
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`. Aus dem Sheet liest dieser Lauf nur, was dort
seine Quelle hat und was er braucht; geschrieben wird es nur über die Projektion
(`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`). Arbeitsdateien liegen im Temp-Ordner des Laufs
(`mktemp -d`), außerhalb des Repos (§233).

## Lesen

| Zweck | Weg |
|---|---|
| das Epic | lies `epics/EP-NNN.md`: Kopf und Rumpf |
| seine Anforderungen | `grep -l '^epic: EP-NNN$' requirements/*.md`, dann jede Datei ganz |
| die offenen Fragen | `grep -l '^status: open$' gaps/*.md`, davon die, deren `concerns` eine Anforderung des Epics oder das Epic nennt |
| die geschlossenen Fragen | ebenso mit `status: closed`; ihre Antwort steht unter `## Answer` |
| die Lösungsansätze der übrigen Epics | `grep -H '^epic:\|^classification:\|^solution_status:' requirements/*.md` und je Datei mit Lösungsansatz die erste Überschrift `###` unter `## Approach`, nicht die Dateien ganz; dazu von jedem anderen Epic der Kopf und `Technical Information` (§398) |
| die Blocker im ganzen Repo | `grep -l '^solution_status: blocked$' requirements/*.md` und die offenen Fragen mit `blocking: yes` |
| `Document Owner` | `Owner Strix` des Epics im Tab `Epics` (`en`: `Strix owner`), ein Feld der Menschen (§280, Regel 5): `Google_Sheets.get_values` je ein Aufruf mit `range` = `'Epics'!A1:A` und `'Epics'!I1:I`, die Zeile über die `Epic-ID`. Ist sie leer oder fehlt das Sheet, fragst du den Lead nach dem Namen |

**Die Dateien holst du nicht alle in den Kontext**: aus `requirements/` liest du nur die des Epics
ganz, aus `gaps/` nur die, die es betreffen.

## Schreiben

**Dieser Lauf schreibt nur das Wie** (§280, Regel 3), und nur an seinem Epic: in der Epic-Datei und in
den Dateien der Anforderungen, deren `epic` das Epic nennt. Was ein anderes Epic betrifft, wird eine
Aufgabe in `todo/` an den Owner jenes Epics (`${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, §359).

| Datei | was dieser Lauf schreibt |
|---|---|
| `epics/EP-NNN.md` | den Rumpf, die Lösung in der Gliederung des Vertrags `${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`; im Kopf `clarification` und `draft`, und `summary` nur nach der Regel unten; die übrigen Felder des Kopfs gehören `epic-structure`, außer `board_key` (`ticket-factory`) und `epic_page` (`solution-epic-page`) |
| `requirements/REQ-NNN.md` | `## Approach` (höchstens drei Lösungsansätze, je `### <Name>`, ein Satz, die Zeilen `Fit:`, `Größe:` mit Bau, Konfiguration und Pflege und `KB:`; der gewählte oder empfohlene zuerst), `## Details` (die Angaben, die der Lösungsansatz braucht, ohne Gewerk), `solution_status` (`proposed` solange die Wahl offen ist, `decided` mit der Wahl, `blocked` beim Blocker), `classification`, `size`, mit `decided` und dem Add-on `solutioning` `effort_estimate_model` (§357: die Rohschätzung in Stunden, frei aus der Lösung, je Teil von `classification` geschätzt und addiert, ohne Spanne; nie `size_estimate_approach`), `depends_on`, bei einem Seitentyp `own_sections`, mit der Wahl `design_needed` und `interface_needed` (`yes` oder `no`). Im Epic der Domäne `design` nichts davon außer `depends_on` (§297) |
| `gaps/GAP-NNN.md` | neue Fragen dieses Laufs ([ref-questions.md](ref-questions.md)); geschlossen wird eine Frage nur über `requirements-update` |
| `decisions/`, `architecture.md` | nach [ref-adr.md](ref-adr.md) |
| `notes/JJJJ-MM-TT-entwurf-EP-NNN-kommentare.md` | die Kommentare und Abweichungen des Entwurfs, wörtlich, mit wer und wo; Material für den nächsten Lauf von `requirements-update` |

**Das Was schreibt dieser Lauf nicht**: `title`, `status`, `scope`, `## Description`,
`## Acceptance criteria`, `## Current state` und `## Sections` gehören `requirements-update`. Die User
Story leitet dieser Lauf im Rumpf der Epic-Datei ab, nicht in der Anforderung (§323,
`${CLAUDE_SKILL_DIR}/../../docs/user-story-contract.md`). Eine Korrektur am Was, die ein Kommentar oder der Lead im Chat bringt, steht in
der Notiz der Kommentare, und der Bericht nennt `requirements-update` als nächsten Lauf (§280,
Regel 6).

**`design_needed` und `interface_needed` mit der Wahl:** `yes` bei Design, wenn der Lösungsansatz eine Ansicht
ändert, deren Gestaltung kein Entwurf und kein Standard des Themes festlegt; `yes` bei Interface,
wenn der Lösungsansatz eine Schnittstelle braucht, auch für Stammdaten aus PIM oder ERP.

**`summary` im Kopf des Epics nennt keinen Lösungsansatz**: sie ist das Kriterium des Schnitts in einem
Satz. Nennt sie einen, etwa einen, den eine ADR dieses Laufs ändert oder ablöst, schreibst du sie ohne
ihn neu, im Plan alt und neu; ein „Größe bestätigt“ (`size_confirmed`, `en`: „Size confirmed“) am Ende bleibt stehen.

**`clarification` im Kopf des Epics** trägt den Stand des Epics: was es aufhält, oder dass es bereit
ist, etwa `GAP-009 blockiert REQ-009` (`clar_gap_blocks`), `Kunde entscheidet den Lösungsansatz für REQ-001`
(`clar_customer_decides`) oder `geprüft; bereit für Tickets` (`clar_reviewed`). Der Kunde liest ihn in
`Klärungsbedarf`: er steht als feste Wendung in der Sprache aus `language`, ohne Namen eines Skills
und einer Datei, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen
Wendungen“ (§337); bei `en` etwa `GAP-009 blocks REQ-009`. Jeder Lauf ersetzt ihn, wenn er sich
geändert hat. Beginnt er mit `Nachprüfen:` (`clar_recheck`, `en`: `Recheck:`), weil
`requirements-update` eine Zeile in `architecture.md` ersetzt hat, prüfst du die Lösung gegen die neue
Zeile und setzt danach `Nachgeprüft: ‹Datum›, trägt` oder `Nachgeprüft: ‹Datum›, geändert`
(`clar_rechecked_holds`, `clar_rechecked_changed`), gefolgt vom neuen Stand.

Jede Datei liest du direkt vor dem Schreiben und zurück danach; was dieser Lauf nicht berührt, bleibt
Zeichen für Zeichen. Erst zurückgelesen und gleich heißt geschrieben.

## Prüfen: jede Anforderung genau einmal

Aus der Spalte `ID` unter `Requirements` und `Discarded` des Rumpfs, in der Sprache des Dokuments,
schreibst du `ids.txt`, eine ID je Tabellenzeile, **ohne Kopfzeile**: das Script liest jede Zeile als
ID, und eine Kopfzeile `ID` meldet es als fremde Anforderung (`once_on_page`). Aus dem Repo schreibst du `anforderungen.tsv` mit der
Kopfzeile `ID` und je Anforderung in `requirements/` ihrer Kennung, und `epics.tsv` mit der Kopfzeile
`Epic-ID<TAB>Anforderungen` (`en`: `Epic ID<TAB>Requirements`) und einer Zeile: die Epic-ID und die
Kennungen seiner Anforderungen, getrennt durch Komma. Dann:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-sheet.py anforderungen.tsv --epics epics.tsv --page EP-003 ids.txt --check once_on_page
```

Exit 0 ohne Befund, 1 mit einer Zeile `once_on_page <ID> <Satz>` je Befund, 2 bei falschem Aufruf. Ein
Befund ist ein Fehler dieses Laufs: du berichtigst den Rumpf und prüfst neu.

## Material suchen

| Material | Weg |
|---|---|
| eine Datei lesen | lies sie |
| in den Dateien suchen | `grep -il '<stichwort>' inputs/* notes/* gaps/* decisions/*`, dann nur die Treffer lesen |

Gesucht wird in den Dateien im Repo, nicht im Kontext.
