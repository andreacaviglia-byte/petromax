---
name: solution-design
description: 'Die Lösung eines Epics führen, in epics/EP-NNN.md und je Anforderung: Lösungsansätze mit Beleg und Wissensbasis, Fragen in gaps/, die Wahl mit ADR und Architektur, Größe; dazu der Entwurf als Google-Doc im Drive, dessen Kommentare Material sind. Nutze das bei "löse EP-003", "Entwurf anlegen", "arbeite die Kommentare ab", "wir nehmen den zweiten". Schneidet KEINE Epics (epic-structure), nimmt KEIN Material auf (requirements-update), überträgt NICHT nach Confluence (solution-epic-page).'
---

Verträge: schreibt `datalayer-contract.md`, `draft-and-epic-page-contract.md`, `inputs-and-notes-contract.md`; liest `solution-choice-contract.md`, `user-story-contract.md`, `kb-contract.md`, `shopify-limits.md`, `connector-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-open-questions.md`, `ref-run-scope.md`.

# Die Lösung eines Epics führen

Am Ende steht **die Lösung des Epics im Rumpf von `epics/EP-NNN.md`**, in der Gliederung des Vertrags
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, **jede Anforderung des Epics genau einmal**, mit ihrem gewählten Lösungsansatz, ihren
Lösungsansätzen oder als verworfen; **in jeder Anforderung des Epics der Lösungsansatz und die
Angaben, die er braucht**, ohne Gewerk (§280); jede Wahl mit ADR, und was sie für andere Epics festlegt, in `architecture.md`. Daraus
**projiziert der Lauf den Entwurf**, ein Google-Doc im Unterordner `Epics` von `Solutioning`, einmal
angelegt und danach gezielt fortgeschrieben (§302), und das Sheet. **Die Dateien im Repo führen, der
Entwurf zeigt sie**; was im Entwurf anders steht, ist Material, keine Korrektur.

**Nicht raten.** Eine fehlende Angabe wird eine Frage in `gaps/`; eine Antwort gilt nur, wenn sie
vorliegt. **Du rufst keinen anderen Skill auf** (§215), außer `grill-me` an den Stellen in Step 9
(§287); den nächsten Lauf nennst du. **Nach Confluence überträgst du nicht**: das tut
`solution-epic-page` für ein geprüftes, freigegebenes Epic (§277).

Drive und Sheets erreichst du nur über die Google-Connectoren `Google_Drive` und `Google_Sheets`. Das
Schema holst du über die Werkzeug-Suche, bevor du das erste Feld setzt. **Scheitert ein Aufruf zweimal
gleich, hältst du an**: kein Ausweichen, der Bericht nennt Aufruf, Meldung und die beabsichtigte
Änderung wörtlich. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und Begründung. **Eine Datei,
die dieser Lauf im Drive kaputt angelegt hat, kommt weg** (§259): sie kommt mit
`Google_Drive.trash_file` in den Papierkorb, sobald sie für die Neuerstellung nichts mehr trägt; nur
was dieser Lauf selbst angelegt hat, ohne Rückfrage; der Bericht nennt Name und Link.

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest und schreibst seine Dateien
direkt, mit dem Umgang, den `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` je Pfad festlegt;
was dort „nie überschrieben" heißt, legst du nur neu an. Was du liest und schreibst, steht in
[ref-repo.md](ref-repo.md). Das Ende des Laufs, Prüfung, Projektion ins Sheet und Commit, steht in
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`. **Die User Story je Anforderung leitest du im
Rumpf der Epic-Datei ab** (§323), nach `${CLAUDE_SKILL_DIR}/../../docs/user-story-contract.md`;
`ticket-factory` schreibt sie von dort ab.

### Step 1 — Die Verbindungen prüfen

Prüf, dass `Google_Drive.search_files`, `Google_Drive.get_file_metadata`, `Google_Drive.create_file`,
`Google_Drive.download_file_content`, `Google_Drive.read_file_content`,
`Google_Docs.read_doc`, `Google_Docs.update_doc`,
`Google_Sheets.get_spreadsheet` und `Google_Sheets.get_values` in der Werkzeugliste stehen. Der Name im
Aufruf trägt ein Präfix des Servers; verglichen wird die Endung. Steht eines nicht da, such es erst
über die Werkzeug-Suche. Findet auch die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets/Docs›
ist in dieser Sitzung nicht verbunden; er wird in den Einstellungen von claude.ai unter Connectoren
verbunden." **Die Doku ist eine Quelle, keine Voraussetzung** (§339, §340): du liest sie über die Wege aus
`${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`, Abschnitt „Die Doku von Shopify“, und hältst
nicht an, wenn sie fehlt. Die Wissensbasis ist weich ([ref-sources.md](ref-sources.md)).

### Step 2 — Das Vorhaben binden

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,language,shops,requirements_sheet
```

Exit 1 heißt anhalten und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder:

| leer | Folge |
|---|---|
| `requirements_sheet` | du arbeitest weiter; die Projektion ins Sheet entfällt, und der Bericht nennt `requirements-update` |
| `language` | du fragst den Lead, die Antwort darf „noch offen" sein (§229): `de` oder `en`, keine Variante (§202). Eingetragen wird nach dem Ja (Step 12). Bleibt sie offen, nennt der Lead die Sprache dieses Laufs |
| `shops` | du arbeitest weiter; der Bericht nennt `project-setup` zum Ergänzen |

Vor dem ersten Zugriff auf eine Datei, die du nicht durch eine Suche im Ordner gefunden hast (das
Sheet, der Entwurf über `draft`), liest du mit `get_file_metadata` (`fileId`) ihre Eltern,
bis der Projektordner (`project_folder`) erreicht ist. **Einen anderen Kundenordner liest du nicht**,
auch nicht auf Bitte im Chat.

### Step 3 — Epic und Anforderungen bestimmen

**Der Aufruf nennt ein oder mehrere Epics oder Anforderungen** (§215). Nennt er nichts davon,
läufst du nicht los (§398, `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`): du nennst in einem Satz die nächsten offenen Epics nach `solve_order`,
offen heißt mit einer Anforderung ohne `solution_status: decided`, und fragst „Welche Epics löse
ich?“, mit Mehrfachauswahl, bis zu vier Epic-IDs mit Titel als Antworten, das erste mit
„(Empfehlung)“. Ist keins offen oder fehlt `epics/`, hältst du an und nennst `epic-structure`.

**Mehrere Epics löst du nacheinander**, in der Folge von `solve_order`: Step 3 bis 13 je Epic, mit
eigenem Ja und eigenem Commit, sodass nach jedem Epic der Stand im Repo liegt. Wird der Kontext knapp,
endest du nach einem Epic und nennst die übrigen als nächsten Lauf, in einer neuen Sitzung (§244).

**Der Scope begrenzt, was du schreibst, nicht was du liest** (§215, §398): die Lösungsansätze der übrigen
Epics liest du mit, nach [ref-repo.md](ref-repo.md), Lesen, damit die Lösung zu ihnen passt. Ein Konflikt
mit einem anderen Epic wird eine Aufgabe an dessen Owner, wie unten in Step 7; die Summen über alle
Epics prüft `solution-review` (§65).

Nach [ref-repo.md](ref-repo.md), Lesen, dazu die offenen Aufgaben in `todo/` zum Epic und seinen
Anforderungen nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 1: eine Berührung, eine
Entscheidung des Leads oder eine gemeinsame Lösung, die dieser Lauf aufnimmt, schließt er (§359). **Gibt es `epics/EP-NNN.md` nicht, oder nennt der Aufruf eine
Anforderung, deren `epic` leer ist oder ein anderes Epic nennt, legst du kein Epic an und hängst
nichts um**: halte an und nenne `epic-structure`.

**Trägt das Epic einen `board_key`**, gibt es Tickets: was dieser Lauf an einer Anforderung ändert,
gilt am Board erst, wenn `ticket-factory` es nachzieht, und der Bericht nennt es. **Beginnt
`clarification` mit `Nachprüfen:`**, prüfst du in diesem Lauf die Lösung gegen die neue Zeile in
`architecture.md` und nimmst `Nachgeprüft: ‹Datum›, trägt` oder `… geändert` in den Plan.

**Ein Epic der Domäne `design` bekommt keinen Lösungsansatz** (§297): es trägt die Arbeit des
UX/UI-Designers, darunter die UX/UI-QA als Story, und `ticket-factory` legt deren Stories ohne
`## Approach` an. Du setzt dort weder `## Approach` noch `solution_status`, `classification`, `size`,
`effort_estimate_model` oder eine ADR; Step 8 und 10 entfallen für seine Anforderungen. Den Rumpf führst du wie bei jedem Epic.

### Step 4 — Die Blocker mit geändertem Ziel nennen

Bevor du am Epic arbeitest, nennst du **jede Anforderung mit `solution_status: blocked` oder einer
offenen blockierenden Frage, deren Ziel sich geändert hat** ([ref-questions.md](ref-questions.md)),
und bietest eine neue Prüfung an: die Anforderungen dieses Epics in diesem Lauf, wenn der Lead Ja
sagt, die anderer Epics mit ihrem Epic.

### Step 5 — Die Architektur lesen

Lies `architecture.md`, liste `decisions/` und lies die ADRs mit `status: accepted`, dazu die ADRs
auf `proposed`, die eine Anforderung des Epics in `depends_on` nennt (die Evaluierung einer App).
**Die Architektur gilt für jede Lösung** (§216): ein Lösungsansatz, der eine `entschieden`e Zeile bricht, ist ein Blocker oder eine neue
ADR mit `supersedes`, nie eine stille Abweichung; ein Lösungsansatz, der eine `offen`e Zeile voraussetzt, sagt
das im Entwurf. Fehlt die Datei, halte an: sie entsteht mit dem Sheet, der nächste Lauf ist
`requirements-update`. **Ein Seitentyp im Theme-Epic braucht die Zeile `Bauform der Storefront: Theme`**
als `belegt` oder `entschieden`, bevor du Lösungsansätze wählst (§285); fehlt sie, wird das eine Architekturfrage.

### Step 6 — Entwurf, Zustand und Kommentare

Nach [ref-draft.md](ref-draft.md), Den Entwurf projizieren, Schritt 1 und 2: den Entwurf finden, seine
Kommentare und seine Abweichungen gegen den Rumpf der Epic-Datei lesen. Den Zustand
bestimmst du nach [ref-draft.md](ref-draft.md), Die Zustände:

| Zustand | Was du tust |
|---|---|
| kein Entwurf | du schreibst den Rumpf nach der Vorlage, Owner nach [ref-repo.md](ref-repo.md), Status `status_in_progress` (`In Arbeit`) |
| Wahl offen | Kommentare und Antworten abarbeiten, fragen, die Lösungsansätze schärfen |
| Wahl benannt | Begründung nach Step 10, ADR und Architektur (Step 10), den gewählten Lösungsansatz eintragen |
| zur Prüfung | die Prüfliste aus [ref-draft.md](ref-draft.md); geprüft wird von Hand (§277) |
| freigegeben | der Entwurf ist eingefroren: Änderungen nur im Repo, der Entwurf wird nicht fortgeschrieben; der Bericht nennt sie als mögliche Change Request |

**Nennt `Document Owner` im Rumpf jemand anderen**, sagst du: „Entwurf in Arbeit bei ‹Owner›, zuletzt
geändert ‹Datum›. Weitermachen?" und wartest.

### Step 7 — Lesen und nach Antworten suchen

Lies nach
[ref-sources.md](ref-sources.md): jede Anforderung des Epics ganz, die offenen und geschlossenen Fragen
in `gaps/`, **alle** Dateien in `inputs/` und `notes/` und `customer.md`. **Steht eine Notiz einer
Runde zu diesem Epic mit `Stand: offen`**, kommt dieser Lauf nach einer abgebrochenen Sitzung: du
nennst ihr Datum und `Lead:` und übernimmst ihre Antworten
(`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Die Notiz einer Runde).

**Je Kommentar und je Abweichung im Entwurf ein Verdikt**, das der Bericht nennt: eine Antwort auf eine
Frage, eine Korrektur am Was, eine Korrektur oder Ergänzung am Wie, eine neue Frage, eine Wahl, nichts
für diesen Lauf (mit Grund). **Eine Antwort und eine Korrektur am Was sind Material für
`requirements-update`** (§280, Regel 6): sie kommen wörtlich in die Notiz der Kommentare
([ref-repo.md](ref-repo.md)), und der Bericht nennt den Lauf. **Eine Korrektur am Wie** arbeitest du
nach dem Ja des Leads ein; eine neue Frage kommt nach `gaps/`; eine Wahl gilt erst mit der Bestätigung
des Leads (Step 10). Du antwortest auf keinen Kommentar und löst keinen auf. **An Dateien eines
anderen Epics schreibst du nicht**: was es betrifft, wird eine Aufgabe in `todo/` an den Owner jenes
Epics, in der Form einer Berührung, nach `ref-tasks.md` (§359).

### Step 8 — Die Lösungsansätze belegen

**Je Anforderung belegst du die Lösungsansätze, die `solution-approach` in die Datei geschrieben hat**
(§401), je mit `kb_match`, eine begründete Empfehlung und `classification` nach
[ref-options.md](ref-options.md): einen streichst du mit Grund, einen besseren nimmst du mit Beleg
auf, höchstens drei; **einen Fit gegen den Standard bestätigst du nur**, mit Beleg, ohne neue
Suche. **Die Wissensbasis liest du für jeden Lösungsansatz**
(`get_file_contents`, erst `index.md`, dann die Stamps), **jede Plattformaussage gegen die
Dokumentation** auf den Wegen des Connector-Vertrags. Trägt keiner, steht die Aussage mit „(noch zu
verifizieren)“ da, bei `en` „(to be verified)“ (§337, §339, §340); ist die Wissensbasis nicht erreichbar,
arbeitest du mit `KB: nicht gelesen` weiter, bei `en` `KB: not read` ([ref-sources.md](ref-sources.md),
§268, §337).
**Steht eine Public App zur Wahl**, evaluierst du mindestens zwei Apps mit Namen gegen die
Muss-Kriterien, je mit Beleg ([ref-options.md](ref-options.md), Eine Public App evaluieren, §320).
**Jedes Muss-Kriterium des gewählten Lösungsansatzes braucht einen Beleg**, für jede Klassifizierung; ein
unbelegtes ist eine blockierende Frage (§326). Sind App Store oder Help Center nicht
erreichbar, hältst du nicht an: der Bericht nennt es, und die Frage entsteht.

**Einen Lösungsansatz, der eine Anforderung aus dem Standard-Leistungssatz bricht, schlägst du nicht
vor**, auch nicht als Empfehlung. Verlangt der Lead ihn, nennst du die Anforderung, die er bricht;
die Wahl bleibt seine, und die ADR nennt sie. Findet sich keiner, obwohl alle Auskünfte vorliegen,
ist die Anforderung ein **Blocker** ([ref-questions.md](ref-questions.md)). **Bei einem Seitentyp**
setzt du mit dem Lösungsansatz Größe und `own_sections` ([ref-options.md](ref-options.md), Die Größe).

### Step 9 — Fragen klären, mit `grill-me`

Erst analysierst du; dann klärst du, was offen bleibt, an zwei Stellen mit `grill-me` (§287): **vor
der Wahl offener Lösungsansätze** und **vor `status_for_approval` zu den Edge Cases**. Du liest
`../grill-me/SKILL.md` und übergibst ihm die Liste deiner Befunde: je Punkt die Anforderung, die Frage,
deine Empfehlung und was die Antwort ändert. `grill-me` fragt den Lead nur dazu, eine Frage nach der
anderen, und gibt eine Tabelle zurück (Punkt, Antwort, `intern entschieden` oder `an den Kunden`); er
schreibt nichts. **`intern entschieden`** ist die Antwort des Leads im Chat und gilt mit „Chat mit dem
Lead vom ‹Datum›"; **`an den Kunden`** wird eine Frage in `gaps/`, mit `blocking: yes`, wenn die Lösung
daran hängt ([ref-questions.md](ref-questions.md)), mit dem Adressaten aus der Tabelle; sie steht
in der Liste der Vorschau wie jede neue Frage
(`${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`); ein Punkt `offen` bleibt offen und steht im
Bericht.

Dazu die Frage des Lösungsansatzes je Anforderung oder Teilthema: „Welcher Lösungsansatz? a)
‹Lösungsansatz› b) ‹Lösungsansatz›, Empfehlung ‹Lösungsansatz›, weil ‹Grund›." Erlaubt sind auch „Offene Frage" (bei `en` „Open question") und „Entscheidung offen,
entscheidet ‹Gewerk›" ([ref-questions.md](ref-questions.md)). Sind mehrere offen, stellst du bis
zu vier in einem Aufruf, je mit ihrer Empfehlung zuerst (§396). **Nach jeder Runde** schreibst du die
Antworten des Leads in die Notiz einer Runde des Epics, committest und pushst sie allein
(`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Die Notiz einer Runde); Anforderungen,
Epic und Entwurf ändern sich erst nach dem Ja. **Eine Frage der Freigabe stellst du
nicht** (§277). Der Entwurf trägt keine offene Frage (§218).

### Step 10 — Die Wahl festhalten

Die Wahl benennt der Lead; du empfiehlst, du wählst nicht. Wählt er deine Empfehlung, ist ihr Grund
die Begründung der ADR, ohne Rückfrage (§396); wählt er eine andere ohne Begründung, fragst du danach. Dann, nach [ref-adr.md](ref-adr.md): die ADR; neue oder geänderte Zeilen in `architecture.md`
mit dem Epic in `gestützt von`; im Rumpf der Epic-Datei nur noch der gewählte Lösungsansatz in `Technical
Information` (W16) und die Wahl als beantwortete Frage unter `Questions`. In der Datei der
Anforderung nach [ref-repo.md](ref-repo.md): `## Approach` mit dem gewählten Lösungsansatz zuerst,
`## Details`, `solution_status: decided`, außer eine blockierende Frage hält sie, `classification`,
`size` nach den Ankern in [ref-options.md](ref-options.md), mit `decided` und dem Add-on `solutioning`
die Modellschätzung `effort_estimate_model` nach [ref-model-estimate.md](ref-model-estimate.md)
(§357), `depends_on`, `design_needed` und `interface_needed`, bei einem Seitentyp `own_sections`.

### Step 11 — Belegpass, Plan und das Ja

Vor dem Plan läuft der **Belegpass** aus [ref-options.md](ref-options.md) und die Quellenregeln aus
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`. Dann zeigst du einen Block nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`, **was wo entsteht oder sich ändert, im Klarnamen**:

- den Rumpf der Epic-Datei, je Stelle alt und neu, und je Kommentar und Abweichung sein Verdikt;
- je Anforderung des Epics die Felder und Abschnitte alt und neu, darunter `effort_estimate_model`
  mit Stunden und Begründung je Teil nach [ref-model-estimate.md](ref-model-estimate.md), In der
  Vorschau, und die Datei der Zerlegung in `.claude/metrics/estimates/`; sie ist die Rohschätzung des Modells, kein Wert für `Aufwand (h)` (§357);
- die neuen Fragen als Liste mit Adressat nach `ref-open-questions.md`, je mit ihrer Datei; die
  Notiz der Kommentare und die Notiz einer Runde mit Dateinamen;
- die ADR mit Dateinamen und Text, die Zeilen in `architecture.md`, `clarification` von Epics und
  `project.yml` alt und neu;
- den Entwurf: „angelegt in `Epics`", oder je Stelle, die fortgeschrieben wird, alt und neu, oder
  „freigegeben, nicht fortgeschrieben";
- die Aufgaben und „Interna: keine“, wie die Vorschau es vorgibt.

### Step 12 — Schreiben, prüfen, projizieren

In dieser Folge, jeweils direkt davor gelesen und danach zurückgelesen. **Zugangsdaten,
Gesundheitsdaten und Daten der Endkunden schreibst du nicht**, in keine Datei und keinen Entwurf
(§236; was darunter fällt, sagt der Datalayer-Vertrag):

1. **`project.yml`**, wenn der Lauf Felder einträgt: nach dem Datalayer-Vertrag, Abschnitt `project.yml`.
2. **Die Dateien der Anforderungen und die Epic-Datei** nach [ref-repo.md](ref-repo.md), die neuen
   Fragen nach [ref-questions.md](ref-questions.md), die Aufgaben nach `ref-tasks.md`, die Notiz der Kommentare, die Notiz einer Runde mit `Stand: abgeschlossen`; mit `effort_estimate_model`
   die Zerlegung in `.claude/metrics/estimates/` nach [ref-model-estimate.md](ref-model-estimate.md).
3. **ADR und Architektur** nach [ref-adr.md](ref-adr.md): leg die ADR an; in der ADR, die sie mit
   `supersedes` ablöst, änderst du nur die Zeile `status:`; schreib `architecture.md` fort.
4. **Prüfen**: `check-page.py` auf den Rumpf der Epic-Datei (`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`) und
   „jede Anforderung genau einmal" ([ref-repo.md](ref-repo.md)). Ein Befund ist ein Fehler dieses
   Laufs: du berichtigst und prüfst neu.
5. **Der Entwurf**, außer das Epic ist freigegeben: nach [ref-draft.md](ref-draft.md), Den Entwurf
   projizieren, Schritt 3 bis 5; ein neu angelegter Entwurf bekommt seinen Link in `draft` der Epic-Datei.
6. **Das Ende** nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, mit
   `caller: solution-design`: `check-repo.py`, die Projektion ins Sheet, `readme.md`, ein Commit mit
   der Nachricht `solution-design: <was>`; hat der Lauf eine Zeile in `architecture.md` ersetzt, nennt
   die Nachricht die ersetzte Aussage (§231).

Scheitert ein Schritt, bleibt stehen, was steht; der Bericht nennt Schritt und Meldung.

### Step 13 — Berichten und den nächsten Lauf nennen

Sag knapp, nach der Regel für Berichte (§397): den Link des Entwurfs, angelegt oder fortgeschrieben,
und den Zustand; je Anforderung Lösungsansatz, Größe und ob er entschieden ist; je Kommentar und Abweichung sein Verdikt; neue Fragen, davon blockierende; die
Blocker; die Entscheidung und was sich an der Architektur ändert, in einem Satz; jede Quelle, die ungelesen
blieb, die Wissensbasis mit den Lösungsansätzen, die `KB: nicht gelesen` tragen; installierte Apps und Theme als
unbekannt, wenn das Material sie nicht nennt; ob der Connector Kommentare am Entwurf geliefert hat und ob jeder nach dem
Fortschreiben noch an seinem Text hängt.

Dann den nächsten Lauf, den der Lead aufruft: `requirements-update` für die Notiz der Kommentare, neues
Material oder Antworten; wieder `solution-design`, wenn Fragen beantwortet sind, und für das nächste
Epic das erste offene nach `solve_order`, der Reihenfolge des Lösens aus `solution-solve-order` (§318, §403);
`solution-critical-path`, sobald diese Lösung `depends_on` setzt oder ändert, damit die Reihenfolge
des Bauens zu den Lösungen passt; danach `solution-review`, wenn der Entwurf gegen die Architektur
gegengelesen werden soll; `epic-structure`, wenn der Schnitt fehlt oder
umgehängt werden soll; `ticket-factory`, sobald ein Lösungsansatz gewählt ist; `solution-epic-page` für ein
geprüftes, freigegebenes Epic, vor seinen Tickets (§313).

## Wann nachfragen (NICHT raten)

- Zwei Quellen sagen Verschiedenes, und keine ist sicher die jüngere: eine Frage, keine Wahl.
- Eine Abweichung im Entwurf widerspricht der Epic-Datei: eine Frage an den Lead, keine Korrektur.
- Ein Kommentar klingt wie eine Wahl oder eine Abnahme: der Lead bestätigt sie, sonst gilt sie nicht.

## Was dieser Lauf nicht tut

Er schneidet nicht, hängt nicht um, klammert nicht aus und legt kein Epic an; das Was einer
Anforderung, `status` und `scope` schreibt `requirements-update`, und eine Frage schließt nur er. Er
setzt keine Checkbox, keinen Prüfpunkt und keine Stunden außer `effort_estimate_model` (§357), schlägt
keine als Wert für `Aufwand (h)` vor, schreibt die Modellschätzung nicht in den Entwurf, legt kein Ticket an, antwortet auf keinen
Kommentar, überträgt nichts nach Confluence und schreibt den Entwurf nach der Freigabe nicht fort.
