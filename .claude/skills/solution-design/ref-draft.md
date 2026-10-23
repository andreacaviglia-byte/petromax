# Den Entwurf führen: Zustände, Projektion, Prüfliste

**Die Form von Epic-Datei, Entwurf und Epic Page setzt der Vertrag**
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md` (§325): Bezeichnungen, Vorlage, Titel,
Kopf, Abschnitte, Stil und Quellenregeln. Hier steht, wie dieser Lauf den Entwurf führt. Die Tiefe der
Angaben in `Technical Information` nach der Wahl steht in [ref-options.md](ref-options.md); wann ein Lauf
die Wissensbasis für einen Lösungsansatz mit `KB: nicht gelesen` gelesen hat und der Satz `kb_unread` fällt, in
[ref-sources.md](ref-sources.md) (§268).

## Die Zustände

`solution-design` liest den Zustand an der Epic-Datei, am Entwurf und an `scope/`:

| Zustand | woran du ihn erkennst |
|---|---|
| kein Entwurf | der Rumpf der Epic-Datei ist leer, `draft` im Kopf ist leer, und in `Epics` liegt kein Doc mit der Epic-ID im Namen |
| Wahl offen | mindestens eine Anforderung des Epics trägt in `Technical Information` Lösungsansätze mit Empfehlung, oder eine hat noch keinen Lösungsansatz |
| Wahl benannt | wie eben, und der Lead nennt die Wahl im Dialog, oder ein Kommentar am Entwurf nennt sie und der Lead bestätigt sie |
| zur Prüfung | jede Anforderung trägt ihren Lösungsansatz oder, mit dem Ja des Leads, `decision_open`, außer im Epic der Domäne `design`; `Status in Blueprint` ist `status_for_approval`. Geprüft wird von Hand: `Geprüft von` und `Geprüft am` im Tab `Epics` setzt ein Mensch, der die Lösung ganz gelesen hat (§277); kein Lauf setzt sie und kein Lauf fragt nach ihnen |
| freigegeben | ein Snapshot in `scope/` trägt eine Freigabe (`scope-snapshot.py latest . --released`), und das Epic steht in seinem Manifest. **Die Freigabe friert den Entwurf ein** (§277): kein Lauf schreibt ihn mehr fort |

**Ein Epic der Domäne `design`** trägt keinen Lösungsansatz (§297): die Zustände Wahl offen und Wahl benannt
gibt es dort nicht.

**Nach der Freigabe** ändert ein Lauf von `solution-design` weiter die Epic-Datei und die Dateien der
Anforderungen, wenn der Lead es bestätigt; der Entwurf bleibt die freigegebene Fassung. Der Bericht
nennt jede Änderung als mögliche Change Request, `ticket-factory` für die Tickets, an denen sie
nachgezogen werden muss, und `solution-epic-page`, wenn eine Seite in Confluence steht.

## Den Entwurf projizieren

**Der Entwurf wird einmal angelegt und danach gezielt fortgeschrieben, nie ersetzt** (§302). Er gehört
auch anderen: der Kunde kommentiert, der Lead ändert von Hand. Ein Aufruf, der den ganzen Inhalt
ersetzt, verliert die Anker der Kommentare; ein neues Doc verliert sie ganz.

**1. Die Kommentare lesen**, bevor der Lauf etwas ändert. Den Entwurf findest du über `draft` im Kopf
der Epic-Datei, sonst mit `Google_Drive.search_files` in der Liste von `Epics` (`query` =
`parentId = '‹Epics›' and title contains '‹Epic-ID›'`, `excludeContentSnippets: true`, jede Seite über
`pageToken`); zwei Treffer: anhalten und beide mit Link nennen. Dann `Google_Drive.read_file_content`
mit `includeComments: true`: je Kommentar sein Wortlaut, wer ihn schrieb, und der Text, an dem er
hängt. Wie Antworten auf einen Kommentar in dieser Ausgabe erscheinen, ist ungemessen; fehlt eine
Antwort, die der Lead nennt, sagt der Bericht es.

**2. Abweichungen lesen.** `Google_Docs.read_doc` mit `documentId` liefert den Text mit `startIndex`
und `endIndex` je Absatz und Zelle. Du hältst ihn Absatz für Absatz und Zelle für Zelle gegen den Rumpf
der Epic-Datei: was im Doc anders steht, hat jemand dort geändert, denn nur dieser Skill schreibt den
Rumpf und projiziert ihn im selben Lauf. **Eine Abweichung ist Material wie ein Kommentar, keine
Korrektur**: du legst sie vor (Step 7), das Repo bleibt die Quelle (§280).

**3. Anlegen**, wenn es noch keinen Entwurf gibt, nach dem Ja und nachdem die Dateien im Repo
geschrieben und zurückgelesen sind. Den Rumpf der Epic-Datei, ab ihrer Überschrift 1, schreibst du als
`entwurf.md` in den Temp-Ordner und prüfst ihn mit `check-page.py` (unten); der Kopf in YAML geht nicht
in den Entwurf, er trägt Felder des Repos und keine Lösung. Dann `Google_Drive.create_file` mit `title`
= der Titel, `parentId` = die ID von `Epics`, `textContent` = der Inhalt von `entwurf.md` und
`contentMimeType: text/markdown`. Daraus entsteht ein Google-Doc mit Überschriften, Tabellen, fett,
kursiv und Listen als Formatierung (gemessen am 04.10.2026). Der Link ist
`https://docs.google.com/document/d/‹ID›/edit`; er kommt in `draft` im Kopf der Epic-Datei. `Epics`
findest du direkt davor: `Google_Drive.search_files` mit `query` = `parentId = '‹Solutioning›' and
title = 'Epics' and mimeType = 'application/vnd.google-apps.folder'`; ein Treffer: seine ID; keiner:
`Google_Drive.create_file` mit `title: Epics`, `contentMimeType: application/vnd.google-apps.folder`,
`parentId` = die ID von `Solutioning`; zwei: anhalten und beide mit Link nennen. `Solutioning` findest
oder legst du davor nach dem Datalayer-Vertrag an (Die Ablage im Drive).

**4. Fortschreiben**, wenn es den Entwurf gibt, nach dem Ja und nachdem die Dateien im Repo geschrieben
und zurückgelesen sind. Geschrieben werden **nur die Stellen, die dieser Lauf im Rumpf geändert hat**:
der Rumpf vor dem Lauf gegen den Rumpf danach. Direkt davor liest du die Struktur noch einmal mit
`Google_Docs.read_doc`; dann `Google_Docs.update_doc`:

- einen eindeutigen Wortlaut (eine Zelle, der Status) mit `requests: [{replaceAllText: {replaceText,
  containsText: {text, matchCase: true}}}]`, nachdem du im gelesenen Text gezählt hast, dass er genau
  einmal vorkommt;
- einen neuen Absatz mit `requests: [{insertText: {text, location: {index}}}]` an einem Index aus dem
  `read_doc` direkt davor;
- mehrere Änderungen, auch eine neue Tabellenzeile, in **einem** `update_doc` mit den passenden
  `requests` (`insertText`, `replaceAllText`, `deleteContentRange`) in absteigender Folge der Indizes.

**Text, den jemand im Doc geändert hat, bleibt stehen**, bis der Lead zu seiner Abweichung entschieden
hat (Step 7); ändert dieser Lauf dieselbe Stelle, fragst du vorher. **Würde eine Änderung den Text
entfernen, an dem ein Kommentar hängt, fragst du vorher.** Auf Kommentare antwortest du nicht, und du
löst keinen auf.

**5. Zurücklesen und prüfen.** `Google_Drive.download_file_content` mit `fileId` = der Entwurf und
`exportMimeType: text/html` liefert das HTML als Base64 in `content`. Ist die Antwort groß, legt die
Sitzung sie als Datei ab und nennt den Pfad; dann dekodierst du sie in den Temp-Ordner des Laufs:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py '<Pfad aus der Antwort>' entwurf.html
```

Kommt sie direkt in der Antwort, schreibst du den Wert von `content` in `entwurf.b64` im Temp-Ordner
und dekodierst ebenso mit `python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py entwurf.b64 entwurf.html`.
`check-page.py` ist grün auf `entwurf.html`, und sein Text gleicht dem Rumpf der Epic-Datei, außer an
den Abweichungen, die nach Schritt 4 stehen bleiben; der Bericht nennt sie. **Ist ein neu angelegter
Entwurf kaputt**, kommt er mit `Google_Drive.trash_file` in den Papierkorb (§259), `draft` bleibt leer,
und der Bericht nennt die Abweichung. **Ist ein fortgeschriebener Entwurf kaputt**, hältst du an und
nennst Stelle und Meldung; ein Doc mit Kommentaren legst du nicht neu an.

Dazu liest du die Kommentare noch einmal und vergleichst sie mit Schritt 1: fehlt einer oder hängt er
an keinem Text mehr, nennt der Bericht ihn. Ob ein Kommentar am geänderten Absatz hängen bleibt, ist
ungemessen; dieser Vergleich misst es in jedem Lauf.

**Prüfen**, an `entwurf.md` vor dem Anlegen und an der Rücklesung:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-page.py --language ‹language› --title "‹Titel›" entwurf.md
```

`‹language›` ist `language` aus `project.yml`, oder die Sprache, die der Lead für diesen Lauf nennt.
Jeder Befund ist ein Fehler dieses Laufs: du berichtigst den Rumpf der Epic-Datei und prüfst neu.

**Ist das Epic freigegeben** (Die Zustände), wird der Entwurf nicht mehr fortgeschrieben; die Schritte
3 bis 5 entfallen, und der Bericht nennt die Änderungen im Repo als mögliche Change Request.

## Prüfliste vor `status_for_approval`

Die Liste läuft, bevor du `Status in Blueprint` auf `status_for_approval` setzt. Du prüfst und
berichtest; eine Checkbox setzt du dafür nicht, und `Geprüft von` und `Geprüft am` setzt ein Mensch
(§277).

- [ ] `check-page.py` ist grün auf dem Rumpf der Epic-Datei und auf der Rücklesung des Entwurfs.
- [ ] Jede Anforderung des Epics steht genau einmal im Dokument (`once_on_page` grün).
- [ ] Jede Zeile trägt ihren Lösungsansatz oder, mit dem Ja des Leads, „Entscheidung offen, entscheidet ‹Gewerk›";
  im Epic der Domäne `design` entfällt der Punkt (§297).
- [ ] Keine offene Frage im Dokument, kein Abschnitt für offene Punkte.
- [ ] `Estimation` und `Initial Estimate` sind leer, alle Checkboxen offen.
- [ ] Keine Zitate, keine internen Quellen und keine Interna, nach den Quellenregeln des Vertrags.
