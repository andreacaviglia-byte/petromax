# Den Stand lesen: die Aufrufe dieses Laufs

**Der Stand ist das Repo** (§280): die Lösung je Epic im Rumpf von `epics/EP-NNN.md`, der Lösungsansatz je
Anforderung in `## Approach` und `## Details` ihrer Datei, die offenen Fragen in `gaps/`, die offenen
Aufgaben in `todo/`, die Architektur in `architecture.md`, die Reihenfolge in `epics/critical-path.md`. Die
Form jeder Datei steht in `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`. **Aus dem Sheet liest
dieser Lauf nur Felder der Menschen**, die dort ihre Quelle haben (§280, Regel 5), und nur die schmale
Spalte: `Owner Strix` der Epics für den Bericht, `Cluster` für einen Umfang nach Workstream.
`Aufwand (h)` liest du nicht (§357). Arbeitsdateien liegen im Temp-Ordner des Laufs (`mktemp -d`),
außerhalb des Repos (§233).

## Das Repo

| Zweck | Weg |
|---|---|
| Steckbrief | lies `project.yml` |
| Architektur | lies `architecture.md` |
| ADRs | liste `decisions/`; lies jede ADR, die `depends_on`, `Quelle/ADR` oder ein Rumpf nennt |
| Epics | liste `epics/EP-*.md`; je Epic den Kopf und den Rumpf ganz |
| Anforderungen je Epic | `grep -l '^epic: EP-NNN$' requirements/*.md`, je Datei nur der Kopf, `## Approach` und `## Details`, mit dem Befehl unten |
| Anforderungen ohne Epic | `grep -L '^epic: EP-' requirements/*.md`, nur die Kennungen |
| offene Fragen | `grep -l '^status: open$' gaps/*.md`, je Datei Kopf und erster Satz |
| offene Aufgaben | `grep -l '^status: open$' todo/*.md`, je Datei Kopf und Rumpf |
| Reihenfolge | lies `epics/critical-path.md`: `Stufen` und `Abhängigkeiten` (§267) |

**Vom Was liest du nur den Kopf**: Beschreibung, Kriterien und Ist-Zustand holst du nur für
eine Anforderung, deren Befund daran hängt. Kopf, Lösungsansatz und Angaben einer Anforderung:

```
awk '/^---$/ && h<2 {h++; print; next} h<2 {print; next} /^## /{p=($2=="Approach"||$2=="Details")} p' requirements/REQ-NNN.md
```

**Gezählt und geprüft** wird eine Anforderung mit `status` `open` oder `confirmed` und `scope` leer
oder `in_scope`. Eine mit `status` `rejected` oder `duplicate` zählt in keiner Summe und trägt keinen Befund; eine mit
`scope: out_of_scope` zählt in keiner Summe und trägt nur den Befund „Must-have, aber Out of Scope“
([ref-checks.md](ref-checks.md), §283, §284, §327).

**Den Stand des Repos** hältst du nach dem Pull fest, `git log -1 --format='%h %cI'`; er steht im Kopf
des Berichts.

## Die Lösung eines Epics

**Ein Epic hat eine Lösung, wenn der Rumpf von `epics/EP-NNN.md` den Abschnitt `Requirements` der
Vorlage trägt** (`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`), den `solution-design` schreibt. Ein Epic ohne ihn steht im Bericht unter „nicht geprüft“, Grund
„keine Lösung“; du suchst keine im Drive und keine in Confluence. Die Überschriften des Rumpfs stehen
in der Sprache aus `language`, nach der Tabelle in diesem Vertrag, Abschnitt „Die
Bezeichnungen“ (§255); hier heißen sie mit ihrer englischen Bezeichnung.

| Stelle | Was du daraus nimmst |
|---|---|
| `Relations and Prerequisites` im Rumpf | die Zeilen aus `architecture.md` und die Epics, auf die die Lösung baut |
| `Requirements` im Rumpf | den übergreifenden Ansatz; je Zeile `ID` und `Technical Information` |
| `Discarded` im Rumpf | was die Lösung ausdrücklich nicht tut |
| `## Approach` der Anforderung | die Lösungsansätze: der erste ist der gewählte oder empfohlene, je Lösungsansatz die Zeile `KB:` (§268) |
| `## Details` der Anforderung | die Angaben, die der Lösungsansatz braucht: Felder, Objekte, Mengen, Apps, Schnittstellen |
| Kopf der Anforderung | `solution_status`, `classification`, `size`, `depends_on`, `own_sections` |

**Trägt eine Anforderung `solution_status: proposed` und mehr als einen Lösungsansatz, ist die Wahl offen**:
sie zählt in den Summen mit jedem Lösungsansatz gesondert, und die Prüfungen nennen, unter welchem Lösungsansatz der
Befund gilt. Mit `blocked` hat sie keinen Lösungsansatz.

## Das Sheet

Ist `requirements_sheet` leer, liest du kein Sheet: der Bericht nennt die
Epics „ohne Owner“, und ein Umfang nach Workstream geht nicht; nach dem Umfang fragst du dann nicht. Sonst liest du vor dem ersten Zugriff mit
`Google_Drive.get_file_metadata` (`fileId`) die Eltern des Sheets, bis der Projektordner
(`project_folder`) erreicht ist. Dann je Bereich ein Aufruf `Google_Sheets.get_values`, mit den
Tab-Namen in der Sprache aus `language`:

| Zweck | `range` | Kopf in Zeile 1, `de` / `en` |
|---|---|---|
| Owner der Epics | `'Epics'!A1:A` und `'Epics'!I1:I` | `Epic-ID`, `Owner Strix` / `Epic ID`, `Strix owner` |
| Workstream, für einen Umfang nach Workstream und für die Frage nach dem Umfang | `'Anforderungen'!A1:A` und `'Anforderungen'!E1:E` (`en`: `'Requirements'!…`) | `ID`, `Cluster` / `ID`, `Cluster` |

**Den ganzen Tab `Anforderungen` liest du nicht mit `get_values`**
(`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`). Die Antwort trägt `values` als Liste von Zeilen;
leere Zellen am Ende fehlen; die Zeile im Sheet ist die Stelle in `values` plus eins, über beide
Bereiche desselben Tabs dieselbe. **Weicht ein Kopf ab**, nimmst du den Bereich nicht: beim Workstream
hältst du an, denn der Umfang ist offen; bei den Owner steht „ohne Owner“, und der Bericht nennt
den Kopf wörtlich.

**Die Lesezeit** ist die Uhrzeit deiner Antwort auf den letzten dieser Aufrufe, mit Datum und
Zeitzone. Sie steht im Kopf des Berichts.

## Die Grenzen der Plattform, nur im Lauf über alle

| Zweck | Aufruf |
|---|---|
| die Grenze zu einer Summe | über die Wege aus `${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`, Abschnitt „Die Doku von Shopify“ (§340), etwa `search_docs_chunks` oder `WebSearch` mit dem Gegenstand und dem Wort „limit“, „metafield definitions limit“ |

Du übernimmst die Zahl nur mit der Fundstelle, die sie nennt, mit URL und Datum. Findet kein Weg
eine, bleibt die Summe stehen und der Bericht sagt, dass die Grenze fehlt (§110).
