# Entwurf und Epic Page: Vorlage, Kopf, Abschnitte, Stil, Quellenregeln

**Dieser Vertrag setzt die Form von Epic-Datei, Entwurf und Epic Page** (§325): `solution-design`
schreibt den Rumpf der Epic-Datei und projiziert ihn in den Entwurf, `solution-epic-page` überträgt den
freigegebenen Entwurf nach Confluence; `solution-review`, `solution-proposal`, `ticket-factory` und
`e2e-testing-sheet` lesen ihn, `check-page.py` und `check-solution-doc.py` prüfen gegen ihn. Wie der
Entwurf angelegt und fortgeschrieben wird, steht bei `solution-design`; wie die Seite nach Confluence
kommt, bei `solution-epic-page`.

**Die Lösung eines Epics steht im Rumpf von `epics/EP-NNN.md`**, in der Gliederung dieser Vorlage
(§280). **Der Entwurf ist ihre Projektion**: ein Google-Doc im Unterordner `Epics` von
`Solutioning` (§260), einmal aus dem Rumpf der Epic-Datei angelegt und danach gezielt fortgeschrieben
(§302), ein Link für das ganze Solutioning. Der Kunde kommentiert im Entwurf; der nächste Lauf liest
die Kommentare und die Abweichungen gegen die Epic-Datei als Material. Ein geprüftes, freigegebenes Epic überträgt `solution-epic-page` als Epic Page nach Confluence
(§218, §313). Für Epic-Datei,
Entwurf und Seite gilt diese Vorlage, Zeichen für Zeichen dieselbe.

**Alle Bezeichnungen stehen in der Projektsprache** (`language` in `project.yml`, §202, §255):
Kopf, Überschriften, Spaltenköpfe, Checkboxen und die festen Sätze, bei `de` alles
deutsch, bei `en` alles englisch, wörtlich wie in der Vorlage dieser Sprache unten. Der Titel ist in
beiden Sprachen gleich (§261). **Inhalt und
Bezeichnungen sind immer einheitlich**: nennt der Lead beim Aufruf eine andere Sprache, gilt sie für
beides. An den Bezeichnungen finden `solution-design`, `ticket-factory` und die übrigen Skills die Stellen
wieder, und `scripts/check-page.py` prüft ein Dokument gegen die Vorlage seiner Sprache.

**In allen Skills heißt eine Stelle mit ihrer Bezeichnung aus der Spalte `en`** der Tabelle unten,
etwa `Technical Information`; im Dokument steht sie in dessen Sprache, bei `de` also `Technische
Umsetzung`.

Ein Abschnitt, der nichts trägt, bleibt mit leerem Rumpf stehen: eine leere Stelle ist eine Auskunft,
eine erfundene nicht. `‹…›` ist ein Platzhalter und wird ersetzt, in der Sprache des Dokuments;
`‹optional›` über einer Tabelle heißt, die Tabelle darf fehlen, und steht nie im Dokument. **Keine
Trennstriche zwischen den Abschnitten**: ein `---` wird beim Import in ein Google-Doc nicht zur
Linie, sondern bleibt als Text stehen, und im Rumpf der Epic-Datei hielte ein Leser es für das Ende
des Kopfs.

## Die Bezeichnungen

Die eine Tabelle beider Sprachen. Die Vorlagen unten tragen genau diese Wörter; `check-page.py` und
`check-solution-doc.py` lesen sie von hier, und eine deutsche Vorlage, die nicht die englische mit
diesen Bezeichnungen ist, lehnt `dev/tests/check-page.py` ab.

| Schlüssel | en | de |
|---|---|---|
| `title` | `[‹Epic-ID›] ‹Titel des Epics›` | `[‹Epic-ID›] ‹Titel des Epics›` |
| `approved_note` | `Approved on ‹D Mon YYYY›.` | `Freigegeben am ‹TT.MM.JJJJ›.` |
| `changed_note` | `Changed on ‹D Mon YYYY›: ‹was, in einem Satz›` | `Geändert am ‹TT.MM.JJJJ›: ‹was, in einem Satz›` |
| `transfer_note` | `Transferred to Confluence on ‹D Mon YYYY›, do not edit further: ‹Link der Seite›` | `Übertragen nach Confluence am ‹TT.MM.JJJJ›, nicht weiter bearbeiten: ‹Link der Seite›` |
| `head_epic` | `Epic` | `Epic` |
| `head_owner` | `Document Owner` | `Dokumentverantwortung` |
| `head_status` | `Status in Blueprint` | `Status im Blueprint` |
| `head_phase` | `Phase of Launch` | `Launch-Phase` |
| `head_initial` | `Initial Estimate (Cost Indication / Blueprint)` | `Erste Schätzung (Kostenindikation / Blueprint)` |
| `head_process` | `Requirements Engineering Process` | `Anforderungsprozess` |
| `check_prepared` | `Solution Architect finished the Req. Page preparation` | `Solution Architect hat die Seite vorbereitet` |
| `check_team` | `Team checked the Req. Page technically` | `Das Team hat die Seite technisch geprüft` |
| `check_customer` | `Customer finished the document and takes ownership (Ready for Refinement)` | `Der Kunde hat das Dokument fertiggestellt und übernimmt es (Ready for Refinement)` |
| `head_approval` | `Approval of effort` | `Freigabe des Aufwands` |
| `approval_text` | `Please keep in mind that the following expenses only represent the implementation effort. The previous conception effort is not included here and is considered as approved within the initial order.` | `Die folgenden Aufwände umfassen nur die Umsetzung. Der vorherige Konzeptionsaufwand ist nicht enthalten und gilt mit dem ursprünglichen Auftrag als freigegeben.` |
| `check_hours` | `___ hours are accepted by the Customer` | `___ Stunden sind vom Kunden freigegeben` |
| `status_in_progress` | `In progress` | `In Arbeit` |
| `status_for_approval` | `Awaiting approval` | `Zur Abnahme` |
| `status_documentation` | `Documentation, no approval` | `Dokumentation, keine Abnahme` |
| `status_approved` | `Approved` | `Abgenommen` |
| `section_goals` | `Goals and vision of the Customer` | `Ziele und Vision des Kunden` |
| `section_assumptions` | `Assumptions and delimitations` | `Annahmen und Abgrenzungen` |
| `section_relations` | `Relations and Prerequisites` | `Abhängigkeiten und Voraussetzungen` |
| `section_requirements` | `Requirements` | `Anforderungen` |
| `section_team` | `Team & Contacts` | `Team und Kontakte` |
| `section_design` | `User interaction and design or data model` | `Bedienung und Design oder Datenmodell` |
| `section_questions` | `Questions` | `Fragen` |
| `section_discarded` | `Discarded` | `Verworfen` |
| `col_id` | `ID` | `ID` |
| `col_summary` | `Summary` | `Zusammenfassung` |
| `col_story` | `User Story / Description` | `User Story / Beschreibung` |
| `col_criteria` | `Acceptance Criteria` | `Akzeptanzkriterien` |
| `col_technical` | `Technical Information` | `Technische Umsetzung` |
| `col_estimation` | `Estimation` | `Schätzung` |
| `col_refinement` | `Refinement Team` | `Refinement-Team` |
| `col_contacts` | `Relevant Contacts` | `Ansprechpersonen` |
| `col_data_model` | `Data Model etc.` | `Datenmodell u. a.` |
| `col_responsible` | `Responsible Contact` | `Zuständig` |
| `col_designs` | `Designs` | `Designs` |
| `col_attachments` | `Other attachments or documentation` | `Weitere Anlagen oder Dokumentation` |
| `col_questioner` | `Questioner` | `Gefragt von` |
| `col_question` | `Question` | `Frage` |
| `col_replying` | `Replying` | `Beantwortet von` |
| `col_answer` | `Answer` | `Antwort` |
| `col_reason` | `Reason / Note` | `Grund / Hinweis` |
| `consultant_placeholder` | `*(to be completed by the consultant)*` | `*(durch den Consultant zu ergänzen)*` |
| `not_included` | `Not included: ‹Gegenstand›, covered by ‹Epic-ID›` | `Nicht enthalten: ‹Gegenstand›, getragen von ‹Epic-ID›` |
| `choice_open` | `Choice open.` | `Wahl offen.` |
| `recommendation` | `Recommendation:` | `Empfehlung:` |
| `way_open` | `Approach open; the question is in the sheet.` | `Lösungsansatz offen; die Frage steht im Sheet.` |
| `decision_open` | `Decision open, decided by ‹Gewerk›` | `Entscheidung offen, entscheidet ‹Gewerk›` |
| `to_confirm` | `(to be confirmed)` | `(zu bestätigen)` |
| `kb_unread` | `Not yet checked against solutions from earlier projects.` | `Noch nicht gegen Lösungen aus früheren Projekten geprüft.` |

`Solution Architect`, `Lead` und `Kunde` in `Questioner` und `Replying` sind Rollen, keine
Bezeichnungen: sie stehen in der Sprache des Inhalts (`Customer` bei `en`).

## Die Vorlage

Nimm den Block der Projektsprache und ersetze nur die Platzhalter. Beide Blöcke sagen dasselbe.

### Vorlage `en`

```markdown
# [‹Epic-ID›] ‹Titel des Epics›

Approved on ‹D Mon YYYY›. ‹nur auf der übertragenen Seite›

| Epic | ‹Epic-ID›: ‹Titel des Epics› |
|---|---|
| Document Owner | ‹Name› |
| Status in Blueprint | ‹Status› |
| Phase of Launch | ‹Release oder Phase› |
| Initial Estimate (Cost Indication / Blueprint) | *(to be completed by the consultant)* |
| Requirements Engineering Process | [ ] Solution Architect finished the Req. Page preparation<br>[ ] Team checked the Req. Page technically<br>[ ] Customer finished the document and takes ownership (Ready for Refinement) |
| Approval of effort | Please keep in mind that the following expenses only represent the implementation effort. The previous conception effort is not included here and is considered as approved within the initial order.<br>[ ] ___ hours are accepted by the Customer |

## Goals and vision of the Customer

‹ein Satz Ziel des Epics›

- ‹Nutzen, ein Punkt je Zeile›

## Assumptions and delimitations

- ‹was Kunde und Dritte liefern, Voraussetzungen, Auswirkungen›
- Not included: ‹Gegenstand›, covered by ‹Epic-ID›

## Relations and Prerequisites

- ‹Abhängigkeit als Text›
- ‹Zeile aus architecture.md, auf die die Lösung baut›

## Requirements

‹zwei bis fünf Sätze übergreifender Lösungsansatz›

| ID | Summary | User Story / Description | Acceptance Criteria | Technical Information | Estimation |
|---|---|---|---|---|---|
| ‹Requirement-ID› | ‹Titel der Anforderung mit Shop-Bezug› | ‹User Story›<br>‹Beschreibung› | • ‹Kriterium 1›<br>• ‹Kriterium 2› | ‹Lösungsansatz der Anforderung› | *(to be completed by the consultant)* |

## Team & Contacts

| Refinement Team | Relevant Contacts |
|---|---|
| ‹Namen› | ‹Namen mit Funktion› |

## User interaction and design or data model

‹optional›

| Data Model etc. | Responsible Contact |
|---|---|

‹optional›

| Designs | Responsible Contact |
|---|---|

‹optional›

| Other attachments or documentation | Responsible Contact |
|---|---|

## Questions

| Questioner | Question | Replying | Answer |
|---|---|---|---|

## Discarded

| ID | Summary | Reason / Note |
|---|---|---|
```

### Vorlage `de`

```markdown
# [‹Epic-ID›] ‹Titel des Epics›

Freigegeben am ‹TT.MM.JJJJ›. ‹nur auf der übertragenen Seite›

| Epic | ‹Epic-ID›: ‹Titel des Epics› |
|---|---|
| Dokumentverantwortung | ‹Name› |
| Status im Blueprint | ‹Status› |
| Launch-Phase | ‹Release oder Phase› |
| Erste Schätzung (Kostenindikation / Blueprint) | *(durch den Consultant zu ergänzen)* |
| Anforderungsprozess | [ ] Solution Architect hat die Seite vorbereitet<br>[ ] Das Team hat die Seite technisch geprüft<br>[ ] Der Kunde hat das Dokument fertiggestellt und übernimmt es (Ready for Refinement) |
| Freigabe des Aufwands | Die folgenden Aufwände umfassen nur die Umsetzung. Der vorherige Konzeptionsaufwand ist nicht enthalten und gilt mit dem ursprünglichen Auftrag als freigegeben.<br>[ ] ___ Stunden sind vom Kunden freigegeben |

## Ziele und Vision des Kunden

‹ein Satz Ziel des Epics›

- ‹Nutzen, ein Punkt je Zeile›

## Annahmen und Abgrenzungen

- ‹was Kunde und Dritte liefern, Voraussetzungen, Auswirkungen›
- Nicht enthalten: ‹Gegenstand›, getragen von ‹Epic-ID›

## Abhängigkeiten und Voraussetzungen

- ‹Abhängigkeit als Text›
- ‹Zeile aus architecture.md, auf die die Lösung baut›

## Anforderungen

‹zwei bis fünf Sätze übergreifender Lösungsansatz›

| ID | Zusammenfassung | User Story / Beschreibung | Akzeptanzkriterien | Technische Umsetzung | Schätzung |
|---|---|---|---|---|---|
| ‹Requirement-ID› | ‹Titel der Anforderung mit Shop-Bezug› | ‹User Story›<br>‹Beschreibung› | • ‹Kriterium 1›<br>• ‹Kriterium 2› | ‹Lösungsansatz der Anforderung› | *(durch den Consultant zu ergänzen)* |

## Team und Kontakte

| Refinement-Team | Ansprechpersonen |
|---|---|
| ‹Namen› | ‹Namen mit Funktion› |

## Bedienung und Design oder Datenmodell

‹optional›

| Datenmodell u. a. | Zuständig |
|---|---|

‹optional›

| Designs | Zuständig |
|---|---|

‹optional›

| Weitere Anlagen oder Dokumentation | Zuständig |
|---|---|

## Fragen

| Gefragt von | Frage | Beantwortet von | Antwort |
|---|---|---|---|

## Verworfen

| ID | Zusammenfassung | Grund / Hinweis |
|---|---|---|
```

**Discarded ist der letzte Abschnitt.** Ein Abschnitt für offene Punkte, Change Requests oder
automatische Tests gibt es nicht (§218, §220). Über dem Kopf steht nichts außer dem Titel und, nur auf
der übertragenen Seite, dem Satz `approved_note`. `transfer_note` und `status_documentation` setzt
kein Lauf mehr; sie bleiben in der Tabelle, weil `check-page.py` ihre Wörter kennt.

## Titel

`title` aus der Tabelle der Bezeichnungen, etwa `[EP-023] Barrierefreiheit`, in jeder Projektsprache
gleich, ohne Präfix (§261); der Titel des Epics ist `title` im Kopf der Epic-Datei. Derselbe Wortlaut
ist die Überschrift 1 des Rumpfs, der Name des Entwurfs im Drive und der Titel der
Seite. Über die Kennung findet jeder Lauf das Dokument wieder, im Drive wie in Confluence.

## Kopf

| Feld | beim Anlegen | danach |
|---|---|---|
| `Epic` | `‹Epic-ID›: ‹Titel des Epics›`, Kennung und Titel aus dem Repo, ohne Link | niemand; auch auf der Seite trägt die Zelle keinen Link auf das Board (§328) |
| `Document Owner` | `Owner Strix` des Epics aus dem Sheet, ein Feld der Menschen (§280, Regel 5); ist es leer, der Name, den der Lead nennt | niemand; ein anderer Owner ist Sache der Menschen |
| `Status in Blueprint` | `status_in_progress` (`In Arbeit`) | `solution-design`: `status_for_approval` (`Zur Abnahme`), sobald jede Anforderung ihren Lösungsansatz trägt oder, mit dem Ja des Leads, `decision_open`, im Epic der Domäne `design` ohne diese Bedingung (§297); `status_approved` (`Abgenommen`), wenn der Kunde den Scope freigegeben hat, der dieses Epic trägt (§277); je in der Sprache des Dokuments |
| `Phase of Launch` | was der Lead nennt, sonst leer | der Lead |
| `Initial Estimate (Cost Indication / Blueprint)` | `consultant_placeholder` | der Consultant (§220) |
| `Requirements Engineering Process`, `Approval of effort` | die Checkboxen offen, `___` bleibt stehen | ein Mensch; kein Lauf setzt eine Checkbox (§218) |

**Auf der übertragenen Seite** setzt `solution-epic-page` den Satz `approved_note`, den Status
`status_approved` und den Owner als Mention.

## Die Abschnitte

Ein fester Satz steht hier mit seinem Schlüssel und dem deutschen Wortlaut; ins Dokument kommt er in
dessen Sprache, aus der Tabelle der Bezeichnungen. Auch ein Beleg wie „Workshop ‹Titel› vom
‹TT.MM.JJJJ›" steht in der Sprache des Dokuments, bei `en` „Workshop ‹title› on ‹D Mon YYYY›"
([Datalayer-Vertrag](datalayer-contract.md), Die festen Wendungen). **Ein Datum steht in der Form der
Sprache** (§337): bei `de` `11.10.2026`, bei `en` `11 Oct 2026`; so in `approved_note`,
`changed_note`, `transfer_note` und in jedem Beleg.

**Goals and vision of the Customer.** Ein Satz: das Ziel des Epics aus Sicht des Kunden. Darunter der
Nutzen, ein Punkt je Zeile. Sachlich, nicht plakativ; Fachsprache, kein Produktjargon.

**Assumptions and delimitations.** Was Kunde und Dritte liefern, was vorausgesetzt wird, was sich
dadurch für Mitarbeitende und Kundschaft ändert, auch das Unbequeme. Je Abgrenzung die Zeile
`not_included`, „Nicht enthalten: ‹Gegenstand›, getragen von ‹Epic-ID›". Eine entschiedene Plattform- oder
Vertragslage ist keine Annahme. Trägt ein Lösungsansatz `KB: nicht gelesen` (`KB: not read`), steht hier als letzter Punkt
`kb_unread`, „Noch nicht gegen Lösungen aus früheren Projekten geprüft.", bis ein Lauf die
Wissensbasis für sie gelesen hat (§268; wann, sagt `solution-design`).

**Relations and Prerequisites.** Abhängigkeiten zu anderen Epics als Text, und die Aussagen der
Architektur, auf die die Lösung baut, mit ihrem Status, etwa „Integrationsschicht: offen; der zweite
Lösungsansatz setzt eine voraus" (§216). Ohne Dateinamen: der Kunde liest mit.

**Eine Aussage der Architektur steht in der Sprache des Entwurfs**, hier und in `Technical
Information`. `architecture.md` bleibt deutsch; bei `en` stehen die Zeilen des Fundaments und der
Status so, die übrige Aussage übersetzt der Lauf sinngemäß, etwa „Integration layer: open; option B
requires one":

| in `architecture.md` | `en` |
|---|---|
| `Shops` | `Shops` |
| `Bauform der Storefront` | `Storefront build` |
| `Integrationsschicht` | `Integration layer` |
| `Systemlandschaft` | `System landscape` |
| `belegt` | `evidenced` |
| `entschieden` | `decided` |
| `offen` | `open` |
| `widersprüchlich` | `contradictory` |

**Requirements.** Zwei bis fünf Sätze übergreifender Lösungsansatz: wie die Anforderungen des Epics
zusammen gelöst werden. Darunter die Tabelle, **eine Zeile je Anforderung des Epics im Umfang**:

| Spalte | Inhalt |
|---|---|
| `ID` | die Kennung der Anforderung |
| `Summary` | `title` aus ihrer Datei mit dem Shop-Bezug hinten, `Staffelpreise (B2B)` oder `(alle Shops)`, in einem Projekt mit einem Shop ohne (§307); die Zelle ist die Ausgabe von `python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/repo_objects.py . ‹Requirement-ID›` ohne die Kennung vorne. Die Epic Page übernimmt sie mit dem Entwurf |
| `User Story / Description` | erst die User Story, abgeleitet aus Ist, Soll, FC und UC der Anforderung nach [user-story-contract.md](user-story-contract.md) (§323), darunter, nach einem `<br>`, der erste Absatz von `## Description`. Immer eine User Story, nie nur die Beschreibung; eine Frage nach dem Nutzen entsteht nur, wo ohne ihn kein Akzeptanzkriterium prüfbar formuliert werden kann, und nennt das Kriterium (§250) |
| `Acceptance Criteria` | die Punkte aus `## Acceptance criteria`, je Kriterium ein Stichpunkt mit `• ` davor, getrennt mit `<br>`. Fehlen sie, bleibt die Zelle leer, und die Frage steht in `gaps/` |
| `Technical Information` | **solange die Wahl offen ist**: `choice_open` („Wahl offen."), die Lösungsansätze je in einem Satz, dann `recommendation` („Empfehlung:") ‹Lösungsansatz›, ‹Stufe und Grund›; setzt ein Lösungsansatz eine offene Aussage der Architektur voraus, steht das dabei (§216, §220). **Nach der Wahl** nur der gewählte Lösungsansatz aus `## Approach` und die Angaben aus `## Details`, in der Tiefe, die `solution-design` festlegt. Fehlt eine Auskunft, ohne die kein Lösungsansatz zu bestimmen ist: `way_open` („Lösungsansatz offen; die Frage steht im Sheet."). Lässt der Lead die Wahl offen: `decision_open` („Entscheidung offen, entscheidet ‹Gewerk›"), dann die Lösungsansätze (§220). **Im Epic der Domäne `design`** nur die Angaben aus `## Details`, sonst bleibt die Zelle leer (§297) |
| `Estimation` | `consultant_placeholder`; `solution-design` schreibt keine Stunden (§220), auch nicht die Modellschätzung `effort_estimate_model` (§357) |

**Jede Anforderung, deren `epic` das Epic nennt, steht genau einmal**, in `ID` unter `Requirements`
oder unter `Discarded`. Eine Spalte für Gewerke gibt es nicht: das Gewerk entsteht erst beim Anlegen
der Tickets (§280, Regel 2).

**Team & Contacts.** Die Namen, die der Lead nennt; sonst bleibt die Tabelle mit ihrem Kopf leer.

**User interaction and design or data model.** Nur die Tabellen mit Inhalt: Datenmodell, Entwürfe
(ein Figma-Frame mit Adresse), andere Unterlagen, je mit dem zuständigen Kontakt.

**Questions.** Nur beantwortete Fragen, die die Lösung geprägt haben, die Wahl eingeschlossen:
`Questioner` die Rolle, die fragte, `Question`, `Replying` wer antwortete, `Answer` mit der Quelle.
**Eine Frage, die `solution-design` gestellt hat**, im Chat oder in `gaps/`, trägt in `Questioner` immer
`Solution Architect`, gleich wem sie galt: der Lauf bereitet die Seite für ihn vor. Eine Frage aus
einem Kommentar oder einem Workshop trägt die Rolle dessen, der sie dort stellte. `Replying` nennt, wer
antwortete, mit der Rolle, etwa `Lead` oder `Kunde, Geschäftsführung`.
Die Antwort einer geschlossenen Frage aus `gaps/` steht unter ihrem `## Answer`. **Eine offene Frage
steht nicht im Dokument**, sondern in `gaps/` und im Sheet (§218, §220).

**Discarded.** Je Anforderung des Epics mit `status: rejected` oder `duplicate` oder mit
`scope: out_of_scope` eine Zeile; `Reason / Note` trägt den Grund aus der ADR der Ausklammerung, bei
einem Duplikat „siehe ‹duplicate_of›" (`en`: „see ‹duplicate_of›"), bei `out_of_scope` dazu, dass sie weiter gewünscht ist. **Eine
ADR-Kennung entfällt beim Übernehmen**, nach den Quellenregeln unten; die Quelle des Grunds bleibt.

## Stil

- **Jede Aussage steht genau einmal.** Eine Annahme wiederholt nicht den Nutzen, der übergreifende
  Lösungsansatz nicht die Zeilen der Tabelle, eine Zeile nicht eine andere. Probe: jeden Absatz
  streichen; fehlt dem Dokument nichts, bleibt er gestrichen.
- **Unsichere Aussagen** tragen am Zeilenende `to_confirm`, „(zu bestätigen)", keine Farbe. Muss jemand sie
  bestätigen, wird daraus eine Frage in `gaps/`.
- **Kürzer fassen.** Verstärker und Füllwörter streichen, wo sie nichts hinzufügen: genau, bereits,
  durchaus, natürlich, grundsätzlich, entsprechend, ohnehin. KI-typische Formulierungen vermeiden,
  „bewusst" ausdrücklich. Abkürzungen und Firmennamen beim ersten Vorkommen mit ihrer Rolle.
- **Shopify heißt Shopify**, nicht „die Plattform" oder „der Anbieter".
- **Keine projektinternen Organisationshinweise**: Epic-Teilungen, Umbenennungen, Arbeitsstände
  stehen im Repo und im Sheet. Zulässig ist der Verweis aus den Abgrenzungen auf das Epic, das ein Thema trägt.

## Quellenregeln, weil der Kunde mitliest

- **Belegt wird mit „Workshop ‹Titel› vom ‹TT.MM.JJJJ›"**, „Chat mit dem Lead vom ‹Datum›" (bei `en`
  „Workshop ‹title› on ‹D Mon YYYY›", „Chat with the lead on ‹D Mon YYYY›", §337) oder der
  öffentlichen Fundstelle; ein Link ist erlaubt. **Keine wörtlichen Zitate** aus Transkripten.
- **Zulässig** sind Confluence-Seiten mit vollständiger Adresse, Systeme des Kunden, Dokumente bei ihm
  oder seinen Partnern mit Titel, Fassung und Datum, öffentliche Fundstellen mit Adresse.
- **Keine interne Quelle**: keine Adresse aus dem Kundenordner, kein Link in die Wissensbasis, keine
  ADR-Kennung, keine Notiz, kein Dateiname des Datalayers, kein Kommentar des Werkzeugs.
- **Keine Interna** (§278): nichts aus einer Quelle mit `Intern: ja` oder einem Abschnitt `## Intern`,
  das der Kunde nicht kennen darf, auch nicht sinngemäß; keine internen Einschätzungen über Personen,
  Prozesse oder Partner, keine Preise und Rabatte, kein Verweis auf ein anderes Kundenprojekt. Die
  Liste steht in `way-of-working.md`, Abschnitt „Interna“; der Plan meldet „Interna: keine“.
- **Namen** stehen nur im Kopf, in `Questioner` und `Replying` und unter `Team & Contacts`.
