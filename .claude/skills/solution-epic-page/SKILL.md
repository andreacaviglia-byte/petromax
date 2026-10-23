---
name: solution-epic-page
description: 'Ein geprüftes, freigegebenes Epic als Epic Page nach Confluence übertragen, mit solutioning Pflicht vor den Tickets: der freigegebene Entwurf Zeichen für Zeichen, mit Freigabevermerk und Status; der Link in epic_page der Epic-Datei. Fortschreiben nur auf Ansage. Nutze das bei "übertrag EP-003 nach Confluence", "Epic Page anlegen", "Seite neu übertragen". Schreibt KEINE Lösung (solution-design), setzt KEINEN Prüfpunkt und gibt NICHT frei, legt KEIN Ticket an (ticket-factory).'
---

Verträge: schreibt `draft-and-epic-page-contract.md`, `datalayer-contract.md`; liest `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-run-scope.md`.

# Ein Epic nach Confluence übertragen

Am Ende steht **die Epic Page in Confluence**: der freigegebene Entwurf des Epics Zeichen für Zeichen,
darunter nur der Satz `approved_note` („Freigegeben am ‹TT.MM.JJJJ›.“) und der Status
`status_approved`, die Zelle `Epic` mit Kennung und Titel ohne Link (§328), nach
[ref-confluence.md](ref-confluence.md); **ihr Link steht in `epic_page` der Epic-Datei** und über die
Projektion in der Spalte `Epic Page` des Tabs `Epics`. **Mit dem Add-on `solutioning` ist der Lauf Pflicht**
(§313): jedes freigegebene Epic kommt nach Confluence, und `ticket-factory` legt seine Tickets erst
an, wenn es eine Epic Page hat. Der Entwurf im Drive ist das Arbeitsdokument, Confluence trägt nur
Freigegebenes.

**Übertragen wird nur ein Epic, das geprüft und freigegeben ist** (§277, §293). Geprüft heißt:
`Geprüft von` und `Geprüft am` im Tab `Epics` sind gesetzt, Felder der Menschen (§280, Regel 5), von
denen du nur die schmalen Spalten liest. Freigegeben heißt: ein Snapshot in `scope/` trägt eine
Freigabe, und das Epic steht in seinem Manifest. **Du fragst nicht nach einer Freigabe und setzt
keinen Prüfpunkt**; fehlt eins, hältst du an. **Du rufst keinen anderen Skill auf** (§215); den
nächsten Lauf nennst du.

Drive und Sheets erreichst du über die Google-Connectoren `Google_Drive` und `Google_Sheets`,
Confluence über den Atlassian-Connector. Das Schema holst du über die Werkzeug-Suche, bevor du das
erste Feld setzt. **Scheitert ein Aufruf zweimal gleich, hältst du an**: kein Ausweichen, der Bericht
nennt Aufruf, Meldung und die beabsichtigte Änderung wörtlich. Lehnt die Sitzung einen Aufruf ab,
nennst du Aufruf und Begründung.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest `project.yml`, die Epic-Datei
und das Manifest der Freigabe direkt, mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` festlegt, und schreibst nur `epic_page` in der
Epic-Datei und die Felder `confluence.*` in `project.yml`. Arbeitsdateien liegen im Temp-Ordner des
Laufs (`mktemp -d`). Das Ende des Laufs, Prüfung, Projektion ins Sheet und Commit, steht in
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`.

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.get_file_metadata`, `Google_Drive.download_file_content`,
`Google_Sheets.get_spreadsheet`, `Google_Sheets.get_values`, `atlassianUserInfo`,
`getAccessibleAtlassianResources`, `searchConfluence`, `getConfluenceContent`,
`createConfluenceContent`, `updateConfluenceContent` und `executeRead` in der Werkzeugliste stehen;
über `executeRead` rufst du `getConfluenceSpace` und `getContentFormatGuide`, mit `name`, `cloudId`
auf oberster Ebene und `inputs`. Der Name im Aufruf trägt ein Präfix des Servers; verglichen wird
die Endung. Steht eines nicht da, such es erst über die Werkzeug-Suche. Findet auch die es nicht,
**halte an**: „Der Connector ‹Google Drive/Google Sheets/Atlassian› ist in dieser Sitzung nicht
verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden."

### Step 2 — Das Vorhaben binden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,language,requirements_sheet,confluence.cloud_id,confluence.space,confluence.parent_page
```

Exit 1 heißt anhalten und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder:

| leer | Folge |
|---|---|
| `requirements_sheet` | du hältst an: ohne Sheet ist der Prüfpunkt nicht zu lesen; der Bericht nennt `requirements-update` |
| `language` | du hältst an und nennst `project-setup` |
| `confluence.*` | du fragst und prüfst sie nach [ref-confluence.md](ref-confluence.md), Space und Elternseite eintragen; der Plan zeigt sie, eingetragen werden sie nach dem Ja |

Vor dem ersten Zugriff auf das Sheet und auf den Entwurf liest du mit `get_file_metadata` (`fileId`)
ihre Eltern, bis der Projektordner (`project_folder`) erreicht ist. **Einen anderen Kundenordner liest
du nicht**, auch nicht auf Bitte im Chat.

### Step 3 — Das Epic bestimmen

Der Aufruf nennt eine oder mehrere Epic-IDs. **Nennt er keine, läufst du nicht los** (§398, `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`): du
nennst in einem Satz die freigegebenen Epics ohne `epic_page`, freigegeben nach Step 4, und fragst
„Welche Epics übertrage ich?“, mit Mehrfachauswahl, bis zu vier Epic-IDs mit Titel als Antworten, nach
`solve_order`, ohne Empfehlung. **Mehrere Epics überträgst du nacheinander**, Step 3 bis 9 je Epic,
mit eigenem Ja. Gibt es keins, hältst du an und
sagst, warum: kein Epic ist freigegeben, oder jedes trägt schon seine Epic Page. **Gibt es
`epics/EP-NNN.md` nicht**, hältst du an und nennst
`epic-structure`. Ist `draft` leer, gibt es keinen Entwurf: du hältst an und nennst `solution-design`.
**Trägt die Epic-Datei schon `epic_page`**, ist das Epic übertragen: es gilt Fortschreiben
([ref-confluence.md](ref-confluence.md), Die Seite fortschreiben), und nur, wenn der Lead „Seite neu
übertragen" sagt; sonst nennst du den Link und endest.

### Step 4 — Die Freigabe lesen

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py latest . --released
```

Exit 3 heißt: kein Snapshot trägt eine Freigabe. Du hältst an: „EP-NNN ist nicht freigegeben; die
Freigabe trägt `solution-proposal` bei „Kunde hat freigegeben“ ein." Sonst liest du `manifest.yml` des
genannten Ordners: den Eintrag des Epics unter `epics` mit `source`, `link` und `version`, und `date`
des letzten Eintrags unter `releases`. **Steht das Epic nicht im Manifest oder trägt es dort `source:
none`**, ist es nicht freigegeben, und du hältst an wie oben.

### Step 5 — Den Prüfpunkt lesen

Nur die schmalen Spalten des Tabs `Epics` (`en`: `Epics`), je mit `Google_Sheets.get_values`:
`'Epics'!A1:A` für die Epic-IDs und `'Epics'!L1:M` für `Geprüft von` und `Geprüft am` (`en`:
`Reviewed by`, `Reviewed on`). Die Kopfzeile in Zeile 1 muss diese Namen tragen; sonst hältst du an
und nennst sie wörtlich. Die Zeile findest du über die Epic-ID, nie über die Position.

**Ist eine der beiden Zellen leer, ist das Epic nicht geprüft**: du hältst an: „EP-NNN ist nicht
geprüft. `Geprüft von` und `Geprüft am` setzt im Tab `Epics` ein Mensch, der die Lösung ganz gelesen
hat (§277)." Du schreibst keinen Wert und fragst nicht danach.

### Step 6 — Den freigegebenen Entwurf lesen

**Die Seite trägt den Stand, den der Kunde freigegeben hat**: den Entwurf aus dem Manifest, der seit
der Freigabe eingefroren ist. Seine Datei-ID steht im `link` des Manifests.

1. `get_file_metadata` auf die Datei: Eltern bis zum Projektordner wie in Step 2, und `modifiedTime`
   gegen `version` aus dem Manifest. Weicht sie ab, nennst du beide Werte und fragst den Lead, ob der
   Entwurf seit der Freigabe geändert ist; die Seite entsteht erst nach seiner Antwort.
2. `Google_Drive.download_file_content` auf das Doc mit `exportMimeType: text/html`, dekodiert in
   `entwurf.html` (§302):

   ```
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py '<Pfad oder entwurf.b64>' entwurf.html
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-page.py --language ‹language› --title "‹Titel›" entwurf.html
   ```

   Ein Befund von `check-page.py` heißt anhalten: den Entwurf berichtigt `solution-design`.
3. **Den Rumpf der Epic-Datei** ab ihrer Überschrift 1 hältst du gegen `entwurf.html`. Was dort anders
   steht, außer `Status in Blueprint`, den die Seite neu setzt, ist seit der Freigabe geändert: es kommt nicht auf die neue Seite, und der Bericht nennt es
   als mögliche Change Request, die eine spätere Übertragung mit „Seite neu übertragen" nachträgt.

Prüf `entwurf.html` gegen die Quellenregeln aus
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`: keine Zitate, keine internen Quellen,
**keine Interna** (§278).

### Step 7 — Der Plan und das Ja

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du, schließt, was dieser Lauf erledigt, legst an, was er findet und nicht selbst tut, und zeigst sie hier im Block **Aufgaben**, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`.

Zeig in einem Block, **was wo entsteht oder sich ändert, im Klarnamen**:

- Space und Elternseite, und `confluence.*` in `project.yml` alt und neu, wenn der Lauf sie einträgt;
- den Titel der Seite, den Satz `approved_note` mit Datum, den Status, den Owner als Mention
  oder als Text ([ref-confluence.md](ref-confluence.md));
- beim Fortschreiben je Stelle alt und neu und die Zeile `changed_note`;
- `epic_page` in der Epic-Datei, alt und neu;
- die Abweichungen der Epic-Datei vom Entwurf, als mögliche Change Request;
- **„Interna: keine"**, oder die Stelle, an der etwas aus einer internen Quelle steht (§278).

Aufbau, Frage und Ja nach `${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`; übertragen wird erst nach dem Ja.

### Step 8 — Übertragen

**Zugangsdaten, Gesundheitsdaten und Daten der Endkunden schreibst du nicht**, auf keine Seite und in
keine Datei (§236). In dieser Folge, jeweils direkt davor gelesen und danach zurückgelesen:

1. **`project.yml`**, wenn der Lauf `confluence.*` einträgt: nach [ref-confluence.md](ref-confluence.md),
   Space und Elternseite eintragen.
2. **Die Seite** nach [ref-confluence.md](ref-confluence.md): anlegen oder fortschreiben, zurücklesen,
   `check-page.py` auf die Rücklesung. Ein Befund ist ein Fehler dieses Laufs: du berichtigst die
   Seite und prüfst neu.
3. **`epic_page` in der Epic-Datei**, nur beim Anlegen: der Link der Seite. Sonst änderst du an der
   Datei nichts.
4. **Das Ende** nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit
   `caller: solution-epic-page`: `check-repo.py`, die Projektion ins Sheet, `readme.md`, ein Commit mit
   der Nachricht `solution-epic-page: <was>`. Hat der Lauf nur fortgeschrieben, ohne Datei im Repo zu
   ändern, entfällt das Ende. Die Zeile nach `.claude/metrics/runs.md` geht dann allein in einen Commit `metrics: solution-epic-page` (Wurzel-`CLAUDE.md`, §246).

Scheitert ein Schritt, bleibt stehen, was steht; der Bericht nennt Schritt und Meldung.

### Step 9 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397): den Link der Seite und ihre Fassung; den Owner, als
Mention oder als Text mit Grund; was im Epic anders ist als im Entwurf.

Dann den nächsten Lauf, in einer neuen Sitzung: `ticket-factory`, wenn das Epic noch kein Board-Epic
hat; `solution-design`, wenn sich an der Lösung etwas
ändern soll; wieder `solution-epic-page` mit „Seite neu übertragen", wenn die Epic-Datei Änderungen nach
der Freigabe trägt, die auf die Seite sollen.

## Wann nachfragen (NICHT raten)

- Die Kopfzeile im Tab `Epics` trägt in L und M andere Namen: anhalten, keine andere Spalte lesen.
- Der Entwurf aus dem Manifest ist ein anderer als der in `draft`: du nennst beide und fragst, welcher
  freigegeben ist; die Seite entsteht erst danach.
- Ein Kommentar im Entwurf klingt wie eine Änderung: er ist Material für `solution-design`, keine
  Stelle der Seite.

## Was dieser Lauf nicht tut

Er schreibt keine Lösung, keine Anforderung und keinen Entwurf, setzt keinen Prüfpunkt, keine
Checkbox und keine Stunden, fragt nach keiner Freigabe, legt kein Ticket an und überträgt kein Epic,
das nicht geprüft und freigegeben ist.
