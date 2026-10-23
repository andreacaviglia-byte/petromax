# Die Grundlage: was der Lauf im Repo liest und ob die Kriterien prüfbar sind

**Die Grundlage ist das Repo** (§280): die Anforderungen in `requirements/`, im Projekt ihr Epic in
`epics/`. Das Sheet ist nur Projektion; aus ihm liest dieser Lauf nichts. Material nimmt er nicht an:
was der Lead im Chat dazugibt, nimmt `requirements-update` an (§282), und der Bericht nennt ihn. Er ist
ein Schritt von `SKILL.md`, kein eigener Skill. Die Dateien holst du nicht alle in den Kontext,
sondern nur die des Umfangs.

## Der Umfang

| Aufruf | Was du liest |
|---|---|
| eine Epic-Kennung, `EP-003` | `epics/EP-003.md` ganz; seine Anforderungen über `grep -l '^epic: EP-003$' requirements/*.md`, jede Datei ganz |
| Anforderungskennungen, `REQ-012, REQ-014` | jede Datei ganz; im Projekt die Epic-Datei aus ihrem Feld `epic` |
| ohne Angabe | du läufst nicht los (§398). Im Projekt nennst du in einem Satz die Epics in `epics/` ohne `board_key` und fragst „Für welche Epics lege ich Tickets an?“ mit „Alle offenen Epics“ und bis zu drei dieser Epic-IDs mit Titel als Antworten, ohne Empfehlung. „Alle offenen Epics“ nimmt jedes Epic, dessen Anforderungen nach dem Abgleich (`SKILL.md`, Step 5) noch ein Ticket fehlt; mehrere Epics laufen nacheinander, je mit eigenem Ja (`SKILL.md`, Step 3). Im Expert Service fragst du nach den Kennungen |
| „Section-Tickets für ‹Seitentyp›“ | die Datei des Seitentyps und ihr Epic |

**Ob das Vorhaben ein Expert Service ist, liest du aus `project_type`** (§303); ist das Feld leer,
fragst du einmal und nennst `project-setup` im Bericht. Daran hängen das Epic
([ref-epic-cut.md](ref-epic-cut.md)) und die Vorschau.

## Welche Anforderungen ein Ticket bekommen

**Jede genannte mit `status` `open` oder `confirmed`, unabhängig von `scope`** (§284). `rejected` und
`duplicate` bekommen keines und keine Rückfrage; der Bericht nennt ihre Zahl. Die Spalte des Boards
folgt `scope`: `out_of_scope` in die Wunschliste (Rolle `card_wishlist`), leer und `in_scope` in den
Eingang (Rolle `card_intake`), nach der Connector-Datei. **Ohne Lösungsansatz bekommt eine Anforderung kein
Ticket** (§275), außer sie steht in einem Epic der Domäne `design` (§297,
[ref-trades.md](ref-trades.md), Anforderungen im Design-Epic).

**Im Projekt braucht eine Anforderung ihr Epic**: ist `epic` leer oder gibt es `epics/EP-NNN.md`
nicht, bekommt sie kein Ticket, und die Vorschau nennt `epic-structure`. Im Expert Service gibt es
keine Epic-Dateien; das Epic kommt vom Board.

## Was du dazu liest

| Zweck | Weg |
|---|---|
| Größe und Annahme der Seitentypen, mehr Sections als angenommen | `python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/check-repo.py . --check page_type --check sections`; je Zeile der Befund für die Vorschau ([ref-trades.md](ref-trades.md), Seitentypen und Sections) |
| offene Fragen | `grep -l '^status: open$' gaps/*.md`, davon die, deren `concerns` eine Anforderung des Umfangs oder ihr Epic nennt; eine mit `blocking: yes` steht in der Vorschau bei ihrer Anforderung |
| die Stufe je Epic | `epics/critical-path.md`, Abschnitt `Zeile im Epic-Ticket` ([ref-ticket-templates.md](ref-ticket-templates.md), Die Reihenfolge) |
| der Shop | das Feld `shops` der Anforderung nennt die Shops (§307); ist es leer, gilt der eine Shop aus `shops` in `project.yml`, bei mehreren fragst du |
| die Freigabe | `python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/scope-snapshot.py latest . --released`; Exit 3 heißt: kein Epic ist freigegeben. Sonst ist freigegeben, was im Manifest des genannten Ordners unter `epics` steht und nicht `source: none` trägt (unten) |
| die Epic Page | trägt die Epic-Datei `epic_page`, liest du die Seite mit `getConfluenceContent`, `content_format: html`, `detail: full` (unten) |

## Die Epic Page

**Mit dem Add-on `solutioning` bekommt ein freigegebenes Epic Tickets erst, wenn es eine Epic Page
hat** (§313): trägt seine Epic-Datei kein `epic_page`, legt der Lauf für dieses Epic nichts an, auch
nicht seine Stories, und die Vorschau nennt es mit `solution-epic-page` als Lauf davor; die übrigen
Epics laufen weiter. Das ist ein Datenstand, keine Pflichtkette (§148). **Ein Epic vor der Freigabe
bekommt Tickets** (§219), etwa für die Wunschliste (§284), ohne Zeile `Epic Page:`.

**Gibt es eine Epic Page, ist sie die Grundlage des Epics** (§219), sonst `requirements/` und
`epics/`. Die Vorschau nennt je Epic die Grundlage mit ihrem Stand: „Epic Page, freigegeben am
‹Datum›“ aus der Zeile `approved_note` unter dem Titel, „Entwurf, nicht freigegeben“, wenn die
Epic-Datei `draft` trägt, sonst „ohne Seite“. **Die Seite ist der freigegebene Stand; was sich danach
ändert, steht im Repo und am Ticket** (§218). Deshalb kommt der Inhalt der Tickets auch dann aus dem
Repo, und jede Stelle, an der die Seite anders steht, ist ein Befund für die Vorschau, mit beiden
Fassungen: eine Anforderung, die auf der Seite fehlt oder dort anders steht, ein Kriterium, ein Lösungsansatz in
`Technical Information`. Der Bericht nennt jeden als mögliche Change Request. Die Stellen heißen hier
mit ihrer englischen Bezeichnung; auf der Seite stehen sie in deren Sprache nach
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, „Die Bezeichnungen“.

## Die Bereitschaft: lassen sich prüfbare Kriterien schreiben? (§192)

**Vor jedem Ticket prüft der Lauf, ob die Kriterien prüfbar sind.** Prüfbar ist ein Kriterium, das
einen Zustand nennt, den jemand am Shop oder im Admin mit ja oder nein feststellen kann. „Funktioniert
gut" ist keines. **Erfunden wird keines**, und der Lauf schreibt keines in die Datei (§280, Regel 3).

**Ist `## Acceptance criteria` leer oder ein Kriterium nicht prüfbar, hält der Lauf nicht an**
(§220): der Block trägt `- offen` bzw. das Kriterium, wie es steht, und die Vorschau nennt es mit
der offenen Frage in `gaps/`, die es klärt. Kennt der Lead die Antwort, ist sie Material (§280,
Regel 6): der Bericht nennt `requirements-update` und danach einen weiteren Lauf dieses Skills, der
das Ticket nachzieht.
