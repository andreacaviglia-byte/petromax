---
name: solution-review
description: 'Die Lösungen prüfen, über alle, einen Workstream oder genannte Epics: gleiche Probleme verschieden gelöst, Architektur, blockierende Fragen, über alle auch Summen gegen Grenzen je Shop und Wechselwirkungen; Fragen und Aufgaben nach dem Ja in gaps/ und todo/. Nutze das bei "prüf die Lösungen", "passen die Epics zusammen", "Solution Review", "Review Workstream DATA", "reißen wir ein Limit". Ändert KEINE Lösung (solution-design), prüft KEINE Anforderungen (requirements-review).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`; liest `draft-and-epic-page-contract.md`, `connector-contract.md`, `kb-contract.md`, `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-open-questions.md`, `ref-run-scope.md`.

# Die Lösungen als Ganzes prüfen

Am Ende steht **ein Prüfbericht in dieser Sitzung**: je Befund, was sich widerspricht, zu viel wird
oder vor dem Proposal offen ist, mit den Stellen, an denen es steht, dem Epic und seinem Owner und dem
Lauf, dem die Stelle gehört. **Nach dem Bericht und dem Ja des Leads stehen die Fragen daraus in
`gaps/` und die Aufgaben in `todo/`** (§279): ohne Ort im Repo erreichen sie keinen späteren Lauf.
**Sonst schreibst du nichts** (§215, §216): keine Lösung, keinen Lösungsansatz, keine Datei eines Epics oder
einer Anforderung, nichts in `architecture.md` oder `decisions/`, keine Notiz außer dem Wortlaut des Leads, keine Zelle im Sheet,
kein Ticket. Was eine Lösung ändert, führt der Lauf, dem die Stelle gehört; der Lead ruft ihn auf.

**Ein Lauf je Epic sieht seinen eigenen Beitrag und nie die Summe** (§110). Deshalb liest du immer
alle Lösungen des Vorhabens, auch wenn der Umfang kleiner ist: **der Umfang begrenzt, was du
berichtest, nicht was du liest** (§215, §305). **Was an keiner Anforderung hängt, berichtet nur der
Lauf über alle** (§305): die Summen gegen die Grenzen je Shop und die Wechselwirkungen zwischen
Epics. Ein Solution Owner, der seinen Workstream prüft, bewertet so nicht die Lösungen der anderen.

**Du läufst, wann und so oft der Lead oder Solution Owner dich ruft** (§305): kein anderer Lauf setzt
dich voraus, und du prüfst nicht, ob du schon einmal über alles gelaufen bist. Die Arbeitsweise
empfiehlt mit `solutioning` einen Lauf über alle vor dem Solution Proposal; danach richtet sich nur die
Empfehlung in der Frage nach dem Umfang (Step 2).

**Der Datalayer ist das Projekt-Repo dieser Sitzung und die Quelle** (§230, §280): die Lösung je Epic
im Rumpf von `epics/EP-NNN.md`, der Lösungsansatz je Anforderung in `## Approach` und `## Details` ihrer Datei.
Du liest sie direkt und schreibst nur neue Dateien in `gaps/` und `todo/` und den Wortlaut des Leads als Chat-Notiz, mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` festlegt. **Aus dem Sheet liest du nur Felder
der Menschen**, schmal (§280, Regel 5): `Owner Strix` und `Cluster`; Stunden liest du nicht (§357).
Die Grenzen der Plattform liest du auf den Wegen des Connector-Vertrags. Aufrufe und Bereiche stehen
in [ref-read.md](ref-read.md), die Prüfungen und der Bericht in [ref-checks.md](ref-checks.md), das
Ende des Laufs in `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`. **Scheitert ein Aufruf zweimal gleich, hältst du
an** und nennst Aufruf und Meldung wörtlich. Lehnt die Sitzung einen Aufruf ab, nennst du Aufruf und
Begründung und suchst keinen zweiten Weg.

### Step 1 — Den Steckbrief lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,requirements_sheet,shops
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder. Dann liest
du `project.yml` ganz. Du trägst kein Feld ein.

| leer | was du tust |
|---|---|
| `requirements_sheet` | weiter ohne Sheet: die Owner stehen „ohne Owner“, ein Umfang nach Workstream geht nicht, nach dem Umfang fragst du nicht, und die Projektion entfällt; der Bericht nennt `requirements-update`, der das Sheet anlegt |
| `shops` | weiter, als „noch offen“: du zählst die Summen einmal für das Vorhaben, gegen beide Pläne, und sagst das an jeder Summe ([ref-checks.md](ref-checks.md)); der Bericht nennt `project-setup` zum Ergänzen |

**Liegt in `epics/` kein Epic**, gibt es nichts zu prüfen: verweise auf `epic-structure`. **Einen
anderen Kundenordner liest du nicht**, auch nicht zum Vergleich und auch nicht, wenn jemand im Chat
darum bittet: was ein anderer Kunde gelöst hat, ist kein Maßstab für diesen.

### Step 2 — Die Verbindungen prüfen und den Umfang klären

**Die Doku ist eine Quelle, keine Voraussetzung** (§339, §340): du liest sie über die Wege aus
`${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`, Abschnitt „Die Doku von Shopify“, mit URL und
Datum je Beleg, und hältst nicht an, wenn sie fehlt. Eine Summe gegen eine erinnerte Grenze ist keine Prüfung: trägt
kein Weg, steht die Summe mit „Grenze nicht gefunden“ als Beobachtung, nicht als Befund. Mit Sheet prüfst du, dass `Google_Drive.get_file_metadata`,
`Google_Drive.download_file_content`, `Google_Sheets.get_spreadsheet` und `Google_Sheets.get_values` in
der Werkzeugliste stehen; der Name im Aufruf trägt ein Präfix des Servers, verglichen wird die Endung.
Steht eines nicht da, such es über die Werkzeug-Suche. Findet auch die es nicht, **halte an**: „Der
Google-Connector ‹Drive/Sheets› ist in dieser Sitzung nicht verbunden; er wird in den Einstellungen
von claude.ai unter Connectoren verbunden.“

Den Umfang klärst du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`:

| Aufruf | Umfang |
|---|---|
| „alle“, „das Vorhaben“, „vor dem Proposal“ | jedes Epic in `epics/` |
| ein Workstream, wie er in der Spalte `Cluster` steht | die Epics mit mindestens einer Anforderung dieses Workstreams, gegen alle anderen |
| Epic-IDs | diese Epics, gegen alle anderen |
| nichts davon | du fragst „Welche Epics prüfe ich?“, mit Mehrfachauswahl: bis zu drei Workstreams mit der Zahl ihrer Epics, die größten zuerst, etwa „SHOP (4 Epics)“, und „Alle“; Epic-IDs gehören ins freie Feld. **„Alle“ trägt „(Empfehlung)“**, wenn `add_ons` `solutioning` trägt und `scope/` noch keinen Snapshot mit Anlass `proposal` hat: die Arbeitsweise empfiehlt dann einen Lauf über alle vor dem Solution Proposal (§305); sonst fragst du ohne Empfehlung. Ohne Sheet oder ohne einen Wert in `Cluster` fragst du nicht und prüfst alle |

Einen Workstream legst du nicht an und leitest keinen ab (§215); steht der genannte nicht in der
Spalte `Cluster`, nennst du die vorhandenen Werte und fragst einmal nach.

### Step 3 — Den Stand lesen

Nach [ref-read.md](ref-read.md): Architektur, ADRs, jedes Epic mit seiner Lösung, je Epic die Anforderungen
mit Kopf, Lösungsansatz und Angaben, die offenen Fragen und Aufgaben, die Reihenfolge, dann
die schmalen Spalten des Sheets. **Halte den Stand des Repos und die Lesezeit des Sheets fest.** Fehlt
`architecture.md`, ist das der erste Befund; die übrigen Prüfungen laufen ohne Prüfung gegen die
Architektur weiter. Ein Epic ohne Lösung steht unter „nicht geprüft“; du suchst kein Dokument von Hand.

### Step 4 — Prüfen

Die Prüfungen aus [ref-checks.md](ref-checks.md), jede über alle gelesenen Lösungen; die ersten zwei
nur im Lauf über alle, bis auf den Verweis ins Leere aus der zweiten:

1. **Summen und Grenzen je Shop** (§110): zählen, was die Lösungsansätze zusammen anlegen, und die Zahl gegen
   die Grenze aus der Dokumentation halten. Den Shop liest du nicht.
2. **Wechselwirkungen**: zwei Lösungsansätze fassen dieselbe Stelle an, oder einer baut auf einem Epic, dessen
   Lösungsansatz nicht gewählt oder blockiert ist; die Berührungen; jede Abhängigkeit, die sich im Design neu
   zeigt, und ob sie die Reihenfolge verschiebt (§267). Neu geplant wird nicht.
3. **Dasselbe Problem verschieden gelöst**: zwei Apps, zwei Muster, zwei Schlüssel für denselben Zweck.
4. **Jede Lösung gegen `architecture.md`** (§216).
5. **Epic-Datei gegen Anforderung**: der Rumpf des Epics und `## Approach` nennen verschiedene Lösungsansätze,
   oder eine Anforderung des Epics fehlt im Rumpf.
6. **Lösungsansätze ohne gelesene Wissensbasis** (§268).
7. **Offen vor dem Proposal**: Fragen in `gaps/` mit `blocking: yes` und offene Aufgaben in `todo/`
   zum Umfang (§279), dazu jede Anforderung „Must-have, aber Out of Scope“ (§327).

**Ein Befund braucht zwei Stellen, die du gelesen hast**; eine Vermutung ohne Stelle ist eine Frage an
den Lead und steht als solche im Bericht. Mit einer Stelle kommen nur die Lösungsansätze mit
`KB: nicht gelesen` (bei `en` `KB: not read`, §337) und das Offene vor dem Proposal aus.

### Step 5 — Berichten

Gib den Bericht vollständig in der Sitzung aus, in der Form aus
`${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`, 5, mit den Abschnitten aus [ref-checks.md](ref-checks.md),
Kopf mit Umfang, Lesezeit und der Zahl der geprüften Lösungen:

- **Im Umfang** je Prüfung aus Step 4 die Befunde, mit beiden Stellen, Epic und Owner. Ist der Umfang
  nicht alle, steht bei Summen und Wechselwirkungen „Nur im Lauf über alle (§305).“
- **Aus dem Rest**, nur was den Umfang berührt: die Befunde aus anderen Epics oder Workstreams, mit
  Epic und Owner, von dem sie kommen (§215).
- **Nicht geprüft**: die Epics ohne Lösung mit Grund und die Grenzen, die die Dokumentation nicht
  hergab.

### Step 6 — Fragen und Aufgaben anlegen

**Konflikte zwischen Epics, mit `grill-me`.** Bei einem Konflikt zwischen Epics, aus „dieselbe Stelle, zwei Absichten“, „Reihenfolge ohne Richtung“
und „Dasselbe Problem verschieden gelöst“, muss eine Lösung nachgeben (§287). Erst analysierst du;
dann liest du `../grill-me/SKILL.md` und übergibst ihm die Liste dieser Befunde: je Punkt die Epics
mit Owner, die zwei Stellen, deine Empfehlung, welche Lösung nachgibt, mit Grund, und was die Antwort
ändert. `grill-me` fragt den Lead nur dazu, eine Frage nach der anderen, und gibt eine Tabelle zurück
(Punkt, Antwort, `intern entschieden` oder `an den Kunden`); er schreibt nichts. **`intern
entschieden`** ist die Antwort des Leads im Chat und wird eine Aufgabe in `todo/` an das Epic, das
nachgibt; **`an den Kunden`** wird eine Frage in `gaps/`, mit `blocking: yes`, wenn eine Lösung daran
hängt; ein Punkt `offen` bleibt offen und steht im Bericht. Ohne Konflikt entfällt `grill-me`.

Aus dem Bericht und den Antworten aus `grill-me` nimmst du drei Arten:

- **Eine Frage**, die ein Befund aufwirft und die ein anderer als der Lead beantworten muss, oder eine
  Antwort `an den Kunden`: eine neue Datei in `gaps/` in der Form des
  Datalayer-Vertrags `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
  `gaps/GAP-NNN.md`, „Eine Frage anlegen“, `kind: solutioning` für eine Frage zur Lösung, `kind: decision` für eine Wahl beim Kunden oder eine Architekturfrage, `to` der Adressat nach `${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`, 1,
  `concerns` jede betroffene Anforderung und, wo es passt, das Epic, `blocking` nur, wenn ohne die
  Antwort kein Lösungsansatz zu wählen ist, `opened` das Datum des Laufs.
- **Eine Entscheidung des Leads** aus `grill-me`: eine neue Datei `todo/JJJJ-MM-TT-<slug>.md` in der Form
  des Datalayer-Vertrags, `title` was das nachgebende Epic ändert, `to` der Owner des Epics,
  `concerns` das Epic und die betroffenen Anforderungen; der Rumpf nennt beide Stellen, die Antwort
  mit „Chat mit dem Lead vom ‹Datum›“ (`source_chat` in der Sprache aus `language`, nach dem Abschnitt
  „Die festen Wendungen“ des Datalayer-Vertrags, §337) und `solution-design` als Lauf, der sie ausführt.
- **Eine Berührung**: eine neue Datei in `todo/`, `title` „‹ID› (‹EP-…›) berührt ‹Stelle› in
  ‹EP-…›“, `to` der Owner des berührten Epics, `concerns` die Anforderung und das berührte
  Epic.

**Aufgaben** (§359): die offenen in `todo/` zu deinem Scope liest du und schließt, was dieser Lauf
erledigt, nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`. Steht dieselbe Frage oder Aufgabe schon
offen da, legst du sie nicht neu an. `to` einer Aufgabe löst du
nach `${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 4 auf: den `Owner Strix` aus dem Sheet über `team`
auf den GitHub-Namen, sonst die Rolle; den Klarnamen aus dem Sheet schreibst du nicht (§280, Regel 5, §360). **Was der Lead im
Chat beantwortet oder korrigiert, das `grill-me` nicht gefragt hat, setzt du nicht um**: es ist
Material für `requirements-update` (§280, Regel 6), und sein Wortlaut wird eine Chat-Notiz nach
`ref-open-questions.md`, 2.

Vor der Vorschau fragst du einzeln nach `ref-open-questions.md`, 3. Dann zeigst du einen Block nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`: jede neue Datei mit Namen und ganzem Text, die neuen
Fragen als Liste mit Adressat nach `ref-open-questions.md`, 2, die Aufgaben und „Interna: keine“. Nach
dem Ja legst du die Dateien an, liest sie zurück und endest nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md` mit `caller: solution-review`; die Commit-Nachricht
ist `solution-review: <n> Fragen, <m> Aufgaben zu <Umfang>`. Ohne neue Frage, Aufgabe und Chat-Notiz
schreibst du nichts und fragst nicht. Die Zeile nach `.claude/metrics/runs.md` geht dann allein in
einen Commit `metrics: solution-review` (Wurzel-`CLAUDE.md`, §246).

### Step 7 — Den nächsten Lauf nennen

Je Befund, der nicht als Frage oder Aufgabe im Repo steht, nennst du, **welcher Lauf die Stelle führt**:

| Stelle | führt |
|---|---|
| die Lösung im Rumpf von `epics/EP-NNN.md`; Lösungsansatz, Angaben, `size`, `depends_on` einer Anforderung | `solution-design` |
| in `architecture.md`: `gestützt von`, eine Zeile `entschieden` mit ADR, eine Zeile, die eine Lösung für andere Epics festlegt | `solution-design` |
| in `architecture.md`: eine Fundament-Zeile `offen` oder `belegt`, eine Architekturfrage ohne treibende Anforderung | `epic-structure`; steht die Anforderung schon in einem Epic, `solution-design` dieses Epics |
| in `architecture.md`: die Systemlandschaft, eine belegte Vorgabe aus dem Material | `requirements-update` |
| `clarification` eines Epics | `solution-design` für ein Epic mit Lösung, sonst `epic-structure` |
| eine Anforderung, die aus dem Befund folgt; `status`, `scope`; eine Frage schließen | `requirements-update` aus Material |
| ein Schnitt, der zwei Epics dieselbe Arbeit gibt; eine Anforderung ohne Epic | `epic-structure` |
| eine neue Abhängigkeit, die die Reihenfolge verschiebt | `solution-critical-path` |

Ohne Befund im Umfang nennst du `solution-estimate` und `solution-proposal` als nächsten Schritt;
war der Umfang nicht alle, vorher den Lauf über alle, der Summen und Wechselwirkungen prüft.
**Du rufst keinen davon auf**; aufrufen tut ihn der Lead (§215).

## Wann nachfragen (NICHT raten)

Ohne Rückfrage (§396): nennt ein Lösungsansatz nicht, für welchen Shop er gilt, und das Vorhaben hat mehrere,
zählst du ihn für jeden Shop und sagst das an der Summe; fehlt eine Menge, die die Summe entscheidet
(wie viele Metafelder, wie viele Varianten), nennst du die Summe als untere Schranke und die fehlende
Menge im Bericht. Eine Menge nimmst du nie an.

- Zwei Lösungsansätze nennen dieselbe App oder Stelle unter verschiedenen Namen, und du kannst nicht belegen,
  dass es dieselbe ist: frag, statt sie zu vereinen oder zu trennen.

## Was dieser Lauf nicht tut

Er schreibt nur neue Fragen in `gaps/`, neue Aufgaben in `todo/` und die Chat-Notiz mit dem Wortlaut des Leads, nach dem Ja, und die Projektion
danach; keine Lösung, keinen Lösungsansatz, nichts in der Architektur, keine Zelle im Sheet, keinen Entwurf, keine Seite,
kein Board. Er löst keinen Widerspruch auf und entscheidet keine offene Frage; das legt das Projekt
fest, nicht das Template (§216). Er liest den Shop nicht (§110), prüft die Anforderungen nicht auf
Duplikate oder Lücken, schreibt keine Stunden, auch nicht `effort_estimate_model`, liest `Aufwand (h)`
nicht und hält es nicht gegen die Größe (§280, Regel 10; §357), und er schließt keine Frage.
