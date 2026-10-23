# Die Wahl: ADR und Architektur

## Die ADR

Eine Datei je Entscheidung in `decisions/` des Datalayers, flach: `ADR-NNN-<slug>.md`, drei Ziffern, von der höchsten Nummer im Ordner weiter, `<slug>` englisch, klein,
kebab-case. Du legst sie an; steht der Name schon, schreibst du nicht und nennst es.

```markdown
---
id: ADR-004
title: <Titel der Entscheidung, in der Sprache des Vorhabens>
status: accepted
supersedes: ADR-002
shops: [b2b]
---

## Entscheidung

<der gewählte Lösungsansatz für ‹EP-003, Teilthema›, in zwei bis vier Sätzen>

## Begründung

<die Begründung, wie der Lead sie gibt, mit Quelle: „Chat mit dem Lead vom ‹Datum›" oder „Workshop
‹Titel› vom ‹Datum›", in der Sprache aus `language` (`source_chat`, `source_workshop`, §337)>

## Verworfene Optionen

- **<Lösungsansatz>**: <warum nicht>

## Betroffene Anforderungen

<IDs>
```

- `supersedes` steht nur, wenn die ADR eine frühere ablöst; sonst fällt die Zeile weg. `shops` nennt
  die `key` aus `shops` in `project.yml`, für die sie gilt; gilt sie für alle Shops, bleibt die Liste
  leer, `shops: []` (§307). Der Titel trägt keinen Schlüssel.
- **Ein Epic der Domäne `design` bekommt keine ADR** (§297): es trägt keinen Lösungsansatz.
- **Ein Stamp oder eine Best Practice, die zur Wahl stand, steht in dieser ADR** (§326): unter
  `## Entscheidung`, wenn genommen, mit Abweichung und Grund, wenn angepasst, sonst unter
  `## Verworfene Optionen`, je mit dem Größenvergleich („SOL-2026-001, Erstbau M, hier S, gegen
  Theme-Anpassung M“), nach `${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`. Eine eigene ADR für die
  Abweichung von der Wissensbasis gibt es nicht.
- **Die Wahl einer Middleware** ist eine Entscheidung des Projekts: ihre ADR nennt die Best Practice,
  nach der sie gewählt ist, und `architecture.md` bekommt die Zeile `Integrationsschicht` (§216, §324).
- **Bei einer Public App trägt die ADR die Evaluierung** (§320, [ref-options.md](ref-options.md), Eine
  Public App evaluieren), nach `## Begründung` unter `## Evaluation`, eine Zeile je Kandidat und
  Muss-Kriterium:

  ```markdown
  ## Evaluation

  | Candidate | Criterion | Result | Level | Source | Date |
  |---|---|---|---|---|---|
  | <Name der App> | <Muss-Kriterium> | met | vendor | <Adresse> | 2026-10-10 |
  ```

  `Result` ist `met`, `not_met` oder `unproven`, `Level` `dev_store`, `vendor`, `help_center`,
  `shopify_dev` oder `assumption`, `Date` der Tag des Belegs; Kopfzeile und Werte bleiben englisch (§295), Kandidat und
  Kriterium stehen in der Sprache des Vorhabens. Ein Lösungsansatz ohne App als zweiter Kandidat trägt seine
  Zeilen ebenso, belegt mit `shopify_dev` oder den übrigen Stufen. Der Name des empfohlenen oder
  gewählten Kandidaten ist der des ersten Lösungsansatzes unter `## Approach`.
- **Die ADR einer Public App entsteht mit der Evaluierung, vor der Wahl**, mit `status: proposed`,
  damit der nächste Lauf die Belege nicht wiederholt: `## Entscheidung` nennt die Empfehlung und
  „Wahl offen", `## Begründung` bleibt leer, und `depends_on` der Anforderung nennt die ADR. Eine ADR
  auf `proposed` ist ein Entwurf (Datalayer-Vertrag): spätere Läufe lesen sie zu ihrem Epic mit und
  schreiben sie fort, Tabelle und Text. **Mit der Wahl** schreibst du Entscheidung und Begründung des
  Leads in dieselbe ADR und setzt `accepted`, **außer ein Kriterium des gewählten Kandidaten ist
  `unproven`**: dann bleibt sie `proposed` und die Anforderung `blocked`, bis jede Frage dazu
  beantwortet ist. `check-repo.py` prüft das (`app_evaluation`).
- **Eine Wahl ohne Begründung ist keine Wahl.** Nennt der Lead keine, fragst du danach; ohne sie
  entsteht keine ADR auf `accepted`, und der Lösungsansatz bleibt offen.
- **Die Begründung ist die des Leads**, nicht deine Empfehlung. Deckt sie sich mit ihr, darf der Lead
  sie übernehmen, aber er sagt es.
- **Der Text einer ADR auf `accepted` wird nie überschrieben.** Kippt eine Entscheidung, entsteht eine neue mit
  `supersedes`, und an der alten ändert sich nur die Zeile `status:` auf `superseded`.
- **Im Entwurf steht keine ADR-Kennung:** die Wahl steht als beantwortete Frage unter `Questions`, der
  gewählte Lösungsansatz in `Technical Information`. In der Datei der Anforderung nennt `depends_on` die ADR.

## Die Zeilen in `architecture.md`

`architecture.md` trägt die geltende Architektur des Vorhabens, eine Aussage je Zeile:
`Aussage | Status | Quelle/ADR | gestützt von` (§216). **`Status` kennt genau vier Werte**, für alle
Läufe dieselben (`docs/datalayer-contract.md`):

| Status | heißt | `Quelle/ADR` |
|---|---|---|
| `belegt` | eine Quelle sagt es; keine Wahl zwischen Alternativen | die Quelle |
| `entschieden` | eine Wahl ist gefallen | die ADR |
| `offen` | noch nicht vorgegeben und nicht gewählt | die treibende Anforderung |
| `widersprüchlich` | zwei Quellen sagen Verschiedenes | beide |

Eine `belegt`e und eine `entschieden`e Zeile gelten gleich; sie unterscheiden sich nur darin, ob es
eine ADR gibt. Die Wahl ändert die Datei so:

| Anlass | Änderung |
|---|---|
| der gewählte Lösungsansatz baut auf einer Zeile | das Epic kommt in `gestützt von` dazu, `EP-003`; nichts fällt dort weg |
| die Wahl legt etwas fest, das andere Epics betrifft (ein Master, ein Muster, eine App, eine Function, ein Schlüssel) | eine neue Zeile am Ende: die Aussage, `entschieden`, die ADR, das Epic; gilt sie nur für einen Shop von mehreren, steht sein Schlüssel vorne, `b2b: …` (§231) |
| die Wahl entscheidet eine `offen`e Zeile, deren Aussage schon der gewählte Stand ist | `Status` `entschieden`, `Quelle/ADR` die ADR |
| die Wahl entscheidet eine `offen`e Zeile, die als Frage formuliert ist (`Integrationsschicht: ob, welche, wer betreibt`) | die Zeile wird ersetzt (§231): an ihrer Stelle die neue Aussage, `entschieden`, die ADR; das Epic kommt in `gestützt von` dazu |
| die Wahl kippt eine `belegt`e oder `entschieden`e Zeile | ebenso |
| zwei Quellen widersprechen sich | `Status` `widersprüchlich`, beide Aussagen in `Quelle/ADR`, die Architekturfrage in `gaps/` ([ref-questions.md](ref-questions.md)) |

**Eine ersetzte Zeile** behält `gestützt von`; den alten Stand hält Git. Die Epics, die vorher dort standen,
bekommen in ihrer Datei `epics/EP-NNN.md` `clarification` = `Nachprüfen: ‹Datum›, Architektur „‹ersetzte
Aussage›“` (`clar_recheck`, bei `en` `Recheck: ‹Datum›, architecture “‹statement›”`, nach
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“, §337), außer ihr `status` ist `dissolved` oder `merged`: deren
Anforderungen tragen jetzt andere Epics, und die stehen selbst in `gestützt von`. Der Commit nennt die
ersetzte Aussage (§231).

**Keine Zeile wird gelöscht, keine umsortiert**, keine Begründung in die Datei geschrieben; das Warum
steht in der ADR. Die Zeile zu den Shops verweist auf `project.yml` und schreibt die Werte nicht ab.

Du liest die Datei direkt vor dem Schreiben und schreibst `architecture.md` fort: den ganzen gelesenen
Text mit genau diesen Änderungen. **Geprüft wird vor jedem Schreiben gegen die gelesene Fassung:**
Kopf und Kopfzeile unverändert; jede gelesene Zeile steht noch an ihrer Stelle, neue nur am Ende; ein
Status ist einer der vier oben; in `gestützt von` fehlt kein Eintrag, der dastand. Hält die neue
Fassung das nicht, wird sie nicht geschrieben.
