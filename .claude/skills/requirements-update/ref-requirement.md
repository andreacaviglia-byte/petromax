# Die Anforderung in `requirements/`, und die Notiz zum Abgleich

Das Verdikt über den Kandidaten steht im Skill an Step 6. Hier steht, wie die Datei dasteht. Die Form,
die Felder und ihre Werte setzt der Datalayer-Vertrag,
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt `requirements/REQ-NNN.md`; die
Anzeige im Sheet entsteht daraus in der Projektion.

**Eine feste Wendung schreibst du in der Sprache aus `language` in `project.yml`** (§337), nach dem
Abschnitt „Die festen Wendungen“ desselben Vertrags; der Schlüssel steht hier in Klammern, die
Beispiele zeigen `de`.

## Die neue Datei

`requirements/REQ-NNN.md`, die Kennung fortgezählt von der höchsten in `requirements/` (§230). **Dieser Lauf schreibt das Was** (§280, Regel 3):

| Feld oder Abschnitt | Was dieser Lauf schreibt |
|---|---|
| `id` | die Kennung, gleich dem Dateinamen |
| `title` | der Bedarf in wenigen Worten, in der Sprache aus `language` (§337), auch wenn das Material eine andere spricht; die wörtliche Formulierung bleibt im Material in `inputs/` und `notes/`. Ohne Schlüssel eines Shops (§307) |
| `shops` | die `key` aus `shops` in `project.yml`, für die sie gilt, `shops: [b2b]`; leer, `shops: []`, wenn sie für alle Shops gilt (§307). Angezeigt wird der Bezug hinten am Titel, `Staffelpreise (B2B)` |
| `status` | `open`; `confirmed` nur, wenn der Kunde sie ausdrücklich bestätigt, mit Quelle beim Kunden (§283) |
| `duplicate_of` | `""`, außer bei `duplicate` |
| `priority` | `must-have` als Vorgabe; `nice-to-have` nur, wenn der Kunde es ausdrücklich sagt, und `source` nennt die Stelle (§327). Geraten wird nie |
| `scope` | `""` bis zur Scope-Freigabe (unten) |
| `design_needed`, `interface_needed` | `yes` oder `no`, wenn das Material es sagt; sonst `open`. `interface_needed` heißt: die Lösung braucht eine Schnittstelle, auch für Stammdaten aus PIM oder ERP (§205) |
| `live` | `yes`, `no`, `partial` oder `verify` aus dem Ist-Zustand; `""`, wenn er „ungeprüft“ (`current_unchecked`) ist |
| `source` | „Workshop ‹Titel› vom ‹Datum›" (`source_workshop`, `en`: „Workshop ‹title› on ‹date›") für einen Termin, „Chat mit dem Lead vom ‹Datum›" (`source_chat`), die Zeile aus `architecture.md` oder der Dateiname der Notiz; bei einer Teilung dazu „; aufgeteilt aus REQ-NNN“ (`source_split`, `en`: „; split from REQ-NNN“) |
| `epic`, `size`, `classification`, `depends_on`, `solution_status`, `design_reference` | `""` oder `[]`; sie führen andere Läufe. `own_sections` nur bei einem Seitentyp (unten) |
| `standard` | nur bei einer Standard-Anforderung eines Add-ons, nach [ref-baseline-rows.md](ref-baseline-rows.md) (§303); sonst `""` |
| `## Description` | der Soll-Zustand, was gelten soll, nicht womit; ein bis drei Sätze, der erste Absatz steht im Sheet |
| `## Acceptance criteria` | ein prüfbares Kriterium je Listenpunkt, an dem die Story abgenommen wird (§281), nur aus dem Material; fehlt das Verhalten dafür, bleibt der Abschnitt leer, und es entsteht eine Frage (unten, UC). Eine Standard-Anforderung trägt das Kriterium aus [ref-baseline-rows.md](ref-baseline-rows.md) |
| `## Current state` | der Ist-Zustand, ein bis drei Sätze; **Pflicht**, und „ungeprüft“ (`current_unchecked`, `en`: „unchecked“), wenn das Material ihn nicht nennt; eine Standard-Anforderung trägt den festen Satz aus [ref-baseline-rows.md](ref-baseline-rows.md) und `live: no` |

`## Approach`, `## Details` und `## Sections` legst du nicht an; die ersten beiden schreiben
`solution-approach` und `solution-design`, `## Sections` dieser Lauf erst mit einer Übergabe des
Designs (unten). **Eine User Story schreibst du nicht** (§323): sie ist eine Ableitung aus Ist, Soll,
FC und UC und entsteht im Entwurf oder im Ticket, nach `${CLAUDE_SKILL_DIR}/../../docs/user-story-contract.md`.
**Keine Zitate mit Sprecher, keine Repo-Adresse, nichts Internes in Titel und
Text** (§278): der Kunde liest das Sheet mit.

```markdown
---
id: REQ-043
title: Versandkosten je Markt
shops: []
status: open
duplicate_of: ""
priority: must-have
scope: ""
epic: ""
design_needed: open
interface_needed: yes
live: partial
source: Workshop Märkte vom 18.08.2026
size: ""
classification: []
depends_on: []
solution_status: ""
own_sections: ""
design_reference: ""
standard: ""
---

## Description

Versandkosten richten sich nach dem Markt der Bestellung, die Sätze kommen aus dem ERP.

## Acceptance criteria

- Im Warenkorb stehen die Versandkosten des gewählten Marktes.

## Current state

Der Shop kennt einen Versandsatz für Deutschland und Österreich.
```

## `status` und `scope`

**`status` sagt, ob eine Anforderung gilt; `scope`, ob sie in diesem Vorhaben gebaut wird** (§283).
Beide setzt dieser Lauf aus dem Material, nie aus einem Eintrag im Sheet.

| Das Material sagt | Folge |
|---|---|
| eine neue Anforderung | `status: open` |
| der Kunde bestätigt sie ausdrücklich | `status: confirmed`, und `source` wächst um die Quelle beim Kunden, als feste Wendung `source_confirmed` |
| der Kunde will sie nicht mehr, oder sie ist nicht gültig | `status: rejected`, dazu eine ADR nach [ref-adr.md](ref-adr.md) |
| dasselbe Wollen wie eine andere | `status: duplicate` an der jüngeren, `duplicate_of` = die Kennung, die gilt; gelöscht wird nichts |
| die Scope-Freigabe des Kunden, im Expert Service die Ansage des Leads | je genannte Anforderung `scope: in_scope` oder `out_of_scope` |
| eine Anforderung wird weiter gewünscht, aber nicht in diesem Scope | `scope: out_of_scope`, dazu eine ADR nach [ref-adr.md](ref-adr.md) |
| sie kommt zurück | `status: open` oder `confirmed`, `scope` wie das Material sagt, und die ADR löst die frühere ab |

**Die Scope-Freigabe ist Material**: das Protokoll des Termins, die Mail des Kunden, im Expert
Service die Ansage des Leads im Chat. Sie nennt, was in den Scope kommt und was nicht; eine
Anforderung, die sie nicht nennt, behält ihr `scope`, und der Bericht zählt sie.

**`priority` sagt, ob der Kunde die Anforderung braucht** (§327): `must-have` ist die Vorgabe jeder
neuen Anforderung. **`nice-to-have` nur, wenn der Kunde es ausdrücklich sagt** („wäre schön“, „kann
später“), mit der Stelle in `source`; Schweigen ist kein Nice-to-have, und geraten wird nie. **Zurück
auf `must-have` geht es nur über Material**, wie jede Änderung am Was. Priorität und Scope sind zwei
Dinge: eine Anforderung kann Must-have sein und doch Out of Scope; das meldet `solution-review`.

## Eine Datei, ein Wollen

**Zwei Dateien für dasselbe Wollen sind ein Duplikat**, auch wenn zwei Termine es verschieden sagen:
die zweite Nennung ergänzt die erste (Verdikt „gehört zu"). **Ein Wollen, das zwei Dinge verlangt, die
getrennt gelöst werden, sind zwei Anforderungen.** Die Probe: kann das eine ohne das andere fertig
sein?

## Die Anforderung trägt den Bedarf, nicht das Werkzeug

`title` ist die teuerste Stelle für einen stillen Beschluss: er steht im Schnitt, im Entwurf und am
Ticket, und er wird gelesen, wo Beschreibung und Ist-Zustand es nicht werden.
„E-Mail-Marketing-Werkzeug anbinden", nicht der Produktname, solange die Wahl aussteht; genannte
Kandidaten stehen mit ihrer Quelle in `## Current state`. **Legt das Material das Werkzeug fest**,
weil der Kunde es einsetzt und behalten will oder eine Entscheidung gefallen ist, steht sein Name
darin. Ein Systemname steht immer in der Schreibweise der Systemlandschaft
(`${CLAUDE_SKILL_DIR}/../../docs/system-landscape-contract.md`).

**Eine ausstehende Werkzeugwahl ist keine Frage dieses Laufs.** Sonst hielte er das Solutioning mit
einer Frage auf, deren Beantwortung das Solutioning ist.

## IST, SOLL, FC und UC

**Jede Anforderung durchläuft IST, SOLL, FC und UC** (§254), die Methodik des Hauses. Du prüfst sie an
jeder neuen und jeder geänderten Datei:

| | Wo | Was du prüfst |
|---|---|---|
| IST | `## Current state`, `live` | wie es heute ist; sagt das Material nichts, steht „ungeprüft" (`current_unchecked`) da, und es entsteht eine Frage an den Kunden: „Wie ist das heute im Shop gelöst?" (`question_current_state`, `en`: „How is this solved in the shop today?"), nicht blockierend |
| SOLL | `## Description` | was gelten soll, nicht womit |
| FC | die Datei selbst | **eine Anforderung trägt genau eine Fähigkeit**, lösungsneutral. Beschreibt das Material mehrere, etwa „Bestände und Bestellungen mit der Warenwirtschaft austauschen", werden es mehrere, je Datenstrom, je Seitentyp, je Prozess |
| UC | `## Acceptance criteria` und die Fragen | das Verhalten, an dem ein Kriterium prüfbar wird: Auslöser, Daten, Ergebnis. Fehlt es so, dass kein Kriterium prüfbar formuliert werden kann, entsteht eine Frage, die das Kriterium nennt |

**Ohne IST ist später nicht entscheidbar, ob etwas geändert oder neu gebaut wird**, und was heute
läuft, verschwindet sonst still. Der Ist-Zustand ist der Stand, den das Material beschreibt, nicht der
eines laufenden Systems am Lesetag: „X wurde umgesetzt" ist das Ergebnis einer späteren Phase.

Nennt eine Quelle ein Werkzeug, steht es als Angabe der Quelle da („der Kunde setzt heute X ein" im
Ist-Zustand, „X wurde vorgeschlagen" in der Beschreibung), nie als Festlegung. Kein Lösungsansatz.
**`design_needed` und `interface_needed`** gehören ab der Wahl `solution-design`: an einer bestehenden
Datei änderst du sie nur, solange sie `open` tragen.

## Korrektur und Ergänzung

Nimmt der Kunde eine Aussage zurück oder ändert sie, **änderst du die bestehende Datei**, nur was das
Material widerlegt: `title`, `## Description`, `## Acceptance criteria`,
`## Current state`, `live`. `source` wächst um „; korrigiert: ‹neue Quelle›" oder „; ergänzt: ‹neue
Quelle›" (`source_corrected`, `source_added`; `en`: „; corrected:“, „; added:“), und die Notiz zum Abgleich nennt alten und neuen Stand. Eine zweite Datei entsteht nicht, und
die Kennung bleibt. Den alten Stand hält Git.

**Trägt eine bestehende Anforderung mehrere Fähigkeiten**, wird sie geteilt (§254): sie behält die
erste, `title` und `## Description` werden enger, und jede weitere wird eine neue Datei mit
„‹Quelle der alten›; aufgeteilt aus ‹Kennung›" (`source_split`, `en`: „; split from ‹Kennung›") in `source`. Steht die alte in einem Epic, nennt der Bericht
`epic-structure` für die neuen. Wird eine Anforderung ganz zurückgenommen, geht sie auf `rejected`;
gelöscht wird sie nie, und eine Kennung wird nie umgewidmet.

**Trägt die Anforderung schon einen entschiedenen Lösungsansatz** (`solution_status: decided`) oder hängt sie an
einem Epic mit `board_key`, markierst du die Änderung im Block: sie gilt im Entwurf und am Ticket erst,
wenn `solution-design` und `ticket-factory` sie nachziehen (§220). **Ändert der Lauf das Was**
(`title`, `## Description`, `## Acceptance criteria`) **einer Anforderung, deren Epic
einen Entwurf hat** (`draft` im Kopf von `epics/EP-NNN.md` gesetzt), nennt der Bericht `solution-design`
für dieses Epic als nächsten Lauf: bis dahin trägt der Entwurf den alten Stand.

## Seitentypen, Theme und Sections

**Die Theme-Entscheidung kommt als Material** (§285): steht das Theme fest oder gibt der Lead es frei,
ist das eine Zeile `Bauform der Storefront: Theme` in `architecture.md`
([ref-architecture.md](ref-architecture.md)), bevor `solution-design` Lösungsansätze wählt.

**Die Seitentypen sind Anforderungen**, je Seitentyp, den wir gestalten, eine Datei (Startseite,
Kollektionsseite, Produktseite, Warenkorb, Blog, Inhaltsseite …), aus dem Ergebnis der UX/UI-Session
mit `design_needed` je Anforderung. Die erste ist „Design-System und globale Sections“, ohne das Add-on
`design` „Theme-Einstellungen und globale Sections“; bei `en` „Design system and global sections“
bzw. „Theme settings and global sections“ (§337). Ins Theme-Epic hängt sie `epic-structure`; ein
Inventar der Sections gibt es vor der Freigabe nicht.

**`own_sections`**, die Annahme, wie viele eigene Sections ein Seitentyp höchstens bekommt, setzt mit
Solutioning `solution-design`. **Ohne das Add-on `solutioning`** setzt sie dieser Lauf aus dem
unterschriebenen Angebot, als Zahl mit dem Angebot in `source`.
Sagt das Angebot nichts zum Umfang der Theme-Arbeit, wird das eine Frage mit `blocking: yes` an den
Lead ([ref-questions.md](ref-questions.md)).

**Die Übergabe eines abgenommenen Seitentyps ist Material**, gleich ob Liste, Figma oder ein Design
des Kunden. Du schreibst in die Datei des Seitentyps den Abschnitt `## Sections`, je angepasste oder
neue Section ein Listenpunkt mit ihrem Namen und dem Link auf ihren Frame (mit `node-id`), und
`design_reference` auf das Design des Seitentyps, wenn es leer ist:

```markdown
## Sections

- Produktgalerie mit Zoom: https://www.figma.com/design/‹Datei›?node-id=12-345
- Bewertungen: https://www.figma.com/design/‹Datei›?node-id=12-401
```

Dann zählst du sie gegen `own_sections`. **Sind es mehr, ist das eine Änderung des Scopes**: eine
Frage mit `blocking: yes` an Lead und Kunden, die beide Zahlen nennt; `check-repo.py` meldet
`sections`, bis die Annahme oder die Liste aus neuem Material stimmt. Danach legt `ticket-factory`
die Section-Subtasks an; der Bericht nennt ihn.

## Interna

**Eine Anforderung aus einer internen Quelle ist Material wie jede andere** (§278): eine Quelle mit
`Intern: ja` im Kopf ihrer Datei in `inputs/`, oder eine Stelle unter `## Intern` ihrer Notiz. Was in
die Anforderung kommt, ist nur die sachliche Fähigkeit, die der Kunde kennt oder kennen darf; Titel,
Beschreibung, Kriterien und Ist-Zustand tragen nichts aus der Liste in `way-of-working.md`, Abschnitt
„Interna“, auch nicht sinngemäß. `source` nennt dann nicht den internen Termin, sondern „Chat mit dem
Lead vom ‹Datum›“ (`source_chat`) oder die Notiz zum Abgleich; die Herkunft hält die Notiz. Eine Frage, die nur
eine interne Quelle aufwirft, geht an den Lead, nicht an den Kunden.

## Den Datalayer schreiben

| Was | Weg |
|---|---|
| neue Anforderung, Frage, Notiz zum Abgleich, Notiz aus dem Chat, ADR | leg die Datei an, mit dem ganzen Text; steht sie schon, schreibst du nicht und nennst es |
| bestehende Anforderung oder Frage | lies sie direkt davor, ändere nur die Felder und Abschnitte aus dem Block, schreib die ganze Datei; was dieser Lauf nicht berührt, bleibt Zeichen für Zeichen |
| `architecture.md` fortschreiben | nach [ref-architecture.md](ref-architecture.md) |
| ADR ablösen | in der alten ADR änderst du nur die Zeile `status:` |
| Wegweiser in einer Notiz | über die erste Zeile der Notiz kommt genau eine Zeile Wegweiser; der alte Text folgt Zeichen für Zeichen |

Jede Datei liest du zurück; erst zurückgelesen und gleich heißt geschrieben.

## Die Notiz zum Abgleich

Name: der Name der Quelle mit `-abgleich` vor der Endung (`2026-09-12-workshop-checkout-abgleich.md`),
bei einer Eingabe im Chat der Name ihrer Notiz (`<JJJJ-MM-TT>-chat-<thema>-abgleich.md`), beim
Standard-Leistungssatz `<JJJJ-MM-TT>-standard-<kennung>-abgleich.md`.

```
# Abgleich ‹Titel der Quelle›

Quelle: ‹Dateiname in inputs/ oder Beschreibung›
Abgeglichen: ‹TT.MM.JJJJ›

## Neu
REQ-043 bis REQ-051

## Geändert
- REQ-012 `Description`: ‹was vorher galt› → ‹was jetzt gilt›
- REQ-019 `status`: open → confirmed

## Fragen
- neu: GAP-014 (blockiert, REQ-044), GAP-015 (REQ-047)
- geschlossen: GAP-009 (REQ-019)

## Entscheidungen und Architektur
- ADR-008 ‹Titel›
- architecture.md: ‹neue oder geänderte Zeile›
- Architekturfrage für den Schnitt: ‹Frage›, treibende Anforderung REQ-…

## Nicht aufgenommen
- ‹Kandidat›: ‹Grund›

## Bekannte Fälle
- REQ-045: ‹Fall aus index.md der Wissensbasis›
```

Ein leerer Abschnitt entfällt. Die Notiz wird nie überschrieben; ist sie falsch, bekommt sie einen
Wegweiser, und eine neue trägt die Korrektur. War die Quelle intern (`Intern: ja` im Kopf ihrer Datei
in `inputs/`), trägt auch die Notiz zum Abgleich diese Zeile.
