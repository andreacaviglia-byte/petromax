# Der Prozess-Test: Quellen, Schnitt, Form

## Quellen

**Die Quellen stehen im Repo** (§280): je Epic `epics/EP-NNN.md`, je Anforderung
`requirements/REQ-NNN.md`, Form im Datalayer-Vertrag. Ein Epic mit `status: merged` liest du nicht;
seine Anforderungen trägt das Ziel-Epic. Je Epic liest du:

| Was | Wo |
|---|---|
| Ziel und Bezüge | im Rumpf der Epic-Datei die Abschnitte `Goals and vision of the Customer` und `Relations and Prerequisites`, in der Sprache des Projekts nach der Tabelle in `${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, Abschnitt „Die Bezeichnungen“ (§255) |
| die Anforderungen | jede Datei in `requirements/` mit `epic:` dieses Epics, etwa `grep -l '^epic: EP-003$' requirements/*.md` |
| je Anforderung | im Kopf `title`, `status`, `scope`, `solution_status`; im Rumpf `## Acceptance criteria`, `## Approach` (nur der gewählte Lösungsansatz, der erste) und `## Details` |
| die Quelle | `draft` im Kopf der Epic-Datei und die Fassung des Entwurfs ([ref-sheet.md](ref-sheet.md), Die Fassung des Entwurfs) |

**Die Kriterien kommen aus der REQ-Datei**, nicht aus der Tabelle im Rumpf der Epic-Datei: die
Datei der Anforderung führt sie (§280, Regel 2). Je Epic ein Block in `e2e-sources.md`, geschrieben
direkt nach dem Lesen:

```
## ‹Epic-ID› ‹Titel› (Entwurf Fassung ‹modifiedTime›, ‹Link aus draft›)
Ziel: ‹was sich für Mitarbeitende und Endkunden ändert, aus Goals and vision of the Customer›
Bezüge: ‹andere Epics, Systeme, Lieferungen Dritter, aus Relations and Prerequisites›
- ‹ID› ‹title› | Shop: ‹key oder alle› | AC: ‹Acceptance criteria› | Lösungsansatz: ‹Approach, der gewählte› | Details: ‹soweit beobachtbar›
- ‹ID› ‹title› | nicht testbar: ‹Grund›
```

**Testbar** ist eine Anforderung, wenn `## Acceptance criteria` mindestens ein Kriterium trägt,
`solution_status` `decided` ist, `status` `open` oder `confirmed` und `scope` nicht `out_of_scope`.
Der Grund einer nicht testbaren nennt das erste, was fehlt: `keine Akzeptanzkriterien`,
`solution_status ‹Wert oder leer›`, `status ‹Wert›`, `out_of_scope`; eine mit `rejected` oder
`duplicate` zählst du nur. Die Kennungen darfst du in der Datei führen, damit der Plan zeigen kann,
welche Anforderungen ein Test verkettet; ins Sheet geht keine, in `tests/E2E-NNN.md` gehen sie
(Zuordnung, unten). **`Shop`** je Zeile kommt aus dem Feld `shops` der Anforderung: nennt es Shops,
gilt sie nur für diese, ist es leer, für alle (§307).

## Schnitt

**Ein Prozess-Test ist ein Ablauf, den eine Rolle beim Kunden von Anfang bis Ende durchläuft**, etwa
eine Bestellung vom Warenkorb bis zur Rechnung oder eine Retoure von der Anmeldung bis zur Erstattung.
Er verkettet die Akzeptanzkriterien mehrerer Anforderungen in der Reihenfolge, in der der Prozess sie
berührt.

- **Ausgangspunkt sind Ziel und Bezüge:** was sich für Mitarbeitende und Endkunden ändert und wo ein
  Epic an ein anderes oder an ein System übergibt, muss vor dem Go-Live durchlaufen werden.
- **Die Schritte und das erwartete Ergebnis kommen aus den Akzeptanzkriterien**, ergänzt um das
  Beobachtbare aus Lösungsansatz und `## Details` (ein Status im Backend, ein Beleg im System des Kunden). Du
  formulierst sie als Prozess neu, schreibst aber nichts hinzu, was keine Quelle trägt. Die
  funktionalen Subtasks, die `ticket-factory` aus der Anforderung anlegt, tragen prüfbare Kriterien
  aus denselben Akzeptanzkriterien, die auch der Test nutzt (§285); den Test leitest du aus der
  REQ-Datei ab, nicht vom Board.
- **Varianten eines Prozesses**, die sich im Ergebnis unterscheiden (Gast und Kundenkonto, Inland und
  Ausland), sind eigene Tests, wenn ein Akzeptanzkriterium sie unterscheidet; sonst nicht.
- **Eine Anforderung, die nur sich selbst berührt** und in keinen Ablauf gehört, steht im Plan als
  „nur je Anforderung getestet".
- Ein Übergang, den keine Quelle trägt, ist eine Frage an den Lead.

## Form einer Zeile

Der Lauf schreibt `ID` bis `Erwartetes Ergebnis` (A bis F, §256); die `ID` vergibt das Script, der
Plan trägt sie nicht.

| Spalte | Inhalt | in `plan.json` |
|---|---|---|
| `Testfall` | kurzer Name des Prozesses, eindeutig im Sheet, ohne Kennung: „Gastbestellung mit Teillieferung". Er ist der Schlüssel; ein zweiter Lauf findet den Test an diesem Text wieder | `testcase` |
| `Shop` | der Shop, durch den der Prozess läuft. Mit einem Shop in `project.yml` dessen `key`. Mit mehreren: nennen die verketteten Anforderungen in `shops` denselben einen `key`, dieser `key`; nennt keine einen (§307), `alle` (`en` `all`), denn der Prozess läuft durch jeden Shop. Tragen sie verschiedene `key`, sind es zwei Prozesse oder eine Frage an den Lead, kein Test mit einer Lesart | `shop` |
| `Rolle` | wer den Prozess durchläuft, beim Kunden oder als Endkunde: „Endkunde", „Händler", „Mitarbeitende Kundenservice". Wechselt die Rolle im Ablauf, steht hier die, die ihn beginnt, und der Schritt nennt die nächste | `role` |
| `Ablauf` | zuerst „Voraussetzung:" (`en` „Precondition:", [ref-sheet.md](ref-sheet.md), Die Sprache des Sheets) mit Testdaten und Ausgangszustand, dann nummerierte Schritte, je eine Handlung einer Rolle | `steps` |
| `Erwartetes Ergebnis` | je Schritt, dessen Ergebnis geprüft wird, das Beobachtbare mit seiner Nummer; zuletzt der Endzustand | `expected` |

- **Sprache** ist `language` aus `project.yml`, für den Text der Zeile wie für Köpfe, Werte und `alle`
  (`all`) nach [ref-sheet.md](ref-sheet.md), Die Sprache des Sheets (§337).
- **Beobachtbar:** was man sieht, eine Mail, ein Status im Backend, ein Beleg. Kein „funktioniert".
- **Keine Kennung** einer Anforderung, eines Epics, einer Frage oder eines Tickets, **keine Adresse**,
  keine Namen; verantwortlich ist eine Rolle.
- **Keine Interna** (§278): das E2E-Sheet ist extern. Kein Hinweis auf eine interne Quelle, kein
  Zitat aus einem Transkript, nichts aus der Liste im Abschnitt „Interna“ von `way-of-working.md`;
  nur sachliche Fakten, die der Kunde kennt oder kennen darf. Steht etwas davon in einer REQ-Datei,
  übernimmst du es nicht, und der Plan nennt die Stelle.
  Das Script lehnt eine Kennung `REQ-`, `EP-` oder `ADR-` oder eine Adresse in einem Textfeld mit
  `forbidden_id` ab; eine Frage- oder Ticket-Kennung prüfst du selbst, ein leeres Feld mit
  `empty_field` und einen `shop` außerhalb der erlaubten Werte mit `shop_unknown`.
- **Shopify heißt Shopify.** Systeme des Kunden stehen mit ihrem Namen.

## Zuordnung

**Je Test trägt `plan.json` zusätzlich, woraus er stammt** (§280); ins Sheet geht davon nichts, das
Script schreibt es nach dem Rücklauf je Test in den Kopf von `tests/E2E-NNN.md`, die Felder der
Spalten C bis F in den Rumpf, unter `## Shop`, `## Role`, `## Steps` und `## Expected result` (§295):

| Feld in `plan.json` | Inhalt |
|---|---|
| `requirements` | die Kennungen der Anforderungen, die der Test verkettet, in der Folge des Ablaufs: `["REQ-001", "REQ-004"]` |
| `sources` | je Epic, aus dessen Anforderungen ein Schritt stammt, ein Eintrag `{"epic": "EP-001", "kind": "draft", "version": "‹modifiedTime›", "link": "‹Link aus draft›"}`; `version` und `link` wie im Block in `e2e-sources.md`. `kind` `page` nimmt dieser Lauf nicht: er liest keine Seite |

Beides kommt aus `e2e-sources.md`, nicht aus dem Gedächtnis. Das Script lehnt einen Test ohne diese
Felder oder mit anderer Form mit `test_file_field` ab, wenn `--tests` gesetzt ist.
