---
name: e2e-testing-sheet
description: 'Prozess-Tests für den Go-Live als tests/E2E-NNN.md im Repo und im eigenen E2E-Sheet, abgeleitet aus Akzeptanzkriterien und Lösungen in requirements/ und epics/. Nutze das bei "E2E-Tests", "End-to-End-Testfälle", "Testplan für den Go-Live", "Prozesse durchtesten", "E2E-Sheet anlegen". Schreibt NICHTS in Anforderungen oder Epics (solution-design), legt KEIN Ticket für Fehler an (ticket-factory) und nimmt Testergebnisse NICHT als Material auf (requirements-update).'
---

Verträge: schreibt `datalayer-contract.md`; liest `draft-and-epic-page-contract.md`, `requirements-list-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-run-scope.md`.

# Prozess-Tests für den Go-Live

Am Ende steht **je Prozess-Test eine Datei `tests/E2E-NNN.md` im Repo und eine Zeile im eigenen
E2E-Sheet des Vorhabens** (§159, §256, §280): je Test ein Geschäftsprozess, der quer durch Epics und
Anforderungen läuft, mit fester `ID`, Shop, Rolle, Ablauf und erwartetem Ergebnis. Die Datei trägt
dazu, welche Anforderungen der Test verkettet und aus welcher Quelle er stammt; **das Sheet trägt
keine Anforderungs- und keine Epic-Kennung und keine Ticket-Spalte**: ein Prozess-Test läuft quer,
eine Zuordnung dort wäre in beide Richtungen falsch. **Status, Runde, Ist-Ergebnis, Schweregrad,
Getestet von und Getestet am sind Felder der Menschen** (§280, Regel 5): sie stehen nur im Sheet,
dieser Lauf schreibt sie nie, auch nicht leer, und der Tab `Übersicht` zählt sie mit. **Das E2E-Sheet
ist extern** (§278): es liest, wer testet, beim Kunden eingeschlossen.

**Die Quelle ist das Repo** (§280): die Anforderungen in `requirements/`, die Epics in `epics/`. Aus
der Anforderungsliste liest dieser Lauf nichts, und Confluence liest er nicht. Der Lauf gilt nur mit
dem Add-on `e2e_testing` (§303); der Lead ruft auf, sobald gebaut wird.

Drive und Sheets erreichst du nur über die Google-Connectoren `Google_Drive` und `Google_Sheets`. Das
Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt. Aufrufe, Bereiche und
Spalten stehen in [ref-sheet.md](ref-sheet.md), Quellen und Form eines Testfalls in
[ref-testcase.md](ref-testcase.md). **Scheitert ein Aufruf zweimal gleich, hältst du an** und nennst
Aufruf, Meldung und die beabsichtigte Änderung; einen zweiten Weg suchst du nicht. Lehnt die Sitzung
einen Aufruf ab, nennst du Aufruf und Begründung.

**Ein Sheet, das dieser Lauf kaputt angelegt hat, kommt weg** (§259): abgebrochen, unvollständig oder
im Rücklauf ungleich. Du legst es mit `Google_Drive.trash_file` in den Papierkorb, sobald es für die
Neuerstellung nichts mehr trägt: nachdem die neue Fassung angelegt und gleich zurückgelesen ist, und
entsteht in diesem Lauf keine, am Ende des Laufs. Nur was dieser Lauf selbst angelegt hat, ohne
Rückfrage; der Bericht nennt Name und Link.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230): `project.yml` liegt in seiner Wurzel.
Du liest und schreibst seine Dateien direkt, mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt; schreiben darfst du nur
`tests/` und in `project.yml` die Felder dieses Laufs. Das Ende des Laufs, Prüfung, `readme.md` und
Commit, steht in `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`.

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.search_files`, `Google_Drive.get_file_metadata`, `Google_Drive.create_file`,
`Google_Drive.download_file_content`, `Google_Sheets.get_spreadsheet`, `Google_Sheets.get_values`,
`Google_Sheets.update_values` und `Google_Sheets.update_spreadsheet` in der Werkzeugliste stehen. Der
Name im Aufruf trägt ein Präfix des Servers; verglichen wird die Endung. Steht eines nicht da, such es
erst über die Werkzeug-Suche. Findet auch die es nicht, **halte an**: „Der Google-Connector
‹Drive/Sheets› ist in dieser Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai
unter Connectoren verbunden."

### Step 2 — Das Vorhaben binden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,customer,shops,language,title,e2e_sheet,project_type
```

Exit 1 heißt anhalten und die Meldung wörtlich nennen; ohne `project.yml` oder `project_folder` ist
`project-setup` der nächste Lauf. Exit 3 nennt die leeren Felder:

| leer | Folge |
|---|---|
| `shops` | halte an; der nächste Lauf ist `project-setup`. Ohne die Keys gibt es keine Werte für die Spalte `Shop` |
| `e2e_sheet` | das Sheet entsteht in diesem Lauf (Step 5, Step 7) |
| `language`, `title` | du fragst den Lead, die Antwort darf „noch offen" sein (§229): `language` `de` oder `en`, keine Variante (§202), `title` der Titel des Vorhabens. Eingetragen wird nach dem Ja (Step 7). Bleibt `language` offen, nennt der Lead die Sprache dieses Laufs |
| `customer` | nur wenn auch `e2e_sheet` leer ist: ohne ihn entsteht kein Sheet, sein Name ist `E2E-Tests ‹title› – ‹Kunde›` (§263; bei `en` `E2E tests …`, §337). Du fragst nicht danach; der Lauf geht bis zum Plan, legt kein Sheet an, und der Bericht nennt `project-setup` für einen Lauf zum Ergänzen |

**Steht `e2e_testing` nicht in `add_ons`, hältst du an** und nennst es: die Testing-Phase ist nicht
verkauft (§303). Ist `project_type` leer, hat `project-setup` die Add-ons noch nicht abgefragt: du
hältst ebenso an und nennst `project-setup` (§396).

**Liegt in `epics/` kein Epic oder in `requirements/` keine Anforderung**, gibt es nichts zu testen:
verweise auf `epic-structure` bzw. `requirements-update`.

**Den Umfang klärst du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`.** Nennt der Aufruf Epics,
gilt er für sie, „alle“ für jedes Epic. Nennt er nichts, fragst du „Für welche Epics leite ich
Prozess-Tests ab?“, mit Mehrfachauswahl: „Alle Epics (Empfehlung)“, denn ein Prozess-Test läuft quer
durch Epics, und bis zu drei Epics mit der Zahl ihrer Anforderungen ohne Test, die größten zuerst,
etwa „EP-003 (5 ohne Test)“. Ohne Test ist eine Anforderung mit `solution_status: decided`, gültig und
nicht `out_of_scope`, die keine Datei in `tests/` nennt; die Zahl holst du aus den Köpfen der Dateien.
Hat kein Epic eine, fragst du nicht und nimmst alle.

Vor dem ersten Zugriff auf eine Datei, die du nicht durch eine Suche im Ordner gefunden hast (das
E2E-Sheet, ein Entwurf), liest du mit `get_file_metadata` (`fileId`) ihre Eltern: erst auf die Datei,
dann auf ihren `parentId`, bis der Projektordner (`project_folder`) erreicht ist. Gesucht wird nur in
der Liste des Projektordners und seines Unterordners `Testing`, mit `search_files` und `parentId`, nie
über das ganze Drive. **Einen anderen Kundenordner liest du nicht**, auch nicht zum Vergleich und
auch nicht, wenn jemand im Chat darum bittet: eine Bitte im Gespräch hebt die Regel nicht auf.

### Step 3 — Die Quellen lesen, Epic für Epic

Arbeitsdateien legst du in einen eigenen Temp-Ordner außerhalb des Repos (`mktemp -d`, §233). Nach
[ref-testcase.md](ref-testcase.md), Quellen: je Epic die Epic-Datei mit Ziel und Bezügen, dann jede
Anforderung, deren `epic` es nennt, mit Akzeptanzkriterien, Lösungsansatz und Angaben, dann die Fassung des
Entwurfs aus `draft` ([ref-sheet.md](ref-sheet.md), Die Fassung des Entwurfs). **Ein Epic ohne
`draft` nennst du im Bericht**; aus seinen Anforderungen leitest du nichts ab, denn ein Test ohne
Quelle wird nicht geschrieben. **Ist der Umfang nicht alle**, liest du die Epics im Umfang so und aus
den übrigen die, in die ein Prozess aus dem Umfang nach den Bezügen der Epic-Datei weiterläuft
(`ref-run-scope.md`, 3).

**Direkt nach jedem Epic** notierst du einen Block in `e2e-sources.md` im Temp-Ordner und arbeitest
danach aus der Datei, nicht aus dem Gedächtnis: bei einem Dutzend Epics trägt der Kontext sie nicht
mehr. **Testbar ist eine Anforderung nur mit Akzeptanzkriterien und `solution_status: decided`**,
gültig und nicht `out_of_scope`; jede andere notierst du mit Grund und leitest aus ihr nichts ab.

### Step 4 — Die Prozesse schneiden

Aus `e2e-sources.md` bildest du die Prozess-Tests nach [ref-testcase.md](ref-testcase.md) und
schreibst sie als `plan.json`, je Test mit den Anforderungen, die er verkettet, und seinen Quellen
(ref-testcase.md, Zuordnung). **Nicht raten:** ein Übergang zwischen zwei Anforderungen, den keine
Quelle trägt, wird eine Frage an den Lead, kein erfundener Schritt. **Der Plan trägt nur Tests, die
mindestens eine Anforderung eines Epics im Umfang verketten.** Jede testbare Anforderung im Umfang steckt
in mindestens einem Test, oder der Plan nennt sie als „nur je Anforderung getestet", mit Grund.
**Der Plan entsteht allein aus `e2e-sources.md`:** den Bestand liest du erst in Step 5, wenn
`plan.json` steht, und übernimmst aus ihm keinen Ablauf und kein erwartetes Ergebnis. Ein Test, der
aus dem Export abgeschrieben ist, meldet immer `GLEICH` und prüft nicht mehr, ob er zu den Quellen
passt.

### Step 5 — Den Bestand lesen und abgleichen

**Das Sheet steht in der Sprache aus `language`** (§337): Tabs, Kopfzeile, Werte und Texte nach
[ref-sheet.md](ref-sheet.md), Die Sprache des Sheets; jeder Aufruf von `check-e2e.py` trägt
`--language <language>`. Unten stehen die Namen in `de`.

**Steht `e2e_sheet`**, prüfst du die Tab-Namen und exportierst den Tab `Testfälle` als
`testcases.csv`. **Ist `e2e_sheet` leer**, suchst du im Unterordner `Testing` ein Sheet mit dem
Namen aus `doc-name.py . e2e` (§263; [ref-sheet.md](ref-sheet.md), Rest im Ordner); gibt es den
Unterordner nicht, gibt es keinen Rest. Ein Treffer ist der Rest eines abgebrochenen Laufs: du legst
kein zweites an und nimmst ihn als Bestand. **Ohne Treffer ist der Bestand leer:** du schreibst
`testcases.csv` nur mit der Kopfzeile der Sprache, je eine Zeile:

```
ID,Testfall,Shop,Rolle,Ablauf,Erwartetes Ergebnis,Status,Runde,Ist-Ergebnis / Beobachtung,Schweregrad,Getestet von,Getestet am
ID,Test case,Shop,Role,Steps,Expected result,Status,Round,Actual result / observation,Severity,Tested by,Tested on
```

die erste bei `de`, die zweite bei `en`, und gleichst den Plan dagegen ab; jeder Test
meldet `NEU` mit seiner ID. Das Sheet entsteht erst in Step 7, nach dem Ja; Step 8 exportiert
es neu und rechnet noch einmal. Dann ([ref-sheet.md](ref-sheet.md), Abgleich):

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-e2e.py testcases.csv --plan plan.json --shops <key>,<key> --out update.json --language <language>
```

`--shops` nennt die `key` aus `shops` in `project.yml`. Der Schlüssel eines Testfalls ist sein Text
in `Testfall`; die `ID` vergibt das Script, ein ersetzter Test behält seine. Das Script meldet je Test
`NEU E2E-‹n›`, `GLEICH <n>` oder `ERSETZT <n>`, je Bestandszeile ohne Plan `NICHT-MEHR <n>`; die
bleibt stehen, gelöscht wird nie, und außerhalb des Umfangs ist sie kein Befund. **Exit 1 heißt anhalten:** `duplicate_key` und `duplicate_id` im
Bestand entscheidet der Lead; `forbidden_id`, `empty_field` und `shop_unknown` im Plan korrigierst du
in `plan.json`, `header` im Sheet korrigiert ein Mensch. **Ähnelt ein neuer Test einem bestehenden
mit anderem Text**, fragst du, ob er umbenannt wurde; sonst stünde derselbe Prozess zweimal da.
Bestätigt der Lead das, trägt der Plan den Text aus dem Bestand in `testcase`; Ablauf und erwartetes
Ergebnis bleiben die aus den Quellen.

### Step 6 — Plan und das Ja

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Zeig in einem Block, **was wo entsteht oder sich ändert, im Klarnamen**: das Sheet mit Namen und
Ordner, wenn es neu ist, und ob der Unterordner `Testing` neu entsteht; die Zeilen von `project.yml`,
die dieser Lauf einträgt, alt und neu; die neuen Testfälle ganz; je ersetztem alten und neuen Text;
die gleichen nur mit Zahl; die nicht mehr abgeleiteten mit Text, ist der Umfang nicht alle nur die, deren
Datei in `tests/` eine Anforderung im Umfang nennt; die nicht testbaren Anforderungen
mit Grund; je Test die Datei `tests/‹ID›.md` mit den Anforderungen, die er verkettet, und seinen
Quellen; **„Interna: keine"**, oder die Stelle, an der ein Testfall etwas Internes trägt (§278,
[ref-testcase.md](ref-testcase.md), Form einer Zeile). Zu jeder Zeile `ERGEBNIS <n>` fragst du
einzeln: Status und Ist-Ergebnis dort gelten dem alten Ablauf.

Aufbau, Frage und Ja nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`. Entsteht und ändert sich nichts, sagt der Block das, und du fragst nicht:
Steps 7 und 8 schreiben dann nichts, Step 9 läuft.

### Step 7 — Das Sheet anlegen und eintragen

Was dieser Lauf außer `e2e_sheet` in `project.yml` einträgt (`language`, `title`), trägst du zuerst
ein ([ref-sheet.md](ref-sheet.md), Steckbrief), auch wenn kein Sheet entsteht.

Nur wenn `e2e_sheet` leer ist und kein Rest gefunden wurde: Sheet im Unterordner `Testing`, den du
direkt davor findest oder anlegst, die Tabs `Testfälle` und `Übersicht`, die Kopfzeile wörtlich,
formatiert mit Dropdowns, bedingten Formaten und Schutz, die Übersicht mit ihren Formeln
([ref-sheet.md](ref-sheet.md), Anlegen); scheitert nur das Formatieren oder die Übersicht, nennt der
Bericht die Meldung wörtlich, und der Lauf geht weiter. **Die Spreadsheet-ID geht erst in
`project.yml`, wenn die Tab-Namen zurückgelesen sind**, und nur als Wert von `e2e_sheet`
([ref-sheet.md](ref-sheet.md), Steckbrief). Hat sich die Datei seit Step 2 geändert, zeigst du die
Änderung und fragst. Erst danach schreibst du Testfälle: ein Sheet ohne Eintrag findet der nächste
Lauf nur über die Suche.

### Step 8 — Die Testfälle schreiben

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht** in einen Testfall
(§236; was darunter fällt, sagt der Datalayer-Vertrag).

**Ein Aufruf für den Tab** mit Bereich und Werten aus `update.json` ([ref-sheet.md](ref-sheet.md),
Schreiben). Direkt davor exportierst du den Tab neu und rufst das Script noch einmal; weicht sein
Ergebnis vom gezeigten ab, zeigst du die Abweichung und fragst. Die Spalten G bis L (`Status` bis
`Getestet am`) schreibst du nie, auch nicht leer. Scheitert der Aufruf, bleibt stehen, was steht; der
Bericht nennt Bereich und Meldung.

### Step 9 — Zurücklesen und die Dateien je Test schreiben

Exportier den Tab neu und ruf das Script mit dem Plan und `--tests tests`
([ref-sheet.md](ref-sheet.md), Zuordnung): **jeder geplante Testfall meldet `GLEICH`**, kein
`duplicate_key` und kein `duplicate_id`, und jede Zeile mit Status oder Ist-Ergebnis trägt es noch.
Erst dann schreibt das Script die Dateien je Test und liest sie zurück; `test_file_not_back` heißt,
`tests/` bleibt, wie es war, und der Bericht nennt die Zeile. Lies `Übersicht` zurück
([ref-sheet.md](ref-sheet.md), Anlegen, Schritt 9): `Testfälle gesamt` ist die Zahl der Zeilen mit
Text in `Testfall`, und kein Wert ist `#ERROR!`. Eine Abweichung nennst du mit Zeile.

### Step 10 — Prüfen, `readme.md`, Commit

Nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Schritt 1, 5 und 6: `check-repo.py`, dann
`project-readme.py` (es nennt den Link des E2E-Sheets), dann ein Commit mit den Dateien unter
`tests/`, `project.yml`, wenn der Lauf es geändert hat, und `readme.md` und `way-of-working.md`, wenn
sie sich geändert haben; Nachricht `e2e-testing-sheet: <was>`. **Die Schritte 2 bis 4, die Projektion
in die Anforderungsliste, entfallen**: keine Spalte dort hat ihre Quelle in `tests/`
(`${CLAUDE_SKILL_DIR}/../../docs/requirements-list-contract.md`). Hat der Lauf weder `tests/` noch
`project.yml` geändert, committest du sonst nichts. Die Zeile nach `.claude/metrics/runs.md` geht dann allein in einen Commit `metrics: e2e-testing-sheet` (Wurzel-`CLAUDE.md`, §246).

### Step 11 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (Wurzel-`CLAUDE.md`, §397): den Umfang; Link des Sheets und ob es neu ist; neue (mit ID), ersetzte, gleiche und
nicht mehr abgeleitete Testfälle mit Zahl, die letzten wie in Step 6; die gelesenen Epics mit der Fassung ihres Entwurfs und die
Epics ohne Entwurf; die nicht testbaren Anforderungen mit Grund; offene Fragen zu Übergängen; jede
Datum in `Getestet am`, das nicht die Form der Sprache hat (§337).

Dann die Läufe, die Grundlage liefern: `requirements-update` für Anforderungen ohne
Akzeptanzkriterien, und sobald Ergebnisse vorliegen, denn sie sind Material; `solution-design` für
Anforderungen ohne entschiedenen Lösungsansatz und für Epics ohne Entwurf. **Du rufst keinen auf**; der Lead
ruft ihn.

## Wann nachfragen (NICHT raten)

- Zwei Anforderungen beschreiben denselben Übergang verschieden: eine Frage, kein Test mit einer
  Lesart.
- Ein Akzeptanzkriterium ist nicht beobachtbar formuliert: du nennst es und schreibst den Test nicht
  schärfer, als die Quelle ihn trägt.
- Unklar, ob zwei Abläufe ein Prozess sind oder zwei: frag den Lead.

## Was dieser Lauf nicht tut

Er schreibt keine Anforderung, kein Epic, keinen Entwurf und nichts in die Anforderungsliste. Er
bewertet keine Ergebnisse, legt für einen Fehler kein Ticket an und nimmt Ergebnisse nicht als
Material auf. In `project.yml` schreibt er nur `e2e_sheet` und, wenn sie leer waren, `language` und
`title`; im Datalayer sonst nur die Dateien unter `tests/`, und `readme.md` über die Projektion.
