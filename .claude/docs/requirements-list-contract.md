# Die Anforderungsliste — die Projektion des Repos in ein Google Sheet je Vorhaben

**Das Sheet ist Überblick und Arbeitsliste, nicht Quelle** (§280, §283). Quelle für Anforderungen,
Epics und offene Fragen ist das Projekt-Repo ([`datalayer-contract.md`](datalayer-contract.md)); das
Sheet ist seine Projektion. **Es gibt ein natives Google Sheet in jedem Vorhaben** (§282):
`requirements-update` legt es beim ersten Lauf im Unterordner `Solutioning` des Projektordners an
(§229, §231) und trägt seine ID in `requirements_sheet` in `project.yml` ein. Das Sheet gehört nicht
zum Datalayer.

**Jedes Sheet hat dieselben Tabs und Spalten** (§283), ohne Bedingung je Art der Beauftragung: was
nicht gebraucht wird, bleibt leer, `Solutioning` ohne das Add-on `solutioning` (§303), `Epics` ohne Schnitt.
Je Rolle gibt es eine Filteransicht statt eigener Spalten.

**Nichts Internes steht darin** (§278), damit der Lead das Sheet mit dem Kunden teilen kann: keine
Einschätzung zum Kunden, keine Marge, kein Hinweis auf andere Kunden. Stunden stehen darin; ob er sie
teilt, entscheidet der Lead.

**Gelesen und geschrieben wird über die Google-Connectoren von claude.ai** (§226), mit dem
Google-Konto des Leads: gelesen mit `Google_Sheets` (`get_spreadsheet` für Tab-Namen und Kopfzeilen,
`get_values` für Bereiche), geschrieben mit `update_values`; angelegt und gefunden wird die Datei mit
`Google_Drive`. Der Connector ändert einzelne Zellen in derselben Datei und hält keine eigene Sperre
gegen fremde Änderungen.

## Die Projektion

**Jeder schreibende Lauf endet gleich** (§280): `check-repo.py` prüft die Objekte im Repo
gegeneinander, dann projiziert `project-sheet.py` sie ins Sheet. Die Projektion geht in eine
Richtung, vom Repo ins Sheet, und schreibt nur die Spalten, deren Eigentümer das Repo ist. Ins Sheet
schreibt nur der Agent `project-sheet-writer` (§230), mit den Befehlen aus
[`ref-sheet-writer.md`](ref-sheet-writer.md); kein Skill schreibt selbst, und einen eigenen Skill für
Abgleich oder Projektion gibt es nicht.

**`project-sheet.py` rechnet die Stellen aus**: aus den Objekten des Repos und der einen Lesung je
Tab die Tabelle `changes` (Tab, Stelle, heute, neu) für den Agent, mit neuen Zeilen, geleerten Zellen
und, im Tab `Offene Punkte`, gelöschten Zeilen.

**Vorgelegt wird die Änderung im Repo, nicht die Projektion.** Der Lead bestätigt im Lauf, was in die
Dateien geht; die Projektion zeigt danach diesen Stand.

**Abgleich statt stillem Überschreiben** (§280, Regel 7): vor dem Schreiben liest die Projektion die
eigenen Spalten, eine Lesung je Tab, und legt eine Zelle, in der etwas anderes steht als das, was sie
zuletzt geschrieben hat, als Abweichung vor. Was bleiben soll, kommt als Material ins Repo; die
Projektion übernimmt nichts aus dem Sheet.

**Antworten kommen als Material, nie durch einen Eintrag ins Sheet** (§276; §280, Regel 6), auch die
des Leads. In den Spalten der Fragen steht nur Offenes.

## Eigentümer je Spalte

**Jede Spalte hat genau einen Eigentümer** (§283): **das Repo**, dann erzeugt die Projektion sie, und
die Spalte trägt einen Warnschutz, oder **die Menschen**, dann schreibt kein Lauf in sie. Der
Eigentümer ist an der Farbe der Kopfzeile zu sehen: Strix-Gelb `#FFDB32` beim Repo, ein helleres Gelb
`#FFF1B0` bei den Menschen. Welche Spalte wem gehört, steht je Tab unten, in der Spalte
`Eigentümer`: `Repo` mit dem Feld oder Abschnitt der Datei, aus dem die Projektion sie schreibt, oder
`Mensch`. **Eine Spalte trägt eine Formel** (`Aufwand (h)` im Tab `Epics`): sie gehört keinem von
beiden, kein Lauf schreibt in sie, und sie ist gefärbt und geschützt wie eine Spalte des Repos.

**Die Felder der Menschen haben ihre Quelle im Sheet** (§280, Regel 5) und stehen in keiner Datei des
Repos. Ein Lauf liest sie nur, wenn er den Wert braucht, und nur die schmale Spalte. Ändert ein Mensch
eine Spalte des Repos, legt der nächste Lauf das als Abweichung vor (oben).

**Eine Zeile findet die Projektion über ihre Kennung**, `ID`, `Epic-ID` oder `GAP-ID`, nie über ihre
Position: so bleiben die Felder der Menschen an ihrer Anforderung, ihrem Epic oder ihrer Frage, auch
wenn eine Zeile dazukommt oder herausfällt.

## Tab `Offene Punkte`

**Eine Zeile je offener Frage aus `gaps/`** (§279, §283): jede Frage mit `status: open` genau einmal,
gleich welcher Art; eine geschlossene Frage nimmt die Projektion samt ihrer Zeile heraus.
`Verantwortlich` und `Bis` sind Felder der Menschen; alle übrigen Spalten projiziert das Repo aus der
Datei der Frage.

**In den Tabs der Anforderungen und des Solutionings steht eine Frage an ihrem Ort** (§279): eine
Frage der Art `discovery` in `Offene Fragen` des Tabs `Anforderungen`, eine der Art `solutioning` oder
`decision` in `Offene Fragen / Entscheidungsbedarf` des Tabs `Solutioning`, je an jeder Zeile, die sie
in `concerns` betrifft. Je Frage steht eine Zeile in der Zelle, ihre Kennung und ihr Kurztext,
`GAP-007 ‹erster Satz der Frage›`, nur solange sie offen ist (§276).

## Die Anzeigewerte

**Im Repo sind Feldnamen und Werte englisch, im Sheet stehen sie in der Sprache des Projekts**
(§295), nach `language` in `project.yml`. Übersetzt wird an genau einer Stelle, in der Projektion;
ein Wert, der hier fehlt, wird nicht projiziert, sondern von `check-repo.py` abgelehnt. Ein leerer
Wert bleibt leer. **Die Anzeige von `classification` steht im Datalayer-Vertrag**, Abschnitt „Die
Klassifizierung“ ([`datalayer-contract.md`](datalayer-contract.md)), ihrem einzigen Besitzer (§324);
`check-sheet.py` trägt sie von dort.

| Feld im Repo | Wert | `de` | `en` |
|---|---|---|---|
| `status` (Anforderung) | `open` | Offen | Open |
| | `confirmed` | Bestätigt | Confirmed |
| | `rejected` | Verworfen | Rejected |
| | `duplicate` | Duplikat | Duplicate |
| `priority` | `must-have` | Must-have | Must-have |
| | `nice-to-have` | Nice-to-have | Nice-to-have |
| `scope` | `in_scope` | In Scope | In scope |
| | `out_of_scope` | Out of Scope | Out of scope |
| `live` | `yes` | Ja | Yes |
| | `no` | Nein | No |
| | `partial` | Teilweise | Partial |
| | `verify` | Verifizieren | Verify |
| `design_needed`, `interface_needed` | `yes` | ja | yes |
| | `no` | nein | no |
| | `open` | offen | open |
| `size` | `S`, `M`, `L`, `XL` | S, M, L, XL | S, M, L, XL |
| `solution_status` | leer, `proposed` | Entwurf | Draft |
| | `decided` | Entschieden | Decided |
| | `blocked` | Blocker | Blocked |
| `kind` (Frage) | `discovery` | Discovery | Discovery |
| | `solutioning` | Solutioning | Solutioning |
| | `decision` | Entscheidung | Decision |
| `blocking` | `yes` | Ja | Yes |
| | `no` | Nein | No |
| `information` (Epic) | `thin` | Dünn | Thin |
| | `partial` | Teilweise | Partial |
| | `solid` | Tragfähig | Solid |
| `status` (Epic) | `open` | Offen | Open |
| | `in_progress` | In Bearbeitung | In progress |
| | `in_review` | Zur Abnahme | In review |
| | `internal_review` | Interne Abnahme | Internal review |
| | `merged` | Zusammengeführt | Merged |
| | `dissolved` | Aufgelöst | Dissolved |
| `domain` (Epic, §252) | `basic_setup` | Basissetup | Basic setup |
| | `design` | Design | Design |
| | `storefront` | Storefront | Storefront |
| | `product_data` | Produktdaten | Product data |
| | `search_navigation` | Suche & Navigation | Search & navigation |
| | `cart_checkout` | Warenkorb & Checkout | Cart & checkout |
| | `customer_account` | Kundenkonto | Customer account |
| | `b2b` | B2B | B2B |
| | `subscription_loyalty` | Abo & Kundenbindung | Subscriptions & loyalty |
| | `markets_shipping` | Märkte & Versand | Markets & shipping |
| | `legal_consent` | Recht & Consent | Legal & consent |
| | `marketing_crm` | Marketing & CRM | Marketing & CRM |
| | `apps_features` | Apps & Features | Apps & features |
| | `interfaces` | Schnittstellen | Interfaces |
| | `data_migration` | Datenmigration | Data migration |
| | `content_migration` | Content-Migration | Content migration |

## Die Kopfzeilen

**Die Kopfzeilen und die Namen der Tabs stehen in der Sprache des Projekts** (§295), wörtlich so wie
unten, je Tab die Zeile `de` oder `en`. Die Folge der Tabs ist `Anforderungen`, `Solutioning`,
`Epics`, `Offene Punkte`; der erste Tab muss `Anforderungen` sein, denn der CSV-Export liefert nur
ihn. `.claude/scripts/check-sheet.py` trägt dieselben Kopfzeilen und dieselben Eigentümer; aus ihm
formatiert `sheet-format.py` das Sheet und liest `scope-snapshot.py` die Tabs (§247).

Was die Projektion aus einem Feld mit Vokabular schreibt, ist sein Anzeigewert (oben). Titel einer
Anforderung und offene Fragen schreibt der Lauf schon in der Sprache des Projekts (§337); was ein Mensch
sonst geschrieben hat, Beschreibung und Kriterien, steht so, wie es erfasst wurde, nicht übersetzt.

## Tab `Anforderungen` (`Requirements`) — eine Zeile je Anforderung

- `de`: `ID | Anforderung | Beschreibung | Epic | Cluster | Owner Kunde | Owner Strix | Status | Priorität | Scope | Design nötig? | Interface nötig? | Offene Fragen | Kommentar | Quelle | Heute live? | Hinweis (IST) | Shops`, A bis R
- `en`: `ID | Requirement | Description | Epic | Cluster | Customer owner | Strix owner | Status | Priority | Scope | Design needed? | Interface needed? | Open questions | Comment | Source | Live today? | Current state | Shops`, A bis R

| Spalte | Inhalt | Eigentümer |
|---|---|---|
| `ID` | `REQ-` und drei Ziffern (`REQ-001`), im Vorhaben eindeutig, ohne Cluster (§177, §230) | Repo: `id` |
| `Anforderung` | der Bedarf in wenigen Worten, wie erfasst; gilt sie nicht für alle Shops, steht der Shop-Bezug hinten in Klammern, `Staffelpreise (B2B)` (§307; [`datalayer-contract.md`](datalayer-contract.md), „Der Shop-Bezug“) | Repo: `title` und `shops` |
| `Beschreibung` | der erste Absatz des Soll-Zustands | Repo: `## Description` |
| `Epic` | die Kennung des einen Epics (§150); leer vor dem Schnitt | Repo: `epic` |
| `Cluster` | der Workstream (§336), wie ihn die Menschen bei Projektbeginn je Vorhaben schneiden (etwa `SHOP`, `DATA`, `CX`); eine Kategorie innerhalb eines Workstreams (Internationalisierung, B2B, UX/UI) steht nicht hier; gefiltert wird je Rolle über eine Filteransicht | Mensch |
| `Owner Kunde` | wer beim Kunden für die Anforderung spricht | Mensch |
| `Owner Strix` | wer bei uns für sie verantwortlich ist (§293) | Mensch |
| `Status` | Auswahl: Offen, Bestätigt, Verworfen, Duplikat (§283) | Repo: `status` |
| `Priorität` | Auswahl: Must-have, Nice-to-have; Must-have, solange der Kunde nichts anderes ausdrücklich sagt (§327) | Repo: `priority` |
| `Scope` | Auswahl: leer, In Scope, Out of Scope; leer bis zur Scope-Freigabe (§283) | Repo: `scope` |
| `Design nötig?` | ja, nein oder offen | Repo: `design_needed` |
| `Interface nötig?` | ja, nein oder offen: braucht die Lösung eine Schnittstelle, auch für Stammdaten aus PIM oder ERP (§205) | Repo: `interface_needed` |
| `Offene Fragen` | je offene Frage der Art `discovery`, die die Anforderung in `concerns` nennt, eine Zeile `GAP-007 ‹erster Satz der Frage›` (§279) | Repo: `gaps/` |
| `Kommentar` | frei; kein Lauf liest ihn als Antwort (§276) | Mensch |
| `Quelle` | Termin, Notiz, Chat mit dem Lead oder Zeile aus `architecture.md`, aus der die Anforderung entsteht; bei einer Teilung dazu „aufgeteilt aus ‹ID›“ (`en`: „split from ‹ID›“). Die festen Wendungen darin (`source_workshop`, `source_chat`, `source_corrected`, …) stehen in der Sprache des Projekts, nach [Die festen Wendungen](datalayer-contract.md#die-festen-wendungen) (§337) | Repo: `source` |
| `Heute live?` | Auswahl: Ja, Nein, Teilweise, Verifizieren; leer ohne bekannten Ist-Stand (§283) | Repo: `live` |
| `Hinweis (IST)` | der erste Absatz des Ist-Zustands, „ungeprüft“ (`en`: „unchecked“, §337), wenn das Material ihn nicht nennt | Repo: `## Current state` |
| `Shops` | die Schlüssel aller Shops, für die die Anforderung gilt, in Großbuchstaben, getrennt durch Komma und Leerzeichen, in der Folge von `shops` in `project.yml`: `B2C, B2B`; zum Filtern (§307) | Repo: `shops` |

**Die Spalte `Priorität` steht direkt vor `Scope`** (§327), weil beide zusammen gelesen werden:
eine Anforderung, die der Kunde braucht, und ob sie jetzt gebaut wird. **Die Spalte `Shops` steht am Ende.**

## Tab `Solutioning` (`Solutioning`) — eine Zeile je Anforderung

- `de`: `ID | Anforderung | Klassifizierung | Aufwand | Aufwand (h) | Lösungsoption 1 | Lösungsoption 2 | Lösungsoption 3 | Empfehlung | Offene Fragen / Entscheidungsbedarf | Abhängigkeiten | Solutioning-Status`, A bis L
- `en`: `ID | Requirement | Classification | Size | Effort (h) | Solution option 1 | Solution option 2 | Solution option 3 | Recommendation | Open questions / decisions | Dependencies | Solutioning status`, A bis L

**Jede Anforderung hat hier eine Zeile**, mit und ohne das Add-on `solutioning`. **Ein ungeprüfter
Lösungsansatz erscheint hier nicht** (§275): solange `solution_status` leer oder `proposed` ist, bleiben
`Klassifizierung`, `Aufwand`, die Lösungsoptionen, `Empfehlung` und `Abhängigkeiten` leer, und
`Solutioning-Status` zeigt Entwurf.

| Spalte | Inhalt | Eigentümer |
|---|---|---|
| `ID` | die Kennung der Anforderung | Repo: `id` |
| `Anforderung` | ihr Titel, wie im Tab `Anforderungen` mit dem Shop-Bezug hinten (§307) | Repo: `title` und `shops` |
| `Klassifizierung` | die Art des Lösungsansatzes in ihrer Anzeige, ohne Namen; trägt er zwei, beide mit „ + “ (§324) | Repo: `classification` |
| `Aufwand` | die Größe, `S` bis `XL`; nie Stunden (§280, Regel 10) | Repo: `size` |
| `Aufwand (h)` | Stunden je Anforderung, nur von einem Menschen (§280, Regel 10); kein Lauf hält sie gegen die Größe (§357). Nie die Modellschätzung `effort_estimate_model`, die keine Spalte hat (§357) | Mensch |
| `Lösungsoption 1` bis `3` | je Lösungsansatz aus `## Approach`, in der Folge der Datei, ihr Name (die App, der Konnektor, die Middleware), ihr Satz und darunter die Zeile `KB:` (§268) | Repo: `## Approach` |
| `Empfehlung` | der Name des gewählten Lösungsansatzes, des ersten in `## Approach` | Repo: `## Approach` |
| `Offene Fragen / Entscheidungsbedarf` | je offene Frage der Art `solutioning` oder `decision`, die die Anforderung in `concerns` nennt, eine Zeile `GAP-007 ‹erster Satz der Frage›` (§279) | Repo: `gaps/` |
| `Abhängigkeiten` | die Kennungen von Anforderungen, Epics und ADRs, auf denen der Lösungsansatz aufbaut, getrennt durch Komma | Repo: `depends_on` |
| `Solutioning-Status` | Entwurf, Entschieden oder Blocker | Repo: `solution_status` |

## Tab `Epics` (`Epics`) — eine Zeile je Epic

- `de`: `Epic-ID | Domäne | Epic | Kurzbeschreibung | Anforderungen | Status | Informationsstand | Klärungsbedarf | Owner Strix | Owner Kunde | Aufwand (h) | Geprüft von | Geprüft am | Entwurf | Epic Page | Board-Schlüssel`, A bis P
- `en`: `Epic ID | Domain | Epic | Summary | Requirements | Status | Information | Clarification | Strix owner | Customer owner | Effort (h) | Reviewed by | Reviewed on | Draft | Epic page | Board key`, A bis P

| Spalte | Inhalt | Eigentümer |
|---|---|---|
| `Epic-ID` | `EP-` und drei Ziffern (`EP-001`), nie neu vergeben | Repo: `id` |
| `Domäne` | eine aus der festen Liste (§252), ihr Anzeigewert oben | Repo: `domain` |
| `Epic` | der Titel | Repo: `title` |
| `Kurzbeschreibung` | das Kriterium des Schnitts in einem Satz; trägt ein Epic mehr als 12 Anforderungen, steht hier „Größe bestätigt“ (`en`: „Size confirmed“), sobald der Lead die Größe bestätigt hat | Repo: `summary` |
| `Anforderungen` | jede Anforderung, deren Feld `epic` dieses Epic nennt, aufsteigend, getrennt durch Komma und Leerzeichen, keine Bereiche | Repo: `epic` der Anforderungen |
| `Status` | Offen, In Bearbeitung, Zur Abnahme, Interne Abnahme, Zusammengeführt, Aufgelöst | Repo: `status` |
| `Informationsstand` | Dünn, Teilweise oder Tragfähig | Repo: `information` |
| `Klärungsbedarf` | was das Epic aufhält, oder dass es bereit ist, als feste Wendung in der Sprache des Projekts, ohne Namen eines Skills und einer Datei (`clar_…` in [Die festen Wendungen](datalayer-contract.md#die-festen-wendungen), §337) | Repo: `clarification` |
| `Owner Strix` | wer bei uns für das Epic verantwortlich ist | Mensch |
| `Owner Kunde` | wer beim Kunden für das Epic spricht | Mensch |
| `Aufwand (h)` | die Summe von `Aufwand (h)` im Tab `Solutioning` über die Anforderungen, deren `Epic` dieses Epic nennt | Formel |
| `Geprüft von` | wer die Lösung des Epics ganz gelesen hat (§277) | Mensch |
| `Geprüft am` | wann | Mensch |
| `Entwurf` | der Link zum Entwurf im Drive | Repo: `draft` |
| `Epic Page` | der Link zur Epic Page in Confluence, mit `solutioning` für jedes freigegebene Epic; `solution-epic-page` trägt ihn nach der Übertragung ein (§313) | Repo: `epic_page` |
| `Board-Schlüssel` | der Schlüssel des Epic-Tickets (Jira: Vorgangsnummer, Asana: GID der Aufgabe; §310) | Repo: `board_key` |

**Die Formel in `Aufwand (h)`** steht einmal, in Zeile 2, und rechnet für jede Zeile darunter: sie
nimmt die IDs aus `Anforderungen`, deren `Epic` die `Epic-ID` der Zeile ist, und summiert ihre
Stunden aus `Solutioning`. `sheet-format.py --epic-hours` liefert sie, mit den Spalten aus den
Kopfzeilen oben und dem Trenner des Gebietsschemas; geschrieben wird sie mit dem Anlegen des
Sheets. Ungemessen ist, ob `update_values` sie in einem Sheet in `de_DE` und `en_US` annimmt.

## Tab `Offene Punkte` (`Open items`) — eine Zeile je offener Frage

- `de`: `GAP-ID | Art | Frage | An | Betrifft | Blockiert | Verantwortlich | Bis`, A bis H
- `en`: `GAP ID | Kind | Question | To | Concerns | Blocking | Responsible | Due`, A bis H

| Spalte | Inhalt | Eigentümer |
|---|---|---|
| `GAP-ID` | `GAP-` und drei Ziffern | Repo: `id` |
| `Art` | Discovery, Solutioning oder Entscheidung | Repo: `kind` |
| `Frage` | die Frage, der Rumpf der Datei bis zur ersten Überschrift | Repo: Rumpf |
| `An` | an wen die Frage geht | Repo: `to` |
| `Betrifft` | die Kennungen aus `concerns`, getrennt durch Komma | Repo: `concerns` |
| `Blockiert` | Ja oder Nein | Repo: `blocking` |
| `Verantwortlich` | wer die Antwort beschafft | Mensch |
| `Bis` | bis wann | Mensch |

## Die Regeln, ohne die das Sheet driftet

- **Geschrieben wird nur in ein Sheet mit genau diesen Kopfzeilen**, in der Sprache aus `language`.
  Der Agent prüft die Kopfzeile jedes Tabs, den er beschreibt, mit `check-sheet.py --check header`;
  weicht Zeile 1 ab, schreibt er in den Tab nicht, statt in fremde Spalten zu schreiben. Umgestellt
  wird ein Sheet von Hand.
- **Eine Zeile je Kennung.** Eine neue Zeile kommt unter die letzte belegte; eine Kennung, die schon
  in der Spalte steht, schreibt der Agent nicht ein zweites Mal.
- **Gelöscht wird nur im Tab `Offene Punkte`.** Eine Anforderung und ein Epic bleiben mit ihrem
  Status stehen, auch `Verworfen`, `Duplikat` und `Aufgelöst`; eine geschlossene Frage fällt mit
  ihrer Zeile (oben).
- **Eine Spalte der Menschen und die Formel schreibt kein Lauf**; liegen die Spalten des Repos einer
  Zeile zu beiden Seiten einer solchen Spalte, sind es zwei Bereiche.
- **Geprüft wird auf dem Gelesenen**: `.claude/scripts/check-sheet.py` meldet `duplicate_id`
  auf dem Export von `Anforderungen`, dazu mit den Spalten `Epic-ID` und `Anforderungen` aus `Epics`
  `unassigned`, `multiple_epics` und `unknown_id`, und mit den IDs einer Seite `once_on_page`. Auf
  Aufruf prüft es mit `header` die Kopfzeile eines Tabs gegen diesen Vertrag und mit `cut` den
  Schnitt nach §252. Vor dem Schnitt läuft `duplicate_id` ohne die Epics.
