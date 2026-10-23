# Die Architektur `architecture.md` fortschreiben

Die Datei trägt den geltenden Stand der Architektur, eine Aussage je Zeile; das Warum steht in der ADR
(§216). Die Form und ihre Regeln setzt der Vertrag,
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`. Dieser Lauf legt die Datei beim ersten Lauf
mit dem Sheet an (§229) und trägt danach zwei Arten von Zeilen ein: **belegte Vorgaben aus dem
Material** und **die Systemlandschaft**. Eine Quelle steht als feste Wendung in der Sprache aus
`language`, nach dem Abschnitt „Die festen Wendungen“ desselben Vertrags (`source_workshop`, §337);
das Beispiel zeigt `de`, bei `en` „Workshop ‹title› on ‹date›“.

```
| Aussage | Status | Quelle/ADR | gestützt von |
|---|---|---|---|
| Bauform der Storefront: Theme | belegt | Workshop ‹Titel› vom ‹Datum› | |
| System business_central: führt Artikelstamm und Bestände, liefert beides an den Shop. Bleibt | belegt | Workshop ‹Titel› vom ‹Datum› | |
| System newsletter_alt: Versand der Newsletter. Abgelöst durch klaviyo | entschieden | ADR-007 | |
```

## Was eine Zeile wird

| Das Material sagt | Folge |
|---|---|
| eine Fundament-Frage, ausdrücklich: Bauform oder Integrationsschicht | die Fundament-Zeile bekommt `Status` und `Quelle/ADR`; ihre Aussage bleibt, wie sie steht, außer sie war offen formuliert: dann ersetzt du sie durch die Vorgabe |
| Plan, Markets oder Stores eines Shops | keine Zeile und kein Wert aus dem Material: die Zeile zu den Shops verweist auf `project.yml`, `shops`, und dort steht nur, was der Lead angegeben hat (§229); der Bericht nennt sie |
| ein System, das es gibt oder geben wird | eine Zeile `System ‹name›: …` nach `${CLAUDE_SKILL_DIR}/../../docs/system-landscape-contract.md` |
| eine Festlegung, die mehrere Epics betrifft: ein Master, ein Muster, eine App, ein Schlüssel | eine Zeile, nur wenn das Material sie als gefallen nennt |
| einen Wunsch zu Design, Tracking, SEO oder Ähnlichem | keine Zeile, sondern eine Anforderung |

Baut das Vorhaben mehrere Shops und gilt eine Zeile nur für einen, steht sein Schlüssel vorne in der
Aussage, `b2b: Preise kommen aus dem ERP` (§231). Das gilt nur für Zeilen in `architecture.md`;
Anforderung und ADR tragen den Bezug im Feld `shops` (§307).

**`belegt`** heißt, eine Quelle sagt es; **`entschieden`**, eine Wahl zwischen Alternativen ist gefallen, und
dann gibt es zuerst die ADR nach [ref-adr.md](ref-adr.md). Eine Zeile, deren Zukunft das Material
offen lässt, trägt `offen`, und in `Quelle/ADR` die Quelle, die das System nennt.

**Eine Architekturfrage legst du nicht an.** Sie hängt als Frage in `gaps/` an der treibenden
Anforderung, und sie stellen `epic-structure` und `solution-design`. Du nennst sie in der Notiz und
im Bericht, mit der Anforderung, die sie treibt. Fehlt die treibende Anforderung, ist das ein Kandidat
für eine neue Anforderung (§216).

## Anlegen

Fehlt `architecture.md`, wenn der Lauf das Sheet anlegt, entsteht sie mit genau dem Fundament aus dem
Vertrag: Kopf, Kopfzeile und die vier Zeilen, die Aussagen wörtlich, `gestützt von` leer. Trägt
`shops` in `project.yml` Einträge, ist die Zeile zu den Shops `belegt` mit `Quelle/ADR` =
`project.yml`, sonst `offen`; die übrigen drei sind `offen`, `Quelle/ADR` leer. Steht die Datei schon,
bleibt sie, wie sie ist.

```
| Shops, Pläne, Markets oder Expansion Stores: stehen in `project.yml`, `shops` | belegt | `project.yml` | |
```

## Fortschreiben, nie löschen

- Eine neue Aussage ist eine neue Zeile am Ende der Tabelle.
- An einer bestehenden Zeile ändern sich nur `Status` und `Quelle/ADR`; `gestützt von` bleibt, wie es
  steht.
- **Eine überholte Zeile wird ersetzt, nicht durchgestrichen** (§231): an ihrer Stelle steht die neue
  Aussage mit ihrem Status und ihrer Quelle, `gestützt von` bleibt. Den alten Stand hält Git. Jedes
  Epic unter `gestützt von` der ersetzten Zeile markierst du als nachzuprüfen: in seiner Datei
  `epics/EP-NNN.md` wird `clarification` zu `Nachprüfen: ‹Datum›, Architektur „‹ersetzte Aussage›“`
  (`clar_recheck`, `en`: `Recheck: ‹Datum›, architecture “‹statement›”`, §337), nur diese Zeile des Kopfs, und der Block zeigt sie alt und neu. Die Projektion trägt sie
  in `Klärungsbedarf` des Tabs `Epics`.
- **Einen Widerspruch überschreibst du nicht.** Sagt das Material etwas anderes als eine Zeile mit
  `belegt` oder `entschieden`, wird ihr `Status` `widersprüchlich`, `Quelle/ADR` nennt beide Quellen
  und die Frage, die du dazu in `gaps/` anlegst (`kind: decision`, `concerns` = die Anforderungen und
  Epics, die auf der Zeile bauen; [ref-questions.md](ref-questions.md)). Aufgelöst wird er mit dem
  Kunden, nicht in diesem Lauf.
- Keine Zeile wird gelöscht oder umsortiert, die Kopfzeile bleibt.

## Schreiben

Du liest die Datei direkt vor dem Schreiben und baust den ganzen neuen Text auf diesem Stand.
**Geprüft wird vor jedem Schreiben gegen die gelesene Fassung:** Kopf und Kopfzeile unverändert;
jede gelesene Zeile steht noch an ihrer Stelle, neue nur am Ende; ein Status ist `belegt`,
`entschieden`, `offen` oder `widersprüchlich`; in `gestützt von` fehlt kein Eintrag, der dastand.
Hält die neue Fassung das nicht, wird sie nicht geschrieben: du liest neu und baust noch einmal; beim
dritten Mal endet der Schritt, und der Bericht nennt die Abweichung.
