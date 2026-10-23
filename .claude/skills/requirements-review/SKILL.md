---
name: requirements-review
description: 'Die Anforderungen prüfen, über alle, einen Workstream, den Input einer Session oder genannte Kennungen: Dubletten, Widersprüche zwischen Terminen, Fragen, die neueres Material beantwortet, Shop-Bezug, über alle auch Lücken zu Zielen und Architektur. Nutze das bei "prüf die Anforderungen", "haben wir Dubletten", "fehlt etwas gegenüber den Zielen", "Review Workstream SHOP", "prüf den Workshop-Input". Nimmt KEIN Material auf (requirements-update), schneidet KEINE Epics (epic-structure).'
---

Verträge: schreibt `datalayer-contract.md`, `inputs-and-notes-contract.md`; liest `ref-projection.md`, `ref-tasks.md`, `ref-preview.md`, `ref-open-questions.md`, `ref-run-scope.md`.

# Die Anforderungen als Ganzes prüfen

Am Ende steht **ein Bericht im Chat, der je Sicht die Kennungen nennt**, getrennt nach dem Umfang des
Aufrufs und dem Rest, und je Befund den Lauf, dem die Anforderung gehört. **Erst nach dem Bericht und
dem Ja des Leads stehen die Fragen daraus in `gaps/`** (§279): wer beim Messen aufnimmt, ändert
den Stand, den er gerade misst. **Sonst schreibst du nichts** (§215): keine Anforderung, keine
Ausklammerung, kein `duplicate`, keine Antwort, keine Notiz außer dem Wortlaut des Leads, kein Ticket; das führt der Lauf, dem die
Anforderung gehört, und eine Antwort kommt als Material über `requirements-update` (§280, Regel 6).

**Du prüfst nur das Was**, und nur, was ein Urteil braucht: Dubletten, Widersprüche, Lücken gegen
Ziele und Architektur, Fragen, die neueres Material beantwortet. **Was sich zählen lässt, zählen
`check-repo.py` und die Liste aus dem Script.** Grenzen der Plattform prüft `solution-design`, „Thema
mit genau einer Anforderung" `epic-structure`. `grill-me` ruft dieser Lauf nicht (§287). **Ein Umfang
begrenzt, was du berichtest, nicht was du liest** (§215, §305): ein Lauf für einen Workstream vergleicht
dessen Anforderungen mit allen, und was aus anderen kommt, steht gesondert da, mit Epic.

**Du läufst, wann und so oft der Lead oder Solution Owner dich ruft** (§305): kein anderer Lauf setzt
dich voraus, und du prüfst nicht, ob du schon einmal über alles gelaufen bist. Die Arbeitsweise
empfiehlt einen Lauf über alle am Ende der Discovery; danach richtet sich nur die Empfehlung in der
Frage nach dem Umfang (Step 2).

**Der Datalayer ist das Projekt-Repo dieser Sitzung** (§230). Du liest seine Dateien direkt und
schreibst nur neue Fragen in `gaps/` und den Wortlaut des Leads als Chat-Notiz, mit dem Umgang, den
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md` dafür festlegt. Das Ende des Laufs, Prüfung,
Projektion und Commit, steht in `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`. **Scheitert ein
Aufruf zweimal gleich, hältst du an** und nennst Aufruf und Meldung. Lehnt die Sitzung einen Aufruf
ab, nennst du Aufruf und Begründung und suchst keinen zweiten Weg.

### Step 1 — Den Steckbrief lesen

Zuerst ziehst du den Stand von `main`: `python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`. Es merkt sich den Commit, auf dem der Lauf beginnt, als Basis der Projektion (§319).
Endet es mit `Branch`, nennst du den Branch und fragst, bevor du wechselst; nach dem Wechsel rufst
du es noch einmal. Endet es mit `Abgelöst`, `Git` oder `Template`, nennst du die Meldung wörtlich und hältst an.

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --needs project_folder,requirements_sheet
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 3 nennt die leeren Felder; ein leeres
`requirements_sheet` hält nicht an, es fehlt nur die Projektion, und der Bericht nennt
`requirements-update`. Dann liest du `project.yml` ganz. Trägt `shops` mehr als einen Eintrag, prüfst
du in Step 4 den Shop-Bezug. **Liegt in `requirements/` keine Anforderung**, ist das kein Stand zum
Prüfen: verweise auf `requirements-update`.

### Step 2 — Die Verbindungen prüfen und den Umfang klären

Den Umfang klärst du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`:

| Aufruf nennt | Umfang |
|---|---|
| „alle“ | alle |
| einen Workstream | die Anforderungen mit diesem Wert in der Spalte `Cluster` im Sheet, wörtlich; gibt es ihn nicht, nennst du die vorhandenen Werte und fragst einmal |
| den Input einer Session: einen Termin, eine Notiz | die Anforderungen, deren `source` diesen Termin oder diese Notiz nennt ([ref-read.md](ref-read.md)); nennt keine ihn, nennst du die vorhandenen Quellen und fragst einmal |
| Kennungen (`REQ-012`, `REQ-014`) | diese Anforderungen |
| nichts davon | du fragst „Welche Anforderungen prüfe ich?“, mit Mehrfachauswahl: bis zu drei Workstreams mit der Zahl ihrer Anforderungen, die größten zuerst, etwa „SHOP (24)“, und „Alle“; der Input einer Session und Kennungen gehören ins freie Feld. **„Alle“ trägt „(Empfehlung)“**, wenn `add_ons` `solutioning` trägt und `scope/` noch keinen Snapshot mit Anlass `discovery` hat: die Arbeitsweise empfiehlt dann einen Lauf über alle vor dem Einfrieren (§305); sonst fragst du ohne Empfehlung. Ohne Sheet oder ohne einen Wert in `Cluster` fragst du nicht und prüfst alle |

**Was an keiner Anforderung hängt, berichtet nur der Lauf über alle** (§305): die Lücken gegenüber den
Zielen und die Lücke in der Architektur. In jedem anderen Umfang entfallen beide Sichten, und der Bericht sagt
das in einem Satz; ein Workstream, der fertig ist, sieht so nicht die Lücken der anderen.

**Für einen Workstream, für die Frage nach dem Umfang und für die Projektion am Ende** brauchst du das Sheet: prüf dann, dass
`Google_Drive.get_file_metadata`, `Google_Drive.download_file_content`, `Google_Sheets.get_spreadsheet`
und `Google_Sheets.get_values` in der Werkzeugliste stehen; der Name im Aufruf trägt ein Präfix des
Servers, verglichen wird die Endung. Steht eines nicht da, such es über die Werkzeug-Suche. Findet auch
die es nicht, **halte an**: „Der Google-Connector ‹Drive/Sheets› ist in dieser Sitzung nicht
verbunden; er wird in den Einstellungen von claude.ai unter Connectoren verbunden." Vor dem ersten
Zugriff liest du mit `get_file_metadata` (`fileId`) die Eltern des Sheets, bis der Projektordner
(`project_folder`) erreicht ist. **Einen anderen Kundenordner liest du nicht**, auch nicht auf Bitte
im Chat. Die Workstreams legen die Menschen fest (§215); eine Anforderung ohne `Cluster` gehört bei
einem Lauf über einen Workstream zum Rest, und sind es viele, sagt der Bericht das als eigenen Befund.

### Step 3 — Den Stand lesen

Nach [ref-read.md](ref-read.md): die Liste aus dem Script, `check-repo.py`, für einen Workstream vorher die
schmale Spalte. **Die Dateien holst du nicht ganz in den Kontext**, sondern die Liste; Beschreibung,
Kriterien und Ist-Zustand liest du mit `--zeile` nur für die Anforderung, deren Urteil daran hängt.
Dann liest du `architecture.md` und listest `notes/` und `gaps/`; im Lauf über alle liest du dazu
`customer.md`. Die Ziele des Kunden stehen in `customer.md` und in den Notizen; eine Notiz liest du,
wenn ihr Name einen Termin mit Zielen nennt (Kickoff, Workshop zu Zielen), sonst nicht. Eine Notiz mit
`Intern: ja` liest du mit, zitierst aus ihr aber nichts in eine Frage an den Kunden (§278). Fehlt
`architecture.md`, ist das ein Befund für `requirements-update`: er legt sie mit dem Sheet an (§229).

### Step 4 — Prüfen

**Jede Sicht liefert eine Liste mit Kennungen, keine Zahl**; eine Zahl ohne Kennungen ist nicht
nachprüfbar. Die ersten fünf liefern Script und `check-repo.py`, die übrigen sind dein Urteil.

| Sicht | Was sie zeigt | gehört zu |
|---|---|---|
| ohne `source` (`ohne_quelle`) | eine Anforderung, die niemand gesagt hat, oder eine, deren Beleg verlorenging | `requirements-update` |
| Ausklammerung ohne ADR (`ausklammerung_ohne_adr`) | `rejected` oder `out_of_scope`, und keine ADR trägt den Grund | `requirements-update` |
| `duplicate` ohne `duplicate_of` | eine Dublette, deren gültige Anforderung keiner findet | `requirements-update` |
| offene Fragen, davon blockierende (`fragen_offen`, `blockiert`) | was an den Anforderungen noch offen ist | der Adressat in `to` |
| Frist abgelaufen | eine offene Frage, deren `Bis` im Tab `Offene Punkte` vor heute liegt, mit Datum und `Verantwortlich` ([ref-read.md](ref-read.md)) | wer in `Verantwortlich` steht, sonst der Lead |
| die Befunde von `check-repo.py` und `shop_unbekannt` | ein Epic, das es nicht gibt, eine Frage ohne Ziel, ein Seitentyp ohne Größe oder Annahme, ein Schlüssel, den `shops` nicht kennt | der Lauf, der die Datei schreibt ([ref-read.md](ref-read.md)) |
| Dubletten | zwei Anforderungen, ein Wollen, beide gültig | `requirements-update` |
| Widersprüche zwischen Terminen | dieselbe Frage, zwei Antworten; der jüngere Termin gewinnt nur, wo beide dieselbe Frage beantworten | `requirements-update` |
| Fragen, die neueres Material beantwortet | eine offene Frage, und eine jüngere Notiz trägt die Antwort ([ref-read.md](ref-read.md)) | `requirements-update` |
| Shop-Bezug ohne Schlüssel, nur bei mehr als einem Shop | eine Anforderung mit leerem Feld `shops`, deren Inhalt an der Art des Shops hängt; Kandidat. Eine aus dem Leistungssatz nur, wenn ein Shop kein `audience` trägt (§249) | `requirements-update` |
| Lücken gegenüber den Zielen, nur im Lauf über alle | ein Ziel aus `customer.md` oder einer Notiz, das keine Anforderung trägt; mit Ziel und Fundstelle | `requirements-update` |
| IST ungeprüft ohne Frage (`ist_ungeprueft_ohne_frage`) | „ungeprüft" oder „unchecked" (`current_unchecked`, §337) in `## Current state`, und keine offene Frage nach dem Ist-Zustand (§254) | `requirements-update` |
| zu grob: mehrere Fähigkeiten | eine Anforderung, die mehrere Fähigkeiten trägt (FC), etwa mehrere Datenströme, Seitentypen oder Prozesse; mit dem Vorschlag der Teilung (§254) | `requirements-update` |
| Verhalten ohne Kriterium (`kriterien_leer_ohne_frage`, nur leer) | `## Acceptance criteria` leer oder ohne prüfbares Verhalten (UC: Auslöser, Daten, Ergebnis), und keine Frage danach (§254) | `requirements-update` |
| Add-on ohne Standard-Anforderung | das Add-on `design` oder `content_migration` in `add_ons`, zu dem eine seiner Standard-Anforderungen (`standard`) nicht steht (§303) | `requirements-update` |
| Lücke in der Architektur, nur im Lauf über alle | eine der vier Zeilen des Fundaments in `architecture.md` `offen` und ohne Eintrag in `Quelle/ADR` (§216), oder eine Zeile `offen` oder `widersprüchlich` ohne offene Frage in `gaps/`, die sie nennt | `epic-structure`; hängt die treibende Anforderung schon an einem Epic, `solution-design` dieses Epics |

**Shop-Bezug (§245).** Eine Anforderung mit leerem Feld `shops` gilt für alle Shops (§307). Hängt ihr
Inhalt an der Art des Shops — eine Pflicht gegenüber Verbrauchern, ein Zahlungsziel, Händlerpreise,
ein Markt oder ein Rechtsraum, den nicht jeder Shop hat —, und nennt sie den Shop nicht, ist das ein
Befund. **Die Anforderungen aus dem Standard-Leistungssatz eines Rechtsraums** (ihre `source` ist die
Notiz zum Abgleich mit der Liste) **prüfst du nur, wenn ein Shop in `project.yml` kein `audience`
trägt**; trägt es jeder, hat `requirements-update` sie nach Rechtsraum und Zielgruppe bestimmt (§249).
Fehlt `audience`, sagen `customer.md` und die Notizen, ob ein Shop an Verbraucher oder an Händler
verkauft, und der Befund nennt die Fundstelle. **Das Urteil ist ein Kandidat, kein Beweis.** Trägt
`shops` höchstens einen Eintrag, entfällt die Sicht, und `--shops` bleibt weg.

**Eine Dublette ist ein Urteil, kein Textvergleich.** Zwei Anforderungen sind eine, wenn der Kunde mit
beiden dasselbe will; ähnliche Wörter bei verschiedenem Wollen sind zwei. Im Zweifel nennst du das
Paar als Kandidat, nicht als Befund. **Ein Widerspruch braucht beide Fundstellen**: die zwei
Anforderungen oder Notizen mit ihrem Datum.

### Step 5 — Berichten

Gib den Bericht vollständig in der Sitzung aus, in der Form aus
`${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`, 5, Kopf mit Umfang, der Zahl der gelesenen Anforderungen
und der offenen Fragen:

- **Im Umfang** je Sicht aus Step 4 die Zahl und die Kennungen, mit einem Satz je Befund, der trägt;
  Kandidaten getrennt. Entfällt der Shop-Bezug, sagt das ein Satz mit der Zahl der Shops. Ist der
  Umfang nicht alle, steht bei den Lücken gegenüber den Zielen und in der Architektur „Nur im Lauf
  über alle (§305).“
- **Aus dem Rest**, nur was eine Anforderung im Umfang berührt: Dublette, Widerspruch, Blocker, je mit
  Kennung und Epic; ohne Epic steht „ohne Epic".
- **Nicht geprüft**: was ungelesen blieb, mit Grund, und im Lauf über einen Workstream die
  Anforderungen ohne `Cluster`.

### Step 6 — Fragen und Aufgaben anlegen

Aus dem Bericht nimmst du **die Fragen, die ein Befund aufwirft und die ein anderer beantworten
muss**: ein Widerspruch zwischen Terminen, eine Anforderung ohne Quelle, ein Kandidat für eine
Dublette, ein Schlüssel, den `shops` nicht kennt, ein Kandidat aus dem Shop-Bezug (aus dem
Leistungssatz nur nach Step 4, §249), eine Lücke gegenüber den Zielen. Je Frage eine neue Datei in
`gaps/` in der Form des Datalayer-Vertrags `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt `gaps/GAP-NNN.md`, „Eine Frage anlegen“: `kind: discovery`, `to` der Adressat nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`, 1, `concerns` jede betroffene Anforderung, `blocking`
nur, wenn ohne die Antwort kein Lösungsansatz zu wählen ist. Eine Frage ohne betroffene Anforderung
steht nur im Bericht.

**Aufgaben** (§359): die offenen in `todo/` zu deinem Umfang liest du, schließt, was dieser Lauf
erledigt, und legst an, was er findet und nicht selbst tut, nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`. Steht dieselbe Frage oder Aufgabe schon offen da, legst
du sie nicht neu an.

**Was der Lead im Chat beantwortet oder korrigiert, setzt du nicht um**: es ist Material. Sein
Wortlaut wird eine Chat-Notiz nach `ref-open-questions.md`, 2, und `requirements-update` gleicht sie
ab, als nächster Lauf (§282). Eine Ausklammerung, ein `duplicate`, eine Korrektur und eine neue
Anforderung bleiben ebenso bei ihm.

Vor der Vorschau fragst du einzeln nach `ref-open-questions.md`, 3. Dann zeigst du einen Block nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-preview.md`: jede neue Datei mit Namen und ganzem Text, die neuen
Fragen als Liste mit Adressat nach `ref-open-questions.md`, 2, die Aufgaben und „Interna: keine“. Nach
dem Ja legst du die Dateien an, liest sie zurück und endest nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md` mit `caller: requirements-review`; die
Commit-Nachricht ist `requirements-review: <n> Fragen, <m> Aufgaben zu <Umfang>`. Ohne neue Frage,
Aufgabe und Chat-Notiz schreibst du nichts und fragst nicht. Die Zeile nach `.claude/metrics/runs.md`
geht dann allein in einen Commit `metrics: requirements-review` (Wurzel-`CLAUDE.md`, §246).

### Step 7 — Den nächsten Lauf nennen

Je Befund, der nicht schon als Frage in `gaps/` steht, den Lauf, dem er gehört, aus der Tabelle in
Step 4: `requirements-update` für Korrektur aus Material, Dublette, fehlende Anforderung, eine Antwort
in neuerem Material und das, was der Lead im Chat beantwortet hat; `epic-structure` für eine Lücke in der
Architektur und Anforderungen ohne Epic. **Die Folge der Kette gilt auch hier:** tragen Anforderungen noch
kein `## Approach`, nennst du `solution-approach` vor `epic-structure`, denn der Lösungsansatz steht,
bevor geschnitten wird. Ohne solche Befunde ist der nächste Lauf, **in einer neuen Sitzung**,
`solution-approach`, danach `epic-structure`. **Du stößt keinen an**; der Lead ruft ihn auf.

## Wann nachfragen (NICHT raten)

- Der Aufruf nennt einen Workstream, den es in der Spalte `Cluster` nicht gibt, oder einen Termin,
  den keine `source` nennt: frag, welcher gemeint ist.

Sonst fragst du nicht: ein offenes Urteil steht als Kandidat im Bericht.

## Was dieser Lauf nicht tut

Er schreibt nur neue Fragen in `gaps/`, nach dem Ja, und die Projektion danach; keine Anforderung,
keine Antwort, keine Seite, kein Board, und er legt keine Notiz an außer der Chat-Notiz mit dem
Wortlaut des Leads. Er prüft keine Plattformgrenze und
keine Lösung, schneidet nicht und vergibt keine Kennung außer der der neuen Fragen.
