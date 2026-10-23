# Die Wahl des Lösungsansatzes — Größe, Stamp, Stufe, Knowledge Base

**Welcher Lösungsansatz einer Anforderung gewinnt, entscheidet zuerst seine Größe im Projekt**
(§326, §401). Diesen Vertrag lesen `solution-approach`, das je Lösungsansatz die Größe grob schätzt
und eine Empfehlung gibt, und `solution-design`, das sie belegt, wählt und die Größe endgültig setzt;
gegen die Stunden hält sie kein Lauf (§357). Die acht Klassifizierungen, ihr Gewerk und ihre Größe
nach Tabelle stehen im Datalayer-Vertrag, Abschnitt „Die Klassifizierung“
([`datalayer-contract.md`](datalayer-contract.md), §324); was aus der Knowledge Base gilt, steht in
[`kb-contract.md`](kb-contract.md).

## Die Größentabelle

**Die Größe eines Lösungsansatzes zählt drei Teile zusammen** (§401): was gebaut wird, was
eingestellt wird, und was er laufend an Pflege kostet, etwa Updates einer App, eine Schnittstelle, die
bei jeder Änderung am Fremdsystem nachgezogen wird, oder Code im Theme, der jedes Update des Themes
mitgehen muss. Eine Public App ohne Bau, deren Einrichtung viele Einstellungen braucht, ist darum
nicht `S`; eine Theme-Anpassung, die bei jedem Update des Themes nachgezogen wird, trägt die Pflege mit.

`size` einer Anforderung trägt `S`, `M`, `L` oder `XL`; nie Stunden (§280, Regel 10). Die Anker,
jeder mit der Konfiguration und der Pflege, die er üblich mitbringt:

| Größe | trägt |
|---|---|
| `S` | eine Einstellung (Shopify-nativ), eine Einstellung im Theme Editor (Theme-nativ) oder eine Public App ohne Anpassung |
| `M` | eine Theme-Anpassung an einer Ansicht, eine Public App mit Konfiguration und Anpassung am Theme, oder ein Standard-Konnektor, der einen Datenstrom ohne eigene Abbildung trägt |
| `L` | eine Theme-Anpassung an mehreren Ansichten, eine Custom App mit einem Zweck, ein Standard-Konnektor mit eigener Abbildung, oder eine Middleware an ein System |
| `XL` | eine Custom App mit mehreren Teilen oder eine Custom Schnittstelle |

**Trägt Konfiguration oder Pflege mehr als der Anker**, nimmst du die nächste Größe und nennst, was
sie treibt. **Die Migration ist eine Situation, keine Klasse** (§324): sie trägt die Klassifizierung
ihres Lösungsansatzes, und ihre Größe misst sich an den Quellen.

| Situation | Größe |
|---|---|
| eine Migration aus einer Quelle | `L` |
| eine Migration aus mehreren Quellen | `XL` |

**Zwischen zwei Größen nimmst du die größere** und nennst, was sie treibt. Eine Größe über `XL` gibt
es nicht: dann ist das Epic zu schneiden, und der Bericht nennt `epic-structure`. **Im Epic
der Domäne `design` gibt es weder Klassifizierung noch Größe** (§297).

## Die Auswahl

**Unter den Lösungsansätzen, die alle Akzeptanzkriterien decken, gewinnt in dieser Folge** (§401):

1. **Harte Grenzen streichen**, bevor gewogen wird: der Plan des Shops (`shops[].plan` in
   `project.yml`), der Standard-Leistungssatz, die Grenzen der Plattform laut Doku, eine App, die die
   Best Practices der Knowledge Base ausschließen. Ein Lösungsansatz, der nicht alle Kriterien deckt,
   ist keiner.
2. **Die kleinere Größe im Projekt**, aus Bau, Konfiguration und Pflege. Für einen Stamp gilt die
   Größe der Wiederverwendung, nicht die des Erstbaus ([`kb-contract.md`](kb-contract.md), Die Größe
   der Wiederverwendung); ein Stamp deckt nur, wenn sein `requires` im Projekt erfüllt ist.
3. **Bei gleicher Größe der Stamp**: ein Lösungsansatz, den ein gelesener Stamp trägt, ist in einem
   Projekt schon gebaut und gelaufen, und gewinnt vor der Stufe.
4. **Dann die Stufe:** Shopify-nativ → Theme-nativ → Public App oder Theme-Anpassung → Custom App.
   Zwischen Public App und Theme-Anpassung, gleichrangig, entscheidet die Abgrenzung (§203):
   - Funktion eher über eine App, Darstellung eher über das Theme;
   - braucht die Fähigkeit laufend Updates oder müsste sie tief ins Theme gebogen werden, eher App;
   - trägt eine kleine Anpassung die Fähigkeit, Theme;
   - tut eine fertige App genau das, ohne großen Überhang an Kosten, Skripten oder ungenutzten
     Funktionen, App;
   - trägt das Theme die Fähigkeit schon, eingestellt im Theme Editor ohne Code, ist das
     `theme_native`, nicht `theme` (§314).

   **Schnittstellen:** Standard-Konnektor → Middleware → Custom Schnittstelle.
5. **Dann die bevorzugte App** aus den Best Practices und **die Passung zur Gesamtlösung**: eine App,
   die schon im Shop läuft oder eine andere Anforderung trägt; keine zweite App für dieselbe
   Fähigkeit.

**Danach, bei Gleichstand**, Gesamtkosten über zwei Jahre (Lizenz, Bau, Pflege), Pflegbarkeit durch
den Kunden, Risiko bei Updates, Performance und Abhängigkeit vom Anbieter. **Hängt die Wahl an einer
kaufmännischen Präferenz**, etwa monatliche Gebühr gegen einmaligen Bau, wählt die Empfehlung keine
Seite: sie nennt beide Lösungsansätze, und die Frage geht an den Kunden.

## Die Größe je Lösungsansatz

**`solution-approach` schätzt die Größe je Lösungsansatz grob** nach der Tabelle, vergleicht nach
der Auswahl und schreibt die Größe des empfohlenen, im Expert Service des gewählten, als Vorschlag in
`size` der Anforderung und mit demselben Wert in `size_estimate_approach` (§357), neben
`solution_status: proposed`; das Sheet zeigt sie nicht (§275). **`solution-design` prüft sie und
setzt sie endgültig** mit der Wahl.

**Jeder Lösungsansatz trägt die Zeile `Größe:`** unter seinem Satz, in `## Approach` der
Anforderung, und dahinter in Klammern, was Bau, Konfiguration und Pflege tragen, je in wenigen
Wörtern, `nichts`, wo nichts anfällt. Bei einem Stamp nennt sie beide Größen, die des
Erstbaus und die im Projekt. Eine Datei, deren `Größe:` keine Klammer trägt, bleibt gültig. Das
Beispiel zeigt `de`; `KB: keiner` steht bei `en` als `KB: none`
([Die festen Wendungen](datalayer-contract.md#die-festen-wendungen), §337):

```markdown
### Versandprofile je Markt

Versandprofile in Shopify Markets, je Markt eigene Sätze.

Größe: S (Bau nichts, Konfiguration Sätze je Markt, Pflege nichts)

KB: keiner

### Lieferzeiten aus dem Stamp

Lieferzeiten je Markt nach dem Muster aus einem früheren Projekt.

Größe: SOL-2026-001, Erstbau M, hier S (Bau eine Section, Konfiguration nichts, Pflege Updates des Themes)

KB: SOL-2026-001 Lieferzeiten je Markt
```

## Belege für den gewählten Lösungsansatz

**Jedes Muss-Kriterium des gewählten Lösungsansatzes braucht einen Beleg** aus Doku, Listing oder
Messung, für jede Klassifizierung, nicht nur für eine Public App (§326, erweitert §320).
Muss-Kriterien sind die Akzeptanzkriterien der Anforderung und die Pflichten aus dem
Standard-Leistungssatz, die sie berühren. **Fehlt der Beleg, wird das Kriterium eine blockierende
offene Frage** (§279): eine Frage in `gaps/` mit `blocking: yes` an den, der es belegen kann, und die
Anforderung trägt `solution_status: blocked`. Eine Annahme belegt nichts. Bei einer Public App steht
die Evaluierung der Kandidaten zusätzlich als Tabelle in der ADR (§320).

## Die ADR der Wahl

**Ein Stamp oder eine Best Practice, die zur Wahl stand, steht in der ADR der Wahl**, mit dem
Größenvergleich, nach [`kb-contract.md`](kb-contract.md), Die Größe der Wiederverwendung (§326).
