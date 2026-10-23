# Die Modellschätzung: Stunden aus der Lösung

**`effort_estimate_model` ist deine Rohschätzung in Stunden** (§357), und nur dieser Lauf setzt sie:
mit der Wahl, bevor der Lead schätzt. Du setzt sie nur, wenn `add_ons` in `project.yml` `solutioning`
führt, und nur mit `solution_status: decided`; ohne das Add-on schreibst du keine Stundenzahl, auch
nicht im Expert Service. Ändert sich die Lösung, setzt du die Zahl neu; wird sie `blocked` oder wieder
offen, leerst du sie. Die Zahl ist kein Wert für `Aufwand (h)`, du nennst sie nicht als solchen, und
sie steht im Plan, nie im Entwurf.

## Wie du schätzt

- **Frei aus der ausgearbeiteten Lösung**, aus dem gewählten Lösungsansatz in `## Approach` und `## Details` (Mengengerüst, Zahl der
  Elemente, Abhängigkeiten, Edge Cases), ohne Spanne und ohne Tabelle, und nicht aus der Größe allein
  (§109). Die Zahl ist eine Zahl in Stunden, Dezimalpunkt erlaubt.
- **Je Teil geschätzt und addiert:** besteht die Lösung aus mehreren Teilen, mehreren Werten in
  `classification`, schätzt du je Teil und addierst.
- **Entwicklung, Konfiguration und Pflege getrennt** (§401): je Teil schätzt du, was gebaut, was
  eingestellt, und was laufend gepflegt wird, und addierst alle drei, wie die Größe sie zählt
  (`${CLAUDE_SKILL_DIR}/../../docs/solution-choice-contract.md`). Pflege ist, was der Lösungsansatz im
  Vorhaben bis zum Go-Live wiederkehrend kostet: Updates einer App nachziehen, eine Abbildung bei einer
  Änderung am Fremdsystem nachführen, Code im Theme bei einem Update des Themes mitziehen. Der typische
  Fehler der früheren Schätzung im Archiv (Agentkit, Stand 2026-08-06) war eine App-Integration als
  14 h Entwicklung statt 7 h Entwicklung und 7 h Konfiguration.
- **Entwicklung nur als Abweichung vom gewählten Theme:** was das Theme aus `architecture.md`
  (`Bauform der Storefront`) schon kann, kostet keine Entwicklung, höchstens Konfiguration. Das ist die
  zweite Erkenntnis aus derselben Schätzung im Archiv.
- **Kein Faktor beim Schreiben:** einen Korrekturfaktor wendest du nicht an, die Zahl bleibt roh, damit
  die Kalibrierung sie gegen `Aufwand (h)` messen kann. Einen Faktor liest du nicht, bevor du schätzt.

## In der Vorschau

Der Plan aus Step 11 nennt je Anforderung `effort_estimate_model` alt und neu, und darunter je Teil
seine Stunden, getrennt nach Entwicklung, Konfiguration und Pflege, mit der Begründung aus den Details der
Lösung: welche Elemente, welche Mengen, was das Theme schon trägt.

## Die Zerlegung im Repo

**Die Zerlegung schreibst du in `.claude/metrics/estimates/REQ-NNN.md`**, je Anforderung eine Datei,
mit derselben Wahl, die `effort_estimate_model` setzt (§357). Sie liegt versteckt neben den Metriken
und nicht bei Anforderungen und Epics: sie erklärt der Kalibrierung, warum das Modell neben dem Lead
lag, und ist keine Angabe zum Vorhaben. Kein Skill liest sie, und sie geht in keine Projektion.
Ändert sich die Lösung, überschreibst du die Datei; leerst du `effort_estimate_model`, löschst du sie.

```markdown
# REQ-045 Geschenkverpackung im Checkout

Stand: 2026-10-14, solution-design EP-026
Lösungsansatz: app (Checkout Blocks)
effort_estimate_model: 4

| Teil | Art | Stunden | Begründung |
|---|---|---|---|
| app, Endkundenshop | Konfiguration | 2 | Block mit Checkbox und Beschriftung, Speicherung als Attribut, Testbestellungen |
| app, Händlershop | Konfiguration | 1.5 | App installieren, gleicher Block, eine Testbestellung |
| app | Entwicklung | 0 | kein Code; das Theme ist nicht betroffen |
| app | Pflege | 0.5 | ein Update der App bis zum Go-Live prüfen, eine Testbestellung je Shop |

Nicht eingerechnet: Übertragung der Wahl an die Warenwirtschaft (GAP-057).
```

- **Je Teil eine Zeile je Art**, `Entwicklung`, `Konfiguration` oder `Pflege`, auch mit `0`; die Summe
  der Spalte `Stunden` ist `effort_estimate_model`. Eine Zerlegung aus einer älteren Version ohne Zeile
  `Pflege` bleibt gültig.
- **Die Begründung** ist ein Satz aus den Details der Lösung: Elemente, Mengen, was das Theme trägt.
- **„Nicht eingerechnet“** nennt, was offen bleibt, mit der offenen Frage; fehlt nichts, entfällt die Zeile.
- Die Datei trägt keine Daten von Endkunden und keine Zugangsdaten (§236), wie jede Datei im Repo.
