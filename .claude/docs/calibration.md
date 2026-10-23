# Die Kalibrierung — ein Korrekturfaktor je Bereich für die Modellschätzung

**Die KI schätzt die Größe (`S` bis `XL`); Stunden schätzt sie nur als Modellschätzung**
(§280, Regel 10; §357). Stunden je Anforderung setzt ein Mensch in `Aufwand (h)` im Tab `Solutioning`
(§283). Was eine Größe trägt, sagt die Größentabelle in
[`solution-choice-contract.md`](solution-choice-contract.md) (§326).

**`effort_estimate_model` ist die Rohschätzung des Modells in Stunden** (§357); nur `solution-design`
setzt sie, und wie sie entsteht, legt dieser Skill fest. Diese Datei gibt keine Stunden vor und
begrenzt die Rohschätzung nicht; kein Lauf liest einen Faktor, bevor er schätzt. Warum eine Rohschätzung neben
der des Leads lag, zeigt ihre Zerlegung je Teil in `.claude/metrics/estimates/REQ-NNN.md`.

**Die Korrektur:** kalibrierte Modellschätzung = Rohschätzung × Faktor des Bereichs. Sie wird gerechnet,
nirgends gespeichert, damit ein neuer Faktor sofort gilt und die Rohwerte für die nächste Kalibrierung
bleiben.

**Bereiche sind die Positionen der Schätzung** (§355), wie `check-solution-doc.py` sie zuordnet: die
Domäne des Epics (`design`, `data_migration`, `content_migration`) vor dem ersten Wert in
`classification`. Für „Lösungsansatz offen“ gibt es keinen Faktor; eine entschiedene Lösung trägt
immer einen Lösungsansatz.

**Stufe 1 kalibriert gegen den Lead:** der Faktor je Bereich ist der Median von `Aufwand (h)` ÷
Rohschätzung über alle Paare, und der Nachweis ist, dass die kalibrierte Modellschätzung je Bereich
nahe an `Aufwand (h)` liegt. Stufe 2 misst später Modell, Lead und Ist-Aufwand gegeneinander.

**Ein Aufschlag in `Aufwand (h)` geht in den Faktor ein.** Rechnet ein Lead einen Risikoaufschlag in
seine Stunden, ohne ihn auszuweisen, liegt die kalibrierte Modellschätzung um ihn höher, und niemand
sieht es; wer die Faktoren setzt, fragt deshalb vorher, ob und wie viel Aufschlag in `Aufwand (h)`
steckt, und nennt ihn in `basis`.

**Die Faktoren setzt ein Mensch**, aus der Ausgabe von
`python3 .claude/scripts/calibration-report.py <projekt-repo> <hours.json>`, mit `hours.json` als der
schmalen Spalte `Aufwand (h)` mit `ID` aus dem Tab `Solutioning`, in der Form, die `solution-estimate`
liest, im Temp-Ordner, nie im Repo: je Bereich die Zahl der Paare, den Median Lead ÷ Roh als neuen Faktor, die
Abweichung mit dem aktuellen Faktor und ihre Spanne. Darunter zeigt der Bericht je Größe, getrennt für
`size` und `size_estimate_approach`, die Zahl der Anforderungen mit `Aufwand (h)` und Median, kleinsten
und größten Wert von `Aufwand (h)`: so sieht ein Mensch, wie gut das Modell Größen schätzt; ein Faktor
entsteht daraus nicht. Er trägt `factor`, `pairs`, `median_deviation`,
`basis`, `source` und `as_of` ein; kein Lauf schreibt in diese Datei. Das Script liest die Tabelle,
darum bleibt sie in dieser Form.

**Die Startwerte stammen aus dem Archiv** (Agentkit, Stand 2026-08-06), je mit `n=0`; der erste
gemessene Faktor ersetzt sie. Dort senkte ein Faktor von 0,35 bis 0,80 die Stunden für UX/UI, weil
Sections über die Seitentypen wiederverwendet werden, und ein Zuschlag von ×1,10 bis ×1,40 hob die
Entwicklungsstunden für Edge Cases an; beides steht hier als Faktor 0,55 für UX/UI und 1,2 für
Erweiterte Shop-Features und Custom-Erweiterungen, die übrigen Bereiche beginnen bei 1,0.

| area | factor | pairs | median_deviation | basis | source | as_of |
|---|---|---|---|---|---|---|
| shop_setup | 1.0 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| shop_features | 1.2 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| ux_ui | 0.55 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| custom_extensions | 1.2 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| interfaces | 1.0 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| data_migration | 1.0 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |
| content_migration | 1.0 | 0 |  | Startwert n=0 | Archiv, Agentkit, Stand 2026-08-06 | 2026-10-13 |

| Spalte | Inhalt |
|---|---|
| `area` | der Bereich, der Schlüssel der Position aus `POSITIONS` in `check-solution-doc.py`: Shop-Setup `shop_setup`, Erweiterte Shop-Features `shop_features`, UX/UI `ux_ui`, Custom-Erweiterungen `custom_extensions`, Schnittstellen `interfaces`, Daten-Migration `data_migration`, Content-Migration `content_migration` |
| `factor` | der Korrekturfaktor, eine Zahl größer 0 mit Dezimalpunkt |
| `pairs` | die Zahl der Paare aus Rohschätzung und `Aufwand (h)`, aus denen der Faktor stammt; `0` für einen Startwert |
| `median_deviation` | die Abweichung nach Korrektur: der Median der absoluten Abweichung der kalibrierten Modellschätzung von `Aufwand (h)` in Prozent; leer für einen Startwert |
| `basis` | der Stand des Faktors: `Startwert n=0` oder `Stufe 1 n=‹Zahl›` (gegen den Lead), später `Stufe 2 n=‹Zahl›` (gegen das Ist) |
| `source` | woraus der Faktor stammt, etwa die Vorhaben, deren Paare gezählt sind |
| `as_of` | das Datum, an dem der Faktor gesetzt wurde, `JJJJ-MM-TT` |
