# Der Abgleich gegen die Freigabe und der Snapshot am Ende der Discovery

Ein Snapshot in `scope/` hält den Stand der Anforderungsliste fest, wogegen ein Kunde freigegeben hat
oder mit dem die Discovery endet (§266, §280 Regel 8). Er ist Kontext, nie Wahrheit: was gilt, steht
im Repo. Form und Fälle setzt `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
`scope/`; geschrieben und verglichen wird nur über
`${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py`. Gelesen werden die vier Tabs wie für die
Projektion (`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Schritt 2), in Dateien im Temp-Ordner
des Laufs; die Tab-Namen stehen in der Sprache aus `language`.

## Der Abgleich gegen die Freigabe

**Pflicht vor dem ersten Vorlegen des Laufs, wenn es einen freigegebenen Snapshot gibt** (§266):

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py latest . --released
```

Exit 3 heißt, es gibt keinen, und der Abgleich entfällt. Sonst nennt die Ausgabe den Ordner, und du
vergleichst den Stand des Sheets vor diesem Lauf mit ihm:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py compare . scope/‹ordner› --tab Anforderungen=anforderungen.json --tab Solutioning=solutioning.json --tab Epics=epics.json --tab "Offene Punkte"=offene-punkte.json
```

| Zeile | heißt |
|---|---|
| `NEU ‹Tab› ‹ID› \| ‹Titel›` | die Zeile steht heute im Sheet, im Snapshot nicht |
| `ENTFERNT ‹Tab› ‹ID› \| ‹Titel›` | die Zeile stand im Snapshot, heute nicht |
| `GEÄNDERT ‹Tab› ‹ID› \| ‹Spalte›: „alt“ → „neu“` | eine Zelle ist anders |
| `KOPF ‹Tab› \| …` | die Kopfzeile ist anders |
| `ABWEICHUNGEN ‹n›` oder `GLEICH` | Exit 3 oder Exit 0 |

Die Zeilen stehen im Block über den Änderungen unter „Seit der Freigabe vom ‹TT.MM.JJJJ›“. **Jede
Änderung dieses Laufs an einer Anforderung, die der Snapshot trägt, ist ebenfalls eine mögliche Change
Request**, und der Block markiert sie so. **Du meldest nur, du entscheidest nichts**: was davon eine
Change Request ist, entscheidet der Lead mit dem Kunden, und geschrieben wird, was er bestätigt.
Exit 1 nennt einen Snapshot, dem eine Datei fehlt (`snapshot`); dann nennst du die Zeile wörtlich,
und der Abgleich entfällt.

## Der Snapshot am Ende der Discovery

**Nennt der Lead das Ende der Discovery**, hältst du den Stand fest, nachdem die Projektion dieses
Laufs geschrieben ist: der Snapshot zeigt das Sheet, das der Kunde sieht. Im Plan aus Step 7 steht er
als eigene Zeile („Snapshot `discovery` nach der Projektion“). Ist die Projektion unterblieben, entsteht
kein Snapshot, und der Bericht nennt es.

Du liest die vier Tabs neu, nach der Projektion, und nimmst die Lesezeit in UTC:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/scope-snapshot.py write . --occasion discovery --sheet ‹requirements_sheet› --read-at ‹JJJJ-MM-TTThh:mmZ› --tab Anforderungen=anforderungen.json --tab Solutioning=solutioning.json --tab Epics=epics.json --tab "Offene Punkte"=offene-punkte.json
```

Ohne `--pages`: am Ende der Discovery trägt kein Epic einen Entwurf. Trägt eines doch schon einen,
lehnt das Script mit `epic` ab; dann nennst du die Zeile, und der Snapshot entsteht mit
`solution-proposal`, nicht hier. Die Ausgabe `SNAPSHOT scope/‹ordner›` nennt den neuen Ordner; er geht
in den Commit des Laufs. Exit 1 nennt die Prüfung (`input`, `header`, `read_at`, `sheet`, `epic`,
`readback`); dann ist nichts geschrieben, und der Bericht nennt die Zeile wörtlich.
