<!-- Projektion aus .claude/way-of-working-standard.md und den Abweichungen in way-of-working/; nie von Hand ändern (§286). -->
# Arbeitsweise

**So wird in diesem Vorhaben gearbeitet.** Widerspricht diese Arbeitsweise einem Skill, gilt sie, und
der Skill nennt die Abweichung in seiner Vorschau (§286). Was ein Prüf-Script ablehnen würde, braucht
einen abgeleiteten Skill (§225). Wie ein Skill seinen Schritt ausführt, steht in seinen Refs, nicht
hier.

## Die Kette

**In jedem Vorhaben läuft `material-intake` → `requirements-update` → `solution-approach` →
`ticket-factory`** (§282), **im Projekt mit `epic-structure` vor `ticket-factory`**: der Schnitt in
Epics und die Fundament-Fragen gehören zur Discovery (§403). Mit dem Add-on `solutioning` läuft vor
`solution-approach` `requirements-review`, und nach dem Schnitt das Solutioning:
`solution-solve-order` für die Reihenfolge des Lösens, `solution-design` je Epic in dieser Folge,
`solution-critical-path` für die Reihenfolge des Bauens (§318), `solution-review`,
`solution-estimate` und `solution-proposal`; nach der Freigabe je Epic `solution-epic-page`, vor
seinen Tickets (§313).
Mit dem Add-on `e2e_testing` läuft `e2e-testing-sheet` für die Prozess-Tests zum Go-Live. Projekttyp
und Add-ons stehen in `project.yml` (§303).

- `project-setup` fragt im ersten Lauf nur, was nie im Material steht: Projektordner, Sprache,
  Board, Confluence-Space und Team. Kunde, Titel, Shops, Projekttyp und Add-ons schlägt es nach dem
  ersten Einlesen als „Steckbrief“ aus dem Material vor, je Feld mit Fundstelle; der Lead bestätigt
  einmal.
- **Nach `material-intake` läuft `requirements-update` in derselben Sitzung weiter**, in jedem
  Vorhaben, mit einem Ja am Ende für beide (§400). Beim ersten Einlesen kommt zuerst `project-setup`
  „Steckbrief“, in einer neuen Sitzung.
- Material aus dem Chat nimmt `requirements-update` direkt an.
- **`solution-approach` schlägt je Anforderung bis zu drei Lösungsansätze mit Empfehlung vor**,
  ohne Belege (§401). Mit dem Add-on `solutioning` belegt `solution-design` sie je Epic und der Lead
  wählt dort; im Expert Service wählt der Lead schon in `solution-approach`. Seine Antworten stehen
  nach jeder Runde als Chat-Notiz im Repo.
- **Jeder schreibende Lauf endet gleich:** `check-repo.py`, dann die Projektion ins Sheet, in die
  `readme.md` und in diese Datei (§280).

**`requirements-review` und `solution-review` stehen in der Folge, sind aber kein Pflichtschritt**
(§305): der Lead oder Solution Owner ruft sie, wann und so oft er will, über alles, über einen
Workstream, über genannte Anforderungen oder Epics, `requirements-review` auch über den Input einer
Session. Kein Lauf setzt einen Review voraus.

## Wer entscheidet

- **Der Lead entscheidet im Lauf.** Kein Lauf schreibt vor seinem Ja.
- **Das Was kommt nur über Material:** Anforderungen, `Status`, `Scope` und Antworten, auch die des
  Leads, nie durch einen Eintrag im Sheet (§280). Kennt der Lead eine Antwort aus einem Gespräch,
  gehört das Gespräch als Material ins Repo.
- **Fragen an den Kunden beantwortet der Kunde**, nicht der Lead stellvertretend. Sie werden offene
  Fragen in `gaps/` (§279). Jede neue steht vor dem Ja in einer Liste mit Adressat, Kunde, Agentur
  oder ein anderer Dienstleister; der Lead korrigiert, was nicht stimmt (§399).
- **Die Felder der Menschen setzen Menschen, im Sheet** (§280): `Cluster`, `Owner Kunde`, `Owner
  Strix`, `Aufwand (h)`, `Kommentar`, `Geprüft von`, `Geprüft am`, im Tab `Offene Punkte`
  `Verantwortlich` und `Bis`, im E2E-Sheet Status, Ergebnis, getestet von und am.

## Wo was liegt

**Das Repo ist die Quelle der Wahrheit** (§280): Anforderungen in `requirements/`, Epics und die
Reihenfolge des Lösens und des Bauens in `epics/`, offene Fragen in `gaps/`, interne Aufgaben in `todo/`,
Entscheidungen in `decisions/`, E2E-Tests in `tests/`, die Architektur in `architecture.md`, Material in
`inputs/`, Notizen in `notes/`, eingefrorene Stände in `scope/`. Drive trägt Ein- und
Ausgabedokumente und die Projektionen: Anforderungsliste, Schätzung, Proposal, Entwurf je Epic,
E2E-Sheet. Confluence trägt nur Freigegebenes, mit `solutioning` jedes freigegebene Epic (§313). Das Board trägt die Umsetzung. Pfade
und Formate stehen in `.claude/docs/datalayer-contract.md`.

## Übergaben

**Was ein Lauf vom vorigen braucht, steht im Repo**, nie nur im Chat. Eine Übergabe an den nächsten
Lauf oder eine andere Person ist eine Notiz in `notes/`; eine Aufgabe, die jemand erledigen muss, ist
ein Eintrag in `todo/` mit dem, an den sie geht. Eine Frage, an der die Arbeit hängt, ist eine Datei
in `gaps/` mit `Blockiert`.

**Eine Aufgabe legt jeder schreibende Lauf an, der interne Arbeit findet und nicht selbst tut, und
`requirements-update` auch aus Material; schließen tut sie der Lauf, der ihre Arbeit tut, oder jede
Person im Projekt über `project-status`, mit dem Ergebnis in der Datei** (§359). Nur den Vorschlag
zur Arbeitsweise schließt `project-setup`.

## Status und Scope

**`Status` sagt, ob eine Anforderung gilt; `Priorität`, ob der Kunde sie braucht; `Scope`, ob sie
jetzt gebaut wird** (§283, §327). Alle drei setzt `requirements-update` aus dem Material.

| `Status` | heißt |
|---|---|
| Offen | der Ausgangszustand; ob Fragen sie aufhalten, zeigt `Offene Fragen` |
| Bestätigt | vom Kunden bestätigt; braucht eine Quelle beim Kunden |
| Verworfen | nicht mehr gewünscht oder nicht gültig |
| Duplikat | dasselbe Wollen wie eine andere Anforderung, die genannt ist |

| `Priorität` | heißt |
|---|---|
| Must-have | die Vorgabe jeder Anforderung |
| Nice-to-have | nur, wenn der Kunde es ausdrücklich sagt, mit der Stelle als Quelle |

Im Repo ist das das Feld `priority`, `must-have` oder `nice-to-have`; geraten wird nie. Im Sheet steht
die Spalte `Priorität` direkt vor `Scope`, weil beide zusammen gelesen werden (§327).

| `Scope` | heißt |
|---|---|
| leer | noch nicht geschnitten |
| In Scope | wird in diesem Vorhaben gebaut |
| Out of Scope | weiter gewünscht, aber nicht in diesem Scope |

`Scope` setzt `requirements-update` mit der Scope-Freigabe, im Expert Service auf Ansage des Leads.

## Prüfpunkte und Freigaben

- **Eingefroren wird dreimal:** am Ende der Discovery (`requirements-update`), mit dem Proposal und mit
  der Freigabe (beide `solution-proposal`, die Freigabe auf „Kunde hat freigegeben“), je mit Manifest
  und Commit in `scope/` (§280).
- **Prüfpunkt je Epic:** `Geprüft von` und `Geprüft am` im Tab `Epics`, nur von Hand (§277). Das
  Proposal nimmt nur geprüfte Epics auf, die übrigen als „in Arbeit“.
- **Mindestens einmal vollständig, mit dem Add-on `solutioning`** (§305, §322): `requirements-review`
  läuft über alle Anforderungen am Ende der Discovery, `solution-review` über alle Epics vor dem
  Solution Proposal. Ohne das Add-on steht `requirements-review` nicht in der Kette; der Lead kann
  ihn trotzdem aufrufen. Kein Skill prüft das.
- **Vor dem Proposal** prüft `solution-review` offene Fragen mit `Blockiert` und offene Einträge in
  `todo/` zum Scope.
- **Mit der Scope-Freigabe** setzt `requirements-update` den `Scope`, und `ticket-factory` legt alle
  Tickets an. Die Freigabe friert den Entwurf eines Epics ein; danach kann er über
  `solution-epic-page` nach Confluence.

## Größe ja, Stunden nein

**Die KI schätzt die Größe (S–XL); Stunden schätzt sie nur als Modellschätzung** (§280, §357).
Stunden setzt ein Mensch, in `Aufwand (h)` im Tab `Solutioning` und im Schätzdokument; kein Skill
schlägt eine Stundenzahl als Wert dafür vor, auch nicht als Hinweis. **Nur `solution-design` schätzt
Stunden**; kein Lauf hält `Aufwand (h)` gegen die Größe. Die Größe gegen die Stunden zeigt der
Kalibrierungsbericht, `calibration-report.py`, je Größe für einen Menschen.

**Die Schätzungen des Modells stehen nur im Repo** (§357): `solution-approach` schätzt die Größe
und hält sie zusätzlich in `size_estimate_approach` fest. **Stunden schätzt das Modell nur mit dem
Add-on `solutioning`**, in `effort_estimate_model`, sobald die Lösung einer Anforderung entschieden
ist: `solution-design` setzt sie mit der Wahl, bevor der Lead schätzt; kein anderer Lauf.
Sie ist die Rohschätzung des Modells, frei aus der Lösung, ohne Spanne, je Teil geschätzt und addiert,
begründet mit den Details der Lösung; die Zerlegung je Teil liegt in `.claude/metrics/estimates/`.
Korrigiert wird sie mit einem Faktor je Bereich aus
`calibration.md`, gerechnet und nie gespeichert; die Faktoren setzt ein Mensch. Ohne
`solutioning` schreibt kein Lauf eine Stundenzahl, auch nicht im Expert Service. Beide Schätzungen
dienen dem Vergleich mit der Zahl des Menschen und dem Ist-Aufwand und sind keine Zusage: sie stehen
nicht in der Anforderungsliste, im Entwurf, auf der Epic Page, im Proposal, im E2E-Sheet und im
Ticket, und das Schätzdokument rechnet nur mit `Aufwand (h)`.

**Das Solution Proposal nennt keine Stunden** (§355), kein Gesamt und kein Budget. Die Stunden fasst
das interne Schätzdokument zusammen: `solution-estimate` gliedert sie nach Positionen, mit
Projektmanagement, Testing und dem Gesamt. Ein Budget steht dort nicht und nie im Repo (§352, §355);
den Abgleich mit dem verkauften Budget machen PM oder Sponsor außerhalb der Strecke.

## Ticketschnitt

- **Epic → Story → Subtask** (§281). Eine Story je Anforderung; sie trägt User Story und die
  Akzeptanzkriterien, an denen sie abgenommen wird, und ist die Einheit für die Gewerk-QS, das interne
  Review des Solution Owners und die Abnahme des Kunden. Kein Standard-Subtask für Testing oder
  Dokumentation, keine Stunden am Ticket.
- **Ein Gewerk:** die Story trägt die Komponente bzw. `Kategorie`, keine Subtasks. **Mehrere
  Gewerke:** je Arbeitseinheit eines Gewerks ein Subtask mit eigenem Titel, User Story, Kriterien der
  Umsetzung und Angaben; im Theme-Epic ist die Arbeitseinheit die Section. Die Subtasks einer Story
  stehen in Arbeitsreihenfolge, ausgedrückt durch ihre Nummer.
- **Titel:** Story `REQ-012 ‹Titel der Anforderung›`, Subtask `REQ-012-1 ‹eigene Aufgabe›`; das Gewerk
  steht nie im Namen.
- **Owner statt Cluster:** `ticket-factory` setzt an Epic und Story den Owner auf die Person, die den
  Lauf startet; jeder Solution Owner startet den Lauf für seine Stories selbst. Kein Label `DEV` beim
  Anlegen; das setzt ein Mensch in der Umsetzung.
- **Kein stilles Überschreiben:** vor jeder Änderung an einem bestehenden Ticket liest `ticket-factory`
  das Ticket und legt Abweichungen vor.

## Wunschliste

**Tickets entstehen für jede Anforderung mit `Status` Offen oder Bestätigt, unabhängig vom `Scope`**
(§284); für Verworfen und Duplikat entsteht keines. Out of Scope geht in die Spalte Wunschliste des
Boards, leer und In Scope in den Eingang.

## Zuarbeit von UX/UI und die eigenen Sections

- **UX/UI arbeitet zu** (§285). Was das Team liefert, ist Material und geht über `material-intake` und
  `requirements-update` in die Kette; mehrere UX/UI-Sessions sind mehr Material.
- **Vor der Scope-Freigabe** legt die UX/UI-Session mit dem Kunden fest, welche Seitentypen wir selbst
  gestalten, wie weit wir vom alten Shop oder vom Theme abweichen und je Anforderung `Design nötig?`.
  Das Theme steht danach fest und kommt als Zeile `Bauform der Storefront: Theme` in `architecture.md`,
  bevor `solution-design` Lösungsansätze wählt.
- **Kein Inventar vor der Freigabe.** Jeder Seitentyp ist eine Anforderung im Theme-Epic mit einer
  Größe und einer Annahme zu den eigenen Sections. Mit dem Add-on `solutioning` setzt `solution-design`
  beide, der Lead bestätigt, der Kunde bestätigt mit der Scope-Freigabe; ohne es kommt die Annahme aus
  dem Angebot, sonst wird sie eine offene Frage mit `Blockiert`.
- **Das Design entsteht in der Umsetzung**, Seitentyp für Seitentyp. Die Übergabe eines abgenommenen
  Seitentyps ist Material: `requirements-update` schreibt die Sections mit Frame in die Anforderung und
  meldet ein Mehr gegenüber der Annahme als Änderung des Scopes, als offene Frage mit `Blockiert` an
  Lead und Kunden; dann legt `ticket-factory` die Section-Subtasks an.
- **Das Theme-Epic** hat eine Story je Seitentyp; die erste ist „Design-System und globale Sections“.
  Funktion gehört ins Epic ihrer Fähigkeit, auch wenn sie im Theme-Code steckt.
- **Mit dem Add-on `design`** trägt ein eigenes Design-Epic die Arbeit des Designers,
  darin die UX/UI-QA vor dem Go-Live als Story.
- **Die Theme-Arbeit verantwortet der Solution Owner des Workstreams SHOP**; der UX/UI-Designer ist Specialist und
  prüft in der internen QS zu.

## Interna

**Interne Inhalte gehen nie nach außen, auch nicht sinngemäß** (§278). Intern sind ganze Quellen,
die `material-intake` als Ganzes markiert (Transkripte und Notizen interner Termine, Übergaben, das
Pre-Sales-Briefing), und Abschnitte „Intern“ in anderen Notizen. Intern ist insbesondere:

- Preisfindung und Verhandlungstaktik,
- Budgetpuffer,
- Einschätzungen zu Kunde und Personen,
- Potenzial für Folgeaufträge,
- saloppe Formulierungen und Zitate aus internen Gesprächen.

**Erlaubt sind nur sachliche Fakten, die der Kunde kennt oder kennen darf.** Extern ist alles, was
Kunde oder Dritte lesen: Entwurf, Proposal, E2E-Sheet, das geteilte Sheet und die Tickets. Jeder
Ausgabe-Skill meldet in seiner Vorschau „Interna: keine“.

## grill-me

**`grill-me` läuft im Solutioning** (§287), und in `skill-create` beim Klären eines eigenen Skills (§290): in `solution-design` vor der Wahl offener Lösungsansätze und
vor dem Prüfpunkt zu den Edge Cases, in `solution-review`, wenn bei einem Konflikt zwischen Epics
eine Lösung nachgeben muss. Der Lead ruft ihn auch direkt auf.

- Er fragt nur, was der Lead oder Owner selbst entscheidet; Fragen an den Kunden werden offene Fragen
  in `gaps/`.
- Er schreibt nichts; geschrieben wird vom aufrufenden Skill bzw. `requirements-update`.
- Eine Working Session mit dem Kunden ersetzt er nicht.

## Wer diese Arbeitsweise ändert

- **`way-of-working.md` wird nie von Hand geschrieben** (§286). Die Projektion schreibt sie aus dem
  Standard des Templates (`.claude/way-of-working-standard.md`) und den Abweichungen in
  `way-of-working/`, jede unter ihrem Abschnitt.
- **Ändern tut der `project_owner`** aus `project.yml`, mit `project-setup` (§299), oder ein
  Projekt-Admin, wer bei GitHub Admin am Repo ist und damit die Rechte des Owners hat (§390): der Lauf legt ihm
  die Abweichung als Datei für `way-of-working/` vor und schreibt sie nach seinem Ja. Wer nicht Owner
  ist, ändert nur in seinem Auftrag: `project-setup` und, in Claude Code, der Hook `wow-guard.py`
  fragen dann vorher nach (§301).
- **Alle anderen schlagen vor:** `project-status` legt den Vorschlag als Eintrag in `todo/` an den
  `project_owner` an; er nimmt ihn mit `project-setup` an oder lehnt ihn ab, und nimmt er an, nennt
  die Datei der Abweichung beide.
- **Was nur die Arbeit eines Workstreams betrifft**, trägt ein eigener Skill mit dem Solution Owner in
  `verantwortlich:` (§225), angelegt über `skill-create` (§290).
- **Ein Upgrade ersetzt nur den Standard** (§294): `project-upgrade` lässt `way-of-working/`
  unberührt; es führt nur der `project_owner` aus, jeden anderen verweist es an ihn (§350).
