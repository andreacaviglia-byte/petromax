# Asana — der Connector

> **Gliederung ist Vertrag.** Jede Connector-Datei führt dieselben fünf Abschnitte in dieser
> Reihenfolge.

**Asana ist die Variante**, schreibend gemessen. Der Lauf legt Tasks in einem bestehenden Projekt an;
ein Projekt legt er nie an.

## Rollen — worauf sie in diesem Kanal zeigen

| Rolle | Im Kanal | Woher Kennung und Merkmal |
|---|---|---|
| `target` | Asana-Projekt | `board.project` ist die Projekt-GID; der Klarname kommt je Lauf aus `get_project` |
| `card_intake` | die Section, deren Name mit `To be defined` beginnt, im Testprojekt `To be defined (Lead)` | Merkmal ist der Anfang des Namens; die GID liest der Lauf je Lauf aus `get_project` mit `include_sections` |
| `card_wishlist` | die Section, deren Name mit `Wunschliste` (`en`: `Wishlist`) beginnt, im Testprojekt `Wunschliste (PM & Lead)` | Merkmal ist der Anfang des Namens; die GID aus derselben Antwort |
| `card_epic` | dieselbe Section wie `card_intake` (§121) | Asana kennt keinen Typ Epic. Das Epic-Ticket ist ein Task ohne `parent`, der `Beauftragung:` oder `Schlüssel: EP-…` trägt oder Parent einer Story mit `Schlüssel: REQ-…` ist; als eigenes zählt nur eines mit der eigenen `Beauftragung:` (`ref-epic-cut.md`); **geschlossen** ist er mit `completed: true` |
| `card_subtask` | ein Task mit der Story als `parent`, im Projekt und in der Section seiner Story | Merkmal ist der `parent` und die Zeile `Schlüssel: REQ-…-n` |
| `field_category` | Custom Field `Kategorie` an der Story mit einem Gewerk und am Subtask | am Projekt gelesen, mit Aktiv-Kennzeichen |
| `field_owner` | Custom Field `Owner` an Epic-Ticket und Story | am Projekt gelesen; der Wert ist die GID aus `get_me` |
| `field_size` | Custom Field `Aufwand` an der Story | am Projekt gelesen, mit Aktiv-Kennzeichen |

**Die Kategorie ist das Gewerk.** Das Epic-Ticket und die Story mit mehreren Gewerken bleiben ohne
`Kategorie`, das Epic-Ticket auch ohne `Aufwand` (§281). Die Abbildung der Gewerke:

| Gewerk | Wert von `Kategorie` |
|---|---|
| `DEV` | `DEV` |
| `Konfig` | `Konfig` |
| `Schnittstelle` | `Schnittstelle` |
| `UX/UI` | `UX/UI` |

Der Lauf sucht den Wert **exakt** unter den Optionen mit `enabled: true` und nimmt dessen GID, jedes
Mal frisch; eine GID steht in keiner Datei. Fehlt er oder ist er abgeschaltet, hält der Lauf vor der
Vorschau an und nennt Gewerk und Wert: anschalten kann ihn nur ein Mensch, weil das Feld im ganzen
Workspace gilt. Den Wert `Integration` setzt der Lauf nie, auch wenn er im Feld steht. Einen Wert mit
dem Workstream (`DATA`, `CX`, `SHOP`) setzt er nie (§281).

**Die Größe geht in `Aufwand`**, wenn die Anforderung `size` trägt, nur an der Story. `S`, `M`, `L`
gehen 1:1, `XL` wird `L`, und die Vorschau nennt die Abbildung. Ohne `size` bleibt das Feld leer. Ist
der Zielwert abgeschaltet, bleibt es leer, und die Vorschau nennt es.

**Der Owner ist die Person, die den Lauf startet** (§281): der Asana-Connector handelt mit ihrem
Konto, und `get_me` nennt ihre GID. Führt das Projekt kein Feld `Owner`, nennt die Vorschau es, und
die Tickets entstehen ohne Owner.

## Die Aufrufe

Die Werkzeuge kommen vom Asana-Connector. Hol ihr Schema über die Werkzeug-Suche, bevor du das erste
Feld setzt. `search_tasks` benutzt der Lauf nie (Abschnitt „Gemessene Grenzen").
**„Nicht verbunden“ meldest du erst, wenn die Werkzeug-Suche das Werkzeug nicht findet**: nach
einer Wiederaufnahme kann ein Connector zu Beginn eines Turns in der Liste der Werkzeuge noch fehlen
(Nachtest vom 30.09.2026).

### Das Board eintragen — nur, wenn `board.*` leer ist

Aus dem Link liest du die Projekt-GID (die lange Zahl nach `/project/` oder nach `/0/`). `get_project`
mit der GID: das Projekt existiert und ist nicht archiviert. Erst danach stehen `board.tool: asana`
und `board.project` = die GID (SKILL.md, Step 1); zeig den Projektnamen im Klarnamen.

### Ziel auflösen und Felder lesen — vor der Vorschau

`get_project` mit `project_id` = `board.project`, `include_sections: true` und
`opt_fields: name,archived,custom_field_settings.custom_field.name,custom_field_settings.custom_field.gid,custom_field_settings.custom_field.type,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_options.gid,custom_field_settings.custom_field.enum_options.enabled`.
Dazu `get_me` für die GID des Owners.

- `name` ist der Klarname in der Vorschau („Asana-Projekt ‹Name›"); ein archiviertes Projekt ist ein Halt.
- **Die Sections** für den Eingang und, wenn eine Anforderung `out_of_scope` trägt, für die
  Wunschliste suchst du in `sections` am Anfang des Namens: `To be defined` und `Wunschliste`
  (`Wishlist`), ohne Rücksicht auf Groß- und Kleinschreibung. Die Boards hängen die Rolle in Klammern
  an, im Testprojekt `To be defined (Lead)` und `Wunschliste (PM & Lead)` (zweite Proberunde,
  10.10.2026: der volle Name `Wunschliste` fand nichts). Genau ein Treffer: seine GID. Kein oder mehr
  als ein Treffer: frag den Lead nach der Spalte und leg ihm die Namen vor. Die GID wird nie geraten.
- **`Kategorie`, `Aufwand` und `Owner`** suchst du in `custom_field_settings` beim Namen. Das `enabled`
  ist der Punkt des Aufrufs: ohne es sieht ein abgeschalteter Wert aus wie ein gültiger, und der
  Schreibversuch scheitert erst mitten im Anlegen.

### Bestand lesen — vor der Vorschau

`get_tasks` mit `project` = `board.project`, `limit: 20`,
`opt_fields: name,notes,parent.gid,completed,permalink_url`, **Seite für Seite** über `offset`, bis
keine Seite mehr kommt. **Gelesen wird das ganze Projekt, nie nur eine Section**: ein Epic in einer
späteren Section ist sonst keine Überschneidung. Mehr Felder fragst du nicht ab: `notes` trägt den
ganzen Text jedes Tasks, und mit `limit: 100` kam eine Seite mit 92 Tasks auf 93.000 Zeichen und landete
als Datei (Kettentest vom 30.09.2026). Nach jeder Seite hältst du aus ihr fest, was der Abgleich
braucht, und gehst zur nächsten; gesammelt wird der Auszug, nicht die Antwort.

Daraus: die Epic-Tickets mit Titel, Block `Ziel`, `completed` und der Zeile `Beauftragung:`; je Story
und Subtask sein Parent, Titel, Block `User Story` und die Zeilen `Beauftragung:` und `Schlüssel:`.
**Belegt ist ein Ticket erst durch die Zeilen `Schlüssel: <Kennung>` und `Beauftragung: <key>` in
`notes`**, beide exakt verglichen ([ref-epic-cut.md](ref-epic-cut.md)); ein gleicher `name` ohne
sie ist ein Kandidat, den du vorlegst. Bestehende Tasks ohne einen Schlüssel dieses Laufs fasst der
Lauf nicht an. **Vor jeder Änderung an einem bestehenden Task** ist dieser Auszug die Lesung; liegt
sie länger als die Vorschau zurück, liest du die Section des Tasks neu (§280, Regel 7).

### Anlegen

`create_tasks`, erst das Epic-Ticket allein, dann die Stories dieses Epics in einem Aufruf (bis 50),
dann die Subtasks je Story in einem Aufruf, in der Folge ihrer Nummer:

| Feld | Epic-Ticket | Story | Subtask |
|---|---|---|---|
| `name` | `EP-012 ‹Titel des Epics›`, im Expert Service `‹Titel des Epics›` | `REQ-012 ‹Titel› ‹Shop-Bezug›` | `REQ-012-1 ‹Aufgabe›` |
| `html_notes` | der geprüfte Body der Stufe `epic` | der geprüfte Body der Stufe `story` oder `story --split` | der geprüfte Body der Stufe `subtask` |
| `project_id` | `board.project` | dito | dito |
| `section_id` | GID von `card_intake` | GID von `card_intake`, bei `out_of_scope` von `card_wishlist` | die Section seiner Story |
| `parent` | — | GID des Epic-Tickets | GID der Story |
| `custom_fields` | **als JSON-String**: `Owner` | `Owner`, bei einem Gewerk `Kategorie`, `Aufwand` nur mit Größe | `Kategorie` |

Die Werte stehen als `"{\"<feld-gid>\": \"<option-gid>\"}"`, `Owner` als
`"<owner-gid>": ["<gid aus get_me>"]`. Die Story hängt so unter dem Epic-Ticket **und** liegt in ihrer
Section; das ist die Epic-Anbindung dieses Kanals. Der Link ist `permalink_url` aus der Antwort, sonst
aus `get_tasks`.

### Ändern

`update_tasks`, nur an einem Task, den der Lauf direkt davor gelesen und dessen Abweichungen der Lead
in der Vorschau gesehen hat: `html_notes` mit dem geprüften Body, `name`, wenn der Titel vom Titel
aus dem Repo mit Shop-Bezug abweicht (§307; die Vorschau zeigt den alten und den neuen Titel), und
beim Umbau einer Story, weil ein Gewerk dazukommt, `custom_fields` mit leerem `Kategorie`. Sonst
ändert der Lauf an einem bestehenden Task nichts.

### Rücklesen

**Das erste Epic-Ticket, die erste Story, den ersten Subtask und die erste Änderung eines Laufs liest
du zurück**, mit `get_tasks` auf `section` = die Section des Tasks, `limit: 20` und
`opt_fields: name,notes,parent.gid,completed,custom_fields.name,custom_fields.display_value`, Seite
für Seite über `offset`, bis die GID darunter ist. Das Epic-Ticket hat kein `parent`, keinen Wert in
`Kategorie` und `Aufwand`, `Owner` trägt die Person des Laufs, und `notes` trägt die Zeile
`Beauftragung:`, im Projekt dazu `Schlüssel: EP-…`. Die Story hat das Epic-Ticket als `parent`,
`Owner` trägt die Person des Laufs, `Kategorie` den Wert ihres Gewerks oder, mit mehreren Gewerken,
keinen, und `notes` die Zeilen `Beauftragung:` und `Schlüssel:`. Der Subtask hat die Story als
`parent`, `Kategorie` den Wert seines Gewerks und die Zeilen `Beauftragung:` und `Schlüssel:`. Sonst halte an und nenne, was bis dahin angelegt ist.
`get_task` gehört nicht zu diesem Kanal: die Liste liest, was der Abgleich liest.

### Der Text

`html_notes` mit **einem** Wurzelelement `<body>`, **eine** Zeile ohne Umbrüche zwischen den
Elementen: ein `\n` hinter `</h2>` erzeugt in der Ansicht eine Leerzeile. **`<br/>` wird abgelehnt.**
`&`, `<` und `>` müssen maskiert sein, sonst scheitert die Anlage mit `XML is invalid` und ohne Angabe
der Stelle. Den Weg aus der Markdown-Vorlage in diese Form gehen `markdown-to-body.py` und
`validate-html.sh`. Der Schlüssel steht als **letzte** Zeile im Block `Kontext`, nie in einem Linktext.

### Was dieser Lauf hier nie ruft

`add_comment` und `create_project_status_update` rufst du nicht auf. `create_project`, `delete_task`
und `search_tasks` ruft der Lauf nicht: er legt kein Projekt an, löscht nichts und sucht nicht im
Index. `update_tasks` nur nach „Ändern".

## Gemessene Grenzen

| Fähigkeit | Gemessen |
|---|---|
| **Mehrere Tickets je Aufruf** | ja, 1–50 |
| **Story unter Epic-Ticket und in der Section** | ja, mit `parent`, `project_id` und `section_id` zugleich |
| **Sections lesen** | ja, `get_project` mit `include_sections: true` liefert Name und GID, bis 50 Sections |
| **Ticket-Typ** | nein; Aufgabe, Meilenstein, Freigabe, kein Epic, keine Story |
| **Custom Field anlegen** | nein; ein Projekt aus der Vorlage bringt `Kategorie` und `Aufwand` mit |
| **Abgeschalteten Auswahlwert setzen** | nein, `bad_request` |
| **Deduplizieren** | nein; derselbe Aufruf zweimal ergibt zwei Tickets |
| **Tabelle in `html_notes`** | wird angenommen und bleibt erhalten; genutzt wird sie nicht, weil ihre Spalten im Ticket zu schmal stehen (§222) |
| **Frisch angelegter Task in `search_tasks`** | sofort nicht gefunden, nach rund 31 Sekunden gefunden |
| **Frisch angelegter Task in `get_tasks`** | sofort gefunden, über die Section und über das Projekt |
| **Werte im Testprojekt der Strecke** | `Kategorie` aktiv: `DEV`, `Schnittstelle`, `UX/UI`, `Konfig`, dazu `DATA`, `CX`, `SHOP`, `PM`, `Administration`; `Integration` abgeschaltet. `Aufwand` aktiv: `S`, `M`, `L`; `XS-S` und `XL` abgeschaltet |
| **Sections im Testprojekt** | `To be defined (Lead)`, `Interne QS (Lead)` und `Wunschliste (PM & Lead)` stehen, eine Section „Dokumentation" nicht (Wunschliste gemessen 10.10.2026) |

**Deshalb liest der Abgleich die Liste des Projekts, nie die Suche.** Ein Index, der nachläuft,
meldet ein eben angelegtes Ticket als fehlend, und der nächste Lauf legt es ein zweites Mal an. Dazu
beschreibt das Schema `search_tasks` als „Premium accounts only" und verweist sonst auf `get_tasks`.

**Ein abgeschalteter Auswahlwert ist kein Wert.** Das Feld hängt am Workspace, nicht am Projekt: wer
einen Wert abschaltet, ändert ihn für jedes Projekt. Deshalb liest jeder Lauf die Werte vorher.

**Der Linktext überlebt den Weg in den Plaintext nicht.** Dasselbe Ticket liegt in `html_notes` und
in `notes`; in `notes` ist der Linktext durch die URL ersetzt. Der Abgleich liest `notes`.

## Was der Kanal nicht kann

- **Custom Fields oder Auswahlwerte anlegen oder einschalten.** Führt ein Projekt ein Feld nicht,
  bleibt es leer, und der Bericht nennt es.
- **Projekte löschen.** Ein versehentlich angelegtes Projekt bleibt stehen.
- **Deduplizieren.** Derselbe Aufruf zweimal ergibt zwei Tickets.

## Unter welcher Bedingung gemessen wurde

**16.08.2026,** drei Läufe mit echten Tickets in einem Wegwerf-Projekt ohne Felder und in einer Kopie
des Template-Projektboards: mehrere Tickets je Aufruf, Ebenen, Felder, Text. **27. und 28.08.2026,**
zwei angelegte Tickets: Plaintext-Feld und Zeilenumbruch im Body. **25.09.2026,** im Testprojekt der
Strecke, einer Kopie der Vorlage mit fremden Tasks, die kein Lauf ändert: Sections mit
`include_sections`, Tabelle in `html_notes`, Auffindbarkeit eines frischen Tasks über `search_tasks`
und `get_tasks`. **30.09.2026,** rein lesend mit `get_project` im selben Testprojekt: die Werte von
`Kategorie` und `Aufwand` samt `enabled` und die Sections.

**Ungemessen und deshalb im Lauf zurückgelesen:** ob drei Ebenen tragen, ein Subtask unter einer
Story mit `project_id` und `section_id` (§281: das sagt der Product Owner, gemessen ist es nicht); ob
`custom_fields` mit mehreren Feldern und dem Personenfeld `Owner` ankommt; ob das Projekt ein Feld
`Owner` führt; ob `update_tasks` `html_notes` und ein leeres
`Kategorie` annimmt; ob `get_tasks` auf die Section `custom_fields.display_value` liefert.
