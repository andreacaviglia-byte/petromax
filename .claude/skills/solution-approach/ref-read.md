# Die Anforderungen lesen: die Aufrufe dieses Laufs

**Die Anforderungen stehen im Repo** (§280), je eine Datei in `requirements/`. Aus dem Sheet liest
dieser Lauf nur die Spalte `Cluster` (der Workstream, §336), wenn der Aufruf einen Cluster nennt:
sie ist ein Feld der Menschen und hat ihre Quelle dort (§280, Regel 5). Arbeitsdateien liegen im
Temp-Ordner des Laufs (`mktemp -d`), außerhalb des Repos (§233).

## Die Liste

Eine Zeile je Anforderung im Umfang, mit gekürzter Beschreibung und dem Lösungsansatz, den die Datei
schon trägt. Anforderungen mit `status` `rejected` oder `duplicate` zählt das Script nur; eine mit
`scope: out_of_scope` bekommt Lösungsansätze wie jede andere, denn sie bekommt ein Ticket in der
Wunschliste (§284). `--umfang` ist `alle`, IDs mit Komma (`REQ-012,REQ-014`) oder ein Cluster
wörtlich.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/approach-list.py . --umfang '<Umfang>' [--cluster cluster.tsv]
python3 ${CLAUDE_SKILL_DIR}/scripts/approach-list.py . --zeile REQ-012
```

Die Ausgabe ist je Anforderung: ID, Cluster, `status`, `scope`, `title`, Beschreibung (gekürzt),
Lösungsansatz (`entschieden:` oder `blockiert:` mit `classification`, `vorgeschlagen:` mit dem Namen
des ersten Lösungsansatzes und, bei mehreren, der Zahl der übrigen als `(+2)`, sonst leer). Am Ende
stehen die Zahl im Umfang und die Zahl der nur gezählten, darunter die Zeile „ohne Lösungsansatz
(Design-Epic, §297)“ mit den Anforderungen mit `standard: design-concept` oder `design-qa`: sie
stehen nicht in der Liste und bekommen keinen Lösungsansatz. **`--zeile` gibt Beschreibung,
Kriterien, Ist-Zustand und Lösungsansätze einer Anforderung ganz aus; du rufst es für jede
Anforderung im Umfang, die du bearbeitest** (§401), eine nach der anderen: die Liste trägt den
Überblick, das Urteil fällt an der ganzen Anforderung. Exit 1 nennt die Prüfung: `umfang`, wenn ein Cluster oder eine ID nicht
vorkommt, mit den vorhandenen Clustern; `header`, wenn der Cluster-Datei eine Spalte fehlt; `object`,
wenn eine Datei nicht lesbar ist.

**Für einen Umfang nach Cluster** liest du vorher aus dem Tab `Anforderungen` (`en`: `Requirements`)
die Spalten `ID` und `Cluster` mit `Google_Sheets.get_values`, je ein Aufruf mit `range` =
`'Anforderungen'!A1:A` und `'Anforderungen'!E1:E`, nicht den ganzen Tab. Die Antwort trägt `values`
als Liste von Zeilen, leere Zellen am Ende fehlen. Daraus schreibst du `cluster.tsv` mit der Kopfzeile
`ID<TAB>Cluster`, je Zeile des Tabs eine Zeile, mit `csv.writer` und Tab als Trenner.
