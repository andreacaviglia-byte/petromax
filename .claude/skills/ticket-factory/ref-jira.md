# Jira — der Connector

> **Gliederung ist Vertrag.** Jede Connector-Datei führt dieselben fünf Abschnitte in dieser
> Reihenfolge.

**Jira ist der Standard-Kanal.** Gelesen ist er gemessen, das Anlegen einer Story unter einem Epic
über den Connector nicht. Deshalb liest jeder Lauf das erste Epic, die erste Story und den ersten
Subtask, die er anlegt, sofort zurück und hält an, wenn nicht ankommt, was gesendet wurde (Abschnitt
„Rücklesen").

## Rollen — worauf sie in diesem Kanal zeigen

| Rolle | Im Kanal | Woher Kennung und Merkmal |
|---|---|---|
| `target` | Jira-Projekt | `board.project` ist der Projektschlüssel; der Klarname kommt je Lauf aus `listJiraProjects` (über `executeRead`) |
| `card_intake` | der Anfangsstatus des Workflows | ein neuer Vorgang startet dort von selbst; der Lauf übergibt keine `transition` |
| `card_wishlist` | der Status `Wunschliste` (`en`: `Wishlist`) des Workflows | ungemessen, ob es ihn als Status gibt; der Lauf liest die Übergänge der angelegten Story (Abschnitt „Wunschliste") |
| `card_epic` | Vorgangstyp `Epic` | Merkmal ist der Typname in `listJiraProjectIssueTypesMetadata` (über `executeRead`); **geschlossen** ist ein Epic, dessen `status.statusCategory.key` `done` ist |
| `card_subtask` | der Vorgangstyp der Ebene −1 | Merkmal ist `subtask: true` in `listJiraProjectIssueTypesMetadata`; sein Name je Projekt aus derselben Antwort |
| `field_category` | Systemfeld `components` („Komponenten") an der Story mit einem Gewerk und am Subtask | die Werte sind die `allowedValues` von `components` auf der Maske |
| `field_owner` | das Feld `Eigentümer` (`Owner`) an Epic und Story, im Referenzprojekt `customfield_11488` | ein Feld mit `schema.type: user` und diesem Namen auf der Maske; der Wert ist die `account_id` aus `atlassianUserInfo` |
| `field_size` | nicht angebunden | kein Größenfeld gemessen; der Lauf setzt in Jira keine Größe, und das ist kein Befund |

**Die cloudId** ist `confluence.cloud_id` aus `project.yml`, wenn sie gesetzt ist. Ist sie leer, nimmt
der Lauf den einen Eintrag aus `getAccessibleAtlassianResources`, der Jira-Scopes trägt; sind es
mehrere, fragt er den Lead und legt ihm die `url` der Einträge vor.

**Das Epic und die Story mit mehreren Gewerken tragen keine Komponente** (§281). Die
Abbildung der Gewerke: `DEV` → `DEV`, `Konfig` → `Konfig`, `Schnittstelle` →
`Schnittstelle`, `UX/UI` → `UX/UI`. Der Lauf sucht den abgebildeten Namen **exakt** in den
`allowedValues` und nimmt dessen `id`. Fehlt er, hält er vor der Vorschau an und nennt Gewerk und
Komponente.

**Der Owner ist die Person, die den Lauf startet** (§281): der Atlassian-Connector handelt mit ihrem
Konto, und `atlassianUserInfo` nennt ihre `account_id`. Steht kein solches Feld auf der Maske von Epic
oder Story, oder sind es mehrere, nennt die Vorschau es, und das Ticket entsteht ohne Owner; ein Label
oder eine Komponente mit dem Workstream setzt der Lauf nie, auch kein Label `DEV`.

## Die Aufrufe

Die Werkzeuge kommen vom Atlassian-Connector. Hol ihr Schema über die Werkzeug-Suche, bevor du das
erste Feld setzt; verglichen wird die Endung des Namens.
**„Nicht verbunden“ meldest du erst, wenn die Werkzeug-Suche das Werkzeug nicht findet**: nach
einer Wiederaufnahme kann ein Connector zu Beginn eines Turns in der Liste der Werkzeuge noch fehlen
(Nachtest vom 30.09.2026). **Die Lesewerkzeuge** `listJiraProjects`, `listJiraProjectIssueTypesMetadata`,
`getJiraIssueTypeMetaWithFields` und `listJiraIssueTransitions` bietet der Atlassian-Connector nicht
direkt an; sie laufen über `executeRead` mit `name`, `cloudId` und `inputs` (gemessen am 11.10.2026).
Die Namen hier sind die dieses Stands: fehlt einer, suchst du die Operation nach ihrem Zweck über
`discover` (Connector-Vertrag, Der Preflight).

### Das Board eintragen — nur, wenn `board.*` leer ist

Aus dem Link liest du die Site und den Projektschlüssel (`…/projects/<KEY>/…` oder
`…/browse/<KEY>-…`). `getAccessibleAtlassianResources`: nimm die `id` des Eintrags mit Jira-Scopes für
diese Site. Ist `confluence.cloud_id` gesetzt und eine andere, halte an: der Steckbrief hat für eine
zweite Site kein Feld. Dann `listJiraProjects` über `executeRead` mit dieser `id` und `query` = Schlüssel:
gültig ist nur ein Treffer mit **exakt** gleichem `key`, bei einem Teiltreffer fragst du. Erst danach
stehen `board.tool: jira` und `board.project` = der Schlüssel (SKILL.md, Step 1); zeig den
Projektnamen im Klarnamen.

### Ziel auflösen — vor der Vorschau

1. `getAccessibleAtlassianResources`: der Eintrag mit der cloudId muss Jira-Scopes tragen; seine
   `url` ist die Site für die Links. Trägt er keine, halte an.
2. `listJiraProjects` über `executeRead` mit `query` = `board.project`: gültig ist nur ein Treffer mit
   **exakt** gleichem `key`. In der Vorschau steht „Jira-Projekt ‹Name› (‹Schlüssel›)".
3. `listJiraProjectIssueTypesMetadata` über `executeRead`: `Epic`, `Story` und genau ein Typ mit `subtask: true`
   müssen darunter sein, sonst halte an und nenne den fehlenden Typ.
4. `atlassianUserInfo`: die `account_id` für den Owner.

### Pflichtfelder lesen — je Lauf, vor der Vorschau

`getJiraIssueTypeMetaWithFields` über `executeRead` für `Epic`, `Story` und den Subtask-Typ, mit
`issueTypeId` aus der Liste der Vorgangstypen und `requiredFieldsOnly: false`. Daraus:

- **Pflicht** ist ein Feld mit `required: true` und ohne `hasDefaultValue: true`. Die Felder, die
  der Lauf selbst setzt (`project`, `issuetype`, `summary`, `description`, `parent`, `components`,
  das Owner-Feld), sind gedeckt. **Jedes übrige Pflichtfeld ist eine Frage an den Lead**, mit seinen
  `allowedValues`; die Antwort gilt für diesen Lauf und geht über `additional_fields` in jeden Aufruf.
- **Ausnahme „Type":** das Auswahlfeld „Type" (Werte `PROD`, `NONBILLABLE`, `ABSENCE`) ist keine
  Frage. Tickets dieser Strecke sind immer abrechenbar; der Lauf setzt `{"value": "PROD"}` und nennt
  es in der Vorschau. Fehlt `PROD` in den `allowedValues`, fragst du.
- **Die Epic-Anbindung der Story:** steht `parent` auf der Story-Maske, setzt der Lauf `parent` auf
  den Schlüssel des Epics. Nur wenn `parent` fehlt, nimmt er das Feld, dessen `schema.custom`
  `com.pyxis.greenhopper.jira:gh-epic-link` ist, über `additional_fields`.
- **Am Epic:** ist das Feld mit `schema.custom` `com.pyxis.greenhopper.jira:gh-epic-label`
  („Epic-Name") Pflicht, trägt es den Titel des Epics.
- **Das Owner-Feld** suchst du auf den Masken von Epic und Story beim Namen (Rolle `field_owner`).

### Bestand lesen — vor der Vorschau

`searchJiraIssuesUsingJql` mit `responseContentFormat: markdown`, blätternd über `nextPageToken`,
bis keine Seite mehr kommt:

- **Epics des Ziels:** `project = <Schlüssel> AND issuetype = Epic`, Felder `summary`,
  `description`, `status`. Daraus Titel, Block `Ziel`, die Zeile `Beauftragung:` im Block `Kontext`,
  `Schlüssel: EP-…` und offen oder geschlossen.
- **Stories eines Epics:** `parent = <Epic-Schlüssel>`, Felder `summary`, `description`,
  `components`.
- **Subtasks einer Story:** `parent = <Story-Schlüssel>`, Felder `summary`, `description`,
  `components`.

`summary ~` und `text ~` sind Textsuchen und treffen auch Teilwörter. **Belegt ist ein Ticket erst
durch die Zeilen `Schlüssel: <Kennung>` und `Beauftragung: <key>` in seiner Beschreibung**, beide
exakt verglichen ([ref-epic-cut.md](ref-epic-cut.md)); ein gleicher Titel ohne sie ist ein Kandidat,
den du vorlegst.

**Vor jeder Änderung an einem bestehenden Vorgang** liest du ihn mit `getJiraIssue`, Felder
`summary`, `description`, `components`, `status`, und `responseContentFormat: markdown` (§280,
Regel 7).

### Anlegen

`createJiraIssue`, **ein Vorgang je Aufruf**, erst das Epic, dann je Story die Story und ihre
Subtasks in der Folge ihrer Nummer:

| Parameter | Epic | Story | Subtask |
|---|---|---|---|
| `cloudId` | die cloudId aus „Rollen" | dito | dito |
| `projectKey` | `board.project` | dito | dito |
| `issueTypeName` | `Epic` | `Story` | der Name des Subtask-Typs |
| `summary` | `EP-012 ‹Titel des Epics›`, im Expert Service `‹Titel des Epics›` | `REQ-012 ‹Titel› ‹Shop-Bezug›` | `REQ-012-1 ‹Aufgabe›` |
| `description`, `contentFormat: markdown` | der geprüfte Body der Stufe `epic` | der geprüfte Body der Stufe `story` oder `story --split` | der geprüfte Body der Stufe `subtask` |
| `parent` | — | Schlüssel des Epics, wenn `parent` auf der Maske steht | Schlüssel der Story |
| `additional_fields` | „Type", die gefragten Pflichtwerte, der Epic-Name, wo Pflicht, das Owner-Feld `{"<feld-id>": {"accountId": "<account_id>"}}` | „Type", die gefragten Pflichtwerte, das Owner-Feld, bei einem Gewerk `"components": [{"id": "<id>"}]`, sonst das Epic-Link-Feld | „Type", die gefragten Pflichtwerte, `"components": [{"id": "<id>"}]` |

Kein `assignee_account_id`, kein Label. Die Antwort trägt den Schlüssel; der Link ist
`<url der Site>/browse/<Schlüssel>`.

### Wunschliste

**Eine Story mit `scope: out_of_scope` gehört in die Wunschliste** (§284). Nach dem Anlegen liest der
Lauf mit `listJiraIssueTransitions` über `executeRead` ihre Übergänge. Führt genau einer in einen Status mit dem Namen
`Wunschliste` (`Wishlist`), ruft er `transitionJiraIssue` mit dessen `id`; ihre Subtasks bleiben im
Anfangsstatus. Führt keiner oder mehr als einer dorthin, bleibt die Story im Anfangsstatus, und der
Bericht nennt sie, damit ein Mensch sie verschiebt. Einen anderen Übergang ruft der Lauf nie.

### Ändern

`editJiraIssue`, nur an einem Vorgang, den der Lauf direkt davor gelesen und dessen Abweichungen der
Lead in der Vorschau gesehen hat, und nur `description` (`contentFormat: markdown`) und `summary`;
`summary`, wenn der Titel vom Titel aus dem Repo mit Shop-Bezug abweicht (§307), und die Vorschau
zeigt den alten und den neuen Titel.
Komponente und Owner erreicht die Bearbeiten-Maske nicht (Gemessene Grenzen): baut der Lauf eine Story
um, weil ein Gewerk dazukommt, nennt der Bericht die Komponente, die ein Mensch an ihr entfernt.

### Rücklesen

Nach dem ersten Epic, der ersten Story und dem ersten Subtask eines Laufs: `getJiraIssue` mit
`fields: ["summary", "description", "parent", "issuetype", "components", "<Owner-Feld>"]` und
`responseContentFormat: markdown`; nach der ersten Änderung ebenso. Weiter geht es nur, wenn die
Beschreibung alle Überschriften des Bodys trägt, an Story und Subtask die Zeilen `Beauftragung:` und
`Schlüssel:`, am Epic `Beauftragung:` und im Projekt `Schlüssel:`; `parent` der Story auf das Epic zeigt und der des
Subtasks auf die Story; die Story mit einem Gewerk und der Subtask die Komponente ihres Gewerks
tragen, das Epic und die Story mit mehreren Gewerken keine; und das Owner-Feld an Epic und Story die
`account_id` trägt. Sonst halte an: „Der Vorgang ‹Schlüssel› kam ohne ‹was› an. Ich habe bis hier
angelegt: …" Den halben Vorgang entfernt ein Mensch.

### Was dieser Lauf hier nie ruft

`addOrEditJiraIssueComment`, eine Zeitbuchung und eine Verknüpfung von Vorgängen rufst du nicht auf: der Lauf
schreibt keinen Kommentar, bucht keine Zeit und verknüpft keine Vorgänge. `transitionJiraIssue` nur
in die Wunschliste, `editJiraIssue` nur nach „Ändern".

## Gemessene Grenzen

| Fähigkeit | Jira |
|---|---|
| **Mehrere Vorgänge je Aufruf** | nein, einer je Aufruf |
| **Ebenen** | `Epic` (Rang 1) über `Story`, `Task`, `Bug` (Rang 0) über dem Subtask-Typ (Rang −1) |
| **Epic-Anbindung einer Story** | `parent` und das Epic-Link-Feld stehen beide auf der Maske, beide nicht Pflicht; drei aktuelle Stories des gemessenen Projekts hängen über `parent` |
| **Subtask unter einer Story, mit Komponente und „Type" über `additional_fields`** | kommt an (gemessen 25.09.2026) |
| **Spalte bei der Anlage** | nein; die Spalte ist eine Board-Einstellung über den Status |
| **Nachträglich ändern** | `editJiraIssue` erreicht vier Felder: Titel, Typ, Beschreibung, zugewiesene Person |
| **Pflichtfelder** | projektabhängig: im einen Projekt ein Pflicht-Auswahlfeld ohne Voreinstellung, im anderen `reporter` mit Voreinstellung |
| **Komponenten im Referenzprojekt** | `Konfig`, `DEV`, `UX/UI`, `Schnittstelle` |
| **Owner-Feld im Referenzprojekt** | `Eigentümer`, `customfield_11488`, auf den Masken von Story und Epic; gesetzt an 2 Test-Vorgängen (08.10.2026) |
| **DEV-Ansicht im Referenzprojekt** | filtert auf `labels = DEV`; das Label setzt ein Mensch (08.10.2026) |

**Die Werteliste der Anlage-Maske ist projektspezifisch und vorab lesbar.** Was nicht darin steht,
ist in diesem Projekt nicht setzbar, und das fällt vor dem ersten Aufruf auf.

## Was der Kanal nicht kann

- **Mehrere Vorgänge je Aufruf.** Zwanzig Stories sind zwanzig Aufrufe.
- **Eine Spalte setzen, ein Board anlegen.** Keine Board-Werkzeuge; die Spalte folgt dem Status.
- **Komponente oder Owner nachträglich ändern.** Vier Felder auf der Bearbeiten-Maske.
- **Einen Vorgang löschen.** Der Connector führt kein Werkzeug dafür.

## Unter welcher Bedingung gemessen wurde

**Rein lesend, am 25.09.2026**, über den Atlassian-Connector: Vorgangstypen und Anlage-Masken von
Epic, Story und Task in einem aktiven Kundenprojekt der eigenen Instanz als Stellvertreter des
Referenzprojekts und in zwei Testprojekten; die Epic-Anbindung an den drei zuletzt geänderten Stories
des Stellvertreters; die Komponenten des Referenzprojekts. **Rein lesend, am 16.08.2026**, in einem
internen Projekt: die Bearbeiten-Maske und die Signaturen der Werkzeuge. **Schreibend, am
25.09.2026**, im Referenzprojekt: ein Subtask unter einer Test-Story, mit Komponente und „Type",
zurückgelesen. **Rein lesend, am 08.10.2026**, im Referenzprojekt: das Feld `Eigentümer` auf den
Masken und der Filter der DEV-Ansicht.

**Ungemessen und deshalb im Lauf zurückgelesen:** ob `createJiraIssue` mit `parent` eine Story an
ein Epic hängt (das Schema beschreibt `parent` als „Parent for subtasks"); wie die Beschreibung mit
`contentFormat: markdown` ankommt; ob das Owner-Feld über `additional_fields` ankommt; ob `text ~`
einen eben angelegten Vorgang sofort findet; ob ein Größenfeld auf einer Story-Maske steht; ob die
Wunschliste ein Status ist und wie er heißt; ob `editJiraIssue` die Beschreibung in Markdown annimmt.
