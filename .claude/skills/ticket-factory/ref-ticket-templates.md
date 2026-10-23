# Was ein Ticket trägt: Epic-Ticket, Story und Subtask

**Epic → Story → Subtask** (§281). Je Epic ein Epic-Ticket, je Anforderung eine Story, die User Story
und die Akzeptanzkriterien trägt, an denen sie abgenommen wird. **Ein Gewerk:** die Story trägt
Komponente bzw. `Kategorie` und die Angaben, keine Subtasks. **Mehrere Gewerke:** die Story trägt
keine Komponente, darunter je Arbeitseinheit eines Gewerks ein Subtask; im Theme-Epic ist die
Arbeitseinheit die Section. Welcher Fall gilt, sagt [ref-trades.md](ref-trades.md). Stunden setzt der
Lauf an kein Ticket, Verknüpfungen setzt er nicht, kein Label, keinen Kommentar. Die Reihenfolge des
Bauens steht als eine Zeile im Epic-Ticket (Die Reihenfolge, unten) und gilt als Empfehlung (§267).

| Ebene | Was sie ist | Woraus | Stufe des Prüfers |
|---|---|---|---|
| **Epic-Ticket** | Ziel, je Anforderung nur ID und Titel, der übergreifende Lösungsansatz | `epics/EP-NNN.md`; im Expert Service die Anforderungen dieses Laufs | `epic` |
| **Story, ein Gewerk** | eine Anforderung als Auftrag an ein Gewerk | `requirements/REQ-NNN.md`, dazu der Rumpf der Epic-Datei | `story` |
| **Story, mehrere Gewerke** | die Anforderung mit den Kriterien der Abnahme und dem übergreifenden Lösungsansatz | ebenso | `story --split` |
| **Subtask** | eine Arbeitseinheit eines Gewerks mit eigenem Titel und den Kriterien der Umsetzung | die Kriterien seines Gewerks, `## Details`, bei einer Section ihr Eintrag unter `## Sections` | `subtask` |

Die Prüfung macht `scripts/check-ticket-body.py`, aufgerufen nach `SKILL.md`, Step 7. Die Vorlagen
unten tragen Platzhalter in `<…>`; ein gesendeter Body trägt keinen, auch keinen in `‹…›`, und der
Prüfer lehnt ihn sonst mit `Platzhalter` ab. Kein Platzhalter sind die drei Ersatzmarken des
Datalayer-Vertrags: „‹Zugangsdatum entfernt›“, „‹Gesundheitsdaten entfernt›“, „‹Endkundendaten
entfernt›“, bei `en` „‹credential removed›“, „‹health data removed›“, „‹end-customer data removed›“
(`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Die festen Wendungen, §337).

## Die Gewerke

**Das Gewerk steht in der Komponente bzw. `Kategorie`**, an der Story mit einem Gewerk und am Subtask
(§281); im Titel steht es nie. Welches Gewerk eine Klassifizierung trägt, und dass es bei einer
Migration der Domäne des Epics folgt, sagt der Datalayer-Vertrag, Abschnitt „Die Klassifizierung“
(`../../docs/datalayer-contract.md`, §324). Es gibt vier Gewerke, im Text mit den Namen des Glossars:
`DEV`, `Konfig`, `Schnittstelle`, `UX/UI`; heißen sie auf einem Board anders, bildet der
Board-Vertrag sie ab (§220).

| Gewerk | Art | Angaben | Prüfung |
|---|---|---|---|
| `DEV` | Theme | nur, was eine Quelle belegt; nie Bauform, CSS oder Design-Werte | ausführliche Akzeptanzkriterien |
| `DEV` | Custom App | Auslöser, Ressourcen, Scopes, fremde Systeme, Fehlerverhalten, Extension- oder Function-Typ | — |
| `Konfig` | Shopify-nativ, Theme-nativ, Public App | Einstellung, Shop, Wert; Section, Block oder Einstellung im Theme Editor; Name der App | woran man sieht, dass sie greift |
| `Konfig` | Content-Migration (Epic der Domäne `content_migration`) | Quelle, Menge, Lösungsansatz | Stichprobe, Mengenabgleich |
| `Schnittstelle` | Standard-Konnektor, Middleware, Custom Schnittstelle | System, Konnektor oder Middleware mit Namen, Richtung, Felder | ein Datensatz auf beiden Seiten |
| `Schnittstelle` | Datenmigration (Epic der Domäne `data_migration`, gleich über welchen Lösungsansatz) | Quelle, Menge, Lösungsansatz, Felder | Stichprobe, Mengenabgleich |
| `UX/UI` | Design (Figma) | Ansichten, Zustände, Breakpoints, Grundlage | deckt alle Ansichten und Zustände; Frame verlinkt |
| `UX/UI` | Analyse | Gegenstand, Frage, Datenbasis | beantwortet die Frage, mit Empfehlungen |

Die `Angaben` stehen im Block `Angaben für ‹Gewerk›`, je Angabe ein Punkt; was die Quelle nicht
nennt, steht als `- offen` (§220). Die `Prüfung` steht als Kriterium unter `Akzeptanzkriterien`
bzw. `Kriterien der Umsetzung`.

### DEV, Theme

Der Leser baut mit dem Theme-Werkzeug der Umsetzung (`strix-shopify-plugin`, gelesen in v1.4.1). Es
fragt in jedem Bau zuerst nach einer Beschreibung und stellt dann zwingend seine Verhaltensfragen
(„MANDATORY: Use the `AskUserQuestion` tool"): Blöcke, Pflegbarkeit, Responsive-Verhalten,
Datenquellen. Das Ticket liefert die **Antworten**, als ausführliche Kriterien; eine beobachtbare
Antwort ist ein Kriterium. Den Schnitt in Sections und Blöcke macht DEV mit dem Werkzeug; eine
Bauform steht nur, wo die Quelle sie belegt. Abstände, Farben und Typografie zieht das Werkzeug
selbst aus dem Figma-Frame; **gemessene Design-Werte und CSS stehen nie im Ticket.** Den Frame trägt
der Subtask einer Section unter `Links` als `Design-Referenz`; ohne Design fehlt die Zeile (§285).

### DEV, Custom App

Der Leser baut mit dem Custom-App-Werkzeug (`strix-custom-app-plugin`, gelesen am 14.08.2026 an
dreizehn Dateien eines Abzugs). Baut er direkt, fragt es fünf Dinge: den Auslöser (`webhook`,
`schedule`, `http` oder `manual`), die berührten Shopify-Ressourcen, die nötigen Scopes, die fremden
Systeme und das Verhalten bei Fehler und Wiederholung; eine Extension dazu einen von fünf
Extension-Typen, eine Function einen von sieben Function-Typen. Die Angaben tragen, was die Quelle
davon nennt; was sie nicht nennt, wird nicht erfunden. **Kein Ticket trägt ein Arbeitspaket**
(Dateipfade, Prüfbefehle, Pakete setzen das offene App-Repo voraus), und Auth-Modell und Backend gibt
es nicht vor: die setzt die Doktrin des Werkzeugs. Functions, eine Post-Purchase-Extension als Custom
App und Checkout-UI auf Information, Versand und Zahlung hängen an Plus; auf einem Shop ohne Plus
fragt der Lauf den Lead, statt anzulegen.

### Konfig

Der Leser setzt die Einstellung selbst im Admin, ohne Werkzeug, das nachfragt: was das Ticket nicht
sagt, erfährt er nicht. Die Angaben sind konkret: welche Einstellung, an welchem Shop, mit welchem
Wert. Bei einer Public App steht ihr Name und was an ihr einzustellen ist; ihre Bauform gehört dem
Hersteller. **Ein Feed ist keine Schnittstelle**, sondern ein Shopify-nativer Kanal mit Feed-App, und
gehört hierher; ebenso eine Content-Migration.

### Schnittstelle und Datenmigration

Der Leser bewegt Daten zwischen zwei Systemen, laufend oder einmal. Bei einer Schnittstelle stehen das
System, die Klassifizierung mit Namen (Standard-Konnektor, Middleware oder Custom Schnittstelle), die
Richtung und die Felder; das System bringt der Kunde mit, die Middleware wählen wir nach den Best
Practices der Knowledge Base. Bei einer Datenmigration stehen Quelle, Menge, Lösungsansatz und Felder. Kein Werkzeug schneidet hier Kriterien; die Prüfung
aus der Tabelle ist eines.

### UX/UI, Design und Analyse

**UX/UI-Arbeit gibt es nur mit dem Add-on `design`** (`add_ons` in `project.yml`, §209, §303): im
Projekt als Story im Design-Epic, im Expert Service als UX/UI-Subtask an der Story, deren Anforderung
`design_needed: yes` trägt (§285). Der Subtask nennt den Seitentyp als Text (`Seitentyp: PDP`, bei
`en` `Page type: PDP`, §337). Eine
Analyse nennt Gegenstand, Frage und Datenbasis und ist fertig, wenn sie die Frage mit Empfehlungen
beantwortet.

## Die Blockfolge

**Eine Reihenfolge der Blöcke für Story und Subtask** (§209, §281). Überschriften und feste Zeilen
stehen in der Sprache aus `language` (§295), wörtlich nach dem Vokabular unten; der Text darunter
steht so, wie die Quelle ihn trägt.

| Block | Story | Story, mehrere Gewerke | Subtask | Quelle |
|---|---|---|---|---|
| `Kunde` | immer | immer | — | `customer` aus `project.yml`, dazu „Projekt ‹`title`›" |
| `Link zum Shop` | immer | immer | — | `domain` jedes Shops, den `shops` der Anforderung nennt, ein Listenpunkt je Shop (§307) |
| `User Story` | immer | immer | immer | mit `solutioning` abgeschrieben aus der Zelle `User Story / Description` in `epics/EP-NNN.md`, ohne `solutioning` abgeleitet und in der Vorschau vorgelegt, je nach `../../docs/user-story-contract.md` (§323); am Subtask dieselbe, zugeschnitten auf das, was die Arbeitseinheit liefert; nie leer, nie `offen` |
| `Regeln` | nur mit Inhalt | nur mit Inhalt | — | was gilt, ohne beobachtbar zu sein |
| `Akzeptanzkriterien` | immer | immer | — | `## Acceptance criteria`, unverändert, dazu die `Prüfung` der Art |
| `Kriterien der Umsetzung` | — | — | immer | die Kriterien, die [ref-trades.md](ref-trades.md) dem Gewerk zuordnet, mit `## Details` technischer gefasst; nichts, was die Quelle nicht trägt |
| `Nicht enthalten` | immer | immer | — | die Abgrenzungen aus dem Rumpf der Epic-Datei; sonst `- offen` |
| `Lösungsansatz` | immer | immer, übergreifend | — | je Klassifizierung ein Punkt, die Kurzbeschreibung, die Epic Page (§312) |
| `Angaben für ‹Gewerk›` | immer | — | immer | die `Angaben` der Art aus `## Details` |
| `Links` | nur mit Ziel | nur mit Ziel | nur mit Ziel | `Design-Referenz`, `Betroffene Ansicht` |
| `Kontext` | immer | immer | immer | `Beauftragung` und zuletzt der Schlüssel |

## Das Vokabular

**Die Überschriften und festen Zeilen in der Sprache des Projekts** (§295). Übersetzt wird nur hier;
`scripts/check-ticket-body.py` trägt dieselbe Tabelle, und `dev/tests/check-ticket-body.py` hält
beide gleich. `Schlüssel:`, `Beauftragung:` und die Namen der Gewerke stehen in jeder Sprache gleich:
an ihnen findet der Abgleich ein Ticket wieder, auch auf einem Board mit Tickets älterer Läufe.

| de | en |
|---|---|
| `Kunde` | `Customer` |
| `Link zum Shop` | `Shop link` |
| `User Story` | `User story` |
| `Regeln` | `Rules` |
| `Akzeptanzkriterien` | `Acceptance criteria` |
| `Nicht enthalten` | `Not included` |
| `Lösungsansatz` | `Approach` |
| `Angaben für` | `Details for` |
| `Links` | `Links` |
| `Kontext` | `Context` |
| `Kriterien der Umsetzung` | `Implementation criteria` |
| `Ziel` | `Goal` |
| `Anforderungen` | `Requirements` |
| `Design-Referenz:` | `Design reference:` |
| `aus` | `from` |
| `Betroffene Ansicht:` | `Affected view:` |
| `Epic Page:` | `Epic page:` |
| `Design:` | `Design:` |
| `Kunde:` | `Customer:` |
| `Projekt` | `project` |
| `offen` | `open` |
| `Darstellung gemäß Figma (siehe Link)` | `Display as in Figma (see link)` |
| `Entscheidung offen, entscheidet` | `Decision open, decided by` |
| `Alternative` | `alternative` |
| `geprüft und verworfen` | `checked and discarded` |
| `Shopify-nativ` | `Shopify native` |
| `Theme-nativ` | `Theme native` |
| `Public App` | `Public app` |
| `Theme-Anpassung` | `Theme customization` |
| `Custom App` | `Custom app` |
| `Standard-Konnektor` | `Standard connector` |
| `Middleware` | `Middleware` |
| `Custom Schnittstelle` | `Custom integration` |
| `Design (Figma)` | `Design (Figma)` |
| `Analyse` | `Analysis` |

## Titel und Schlüssel

| Ticket | Titel | Schlüssel |
|---|---|---|
| Story | `REQ-012 ‹Titel der Anforderung› ‹Shop-Bezug›`, `title` aus ihrer Datei, dahinter der Shop-Bezug aus `shops` (unten) | `REQ-012`, zusammen mit der Zeile `Beauftragung:` |
| Subtask | `REQ-012-1 ‹eigene Aufgabe›`, etwa `REQ-012-1 App installieren`; bei einer Section ihr Name | die Kennung der Anforderung mit der Nummer, die die Arbeitsreihenfolge trägt (§285), zusammen mit der Zeile `Beauftragung:` |
| Epic-Ticket im Projekt | `EP-003 ‹title aus epics/EP-003.md›` | `EP-003`, zusammen mit der Zeile `Beauftragung:` |
| Epic-Ticket im Expert Service | der Titel des Epics nach dem Thema | keiner; das Epic trägt nur die Zeile `Beauftragung:` (§220) |

**Der Shop-Bezug steht hinten am Titel der Story**, erzeugt aus dem Feld `shops` der Anforderung
(§307): `REQ-012 Staffelpreise (B2B)`, `(B2B & B2C)`, `(3 Shops)`, `(alle Shops)`; in einem Projekt mit
einem Shop keiner. Du schreibst ihn nicht von Hand, sondern nimmst die Zeile aus
`python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/repo_objects.py . REQ-012`; dieselbe
Zeile steht unter `Anforderungen` am Epic-Ticket.

**Das Gewerk steht nie im Titel** (§281); der Prüfer lehnt es mit `title` ab. **`Schlüssel` ist die
letzte Zeile des Blocks `Kontext`**, nie in einem Linktext und nie doppelt. Im Plaintext des Kanals
wird ein Linktext durch die URL ersetzt, und der Schlüssel wäre für den Abgleich unsichtbar.
**Direkt davor steht an jedem Ticket `Beauftragung:`** mit dem `key` aus `project.yml`. Die Kennung
zählt je Repo: auf einem Board mit einem zweiten Vorhaben stehen dieselben `EP-…` und `REQ-…`
mehrmals (Probe 0.5, 10.10.2026), und eigen ist ein Ticket erst, wenn beide Zeilen passen
([ref-epic-cut.md](ref-epic-cut.md)). **Der
`Kontext` ist eine Liste:** einen Umbruch erzeugen im Kanal nur ein Listenpunkt oder eine Überschrift.

## Wie die Blöcke gefüllt werden

**Ausführlich sind allein die Kriterien, knapp ist alles andere.** Die Leser bauen mit Werkzeugen,
die nachfragen (Abschnitte der Gewerke oben); das Ticket liefert die Antworten, und eine beobachtbare
Antwort ist ein Kriterium.

**Die Quelle ist das Repo** (§280): Titel und Kriterien aus der Datei der Anforderung, die User Story
nach dem Vertrag (unten), der Lösungsansatz aus `## Approach`, die Angaben aus `## Details`, die Abgrenzungen aus dem Rumpf der Epic-Datei
(`Assumptions and delimitations` und `Discarded`, in der Sprache der Datei nach
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, „Die Bezeichnungen“). **Was das Repo
nicht trägt, steht nicht im Ticket**: eine Antwort des Leads im Chat ist Material für
`requirements-update` (§280, Regel 6), und der nächste Lauf zieht sie nach.

**Die User Story ist eine Ableitung aus Ist, Soll, FC und UC** (§323), nach
[`user-story-contract.md`](../../docs/user-story-contract.md): mit dem Add-on `solutioning` schreibst
du den Satz aus der Zelle `User Story / Description` der Epic-Datei ab, ohne `solutioning`, auch im
Expert Service, leitest du ihn nach dem Vertrag ab, und die Vorschau zeigt ihn. Am Subtask gilt
derselbe Satz, zugeschnitten auf die Arbeitseinheit. Der Block trägt nie `offen`; in die Anforderung
schreibst du ihn nicht zurück (§280, Regel 3).

**Ein Pflichtblock ohne Quelle trägt die eine Zeile `- offen`**, außer `User Story`. Ein leerer Block sähe aus wie ein
vergessener, ein weggelassener fiele durch die Prüfung. Die Vorschau nennt jede solche Zeile.

**Übernommener Text wird entwrappt.** Der Body erreicht den Kanal als eine Zeile oder als
Markdown-Absätze. Ein Zeilenumbruch in einem Punkt wird ein Leerzeichen; ein Punkt, der umbricht,
bleibt ein Punkt.

### `Regeln` trägt nur, was kein Kriterium ausdrücken kann

**Der Block fällt weg, wenn er leer wäre.** Was als Kriterium formulierbar ist, steht als Kriterium:
dort ist es beobachtbar und wird bei der Abnahme geprüft. Hierher gehört, was gilt, ohne beobachtbar
zu sein:

- **der Fehlerfall als Zustand**: „bricht der Upload ab, liegt kein Nachweis vor; es gibt keinen
  halben Zustand";
- **die Grenze der Geltung:** „die Wahl des Besuchers gilt für alle Pixel, nicht für einzelne";
- **was aus dem Altsystem bindend ist:** Adressformen für Weiterleitungen, gewohntes Verhalten,
  übernommene Datenstrukturen, Mengen.

**Zwei Sätze, die dasselbe sagen, sind einer zu viel.** Steht ein Punkt hier und als Kriterium, gilt
das Kriterium. Die Ausgangslage steht in keinem Ticket.

### `Nicht enthalten` ist die Grenze des Auftrags

Ohne Grenze fragt das nachgelagerte Werkzeug breiter. Die Zeilen kommen aus `Assumptions and
delimitations`, soweit sie diese Anforderung abgrenzen, aus `Discarded`, wo eine verworfene Zeile
dasselbe Wollen weiter fasst als diese Anforderung, und aus dem, was der gewählte Lösungsansatz nicht kann; im
Expert Service, ohne Epic-Datei, aus dem, was `## Description` ausdrücklich ausnimmt. Nennt eine
Abgrenzung das Epic, das sie trägt, bleibt der Verweis stehen. **Nicht in Fachsprache umformuliert:**
die schlichtere Zeile sieht bei jedem Lauf gleich aus.

### Der `Lösungsansatz`: Klassifizierung, Kurzbeschreibung, Epic Page

**Der Block sitzt hinter `Nicht enthalten`** und heißt immer `Lösungsansatz`, vorgeschlagen wie
entschieden (§312). Das Ticket sagt zuerst, was gewollt ist, in der Sprache des Kunden; der Lösungsansatz ist
unsere Wahl und kommt danach, an Epic, Story und Story mit Subtasks in derselben Form, **jede Zeile
ein Listenpunkt** (im Kanal bricht nur ein Listenpunkt um):

```
## Lösungsansatz
- ‹Klassifizierung›                 je Klassifizierung ein Punkt, mit dem Anzeigenamen unten
- ‹Kurzbeschreibung›                ein bis drei Sätze
- Epic Page: ‹Link›                 nur, wenn das Epic eine hat
```

**Der Anzeigename ist die Anzeige aus dem Datalayer-Vertrag**, Abschnitt „Die Klassifizierung“
(`../../docs/datalayer-contract.md`, §324), in der Sprache des Projekts; ein drittes Vokabular gibt
es nicht. Bei `app` und den drei Schnittstellen steht dahinter der Name dessen, was den Lösungsansatz trägt:

| `classification` | Punkt im Ticket | wie konkret in der Kurzbeschreibung |
|---|---|---|
| `shop` | `- Shopify-nativ` | welche Einstellung, an welchem Shop |
| `theme_native` | `- Theme-nativ` | welche Section, welcher Block oder welche Einstellung im Theme Editor (§314) |
| `app` | `- Public App: ‹Name der App›` | ihre Grenze; die Bauform gehört dem Hersteller |
| `theme` | `- Theme-Anpassung` | keine Zusage über den Schnitt; eine Bauform nur, wo die Quelle sie belegt |
| `custom_app` | `- Custom App` | wie Theme |
| `integration_connector` | `- Standard-Konnektor: ‹Name› an ‹System›` | Richtung und Datenstrom |
| `integration_middleware` | `- Middleware: ‹Name› an ‹System›` | Richtung und Datenstrom |
| `integration_custom` | `- Custom Schnittstelle: an ‹System›` | Richtung, Datenstrom, laufend oder einmalig |

Bei `language: en` stehen die Anzeigen auf Englisch nach dem Datalayer-Vertrag, „Die Klassifizierung“, und statt „an“ steht „to“ (§337).

Eine Migration trägt die Klassifizierung ihres Lösungsansatzes; dass sie eine Migration ist, sagt die Domäne des
Epics, und die Kurzbeschreibung nennt Quelle, Menge und Lösungsansatz.

**Die Kurzbeschreibung trägt keine Kennungen** (`GAP-`, `ADR-`, `REQ-`, `EP-`) **und keine Zuteilung
an Gewerke** (§312): die Gewerke zeigen die Subtasks selbst, und eine geschlossene Frage gehört nicht
ins Ticket. **An der Story mit mehreren Gewerken und am Epic-Ticket ist der Block übergreifend**
(§281): je Klassifizierung des ganzen Lösungsansatzes ein Punkt, am Epic die Klassifizierungen seiner
Anforderungen, dazu eine Kurzbeschreibung des ganzen Lösungsansatzes.

**Die Zeile `Epic Page:` zeigt auf die freigegebene Fassung** (§312, §313) und steht nur, wenn die
Epic-Datei `epic_page` trägt. **Kein Ticket verlinkt den Entwurf**, unter keinem Namen: er wird nach
der Freigabe weitergeschrieben (§302). Ein Ticket vor der Freigabe trägt keinen Link (§219, §284).

**Im Design-Epic ohne Lösungsansatz** (§297) nennt der Punkt der Klassifizierung die Art der Arbeit des
Designers aus der Gewerk-Tabelle, `- Design (Figma)` oder `- Analyse`, und die Kurzbeschreibung sie,
so wie `## Description` sie beschreibt; sonst `- offen` ([ref-trades.md](ref-trades.md),
Anforderungen im Design-Epic).

**Ist der Lösungsansatz nicht entscheidbar und lässt der Lead ihn offen** (§209, §220), steht an der Stelle der
Klassifizierung: „- Entscheidung offen, entscheidet ‹Gewerk›; Alternative ‹…›; geprüft und verworfen
‹…›", in der Sprache des Projekts nach dem Vokabular.

**Der Block nennt das Gewählte, nicht seine Herkunft.** Seit wann etwas bei uns gilt, warum unsere
Regel hier greift und welcher Lösungsansatz fiel, steht in der ADR. Der Prüfer fängt ein Datum und die
Wendungen einer Hausregel am Text, eine Kennung in der Kurzbeschreibung und einen Block, dessen
erster Punkt keine Klassifizierung ist.

### Design: Frame, Referenz und das Kriterium der Darstellung

**DEV-Arbeit trägt keine Optik**; das Theme-Werkzeug holt sie aus dem Frame (§285). Gesetzt wird nur,
was das Repo trägt, kein Link wird von Hand nachgepflegt:

- **der Frame je Section** an ihrem Subtask, `Design-Referenz: ‹Link mit node-id›` aus `## Sections`;
- **an der Story eines Seitentyps**, wenn `figma` gesetzt ist, das Kriterium „Darstellung gemäß
  Figma (siehe Link)" unter `Akzeptanzkriterien`;
- **der Link zum ganzen Design** einmal an das Epic-Ticket des Theme-Epics, `Design: ‹figma›`;
- **`design_reference` einer Fähigkeit** an ihrer Story, `Design-Referenz: ‹Link›`;
- **im Expert Service** trägt der DEV-Subtask nach einem UX/UI-Subtask `Design-Referenz: aus
  ‹Schlüssel des UX/UI-Subtasks›`, etwa `Design-Referenz: aus REQ-012-2`.

**Gibt es keines davon, fehlt die Zeile**; eine Zeile mit `TODO` oder einem Strich behauptet eine
Referenz, die niemand hat. Der Prüfer nimmt nur die Adresse oder `aus ‹Schlüssel›` an.

## Die Story, ein Gewerk

```markdown
## Kunde
<Kunde>, Projekt <Titel des Vorhabens>

## Link zum Shop
- <Domain des betroffenen Shops>

## User Story
Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.

## Regeln
- <was gilt, ohne beobachtbar zu sein; der Block entfällt, wenn es nichts gibt>

## Akzeptanzkriterien
- <je Kriterium der Anforderung ein Punkt, unverändert, dazu die Prüfung der Art>

## Nicht enthalten
- <je Abgrenzung ein Punkt, mit dem Epic, das sie trägt, sonst: offen>

## Lösungsansatz
- <Klassifizierung>
- <Kurzbeschreibung des Lösungsansatzes, ein bis drei Sätze>
- Epic Page: <Adresse der Epic Page>

## Angaben für <Gewerk>
- <je Angabe der Art ein Punkt, sonst: offen>

## Links
- Design-Referenz: <Adresse des Designs>
- Betroffene Ansicht: <URL im Shop>

## Kontext
- Beauftragung: <key aus project.yml>
- Schlüssel: <Kennung>
```

## Die Story, mehrere Gewerke

```markdown
## Kunde
<Kunde>, Projekt <Titel des Vorhabens>

## Link zum Shop
- <Domain des betroffenen Shops>

## User Story
Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.

## Regeln
- <was gilt, ohne beobachtbar zu sein; der Block entfällt, wenn es nichts gibt>

## Akzeptanzkriterien
- <je Kriterium der Anforderung ein Punkt, unverändert, dazu die Prüfung der Art>

## Nicht enthalten
- <je Abgrenzung ein Punkt, mit dem Epic, das sie trägt, sonst: offen>

## Lösungsansatz
- <Klassifizierung>
- <Kurzbeschreibung des ganzen Lösungsansatzes, ein bis drei Sätze>
- Epic Page: <Adresse der Epic Page>

## Links
- Design-Referenz: <Adresse des Designs>
- Betroffene Ansicht: <URL im Shop>

## Kontext
- Beauftragung: <key aus project.yml>
- Schlüssel: <Kennung>
```

## Der Subtask

```markdown
## User Story
Als <Rolle> möchte ich <Ziel der Arbeitseinheit>, damit <Nutzen>.

## Kriterien der Umsetzung
- <je Kriterium seines Gewerks ein Punkt, technischer als an der Story, dazu die Prüfung der Art>

## Angaben für <Gewerk>
- <je Angabe der Art ein Punkt, sonst: offen>

## Links
- Design-Referenz: <Adresse des Frames>

## Kontext
- Beauftragung: <key aus project.yml>
- Schlüssel: <Kennung>-<n>
```

## Das Epic-Ticket

**Je Anforderung nur ID und Titel** (§281): eine Zeile `REQ-012 ‹Titel› ‹Shop-Bezug›` je Anforderung des Epics,
die ein Ticket bekommt; User Story und Kriterien stehen an der Story. Das Epic trägt keine Komponente.
**Eine Tabelle steht in keinem Body** (§222).

```markdown
## Ziel
<das Ziel des Epics aus Goals and vision of the Customer>

## Kontext
- Kunde: <Kunde>, Projekt <Titel des Vorhabens>
- Stufe <n> · wartet auf <EP-…>
- Beauftragung: <key aus project.yml>
- Schlüssel: <Epic-ID>

## Anforderungen
- <Kennung> <Titel der Anforderung mit Shop-Bezug>

## Lösungsansatz
- <Klassifizierung>
- <Kurzbeschreibung des übergreifenden Lösungsansatzes, ein bis drei Sätze>
- Epic Page: <Adresse der Epic Page>

## Links
- Design: <Link zur Figma-Datei>
```

`Ziel` kommt im Projekt aus dem ersten Satz unter `Goals and vision of the Customer` der Epic-Datei,
die Kurzbeschreibung im `Lösungsansatz` aus den Sätzen über der Tabelle unter `Requirements`, ohne
Kennungen gefasst; die Punkte der Klassifizierung aus `classification` seiner Anforderungen. Im
Expert Service fasst der Lauf das Ziel aus dem Wollen der Anforderungen und den Lösungsansatz aus
ihren Lösungsansätzen, und die Vorschau zeigt beides.

**Die Zeile `Beauftragung` steht an jedem Epic**, mit dem `key` aus `project.yml`, exakt, im Projekt
direkt vor `Schlüssel`. Ein Board kann mehrere Vorhaben tragen, und die Epic-ID zählt je Repo:
`EP-001` kann auf einem geteilten Board mehrmals stehen. Als eigenes zählt ein Lauf deshalb nur ein
Epic mit seinem `key` ([ref-epic-cut.md](ref-epic-cut.md)). Die Zeile `Schlüssel` steht nur im
Projekt; im Expert Service fehlt sie (§220). `Links` trägt am Theme-Epic die Figma-Datei; sonst
fällt der Block weg.

## Die Reihenfolge

**Je Epic-Ticket eine Zeile mit seiner Stufe** (§267), im `Kontext` nach `Kunde`, genau in der Form
`Stufe ‹n› · wartet auf ‹EP-…›, ‹EP-…›`; wo keine Abhängigkeit belegt ist, nur `Stufe ‹n›`; bei `en`
`Stage ‹n› · waits for ‹EP-…›` und `Stage ‹n›` (§337). Die Zeile
kommt Zeichen für Zeichen aus `epics/critical-path.md`, Abschnitt `Zeile im Epic-Ticket`; der Lauf
rechnet sie nicht selbst. **Sie ist Text, keine Verknüpfung** (§209). Sie fehlt, und die Vorschau nennt
den Grund, wenn es die Datei nicht gibt, sie das Epic nicht nennt oder `keine Stufe` (`no stage`) trägt, oder sie
Varianten trägt und der Lead keine wählt.

**Einen Durchstich, den die Datei vorschlägt, legt der Lauf nicht an**: die Vorschau nennt ihn mit
den Anforderungen, die er umfasst. Eine Story je Anforderung (§281) lässt keine zweite Story für
dieselbe Anforderung zu; wie ein Durchstich auf das Board kommt, ist offen.

## Was nie in einem Body steht

**Stunden, Preise, Schätzungen, Größen.** `size` geht nur in das Größenfeld des Boards, wo es eines
gibt ([ref-jira.md](ref-jira.md), [ref-asana.md](ref-asana.md)); das Board ist kundensichtbar.
Geprüft wird das am fertigen Body.

**Offene Fragen als Kommentar.** Offenes steht im Text (§220); einen Kommentar schreibt der Lauf
nicht.

**Interna** (§278): nichts aus einer internen Quelle, auch nicht sinngemäß; die Liste steht in
`way-of-working.md`, Abschnitt „Interna“.

**Ein Link ins private Repo der Wissensbasis**, auch nicht der Treffer eines Lösungsansatzes: der Leser landet
auf einer Seite, die er nicht öffnen kann.

**Überschriften tiefer als Ebene 2.** Der Kanal-Vertrag führt nur Ebene 1 und 2.
