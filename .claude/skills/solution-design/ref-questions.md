# Fragen und Blocker: in `gaps/`

Ein fester Satz oder Status, der von hier in den Entwurf geht, etwa „Lösungsansatz offen; die Frage steht
im Sheet." oder `Zur Abnahme`, steht dort in der Sprache des Entwurfs, nach
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, Die Bezeichnungen (§255).

**Eine offene Frage zur Lösung ist eine Datei in `gaps/`** (§279), nie ein Satz im Entwurf (§218).
Die Form setzt der Datalayer-Vertrag `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt `gaps/GAP-NNN.md` mit „Eine Frage anlegen“: die Kennung von der höchsten in
`gaps/` weiter, `kind: solutioning` für eine Frage zur Lösung, `kind: decision` für eine Wahl beim
Kunden oder eine Architekturfrage, `to` der Adressat nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`, 1, `concerns` jede betroffene Anforderung und, wo es
passt, das Epic, `blocking` nach unten, `opened` das Datum des Laufs. Der erste Satz des Rumpfs ist die
Frage selbst; ihn zeigt das Sheet. **Geschlossen wird eine Frage nur über `requirements-update`**, aus
Material (§276); dieser Lauf schließt keine.

**Vor jeder neuen Frage suchst du**, ob eine Datei in `inputs/` oder `notes/`, eine ADR, eine
geschlossene Frage oder ein Kommentar am Entwurf sie schon beantwortet ([ref-sources.md](ref-sources.md)).
Steht dieselbe Frage schon offen da, legst du sie nicht noch einmal an; betrifft sie eine weitere
Anforderung, wächst ihr `concerns`.

**Nur Fragen, die bis zur Umsetzung zählen** (Umbauplan, Baustein `solution-design`): eine Frage
entsteht, wenn ihre Antwort den Lösungsansatz, die Größe, den Scope oder ein Kriterium ändert. Was erst die
Umsetzung klärt und nichts davon ändert, ist keine Frage in `gaps/`; es steht als Satz „in der
Umsetzung zu klären“ in `## Details` der Anforderung.

## Architekturfragen

Eine Frage, deren Antwort andere Epics bindet (Bauform, ein Store oder mehrere, Integrationsschicht,
ein Master für Daten), ist eine **Architekturfrage** (§216): `kind: decision`, ihr Rumpf beginnt mit
`Architektur:`, `concerns` nennt die Anforderung, die sie treibt, und die zugehörige Zeile in
`architecture.md` ist `offen` mit dieser Anforderung und der Kennung der Frage in `Quelle/ADR`.
Andere Anforderungen, die an ihr hängen, tragen die treibende Anforderung in `depends_on`
(§216), nie die Kennung der Frage: `depends_on` kennt nur Anforderungen, Epics und ADRs. Steht die
Architekturfrage schon offen da, legst du sie nicht neu an.

## Blockierend oder nicht

**Blockierend** heißt: ohne die Antwort ist kein Lösungsansatz für die Anforderung zu bestimmen. Dann trägt die
Frage `blocking: yes`, die Anforderung bekommt keinen Lösungsansatz und `solution_status: blocked` (so legt es
der Datalayer-Vertrag fest: der Lösungsansatz hängt an einer offenen Frage mit `blocking: yes`), und im Entwurf
steht `way_open` („Lösungsansatz offen; die Frage steht im Sheet."). **Nicht blockierend**
heißt: der Lösungsansatz steht, die Antwort schärft ihn. Dann trägt die Anforderung ihren Lösungsansatz.

## Die Frage des Lösungsansatzes

Der Lauf stellt dem Lead je Anforderung oder Teilthema die Frage des Lösungsansatzes, mit den Lösungsansätzen
und der Empfehlung, im Block mit den übrigen (Step 9 der SKILL.md):

| Antwort | Folge |
|---|---|
| **ein Lösungsansatz** | die Wahl ([ref-adr.md](ref-adr.md)) |
| **„Offene Frage"** (`en` „Open question") | eine Frage `kind: decision`; an wen sie geht, steht in `to`: der Kunde (`to_customer`, bei `en` `Customer`), eine Agentur oder ein anderer Dienstleister, wie das Material ihn nennt, Rumpf „Welcher Lösungsansatz für ‹Gegenstand›? ‹Lösungsansätze›, Empfehlung ‹Lösungsansatz›“ (`question_way`, bei `en` „Which approach for ‹subject›? ‹options›, recommendation ‹option›“), in der Sprache aus `language` nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“ (§337); im Entwurf bleiben Lösungsansätze und Empfehlung (W16), `solution_status` bleibt `proposed` |
| **„Entscheidung offen, entscheidet ‹Gewerk›"** | im Entwurf dieser Satz und die Lösungsansätze (§212); `solution_status` bleibt `proposed`, die Anforderung zählt für `status_for_approval` als erledigt |

**Eine Frage der Freigabe stellt dieser Lauf nicht** (§277): „Ich gebe frei“ im selben Lauf entfällt,
geprüft wird von Hand mit `Geprüft von` und `Geprüft am`, und freigegeben ist ein Epic mit der
Freigabe des Scopes (ref-draft.md, Die Zustände). Solange eine Anforderung „Offene Frage" trägt,
setzt dieser Lauf `status_for_approval` nicht.

## Ein Blocker

**Ein Blocker ist eine Anforderung, für die sich kein Lösungsansatz findet**, obwohl alle Auskünfte vorliegen.
Fehlt eine Auskunft, ist es eine Frage, kein Blocker. Am Blocker gilt:

- **Datei:** `solution_status: blocked`, wie bei jeder blockierenden Frage; `depends_on` nennt die Anforderung oder ADR, mit der zusammen
  keiner geht, oder die eigene Kennung, wenn es schon für sie allein keinen gibt.
- **Frage:** eine Frage mit `blocking: yes`, an einen Adressaten, mit einer Empfehlung, den versuchten
  Lösungsansätzen je mit dem Grund ihres Scheiterns und diesen Optionen, nur denen, die es gibt:
  - **A ausklammern:** die Anforderung geht auf `rejected` oder `out_of_scope`, über
    `requirements-update` aus Material. Diese Option steht immer da.
  - **B die Randbedingung ändern:** benannt, welche: die ADR oder Architekturzeile aus `depends_on`, die
    andere Anforderung und was an ihr nachgäbe, oder das Ziel, enger gefasst. Folge: ADR und neuer
    Versuch.
  - **C einen verworfenen Lösungsansatz zulassen:** mit dem, was ihn verwerfen ließ. Nur, wenn es einen gibt.
- **Entwurf:** die Zeile trägt `way_open` („Lösungsansatz offen; die Frage steht im Sheet.").

**Ein Epic hat keinen Blocker-Status.** Welche Epics Blocker tragen, zeigt ein Filter im Sheet.

## Auflösen im nächsten Lauf

Eine Antwort gilt nur, wenn sie vorliegt: als `## Answer` einer Frage, die `requirements-update`
geschlossen hat, oder vom Lead im Dialog, wo die Frage ihm selbst gilt (die Wahl, das Vorgehen).
**Eine Antwort des Kunden in einem Kommentar am Entwurf** schreibst du in die Notiz der Kommentare;
die Frage schließt `requirements-update`, und erst danach gilt die Antwort.

| Antwort | Folge |
|---|---|
| auf eine blockierende Frage | die Anforderung bekommt Lösungsansätze zur Wahl oder ihren gewählten |
| **A** | du klammerst nicht aus; die Anforderung geht über `requirements-update` auf `rejected` oder `out_of_scope` und steht danach im Entwurf unter `Discarded` |
| **B** | eine ADR mit der Antwort, mit `supersedes`, wenn sie eine ADR aus `depends_on` ablöst, dann ein neuer Versuch in diesem Lauf. Trägt er, wie bei einer Wahl; trägt er nicht, bleibt der Blocker, und der Versuch kommt in einer neuen Frage zu den versuchten Lösungsansätzen |
| **C** | der zugelassene Lösungsansatz wird gewählt, mit ADR |

## Ein Ziel hat sich geändert

Zu Beginn jedes Laufs nennst du jede Anforderung mit `solution_status: blocked` oder einer offenen
blockierenden Frage, deren Ziel sich geändert hat, und bietest eine neue Prüfung an:

| Ziel | geändert heißt |
|---|---|
| eine blockierende Frage | sie ist geschlossen |
| eine Anforderung | sie steht auf `rejected`, `duplicate` oder `out_of_scope`, oder ihr `solution_status` ist `decided` |
| eine ADR | sie steht auf `superseded`, oder eine andere ADR nennt sie in `supersedes` |
| eine Zeile in `architecture.md` | sie ist ersetzt, oder ihr Status ist nicht mehr `offen` |

Eine Anforderung mit geändertem Ziel in einem anderen Epic nennst du mit ihrem Epic; geprüft wird sie
im Lauf für dieses Epic.
