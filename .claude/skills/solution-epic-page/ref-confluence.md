# Die Epic Page in Confluence: eintragen, anlegen, fortschreiben

**Die Seite folgt der Vorlage des Entwurfs**, Zeichen für Zeichen dieselbe:
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, mit der Tabelle der Bezeichnungen
in beiden Sprachen (§218, §255). Eine Stelle heißt hier mit ihrer Bezeichnung aus der Spalte `en`,
etwa `Status in Blueprint`; auf der Seite steht sie in der Sprache des Entwurfs. Neu auf der Seite sind
nur der Satz `approved_note`, der Status und, wo es geht, der Owner als Mention; alles andere kommt
aus dem freigegebenen Entwurf.

## Space und Elternseite eintragen

Nur wenn `confluence.cloud_id`, `space` oder `parent_page` in `project.yml` leer sind, vor dem Plan
(§229). Du fragst den Lead nach dem Link zum Space und nach der Elternseite, als Link oder mit ihrem
Titel; die Antwort darf „noch offen" sein, dann unterbleibt die Übertragung. Eingetragen wird nur, was
geprüft ist:

1. Aus dem Link liest du die Site und den Space-Schlüssel (`…/wiki/spaces/<KEY>/…`).
   `getAccessibleAtlassianResources` liefert je Produkt einen Eintrag; nimm die `id` des Eintrags mit
   Confluence-Scopes für diese Site. **Als `cloud_id` steht nur diese UUID, nie der Hostname**: mit dem
   Hostnamen scheitern die Aufrufe, obwohl die Werkzeugbeschreibung ihn anbietet.
2. `executeRead` mit `name: getConfluenceSpace`, `cloudId` und `inputs: {spaceIdOrKey: ‹Space-Schlüssel›}`:
   der Space existiert, sonst fragst du.
3. Die Elternseite als Link: die Zahl nach `/pages/`. Mit Titel: `searchConfluence`, `cql` =
   `space = "‹Space-Key›" AND type = page AND title = "‹Titel›"`; gültig ist genau ein Treffer, bei
   keinem oder mehreren fragst du nach dem Link. Dann `getConfluenceContent` mit `content_id` = ihre
   ID und `detail: summary`: sie existiert und liegt im Space aus 2.
4. Zeig Space-Name und Seitentitel im Klarnamen. `confluence.cloud_id` = die UUID,
   `confluence.space` = der Schlüssel, `confluence.parent_page` = die Seiten-ID, `space` und
   `parent_page` in Anführungszeichen. Sie stehen im Plan und werden nach dem Ja eingetragen, nach dem
   Datalayer-Vertrag, Abschnitt `project.yml`; danach:

   ```
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
   ```

   Meldet es einen Verstoß, nennst du ihn wörtlich, und die Übertragung unterbleibt.

## Was neu auf die Seite kommt

| Stelle | Inhalt |
|---|---|
| unter dem Titel | nur `approved_note`, bei `de` „Freigegeben am ‹TT.MM.JJJJ›.", bei `en` „Approved on 11 Oct 2026.": das Datum, in der Form der Sprache (§337), ist `date` des letzten Eintrags unter `releases` im Manifest der Freigabe. Kein Link, auch nicht auf das Board (§328) |
| `Epic` | Kennung und Titel aus dem Repo, `‹Epic-ID›: ‹Titel des Epics›`, wie im Entwurf, ohne Link (§328) |
| `Status in Blueprint` | `status_approved`, bei `de` `Abgenommen`: der Kunde hat den Scope freigegeben, der dieses Epic trägt (§277) |
| `Document Owner` | der Name aus dem Entwurf. `atlassianUserInfo` liefert nur die `account_id` der Person dieser Sitzung, keinen Namen (gemessen am 10.10.2026); ob sie der Document Owner ist, fragst du deshalb im Plan. Ist sie es, steht er als Mention mit dieser `account_id`, sonst bleibt der Name als Text, und der Bericht nennt es |

## Die Seite anlegen

1. `executeRead` mit `name: getContentFormatGuide` und `inputs: {toolName: createConfluencePage}`; die
   Formatregeln hältst du ein. Der Connector verlangt vor dem Schreiben einmal je Space
   `getConfluenceSpace` (Schritt 2 oben, sonst jetzt): trägt die Antwort `spaceInstructions`, hältst du
   sie ein, wo sie der Vorlage nicht widersprechen; einen Widerspruch nennt der Bericht, und die
   Vorlage gilt.
2. Aus `entwurf.html` entsteht die Seite als HTML, **Inhalt Zeichen für Zeichen aus dem Entwurf**; neu
   ist nur, was die Tabelle oben nennt. Überschriften stehen als `<h2>`, ohne Nummer. **Ein Datum steht
   als Text**, in der Form der Sprache wie im Entwurf (`de` `TT.MM.JJJJ`, `en` `11 Oct 2026`, §337), nie als `<time>`: Confluence rendert `<time>` in der
   Sprache der Oberfläche, gemessen am 30.09.2026 als „September 30, 2026" auf einer deutschen Seite.
   Der Owner steht als `<span data-type="mention" data-user-id="‹account_id›">@‹Name›</span>`, der
   Status als `<span data-type="status" data-color="neutral">‹Status›</span>`, die Checkboxen als
   Task-Liste, alle offen (§218).
3. `createConfluenceContent` mit `cloudId`, `contentType: page`, `parent: {parentContentId:
   ‹confluence.parent_page›}`, `title` = der Titel des Entwurfs und `body: {format: html, value: ‹die
   Seite›}`.
4. Zurücklesen mit `getConfluenceContent`, `content_id` = die neue Seite, `content_format: html` und
   `detail: full` in `seite.html`; die Fassung der Seite steht in derselben Antwort. Dann prüfen:

   ```
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-page.py --language ‹language› --title "‹Titel der Seite›" seite.html
   ```

   Kommt die Rücklesung direkt in der Antwort und nicht als Datei, schreibst du den Wert von `body`
   mit dem Write-Werkzeug in `seite.html`, die JSON-Escapes aufgelöst (`\"` wird `"`, `\n` ein
   Zeilenumbruch, `ü` ein `ü`), und gleichst seinen reinen Text gegen die gesendete Fassung ab.
   **Die gesendete Fassung ersetzt die Rücklesung nie**: geprüft wird, was Confluence gespeichert hat.

   Die Rücklesung liefert die erste Zeile jeder Tabelle als `<thead>`, im Kopf mit `th` und `td`
   nebeneinander (gemessen am 30.09.2026). Das ist die Gestalt, die Confluence speichert, kein Fehler
   der Übertragung; `check-page.py` liest sie so.

**Scheitert das Anlegen an der Validierung**, hältst du an und nennst die Meldung; du legst keine
vereinfachte Fassung an. Der Entwurf bleibt der einzige Stand, und `epic_page` bleibt leer.

## Die Seite fortschreiben

Nur nach dem Ja des Leads zu „Seite neu übertragen" im Plan. Die Stellen sind die Abweichungen
zwischen dem Rumpf der Epic-Datei und der Seite, ohne die Stellen, die nach der Übertragung andere
führen: `Estimation`, `Initial Estimate`, Status und Checkboxen (die Menschen) und die Zeilen
`approved_note` und `changed_note`. Kein anderer Skill schreibt auf die Seite (§328).

1. Die Seite mit `getConfluenceContent`, `content_format: html` und `detail: full` in `seite-alt.html`
   lesen; die Antwort trägt die Fassung und den `snapshotToken`, den das Schreiben braucht.
2. Die neue Fassung entsteht aus `seite-alt.html`: **geändert werden nur die Stellen aus dem Plan**,
   alles andere bleibt Zeichen für Zeichen. Unter `approved_note` steht die Zeile `changed_note`, bei
   `de` „Geändert am ‹TT.MM.JJJJ›: ‹was, in einem Satz›", bei `en` „Changed on 11 Oct 2026: …"; eine frühere Zeile dieser Art bleibt darüber
   stehen. **Der Satz ist kurz und zählt nichts auf** (§264): keine Liste von Epic-IDs, REQ-IDs,
   Fassungen oder Seiten. Also „Geändert am 08.10.2026: Die Seite trägt nur noch den Bestand.", nicht
   „…; Artikelstamm, Preise und Aufträge stehen auf den Seiten von EP-027 bis EP-030." Wohin etwas
   gewandert ist, zeigen das Sheet und die Abgrenzungen der Seite.
3. `executeRead` mit `name: getContentFormatGuide` und `inputs: {toolName: updateConfluencePage}`;
   dann `updateConfluenceContent` mit `cloudId`, `contentId` = die Seiten-ID, `snapshotToken` aus 1 und
   `body: {format: html, value: ‹die neue Fassung›}`, ohne `title`, damit er bleibt.
4. Zurücklesen und mit `check-page.py` prüfen wie beim Anlegen. Stimmt die Fassung nicht um eins
   höher als in 1, hat jemand dazwischen geschrieben: du hältst an und nennst beide Fassungen.

Der Entwurf bekommt keinen Vermerk und keine Änderung.
