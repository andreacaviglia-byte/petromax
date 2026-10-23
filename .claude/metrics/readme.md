# Laufzeit und Kosten je Lauf

**Dieser Ordner gehört nicht zum Vorhaben** (§246). Kein Skill liest ihn. Das Template liefert
`run-metrics.py` und diese Datei; `runs.md` entsteht im Projekt-Repo mit dem ersten Lauf, und
`project-upgrade` fasst sie nie an (§237).

**`estimates/` trägt die Zerlegung der Modellschätzung** (§357), je Anforderung eine Datei
`REQ-NNN.md`, geschrieben nur von `solution-design` mit `effort_estimate_model`. Sie erklärt bei der
Kalibrierung, warum das Modell neben dem Lead lag; kein Skill liest sie, und `project-upgrade` fasst
sie nie an.

Am Ende jedes Laufs, direkt vor seinem Commit, schreibt die Sitzung eine Zeile:

```
python3 .claude/metrics/run-metrics.py --skill <skill> [--cost <usd> --ccr-session <id>]
```

In einer Cloud-Sitzung gehen davor zwei Schritte, die die Kosten früherer Läufe genau machen:

```
python3 .claude/metrics/run-metrics.py --open --ccr-session <eigene id>
python3 .claude/metrics/run-metrics.py --settle <id>=<usd> [--settle <id>=<usd> ...]
```

`--open` nennt zeilenweise die ID jeder Cloud-Sitzung, deren letzte Zeile noch eine Untergrenze oder
`ungemessen` trägt, ohne die eigene. Je ID liefert `get_session(session_id)` den genauen Wert als
`cost_usd`; `--settle` setzt ihn in die Zeile. Liefert `get_session` für eine ID keinen Wert, bleibt
die Zeile, wie sie ist, und der Lauf geht weiter. Die eigene ID und die eigene Untergrenze liefert
`get_session` ohne `session_id`.

Die Zeile geht in den Commit des Laufs; committet ein Lauf sonst nichts, geht sie allein in einen
Commit `metrics: <skill>`, sonst ginge sie mit dem Container verloren oder hielte das nächste Upgrade an. Je Lauf eine frische Sitzung (§244): die Sitzung ist der Lauf.

## Die Spalten

| Spalte | Was |
|---|---|
| Datum | Tag des ersten Zeitstempels, Ortszeit |
| Skill | was `--skill` nennt |
| Sitzung | die ID der Cloud-Sitzung aus `--ccr-session` (`session_…`); ohne sie die ersten acht Zeichen der Sitzungs-ID des Protokolls, die ganze steht in seinem Dateinamen |
| Wandzeit | erster bis letzter Zeitstempel der Hauptsitzung, h:mm |
| aktiv | je Turn von der Eingabe des Leads bis zur letzten Zeile vor seiner nächsten Eingabe, ohne die Zeit, in der eine Rückfrage (AskUserQuestion) auf Antwort wartet, h:mm. Warten auf einen Subagent zählt mit. Steuert eine andere Sitzung den Lauf per `send_message`, ist ihre Nachricht die Eingabe, auch in der Cloud, wo sie als `task-notification` ohne Hülle ankommt. Erkennt das Script keine Eingabe, steht `ungemessen` |
| Eingabe, Cache lesen, Cache schreiben, Ausgabe | Tokens der Hauptsitzung und ihrer Subagents, je Antwort (`message.id`) einmal |
| Kosten | in USD, mit Quelle: „mind. … (get_session, ohne letzten Turn)“ (Wert aus `--cost`), `get_session` (genau, aus `--settle`), `Kostenstand` (aus dem Protokoll) oder `ungemessen` |
| Modell | das Modell der Antworten der Hauptsitzung |

## Wie gemessen wird

Das Script liest das Protokoll, das Claude Code auf der Maschine führt:
`~/.claude/projects/<ordner>/<sitzung>.jsonl`, die Subagents unter `<ordner>/<sitzung>/subagents/`.
`<ordner>` ist das Arbeitsverzeichnis der Sitzung mit `-` statt `/`. Ohne `--transcript` nimmt es das
jüngste Protokoll dort; das ist die laufende Sitzung.

Die Kosten nimmt es aus `--cost`. In einer Cloud-Sitzung liefert sie das Werkzeug `get_session` ohne
`session_id` als `cost_usd`, dazu die ID der Sitzung für `--ccr-session`. Fehlt `--cost`, nimmt es den letzten `cost-state` im Protokoll, wenn
danach keine Antwort mehr kam; sonst steht `ungemessen`. Kosten werden nie aus Tokens und Preisen
gerechnet, weil Preise sich ändern.

## Grenzen

- **`get_session` zählt den laufenden Turn nicht mit**: es liefert die Kosten bis zum Ende des
  vorigen Turns, im ersten Turn gar keine. Der Wert aus `--cost` ist deshalb eine Untergrenze, und
  ein Lauf, der in einem Turn durchläuft, ruft ohne `--cost` auf und bekommt `ungemessen` (§388);
  gemessen am 04.10.2026 an einer Schätzung: 0,56 USD in der Zeile, 4,53 USD nach dem Lauf. Nach dem Ende der Sitzung liefert
  `get_session(session_id)` die vollen Kosten; genau wird die Zeile deshalb erst im nächsten Lauf
  mit `--settle`. Eine Zeile ohne ID der Cloud-Sitzung bleibt eine Untergrenze.
- **Laufen mehrere Läufe in einer Sitzung**, ersetzt `--settle` nur die Untergrenze oder `ungemessen` in ihrer letzten
  Zeile; sie trägt dann die Kosten der ganzen Sitzung, die Zeilen davor ihre Untergrenze.
- **Einen `cost-state` schreibt Claude Code nur, wenn die Sitzung pausiert**, nicht am Ende eines
  Laufs. Auf dem Rechner eines Leads gibt es `get_session` nicht; dort steht ohne `--cost` meist
  `ungemessen`.
- **Die Tokens zählen nur Antworten, die im Protokoll stehen.** Die abgerechnete Menge liegt darüber;
  welche Aufrufe im Protokoll fehlen, ist ungemessen.
- **Wartet ein Werkzeugaufruf auf die Freigabe des Leads**, zählt das als aktiv. Ob das Protokoll
  diese Wartezeit kennzeichnet, ist ungemessen; das Script zieht nur die Rückfrage ab.
- Was nach dem Aufruf kommt, der Commit und der Bericht, fehlt in der Zeile.
