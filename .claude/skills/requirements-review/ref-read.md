# Den Stand lesen und zählen: die Aufrufe dieses Laufs

**Der Stand ist das Repo** (§280): die Anforderungen in `requirements/`, die offenen Fragen in
`gaps/`, die Entscheidungen in `decisions/`, die Architektur in `architecture.md`. Aus dem Sheet liest
dieser Lauf nur, was dort seine Quelle hat und was er braucht: die Spalte `Cluster` für einen Umfang
nach Workstream (§280, Regel 5). Arbeitsdateien liegen im Temp-Ordner des Laufs (`mktemp -d`), außerhalb
des Repos (§233).

## Die Liste zum Prüfen

Eine Zeile je Anforderung, ohne Beschreibung und Ist-Zustand. `--umfang` ist `alle`, IDs mit Komma
(`REQ-012,REQ-014`), ein Workstream wörtlich, wie er in der Spalte `Cluster` steht, oder
`source:<Termin oder Notiz>` für den Input einer Session; die Spalte `umfang` oder `andere` sagt,
wohin die Anforderung im Bericht gehört. Alle übrigen Anforderungen stehen trotzdem in der Liste: der
Umfang begrenzt, was du berichtest, nicht was du liest (§305).

```
python3 ${CLAUDE_SKILL_DIR}/scripts/review-list.py . --umfang '<Umfang>' [--cluster cluster.tsv] [--shops '<key>,<key>']
python3 ${CLAUDE_SKILL_DIR}/scripts/review-list.py . --zeile REQ-012
```

Die Ausgabe ist je Anforderung: ID, Umfang, Cluster, `status`, `scope`, `title`, `source` (gekürzt),
`epic`, Befunde; am Ende die Zahl. Die Befunde stehen im Kopf des Scripts: `ohne_quelle`,
`duplikat_ohne_verweis`, `ausklammerung_ohne_adr`, `fragen_offen=N`, `blockiert=N` und, nur mit
`--shops`, `shop_unbekannt=<schlüssel>`; dazu `ist_ungeprueft_ohne_frage` und
`kriterien_leer_ohne_frage` für die Sichten „IST ungeprüft ohne Frage“ und „Verhalten ohne
Kriterium“. Beide sind Kandidaten: ob eine Frage den Ist-Zustand oder ein Kriterium meint, liest das
Script am Wortlaut, und prüfst du mit `--zeile`; Kriterien, die dastehen und trotzdem kein prüfbares
Verhalten tragen, findest du selbst. `--shops` gibst du nur, wenn `shops` in `project.yml` mehr
als einen Eintrag trägt, mit allen `key`, wie sie dort stehen; `shop_unbekannt` nennt dann einen
Schlüssel im Feld `shops` einer Anforderung, den die Liste nicht trägt (§307). Die Spalte `title`
zeigt den Shop-Bezug hinten, `(B2B)` oder `(alle Shops)`.
Beschreibung, Kriterien, Ist-Zustand und offene Fragen einer einzelnen Anforderung holst du
mit `--zeile`. Exit 1 nennt eine ID oder einen Workstream, den es nicht gibt (mit den vorhandenen
Werten), einen Termin, den keine `source` nennt (mit den vorhandenen Quellen), oder eine Datei, die
nicht lesbar ist; Exit 2 einen falschen Aufruf oder eine fehlende Spalte.

**Für den Input einer Session** nimmst du den Termin, wie `source` ihn schreibt („Workshop ‹Titel›
vom ‹Datum›“, bei `en` „Workshop ‹title› on ‹date›“, die Wendung `source_workshop` in
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“, §337), oder
den Dateinamen der Notiz; das Script sucht den Text in `source` ohne
Unterschied in Groß- und Kleinschreibung. Nennt der Aufruf nur einen Tag oder ein Thema, wählst du
den Termin aus `notes/` und nennst ihn im Bericht. Eine Anforderung, die eine Session nur korrigiert
oder ergänzt hat (`; korrigiert: ‹Quelle›`, `; ergänzt: ‹Quelle›`, bei `en` `; corrected: ‹source›`,
`; added: ‹source›`), gehört damit auch zu ihrem Input. Ein Repo kann beide Sprachen tragen, wenn
`language` gewechselt hat; du erkennst beide Formen.

**Für einen Umfang nach Workstream und für die Frage nach dem Umfang** liest du vorher die Spalten `ID` und `Cluster` des Tabs
`Anforderungen` (`en`: `Requirements`), nicht den ganzen Tab: `Google_Sheets.get_values` je ein Aufruf
mit `range` = `'Anforderungen'!A1:A` und `'Anforderungen'!E1:E`. Die Antwort trägt `values` als Liste
von Zeilen, leere Zellen am Ende fehlen, und die Zeilennummer ist die Stelle plus eins. Daraus
schreibst du `cluster.tsv` mit der Kopfzeile `ID<TAB>Cluster`, eine Zeile je Zeile des Tabs, mit
`csv.writer` und Tab als Trenner. Eine Anforderung, die im Sheet noch fehlt, hat keinen Cluster.

## Die abgelaufene Frist

`Verantwortlich` und `Bis` einer offenen Frage sind Felder der Menschen im Tab `Offene Punkte`
(`en`: `Open items`) und stehen nicht in `gaps/` (§280, Regel 5). Du liest nur die drei schmalen
Spalten: `Google_Sheets.get_values` je ein Aufruf mit `range` = `'Offene Punkte'!A1:A`,
`'Offene Punkte'!G1:G` und `'Offene Punkte'!H1:H`. Ein Befund ist eine Zeile, deren Kennung in `gaps/`
mit `status: open` steht und deren `Bis` ein Datum vor heute trägt; ein leeres `Bis` ist keiner. Ein
Wert, den du nicht sicher als Datum liest, nennst du wörtlich als Kandidat. Ohne Sheet entfällt die
Sicht, und der Bericht sagt es.

## Die Fragen, die neueres Material beantwortet

Für jede offene Frage in `gaps/` (`status: open`) prüfst du, ob eine Notiz in `notes/`, die jünger ist
als `opened`, sie beantwortet: du suchst mit `grep -il` nach den Stichworten der Frage in den Notizen
ab ihrem Datum und liest nur die Treffer. Eine Antwort dort ist ein Befund für `requirements-update`,
das sie aus dem Material schließt; du schließt sie nicht.

## Prüfen

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-repo.py .
```

Exit 0 ohne Befund, 1 mit einer Zeile `<prüfung> <Datei oder Kennung> <Satz>` je Befund. Der Bericht
nennt sie wörtlich; jede gehört dem Lauf, der die Datei schreibt (`epic` gehört `epic-structure`,
`gap_target` dem Lauf, der die Frage angelegt hat, `page_type` und `sections` `requirements-update`
und `solution-design`).
