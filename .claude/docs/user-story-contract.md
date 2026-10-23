# Die User Story — eine Ableitung aus Ist, Soll, FC und UC

**Die User Story ist eine Ableitung, keine Quelle** (§323). Sie entsteht aus dem, was die Anforderung
trägt: dem Ist (`## Current state`), dem Soll (`## Description`), der einen Fähigkeit (FC, die Datei
selbst) und dem Verhalten, an dem sie abgenommen wird (UC, `## Acceptance criteria`). **Sie steht im
Entwurf, auf der Epic Page und im Ticket, nie in der Anforderung**: die Datei in `requirements/` hat
keinen Abschnitt `## User story`, und kein Lauf schreibt einen hinein (§280, Regel 3). Diesen Vertrag
lesen `solution-design`, das sie im Entwurf ableitet, und `ticket-factory`, das sie ins Ticket
schreibt.

## Wer sie wann schreibt

| Vorhaben | Wer | Wo |
|---|---|---|
| mit dem Add-on `solutioning` | `solution-design` leitet sie je Anforderung ab | im Rumpf von `epics/EP-NNN.md` und im Entwurf, Zelle `User Story / Description` der Tabelle unter `Requirements` |
| | `solution-epic-page` übernimmt sie Zeichen für Zeichen mit dem freigegebenen Entwurf | auf der Epic Page |
| | `ticket-factory` schreibt sie aus `epics/EP-NNN.md` ab, leitet keine neue ab | im Block `User Story` der Story; am Subtask zugeschnitten (unten) |
| ohne `solutioning`, auch im Expert Service | `ticket-factory` leitet sie nach diesem Vertrag ab und legt sie in der Vorschau vor | im Block `User Story` der Story und des Subtasks |

`requirements-update` schreibt keine User Story. **Die Zelle `User Story / Description`** trägt zuerst
den Satz, darunter, nach einem `<br>`, den ersten Absatz von `## Description`. `ticket-factory` nimmt
den Teil vor dem ersten `<br>`. Fehlt die Zelle oder trägt sie keinen Satz in der Form unten, schreibt
`ticket-factory` nicht ab, sondern leitet ab und legt die Abweichung in der Vorschau vor; der Bericht
nennt `solution-design` für das Epic.

## Die Form

**Ein Satz in der Sprache des Projekts** (`language` in `project.yml`, §295):

| `language` | Form |
|---|---|
| `de` | `Als ‹Rolle› möchte ich ‹Ziel›, damit ‹Nutzen›.` |
| `en` | `As ‹role›, I want ‹goal› so that ‹benefit›.` |

**Nie leer, nie „offen“ oder „open“, nie „Als Entwickler …“ / „As a developer …“.** Der Satz trägt keine
Kennung (`REQ-`, `EP-`, `GAP-`, `ADR-`) und kein Gewerk; an der Story auch keinen Lösungsansatz und
keinen Werkzeugnamen, außer der Titel der Anforderung nennt das Werkzeug, weil der Kunde es einsetzt
und behalten will. **Kein Lauf schreibt sie in die Anforderung zurück** (§280, Regel 3).
`check-ticket-body.py` lehnt an Story und Subtask eine User Story ab, die leer ist, „offen“ oder
„open“ trägt oder nicht mit „Als … möchte ich …“ bzw. „As … I want …“ beginnt.

## Die Ableitung

| Teil | woraus | Regel |
|---|---|---|
| Rolle | Soll und Material: wer das Wollen hat oder wen der Soll-Zustand betrifft | ein Endkunde, ein Team oder eine Rolle beim Kunden („Kundenservice“, „Einkauf“); **ist die Rolle mehrdeutig, steht der Kunde**, wer die Anforderung eingebracht hat |
| Ziel | Soll (`## Description`), begrenzt auf die eine Fähigkeit (FC) | was gelten soll, nicht womit; nennt das Ist etwas Bestehendes, sagt das Ziel, was sich daran ändert |
| Nutzen | folgt aus dem Soll | der Grund, den das Material nennt; nennt es keinen, der, der unmittelbar aus dem Soll folgt, ohne neuen Bedarf |
| Grenze | UC (`## Acceptance criteria`) | der Satz verspricht nichts, was kein Kriterium prüft |

**Eine Frage nach dem Nutzen entsteht nur, wo ohne ihn kein Akzeptanzkriterium prüfbar formuliert
werden kann** (§250); sie nennt das Kriterium und kommt als Frage in `gaps/`. Sonst steht der Nutzen,
der aus dem Soll folgt.

## Am Subtask zugeschnitten

**Der Subtask trägt dieselbe Rolle und denselben Nutzen wie die Story**; das Ziel wird enger, auf das,
was die Arbeitseinheit liefert, und darf dafür den gewählten Lösungsansatz nennen. Aus „Als Kunde möchte ich Bestände aus der Warenwirtschaft im Shop sehen,
damit …“ wird am Subtask der Einrichtung „Als Kunde möchte ich, dass der Konnektor die Bestände je Lager
überträgt, damit …“. Eine Rolle aus dem Team, das baut, ist keine Rolle.

## Die festen Sätze der Standard-Anforderungen

**Die Standard-Anforderungen der Add-ons tragen einen festen Satz** (§303); er wird nicht abgeleitet und
ohne Frage übernommen. Die Kennung steht in `standard` der Anforderung.

| `standard` | `de` | `en` |
|---|---|---|
| `design-concept` | Als Kunde möchte ich vor der Umsetzung ein Designkonzept je Seitentyp und ein Design-System, damit Theme und Sections auf einer abgestimmten Gestaltung aufbauen. | As the customer, I want a design concept per page type and a design system before implementation so that theme and sections build on an agreed design. |
| `design-qa` | Als Kunde möchte ich vor dem Go-Live einen Shop, der auf allen Seitentypen, Geräten und Browsern geprüft ist, damit Endkunden keine Brüche sehen. | As the customer, I want a shop checked on all page types, devices and browsers before go-live so that end customers see no breaks. |
| `content-migration` | Als Kunde möchte ich die Inhaltsseiten und Blogbeiträge des Altshops im neuen Shop, damit zum Go-Live keine Inhalte verloren gehen. | As the customer, I want the content pages and blog posts of the old shop in the new shop so that no content is lost at go-live. |

## Beispiele

**Eine Pflicht-Anforderung aus dem Standard-Leistungssatz.** Soll: „Vor der Zustimmung lädt der Shop
keine Marketing-Pixel.“ Ist: „ungeprüft“ (`current_unchecked`, bei `en` „unchecked“, [datalayer-contract.md](datalayer-contract.md), Die festen Wendungen). Kriterium: „Ohne Zustimmung feuert kein Marketing-Pixel.“

> Als Endkunde möchte ich selbst entscheiden, welche Marketing-Pixel der Shop lädt, damit meine Daten
> nur mit meiner Zustimmung weitergegeben werden.

**Eine Schnittstelle.** Soll: „Bestände kommen je Lager aus der Warenwirtschaft.“ Ist: „Bestände
werden heute von Hand gepflegt.“ Kriterium: „Eine Bestandsänderung in der Warenwirtschaft steht
innerhalb von 15 Minuten im Shop.“ Die Rolle ist mehrdeutig (Lager, Vertrieb, Endkunde): es steht der
Kunde.

> Als Kunde möchte ich die Bestände je Lager aus der Warenwirtschaft statt von Hand im Shop, damit
> Endkunden nur bestellen, was vorrätig ist.

**Englisch, ein Feature.** Soll: “Shipping costs follow the market of the order.” Kriterium: “The cart
shows the shipping costs of the selected market.”

> As an end customer, I want to see the shipping costs for my country before checkout so that I am
> not surprised at payment.
