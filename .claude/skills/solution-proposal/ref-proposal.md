# Das Proposal: lesen, Arbeitsdateien, prüfen, anlegen

**Gerechnet wird aus dem Projekt-Repo** (§280). Das Script liest selbst `project.yml` (`customer`,
`title`, `language`, `shops`), `requirements/`, `epics/`, `gaps/` und `decisions/`, in der Form des
Datalayer-Vertrags. Aus dem Sheet nimmt es nur die Felder der Menschen, die es braucht (§280 Regel 5).
Alle Arbeitsdateien liegen im Temp-Ordner des Laufs (§233).

## Lesen

**Die vier Tabs liest du einmal**, wie für die Projektion
(`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Schritt 2), mit ihren Namen in der Sprache aus
`language`, in dieselben Dateien: `anforderungen.json`, `solutioning.json`, `epics.json`,
`offene-punkte.json`. Sie tragen das Proposal und den Snapshot (§266) mit derselben Lesezeit; so hält
der Snapshot genau den Stand fest, aus dem das Proposal gerechnet ist. **Eine Antwort von
`get_values` geht auf die Platte, nicht durch den Kontext**: legt die Sitzung sie als Datei ab,
nimmst du diese.

**Die Lesezeit** nimmst du direkt nach der letzten Lesung: `date -u +%Y-%m-%dT%H:%MZ`. Sie gilt für
Proposal und Snapshot.

Aus `epics.json` und `offene-punkte.json` nimmt das Script nur diese Spalten, an
ihrer Kopfzeile in der Sprache des Projekts:

| Datei | Spalten (`en`) | wofür |
|---|---|---|
| `epics.json` | `Epic-ID`, `Geprüft von`, `Geprüft am` (`Epic ID`, `Reviewed by`, `Reviewed on`) | geprüft ist ein Epic, wenn beide Felder etwas tragen (§277) |
| `offene-punkte.json` | `GAP-ID`, `Bis` (`GAP ID`, `Due`) | die Frist einer Frage unter „Vor Beauftragung zu klären“ |

`anforderungen.json` und `solutioning.json` braucht nur der Snapshot; Stunden liest das Proposal nicht
(§355). Fehlt eine Spalte, lehnt das Script mit `header` ab.

## Die Arbeitsdateien

**`meta.json`**, aus dem Repo und der Lesung:

```json
{"repo": "‹Pfad des Projekt-Repos›", "commit": "a0447d3", "read_at": "2026-09-30T14:05Z"}
```

`repo` ist `git rev-parse --show-toplevel`, `commit` ist `git rev-parse --short HEAD` nach dem Pull
aus Step 2, `read_at` die Lesezeit. **Sonst steht nichts darin** (§355): keine Sätze, keine
Zusatzpositionen (`meta`), kein Budget (`budget`).

**`assumed.json`**, nur wenn ein geprüftes Epic eine offene Kundenfrage schon als Annahme führt
(§241, Step 3): je Frage ihre Kennung mit dem Epic und der Annahme wörtlich aus `Assumptions and
delimitations` im Rumpf seiner Datei.

```json
{"GAP-003": {"epic": "EP-001", "quote": "Das ERP liefert Preise je Markt."}}
```

## Was ins Proposal geht

- **Kein Aufwand** (§355): keine Stunden, keine Tabelle zum Aufwand, keine Zeilen für
  Projektmanagement und Testing, kein Gesamt, kein Budget. Oben stehen die Kopftabelle und „Stand: ‹Datum›“.
- **Die Tabelle Scope** nennt je Epic, das nicht `merged` oder `dissolved` ist, in der Folge der
  Domänen, ihren Anzeigenamen, Epic Page und `Status in Blueprint` aus dem Kopf seiner Datei. Ein geprüftes Epic zeigt den Link aus `epic_page`
  oder, mit `draft`, „Entwurf, nicht freigegeben“ ohne Adresse; ein ungeprüftes steht als „in Arbeit“.
- **Je Domäne die geprüften Epics**, ohne Stunden (§355), mit `Goals and vision of the Customer` und
  `Assumptions and delimitations`, wörtlich aus dem Rumpf ihrer Datei, gefunden an der Bezeichnung der Projektsprache
  aus `${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, Abschnitt „Die Bezeichnungen“
  (§255). Im Theme-Epic (`domain: storefront`) folgt unter den Annahmen je Seitentyp mit
  `own_sections` eine Zeile „‹REQ-ID› ‹Titel›: bis zu ‹n› eigene Sections“ (§285).
- **„Nicht im Scope“** nennt jede Anforderung mit `status: rejected` oder `scope: out_of_scope`, mit
  ihrer Priorität, Must-have zuerst (§327): eine Anforderung, die der Kunde braucht und die doch nicht
  gebaut wird, steht dort sichtbar, mit dem Satz `Entscheidung:` der jüngsten ADR mit `status: accepted`, die sie unter `Betrifft:` nennt
  (`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Die ADR in `decisions/`); eine ADR-Kennung am Ende schneidet das Script ab.
- **„Blocker“** nennt jede gezählte Anforderung mit `solution_status: blocked`, mit den offenen,
  blockierenden Fragen an den Kunden, die sie betreffen; hängt sie nur an einer Frage an uns, steht
  dort „in interner Klärung“.
- **„Vor Beauftragung zu klären“** nennt jede offene Frage in `gaps/`, deren `to` mit `Kunde` oder
  `Customer` beginnt und deren `concerns` eine gezählte Anforderung oder ein Epic nennt: die Frage,
  die Kennungen, an wen und `Bis`, blockierende zuerst und markiert. Ausgenommen ist, was
  `assumed.json` trägt. Ohne solche Frage fehlt der Abschnitt.

## Die Prüfungen

Exit 1 des Scripts nennt eine Zeile `<prüfung> <stelle>`:

| Prüfung | heißt | was du tust |
|---|---|---|
| `meta`, `input` | eine Arbeitsdatei, `project.yml` oder eine Datei im Repo ist nicht in der Form des Vertrags; `meta` auch, wenn `meta.json` Sätze oder Zusatzpositionen trägt (§355) | deine Datei korrigierst du aus der Lesung; `project.yml` ergänzt `project-setup`, eine Datei im Repo der Lauf, dem sie gehört |
| `budget` | `meta.json` trägt ein Budget, oder im Text für den Kunden steht „Budget“ (§355); die Meldung nennt die Datei | aus `meta.json` nimmst du es und rechnest neu; steht es im Text, hältst du an: `solution-design` nimmt es aus dem Epic, `requirements-update` aus Frage oder ADR |
| `effort` | im Text für den Kunden steht eine Stundenangabe oder „Aufschlag“ (§355); die Meldung nennt die Datei | anhalten; `solution-design` nimmt sie aus dem Epic, `requirements-update` aus Anforderung, Frage oder ADR |
| `header` | eine Spalte aus der Tabelle oben fehlt in der Kopfzeile ihres Tabs | anhalten; umgestellt wird ein Sheet von Hand |
| `domain` | ein Epic trägt keine Domäne der festen Liste, oder sie hat dort keinen Anzeigenamen, und gehört zu keiner Gruppe | anhalten; die Domäne setzt `epic-structure` |
| `assumed` | ein Eintrag in `assumed.json` ohne Fundstelle, mit einer, die nicht wörtlich unter den Annahmen des Epics steht, an einem Epic, das nicht geprüft ist, oder ohne offene Kundenfrage dieser Kennung | du nimmst den Eintrag heraus oder korrigierst ihn aus der Lesung |
| `internal_source` | im Text für den Kunden steht eine Drive-Adresse, eine ADR-Kennung oder ein Pfad des Repos; die Meldung nennt die Datei | anhalten; `solution-design` nimmt ihn aus dem Epic, `requirements-update` aus Frage oder ADR |
| `questions_section` | ein Epic trägt eine Überschrift „Offene Fragen“ | anhalten; `solution-design` nimmt sie heraus |
| `html_markup` | ein Text aus den Daten steht unmaskiert im HTML | anhalten und die Zeile nennen |

## Das Doc anlegen

Name: `Solution Proposal ‹title› – ‹Kunde›` (§263), ohne Datum und Uhrzeit, die Art in jeder Sprache
gleich. Den Namen bildest du nicht selbst, das Script bildet ihn aus `project.yml`:
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/doc-name.py . proposal`. Exit 1 nennt das leere Feld; dann
hältst du an und nennst `project-setup`. **Jede Fassung trägt denselben Namen**; flach in
`Solutioning` liegt nur die aktuelle, die vorigen verschiebt der Lauf nach `Archiv` (§260), und das
Datum der Lesezeit steht im Dokument („Stand: ‹TT.MM.JJJJ›“, bei `en` „As of: 11 Oct 2026“, §337; Uhrzeit und Stand des Repos im Commit
des Laufs, §264).

| # | Zweck | Aufruf |
|---|---|---|
| 0 | den Unterordner finden oder anlegen | `Google_Drive.search_files` mit `query` = `parentId = '‹project_folder›' and title = 'Solutioning' and mimeType = 'application/vnd.google-apps.folder'`. Ein Treffer: seine ID ist `‹solutioning›`. Keiner: `Google_Drive.create_file` mit `title: Solutioning`, `contentMimeType: application/vnd.google-apps.folder`, `parentId` = `project_folder`, die zurückgegebene ID ist `‹solutioning›`. Zwei: anhalten und beide mit Link nennen; welcher gilt, entscheidet der Lead (§231) |
| 1 | die vorige Fassung finden | `Google_Drive.search_files` mit `query: "parentId = '‹solutioning›'"` und `excludeContentSnippets: true`, jede Seite über `pageToken`, bis kein `nextPageToken` mehr kommt; den Namen vergleichst du in der Antwort. Jeder Treffer mit dem Namen ist eine vorige Fassung (§262): du merkst dir ID und Namen und legst trotzdem an |
| 2 | das Doc anlegen, mit Inhalt | `Google_Drive.create_file` mit `title` = Name, `parentId` = `‹solutioning›`, `contentMimeType: text/html`, `textContent` = die Ausgabe des Scripts (HTML), Zeichen für Zeichen |
| 3 | Ort prüfen | `get_file_metadata` mit `fileId` = ID aus Schritt 2; die Antwort nennt `‹solutioning›` als `parentId` und den Typ Google-Doc |
| 4 | zurücklesen und vergleichen | `Google_Drive.read_file_content` mit der ID; den Text der Antwort schreibst du in eine Datei im Temp-Ordner und vergleichst: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py readback proposal <ordner> <datei>`. `GLEICH` heißt: der Text des Docs ist der des Scripts |
| 5 | Seite, Fußzeile und Schrift | `python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-solution-doc.py layout` gibt die `requests` für `Google_Docs.update_doc` mit `documentId` = ID aus Schritt 2 aus: A4, Ränder, eine leere Fußzeile. Die Antwort trägt unter `createFooter` die `footerId`. Dann `check-solution-doc.py footer proposal <ordner> <footerId>` und dessen Ausgabe als `requests` an einen zweiten `update_doc`: Text und Stil der Fußzeile. Dann `Google_Docs.read_doc` mit `documentId` = ID aus Schritt 2; die Antwort (JSON) liegt in einer Datei im Temp-Ordner, und hat die Sitzung sie schon selbst als Datei abgelegt, nimmst du diese. `check-solution-doc.py font <datei>` gibt die `requests` für einen dritten `update_doc` aus: Poppins auf den ganzen Body, danach die Fettung, wie sie vorher stand. Die `requests` gehen unverändert und vollständig in diesen einen Aufruf. Der Schritt läuft immer, auch wenn das Doc schon Poppins zeigt |
| 6 | ältere Fassungen nach `Archiv` (§260, §262) | Nur wenn Schritt 4 `GLEICH` meldete, nach Schritt 5. Ältere Fassung ist jede Datei aus der Liste von Schritt 1 mit dem Namen aus `doc-name.py`, deren ID nicht die aus Schritt 2 ist und deren `createdTime` vor der des neuen Doc liegt; `createdTime` liest du je Datei mit `Google_Drive.get_file_metadata`, für das neue Doc aus Schritt 3. Trägt eine Antwort kein `createdTime`, verschiebst du diese Datei nicht und nennst sie. Gibt es keine ältere Fassung, entfällt der Schritt. Sonst `Archiv` finden oder anlegen: `Google_Drive.search_files` mit `query` = `parentId = '‹solutioning›' and title = 'Archiv' and mimeType = 'application/vnd.google-apps.folder'`. Ein Treffer: seine ID ist `‹archiv›`. Keiner: `Google_Drive.create_file` mit `title: Archiv`, `contentMimeType: application/vnd.google-apps.folder`, `parentId` = `‹solutioning›`. Zwei: nichts verschieben, beide mit Link nennen. Dann je ältere Fassung `Google_Drive.update_file` mit `fileId` = ihre ID und `parentId` = `‹archiv›` |

- **Gesucht wird über die Liste des Ordners, nicht über den Namen** im ganzen Drive.
- **Der Inhalt geht in Schritt 2 als HTML mit Inline-Stilen** (§248): `create_file` mit
  `contentMimeType: text/html` legt ein Google-Doc an und behält Farben, Tabellenköpfe und
  Rahmen (gemessen am 04.10.2026), dazu die Abstände um Überschriften und Tabellen, die das Script als
  `margin` setzt (gemessen am 08.10.2026). Die Schrift behält es nicht bei jedem Doc: am 08.10.2026
  kam das Schätzdokument in Arial an, das Proposal desselben Stands in Poppins, aus demselben
  HTML-Aufbau. Deshalb setzt Schritt 5 sie nach. Die Seite kommt als US Letter; A4 und die Fußzeile
  setzt Schritt 5. Eine neue Fassung ist ein neues Doc.
- **Scheitert Schritt 5, bleibt das Doc gültig**: der Inhalt steht, nur Seite, Fußzeile oder Schrift
  fehlen; der Bericht nennt Aufruf und Meldung wörtlich.
- Ein Doc, das es schon gibt, schreibt dieser Weg nie, auch keine frühere Fassung.
- **Angelegt ist das Doc erst**, wenn Schritt 3 den Unterordner `Solutioning` nennt und Schritt 4
  `GLEICH` meldet. Sonst nennt der Bericht das Doc als nicht bestätigt, mit der Zeile, die `readback`
  als erste abweichende nennt.
- **Ein kaputt angelegtes neues Doc kommt weg** (§259), **erkannt an der ID aus Schritt 2, nie am
  Namen**: die vorige Fassung trägt denselben Namen (§262) und bleibt dann flach liegen, wie sie ist.
- **Scheitert Schritt 6, bleibt die ältere Fassung in `Solutioning` liegen** (weich); der Bericht
  nennt sie mit Name und Link. Verschoben wird nur, was dieser Weg als ältere Fassung erkennt, kein
  Schätzdokument und kein anderes Doc.
