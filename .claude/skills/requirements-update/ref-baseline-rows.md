# Aus einer Zeile des Standard-Leistungssatzes wird eine Anforderung

**Was wir in einem Rechtsraum immer bauen, ist fest im Umfang**, in jedem Projekt, nie „optional". Die
Zeilen der Liste werden Anforderungen wie jede andere, je Zeile eine Datei in `requirements/`: zählbar,
mit Lösung und Ticket.

## Woher Rechtsraum und Zielgruppe kommen

Aus `jurisdiction` des Shops in `project.yml`; die Kennung ist der Dateiname der Liste. **Aus den
Märkten folgt er nicht:** ein Markt ist ein Verkaufsgebiet, keine Rechtsordnung. **Ist `jurisdiction`
leer, fragst du den Lead** je Shop nach der Kennung des Rechtsraums (§229); die Antwort darf „noch
offen" sein. Eingetragen wird sie nach dem Datalayer-Vertrag, Abschnitt `project.yml`, erst wenn die
Liste zu ihr lesbar ist; sonst bleibt das Feld leer, und es gilt der nächste Absatz. Sagt der Lead „noch
offen", entsteht keine Listenzeile, und der Bericht nennt den Shop. Ist `shops` leer, gibt es keinen
Rechtsraum zu fragen; der Bericht nennt es.

**Ist `audience` leer, fragst du in derselben Frage**, an wen der Shop verkauft: an Verbraucher (`b2c`),
an Händler (`b2b`) oder an beide (`both`) (§249). Eingetragen wird die Antwort nach dem Vertrag; aus
dem Schlüssel des Shops folgt sie nicht. Sagt der Lead „noch offen", gilt für diesen Shop eine Zeile
für Verbraucher, die Zeile `nur Händler` nicht, der Bericht nennt den Shop, und den Shop-Bezug prüft
`requirements-review` (§245).

## Woher die Liste kommt und warum die Kopie zählt

**Gelesen wird `minimum-standard/<kennung>.md` der Wissensbasis**, erst `index.md`, dann die Datei,
auf dem Weg, den der Vertrag `${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md` festlegt: mit
`get_file_contents`, in einer Cloud-Sitzung nach `add_repo`, ohne Klon. Ist die Liste nicht lesbar oder fehlt sie für den Rechtsraum, entsteht
**eine Frage** an den Lead, in der Notiz und im Bericht, keine Anforderung: aus einer ungelesenen Liste
entsteht keine Anforderung, und ohne Anforderung hat die Frage kein Ziel in `gaps/`. Der Bericht nennt die Wissensbasis als ungelesene Quelle.

**Die Notiz zum Abgleich hält den gelesenen Stand fest**: Pfad der Liste, `sha` aus der Antwort von
`get_file_contents` und Lesedatum im Kopf, darunter je Zeile der Liste ihre ID oder „nicht
aufgenommen" mit Grund ([ref-requirement.md](ref-requirement.md)). Der `sha` ist der Stand, gegen den das
Vorhaben geschnitten wurde; die Liste in der Wissensbasis bewegt sich weiter. `source` der
Anforderungen ist der Dateiname dieser Notiz.

**Denselben Stand schreibst du nach `baselines.yml`** (§269): je gelesenem Rechtsraum `path`, `sha`
und `read_on`, nach dem Datalayer-Vertrag (Abschnitt `baselines.yml`). Ein neuer Lesestand ersetzt
den Eintrag seines Rechtsraums; die Einträge anderer Rechtsräume bleiben, und die Notiz bleibt.
Ist die Liste nicht lesbar, ändert sich die Datei nicht.

## Für welchen Shop die Zeile gilt

**Eine Zeile gilt für einen Shop, wenn er den Rechtsraum trägt und seine Zielgruppe zur Spalte `für`
der Liste passt** (§249): `alle` passt zu jedem `audience`, `Verbraucher` zu `b2c` und `both`, `nur
Händler` zu `b2b`. Daraus die Form:

| Die Zeile gilt für | Form |
|---|---|
| alle Shops des Vorhabens | einmal, ohne Schlüssel |
| einen oder mehrere, nicht alle | ihre `key` im Feld `shops`, `shops: [b2c]` (§307) |
| keinen | keine Anforderung; die Notiz nennt die Zeile unter „nicht aufgenommen", mit dem Grund |

**Zur Zielgruppe entsteht keine Frage in `gaps/`:** die Anforderung kommt aus der Liste oder nicht.

## Die Standard-Anforderungen der Add-ons

**Mit dem Add-on `design` oder `content_migration` in `add_ons` von `project.yml` stehen seine
Standard-Anforderungen aus der festen Liste unten** (§303); mit `design` gehört die UX/UI-QA vor dem
Go-Live dazu (§285). Fehlt eine in `requirements/`, legst du sie an wie jede andere, mit `source`
„Angebot" (`source_offer`, `en`: „Offer") und
**`standard`**, an dem Schnitt, Schätzung und `requirements-review` sie erkennen. Die Wendungen stehen
in `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“ (§337):

| Add-on | `standard` | `title` | `## Description` | `## Acceptance criteria` |
|---|---|---|---|---|
| `design` | `design-concept` | Designkonzept und Design-System | Ein Designkonzept je Seitentyp und ein Design-System mit Token, Header, Footer und globalen Sections. | Für jeden Seitentyp im Scope liegt ein Designkonzept vor, und das Design-System legt Token, Header, Footer und globale Sections fest. |
| `design` | `design-qa` | UX/UI-QA vor dem Go-Live | Der UX/UI-Designer prüft vor dem Go-Live den ganzen Shop auf das, was erst im Zusammenspiel auffällt: Einheitlichkeit über die Seitentypen, echte Inhalte aus der Migration, Apps mit eigener Oberfläche, Geräte und Browser. Befunde werden Tickets an der Story des betroffenen Seitentyps. | Vor dem Go-Live ist jeder Seitentyp mit echten Inhalten auf den vereinbarten Geräten und Browsern geprüft, und jeder Befund steht als Ticket an der Story seines Seitentyps. |
| `content_migration` | `content-migration` | Content-Migration | Inhaltsseiten und Blogbeiträge des Altshops sind im neuen Shop angelegt. | Jede Inhaltsseite und jeder Blogbeitrag des Altshops ist im neuen Shop angelegt oder mit dem Kunden als nicht übernommen vereinbart. |

Bei `language: en`:

| Add-on | `standard` | `title` | `## Description` | `## Acceptance criteria` |
|---|---|---|---|---|
| `design` | `design-concept` | Design concept and design system | A design concept for each page type and a design system with tokens, header, footer and global sections. | For every page type in scope there is a design concept, and the design system defines tokens, header, footer and global sections. |
| `design` | `design-qa` | UX/UI QA before go-live | Before go-live, the UX/UI designer reviews the whole shop for what only shows when everything comes together: consistency across page types, real content from the migration, apps with their own interface, devices and browsers. Findings become tickets on the story of the affected page type. | Before go-live, every page type has been checked with real content on the agreed devices and browsers, and every finding is a ticket on the story of its page type. |
| `content_migration` | `content-migration` | Content migration | Content pages and blog posts of the old shop are created in the new shop. | Every content page and blog post of the old shop is created in the new shop or agreed with the customer as not carried over. |

**Das Kriterium steht fest, aus der Tabelle**; der Lauf leitet keins aus dem Material ab und stellt
dazu keine Frage. Eine User Story schreibt der Lauf nicht; den festen Satz je `standard` trägt
`${CLAUDE_SKILL_DIR}/../../docs/user-story-contract.md` (§323). **Einen Ist-Zustand im Shop hat keine der drei**: sie sind Leistungen dieses
Vorhabens. `## Current state` heißt deshalb „Leistung dieses Vorhabens, im Shop noch nicht
vorhanden." (`current_standard`, `en`: „A deliverable of this project, not yet in the shop."), `live` ist `no`, und es entsteht keine Frage nach dem Ist-Zustand.

`title`, `## Description`, `## Acceptance criteria` und `## Current state` schreibst
du in der Sprache aus `language`, aus der Tabelle dieser Sprache (§337). Ändert der Lead den Titel, bleibt `standard`. **Setup, Datenmigration und Theme-Arbeit sind keine Add-ons:** sie kommen als
Anforderungen aus dem Material, ohne automatisch angelegte Anforderung (§303).

**Ist `project_type` leer, hat `project-setup` die Add-ons noch nicht abgefragt:** du fragst den Lead
einmal, welche Add-ons das unterschriebene Angebot nennt, legst für diesen Lauf danach an, trägst
nichts in `project.yml` ein und nennst `project-setup` im Bericht.

## Die Zeile ist die Einheit

**Nie zwei Zeilen der Liste zu einer Anforderung.** Wer zwei bündelt, macht eine davon unzählbar. Steht
eine Anforderung für dieselbe Pflicht schon aus dem Material des Kunden, ergänzt die Listenzeile sie
(Verdikt „gehört zu") und legt keine zweite an.

## Was wir nicht tun

Die Rechtstexte formulieren wir nicht, wir binden sie ein. Was die Liste einer anwaltlichen
Einzelfreigabe zuschreibt, steht in `## Description` als Grenze. **Ob der Shop damit rechtlich
vollständig ist, sagt dieser Lauf nie**; der Satz ist unsere Leistung, die Prüfung schuldet der Kunde
mit seinem Anwalt.

Erfüllt der Shop eine Pflicht heute schon, ist das kein Grund, sie wegzulassen; der heutige Stand steht
in `## Current state`, und `live` ist `yes` oder `partial`. Was die Liste als rein operativ führt, wird keine Anforderung, sondern steht mit Grund
unter „nicht aufgenommen" in der Notiz.
