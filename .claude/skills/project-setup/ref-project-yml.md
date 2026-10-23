# Den Steckbrief `project.yml` schreiben

## Das Schema

**Es steht nur im Datalayer-Vertrag**, `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt `project.yml`. Lies es dort, bevor du den Text baust; eine zweite Fassung hier liefe
auseinander. `${CLAUDE_SKILL_DIR}/../../scripts/check-project.py` prüft den Text gegen dieses Schema.
Für diesen Lauf gilt dazu:

- **Jedes Feld des Schemas steht im Text, auch leer, als `""`** (Listen als `[]`): so sieht der nächste
  Lauf, dass es fehlt, und das Script findet einen Tippfehler im Namen.
- **„noch offen" heißt leer**, nie ein Platzhalter wie `offen` oder `tbd`.
- `project_folder` ist die bestätigte ID aus Step 7, nie ein Name und nie ein Link.
- `key` ist aus dem Titel vorgeschlagen und bestätigt; steht er schon, änderst du ihn nicht (§233).
- `project_owner` ist der GitHub-Name aus `wow-guard.py --whoami` (SKILL.md, Step 5), nie gefragt,
  außer das Script kennt keinen; steht er schon, änderst du ihn nicht (§289, §294).
- `language` ist `de` oder `en` (§202).
- `shops`: ein Eintrag je Shop, auch je Expansion Store (§231). `plan` ist `plus` oder der Plan, wie
  der Admin ihn nennt; `markets` eine Liste der Länderkürzel (`[DE, AT]`). `jurisdiction` bleibt leer,
  bis der Skill fragt, der den Rechtsraum braucht: aus `markets` folgt kein Rechtsraum, ein Markt ist
  ein Verkaufsgebiet. `audience` ist `b2c`, `b2b` oder `both`, wie der Lead es sagt (§249); aus dem
  Schlüssel des Shops folgt es nicht. Der `key` steht im Feld `shops` von Anforderungen und ADRs und,
  groß geschrieben, hinten an ihrem Titel, `Staffelpreise (B2B)` (§307): kurz, wie das Team den Shop
  nennt.
- `team` (§360): je Person des Teams der Agentur `name`, wie er im Material steht, `role` (die
  Projektrolle: `sponsor`, `lead`, `solution_owner`, `associate`, `specialist`), `github` und beim
  Solution Owner `workstream`. Der `project_owner` steht darin mit der Rolle, die du ihn fragst.
  Menschen beim Kunden stehen nicht darin. Sagt der Lead „noch offen", bleibt es `[]`.
- `project_type` ist `project` oder `expert_service`, wie das Angebot es nennt (§303).
- `add_ons` ist eine Liste in eckigen Klammern aus `solutioning`, `design`, `content_migration` und
  `e2e_testing`, genau die Add-ons, die der Lead aus dem Angebot nennt (§303); keines heißt `[]`.
  Sagt der Lead zum Projekttyp „noch offen", bleiben beide leer.
- `requirements_sheet`, `e2e_sheet` und `figma` bleiben leer; sie tragen die Skills ein, die
  sie anlegen oder zuerst brauchen (§229).
- `confluence.space` und `confluence.parent_page` stehen in Anführungszeichen, damit ein persönlicher
  Space (`~…`) und eine Seiten-ID Text bleiben.
- Angaben, die dieser Lauf nicht berührt, schreibst du so zurück, wie du sie gelesen hast, auch
  Kommentare und Reihenfolge.

## Lesen und schreiben

| Fall | Weg |
|---|---|
| lesen | lies `project.yml` |
| neu | leg `project.yml` an, mit dem ganzen Text |
| steht schon | überschreib `project.yml` ganz, mit dem ganzen Text |

Du überschreibst die ganze Datei, keine Teiländerung. Deshalb liest du direkt davor und schreibst den
vollständigen Text; danach liest du ihn zurück und lässt das Script laufen.

## Den Projektordner zeigen

| Zweck | Aufruf |
|---|---|
| der Ordner selbst | `Google_Drive.get_file_metadata` mit `fileId` = die ID aus dem Link (`/folders/<ID>`) |
| seine oberste Ebene | `Google_Drive.search_files` mit `query` = `parentId = '<ID>'`, `excludeContentSnippets: true`, jede Seite über `pageToken` |

`search_files` nie ohne `parentId`. Ob die Liste Dateien im Papierkorb mitliefert, ist ungemessen; der
Lead sieht die Liste und bestätigt den Ordner, nicht jede Datei darin.

## Board und Space prüfen

**Board, Jira.** Aus dem Link liest du die Site und den Projektschlüssel (`…/projects/<KEY>/…` oder
`…/browse/<KEY>-…`). `getAccessibleAtlassianResources` liefert je Produkt einen Eintrag; nimm die `id`
des Eintrags mit Jira-Scopes für diese Site. `listJiraProjects` über `executeRead` mit dieser `id` und
`query` = Projektschlüssel; gültig ist nur ein Treffer mit **exakt** gleichem `key`, bei einem
Teiltreffer fragst du. Dann `board.tool: jira`, `board.project` = der Schlüssel. Zeig den Projektnamen
im Klarnamen.

**Board, Asana.** Aus dem Link liest du die Projekt-GID (die lange Zahl nach `/project/` oder nach
`/0/`). `get_project` mit der GID: das Projekt existiert und ist nicht archiviert. Dann
`board.tool: asana`, `board.project` = die GID. Zeig den Projektnamen im Klarnamen.

**Confluence.** Aus dem Link liest du die Site und den Space-Schlüssel (`…/wiki/spaces/<KEY>/…`).
Nimm aus `getAccessibleAtlassianResources` die `id` des Eintrags mit Confluence-Scopes für diese Site.
**Als `cloud_id` steht nur diese UUID, nie der Hostname**: mit dem Hostnamen scheitern die Aufrufe,
obwohl die Werkzeugbeschreibung ihn anbietet. Dann `executeRead` mit `name: getConfluenceSpace`, `cloudId` und
`inputs: {spaceIdOrKey: ‹Space-Schlüssel›}`: der Space existiert, sonst fragst du. `confluence.space` = der Schlüssel, in Anführungszeichen. Die
Elternseite fragt `solution-epic-page`, wenn es die erste Seite überträgt. Liegen Board und Space in Jira
auf verschiedenen Sites, **halte an**: der Steckbrief hat für eine zweite Site kein Feld.

## Die Fragen des ersten Laufs

Was nie im Material steht. Du stellst sie **alle in einer Nachricht**, als nummerierte Liste.

| Feld | Frage |
|---|---|
| `project_folder` | Der Ordner des Vorhabens im Drive, als Link oder ID; nicht der Kundenordner (§229) |
| `language` | In welcher Sprache wird geschrieben, `de` oder `en`? Eine Variante (`de-CH`) nimmst du nicht an, du fragst, welche der beiden gilt (§202) |
| `board` | Der Link zum Board, Jira oder Asana |
| `confluence` | Der Link zum Confluence-Space |
| `team` | Wer arbeitet bei uns im Vorhaben mit? Je Person Name, Projektrolle und GitHub-Name, beim Solution Owner der Workstream; zuerst deine eigene Rolle. Darüber gehen die Aufgaben in `todo/` an die richtige Person (§360) |

## Die Fragen des Steckbriefs

Was im Material steht; der Steckbrief schlägt es nach [ref-steckbrief.md](ref-steckbrief.md) mit
Fundstelle vor. Diese Fragen stellst du nur, wenn in `inputs/` kein Material liegt, und dann **alle
in einer Nachricht**.

| Feld | Frage |
|---|---|
| `customer` | Wie heißt der Kunde? |
| `title` | Wie heißt das Vorhaben? |
| `key` | Eine kurze Kennung des Vorhabens, klein, `a-z`, `0-9`, `-` und `_` (`relaunch`); sie steht an jedem Epic-Ticket in der Zeile `Beauftragung:` (§233). Du schlägst sie aus dem Titel vor. Steht sie schon, änderst du sie nicht |
| `shops` | Ein Shop oder mehrere? Je Shop: Domain, ob er auf Shopify Plus läuft (sonst der Plan, wie der Admin ihn nennt), welche Märkte er über Markets bedient, und an wen er verkauft: an Verbraucher (`b2c`), an Händler (`b2b`) oder an beide (`both`) (§249). **Ein Expansion Store ist ein eigener Shop** mit eigenem Eintrag (§231). Den Schlüssel je Shop schlägst du vor (`b2c`, `b2b`, `ch`), der Lead bestätigt ihn |
| `project_type` | Ist das Vorhaben laut unterschriebenem Angebot ein Projekt (`project`) oder ein Expert Service (`expert_service`)? (§303) |
| `add_ons` | Welche Add-ons nennt das unterschriebene Angebot: Solutioning (`solutioning`), Design (`design`), Content-Migration (`content_migration`), E2E-Testing (`e2e_testing`)? Was nicht verkauft ist, fehlt in der Liste. Setup, Datenmigration und Theme-Arbeit sind keine Add-ons, sie kommen aus dem Material (§303) |

## Die Vorschau

**Der Lead bestätigt eine Tabelle in Klartext, kein YAML.** Je Feld des Schemas eine Zeile, auch die
leeren, in dieser Folge: Kunde, Vorhaben, Kennung, Sprache, Projektordner, Projekt-Owner, Projekttyp,
Add-ons, Board, Confluence, Anforderungsliste, E2E-Sheet, Figma. Shops und Team stehen darunter als
eigene Tabellen, je Shop und je Person eine Zeile.

| Spalte | Inhalt |
|---|---|
| Feld | die Bezeichnung in Klartext, dahinter der Schlüssel in Backticks |
| Wert | lesbar: der Projektordner mit Titel und Link, das Board mit Projektnamen, ein Add-on ausgeschrieben |
| Woher | „von dir“, „geprüft: ‹was›“, die Fundstelle als Datei in `inputs/` mit Abschnitt, „steht schon“, „setzt ‹Skill›“, oder „noch offen“ mit der Meldung einer gescheiterten Prüfung |

Darunter, je Zeile: was der Lead noch beantworten kann, und beim ersten Lauf die oberste Ebene des
Projektordners. Den Text von `project.yml` zeigst du nur, wenn der Lead danach fragt; geschrieben wird
er so, dass er genau die bestätigte Vorschau trägt.

**`project_owner` fragst du nicht, du setzt ihn auf die Person, die diesen Lauf ausführt** (§289,
§294): ihren GitHub-Namen liefert

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --whoami
```

aus derselben Quelle, mit der der Hook `wow-guard` später prüft. Endet der Aufruf mit Exit 1,
fragst du nach dem GitHub-Namen, schreibst ihn so, wie er genannt ist, und sagst im Bericht, dass er
ungeprüft ist und der Hook ohne Namen der Sitzung bei jeder Änderung in `way-of-working/` nachfragt.
