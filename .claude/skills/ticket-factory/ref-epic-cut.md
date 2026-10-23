# Das Epic am Board: wiederfinden, wählen, anlegen, ergänzen

**Im Projekt steht das Epic im Repo**, `epics/EP-NNN.md`, und dieser Schritt findet nur sein Ticket.
**Im Expert Service gibt es keine Epic-Datei**: dieser Schritt entscheidet, in welches Epic am Board
eine Anforderung kommt (§214). Die Suche nach Überschneidungen mit Epics anderer Vorhaben gilt in
beiden. Er ist ein Schritt von `SKILL.md`, kein eigener Skill. Wie die Epics des Ziels gelesen werden
und welcher Zustand „geschlossen" heißt, sagt die Connector-Datei.

## Das eigene Epic

**Ein Epic gehört diesem Vorhaben, wenn die Zeile `Beauftragung:` im Block `Kontext` exakt den `key`
aus `project.yml` trägt** ([ref-ticket-templates.md](ref-ticket-templates.md), „Das Epic-Ticket"). Ein
Board kann mehrere Vorhaben tragen; ein Epic eines anderen ist dessen Abnahmefläche, und eine
Anforderung dieses Vorhabens kommt nicht hinein. **Ein Epic mit anderer oder ohne Zeile
`Beauftragung:`**, etwa von Hand angelegt, zählt nie als eigenes: passt es, nennt die Vorschau es als
mögliche Überschneidung mit Titel und Adresse, und der Lead klärt sie.

## Im Projekt: das Ticket des Epics

| Befund | Folge |
|---|---|
| `board_key` in `epics/EP-NNN.md` ist gesetzt, und das Ticket steht | dieses Epic-Ticket; du liest es vor jeder Änderung (`SKILL.md`, Step 5) |
| `board_key` ist gesetzt, das Ticket fehlt am Board | **halte an** für dieses Epic und nenne Schlüssel und Ziel: ein zweites Epic-Ticket entsteht nicht ohne den Lead |
| `board_key` ist leer, ein eigenes Epic trägt `Schlüssel: EP-NNN` | dieses Epic-Ticket, wiedergefunden; sein Schlüssel kommt nach dem Ja in `board_key` |
| `board_key` ist leer, zwei eigene tragen den Schlüssel | **halte an** und nenne beide mit Adresse |
| `board_key` ist leer, kein eigenes trägt ihn | ein neues Epic-Ticket |
| das Epic-Ticket ist geschlossen | eine neue Story kommt nur mit dem Ja des Leads hinein; sonst entsteht für diese Anforderung keine, und der Bericht nennt sie |

## Im Expert Service: welches Epic eine Anforderung nimmt

**Eine Anforderung kommt in das passende Epic, solange es offen ist; ist es geschlossen, entsteht ein
neues** (§214). Ein geschlossenes Epic ist abgenommen und wird nicht wieder geöffnet. **Je Lauf suchst
du das offene Epic auf dem Board**, unter den eigenen.

**Passend ist ein Epic, dessen Ziel die Anforderung trägt**: sie bedient dasselbe Wollen, denselben
Ablauf oder dieselbe Seite des Shops, und ihre Abnahme gehört zu seiner. Gelesen werden der Titel, der
Block `Ziel` und die Zeile `Beauftragung:` des Epics. Trägt keins, entsteht ein neues Epic mit einem
Titel nach dem Thema, nicht nach der einzelnen Anfrage.

| Befund | Vorschlag in der Vorschau |
|---|---|
| genau ein offenes Epic dieses Vorhabens passt | dieses Epic, mit Titel und Adresse |
| mehrere offene passen | das mit dem engsten Ziel zuerst, die übrigen als Wahl |
| das passende ist geschlossen | ein neues Epic; das geschlossene steht mit Adresse daneben |
| keins dieses Vorhabens passt | ein neues Epic |
| ein Epic mit anderer oder ohne Zeile `Beauftragung:` passt | der Vorschlag nach den Zeilen darüber, dazu dieses Epic als mögliche Überschneidung mit Adresse |

**Die Wahl trifft der Lead in der Vorschau** (§213): er nimmt den Vorschlag, wählt ein anderes Epic
oder ein neues. Im Expert Service schreibt der Lauf keinen Schlüssel ins Repo; das Epic findet der
nächste Lauf wieder an seiner Zeile `Beauftragung:`.

## Kandidaten und Überschneidungen

**Belegt ist ein Ticket nur durch seine Zeilen `Schlüssel:` und `Beauftragung:`**, beide exakt
verglichen: die Kennung zählt je Repo, und auf einem Board mit einem zweiten Vorhaben steht dieselbe
`EP-…` oder `REQ-…` mehrmals (Probe 0.5, 10.10.2026). Daneben suchst du:

- **Kandidat:** ein Ticket mit gleichem Titel, aber ohne Zeile `Schlüssel:`; oder im gewählten Epic
  eine Story ohne Schlüssel dieses Vorhabens, die dasselbe Wollen am selben Ort trägt. Verglichen
  werden Titel ohne Kennung und ohne Shop-Bezug (`(B2B)`, §307) und Block
  `User Story` mit `title` der Anforderung und der User Story, die dieser Lauf für sie schreibt.
- **Überschneidung:** ein Epic mit anderer oder ohne Zeile `Beauftragung:` am selben Board, das zu
  einem Epic dieses Laufs passt, oder dessen Stories eine Anforderung dieses Laufs tragen; eine Story
  oder ein Subtask mit dem Schlüssel dieses Laufs unter anderer `Beauftragung:` gehört dem anderen
  Vorhaben und ist nie das eigene Ticket. Ein Board
  eines anderen Kanals wird nicht gelesen.

**Jeden Kandidaten und jede Überschneidung legst du vor, bevor du Fragen stellst** (`SKILL.md`,
Step 6), damit der Lead nichts zu einer Anforderung beantwortet, die dann kein Ticket bekommt:

| Antwort | Folge |
|---|---|
| „dieselbe" | keine Story, keine Frage, kein Body; das Ticket steht als wiedergefunden in Vorschau und Bericht |
| „ist eine andere Anforderung" | die Anforderung läuft weiter wie ohne Treffer |
| „gleiches Wollen, anderes Vorhaben" (nur bei einem Treffer unter anderer `Beauftragung:`) | keine Story in diesem Lauf; Vorschau und Bericht nennen das Ticket des anderen Vorhabens mit Adresse als Träger und dass die Abnahme dort liegt. Ob die Arbeit diesem Vorhaben gehören soll, klären die Leads beider; der Lauf verschiebt kein Ticket |

Ohne Antwort gilt bei einem Kandidaten „dieselbe"; eine Überschneidung ohne Antwort sperrt nichts. Der
Lead kann eine überschneidende Anforderung außerdem zurückstellen; sie bekommt dann in diesem Lauf
kein Ticket.

## Ein stehendes Epic-Ticket ergänzen

**Ein weiterer Lauf ergänzt nur**, weil er bestehende Tickets vor jeder Änderung liest (§280,
Regel 7). Kommt eine Anforderung in ein stehendes Epic, hängt ihre Story an ihm, und der Block
`Anforderungen` des Epic-Tickets bekommt ihre Zeile `REQ-NNN ‹Titel› ‹Shop-Bezug›` am Ende; alles andere im Body
bleibt Zeichen für Zeichen. Jede Stelle, an der das gelesene Ticket anders steht als der Body, den
dieser Lauf aus dem Repo baut, legst du als Abweichung vor (`SKILL.md`, Step 5).

## Ein neues Epic-Ticket

Es trägt die Blöcke aus [ref-ticket-templates.md](ref-ticket-templates.md): im Projekt aus der
Epic-Datei, mit `Schlüssel: EP-NNN`; im Expert Service `Ziel` aus dem Wollen der Anforderungen und
`Lösungsansatz` aus ihren Lösungsansätzen, ohne Epic-ID und ohne Zeile `Schlüssel` (§220). Im `Kontext` steht
immer die Zeile `Beauftragung:` mit dem `key` aus `project.yml`.
