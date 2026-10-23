# Den Steckbrief aus dem Material vorschlagen

**Nach dem ersten Einlesen trägt das Material, was der erste Lauf nicht fragt**: Kunde, Titel, Shops,
Projekttyp und Add-ons stehen im Angebot und in der Übergabe aus dem Vertrieb. Du liest sie dort,
schlägst jedes leere Feld mit seiner Fundstelle vor, und der Lead bestätigt **einmal**, an der ganzen
Vorschau. Felder, die schon stehen, schreibst du Zeichen für Zeichen zurück.

## Das Material lesen

Lies in `inputs/` zuerst die Quellen mit `Intern: ja` im Kopf (Übergabe, Projektbriefing,
Pre-Sales-Briefing) und das Angebot, dann die übrigen, bis jedes leere Feld eine Fundstelle hat oder
das Material erschöpft ist. Die Notizen in `notes/` zeigen, welche Quelle ein Thema berührt; die
Fundstelle ist immer die Datei in `inputs/` mit ihrem Abschnitt.

| Feld | woher |
|---|---|
| `customer` | Angebot oder Übergabe: der Auftraggeber, wie er dort heißt |
| `title` | Angebot oder Übergabe: wie das Vorhaben dort heißt |
| `key` | aus dem Titel abgeleitet, nie aus dem Material: kurz, klein, `a-z`, `0-9`, `-` und `_`; steht er schon, änderst du ihn nicht (§233) |
| `shops` | je Instanz und je Expansion Store ein Eintrag (§231): Domain, Plan, Märkte, Zielgruppe (§249). Den Schlüssel je Shop schlägst du vor (`eu`, `us`, `b2b`). `jurisdiction` bleibt leer |
| `project_type` | das unterschriebene Angebot: Projekt oder Expert Service (§303) |
| `add_ons` | das unterschriebene Angebot: genau die verkauften aus `solutioning`, `design`, `content_migration`, `e2e_testing` (§303) |

**Ohne Fundstelle bleibt ein Feld leer** und steht in der Vorschau als Frage. Geraten wird nichts:
aus einem Markt folgt kein Rechtsraum, aus einem Shop-Namen keine Zielgruppe, aus einer Erwähnung
keine Beauftragung. Ein Add-on oder ein Shop, den das Material nur als Möglichkeit nennt, gilt nicht
als verkauft.

**Liegt in `inputs/` kein Material**, fragst du die Felder der Tabelle **alle in einer Nachricht**,
mit den Fragen aus [ref-project-yml.md](ref-project-yml.md), „Die Fragen des Steckbriefs“, und sagst
dazu, dass jede Antwort „noch offen" sein darf.

**Widerspricht das Material einem Feld, das schon steht**, etwa ein anderes Board, ein anderes Team
oder eine andere Sprache, nennst du beide Stellen und fragst, welche gilt. Du änderst das Feld nur
auf diese Antwort.

## Zeigen, Ja, schreiben

Die Vorschau folgt [ref-project-yml.md](ref-project-yml.md), „Die Vorschau“: jedes Feld mit Wert und
Fundstelle, die übernommenen Felder mit „steht schon“, die leeren mit „noch offen“. **Geschrieben wird
erst nach einem ausdrücklichen Ja zu dieser Vorschau.** Dann schreibst und prüfst du `project.yml`
nach SKILL.md, Step 8, und endest nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Teile 1, 5
und 6: `check-repo.py`, `readme.md` und `way-of-working.md`, Commit und Push, Nachricht
`project-setup: Steckbrief`. Ins Sheet projiziert dieser Lauf nichts.

## Das Ende

Sag knapp, welche Felder jetzt stehen, welche leer blieben und welcher Skill sie später fragt. Dann
den nächsten Lauf, in einer neuen Sitzung: `requirements-update`, das mit Kunde und Titel Sheet und
Architektur beim ersten Lauf anlegt (§282).
