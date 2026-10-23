# Material finden und lesen

Die Drive- und Docs-Aufrufe gehen über den Google-Connector `Google_Drive` von claude.ai. Ihn und die
übrigen Connectoren sprichst du über die Werkzeug-Suche an, verglichen wird die Endung des Namens; das
Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt. Was gelesen ist, liegt als
Datei im Temp-Ordner des Laufs und wird von dort verarbeitet, nicht aus der Antwort: eine große Antwort
legt die Sitzung selbst als Datei ab, eine kleine steht in der Antwort, und du schreibst sie in eine.

## Im Projektordner suchen

| Zweck | Aufruf |
|---|---|
| `00 Material` und andere Unterordner finden | `Google_Drive.search_files` mit `query` = `parentId = '<project_folder>' and mimeType = 'application/vnd.google-apps.folder'` und `excludeContentSnippets: true` |
| Dateien eines Ordners | `search_files` mit `query` = `parentId = '<Ordner-ID>'` und `excludeContentSnippets: true`; jeder Unterordner einzeln |
| eine verlinkte Datei vor dem Lesen einordnen | `Google_Drive.get_file_metadata` mit `fileId`; die Antwort trägt `parentId` und `title`. Dann dasselbe auf ihren `parentId`, bis der Projektordner erreicht ist |

Gesucht wird nur mit `parentId`, nie über das ganze Drive. **Ein Listing kann gekappt sein**: bringt
die Antwort eine weitere Seite, holst du sie mit `pageToken`, bis keine mehr kommt. Ob die Liste
Dateien im Papierkorb enthält, ist ungemessen; die Suche kennt keinen Filter dafür. Die Größe jeder
Datei aus der Antwort brauchst du für die Prüfung auf einen stillen Deckel
([ref-source-defects.md](ref-source-defects.md)).

## Lesen je Art

| Material | Aufruf |
|---|---|
| Textdatei | `Google_Drive.download_file_content` mit `fileId`, ohne `exportMimeType` |
| PDF, Office | `Google_Drive.read_file_content` mit `fileId` |
| Google-Doc im Ordner oder verlinkt | `read_file_content` mit der ID aus dem Link oder der Liste |
| Google-Sheet | `download_file_content` mit `exportMimeType: text/csv`; das liefert nur den ersten Tab, weitere Tabs nennst du als ungelesen |
| Jira-Ticket | `getJiraIssue` mit `issueIdOrKey` aus dem Link, `fields` = `summary`, `description`, `status`, `comment`, `responseContentFormat: markdown`; `cloudId` ist `confluence.cloud_id` aus dem Steckbrief, fehlt sie, die Site aus dem Link |
| Kanal | `slack_read_channel`, ein Faden mit `slack_read_thread` |
| Termin-Mitschrift | `search_recording_transcripts` mit Titel oder Datum, dann `get_recording_transcript` |

**Auf die Platte.** Die Antwort von `download_file_content` trägt `content` als Base64. Ist sie groß,
legt die Sitzung sie als Datei ab und nennt den Pfad (gemessen am 04.10.2026: 280.691 Zeichen als
Datei); dann dekodierst du sie in den Temp-Ordner des Laufs:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/decode-export.py '<pfad>' quelle.txt
```

Kommt sie direkt in der Antwort, schreibst du den Wert von `content` in eine Datei im Temp-Ordner und
dekodierst sie mit demselben Script, diese Datei statt des Pfads. Den Text von `read_file_content` schreibst du in eine Datei im
Temp-Ordner; legt die Sitzung eine große Antwort selbst als Datei ab, nimmst du diese.
`read_file_content` kappt bei rund 467.000 Zeichen ohne Meldung
([ref-source-defects.md](ref-source-defects.md)). Scheitert das Lesen, steht die Quelle als ungelesen
im Bericht.

**Ist ein Link nicht erreichbar**, nennst du ihn als unerreichbar und sagst dazu, dass die Person die
Datei in den Projektordner legen kann.

## Die Herkunft

Im Kopf der abgelegten Datei steht als `Herkunft` der Dateiname im Projektordner, beim Link
die Adresse ohne Parameter, beim Ticket sein Schlüssel, beim Kanal Kanal und Zeitraum. Daran erkennt der
nächste Lauf, dass eine Quelle schon abgelegt ist.
