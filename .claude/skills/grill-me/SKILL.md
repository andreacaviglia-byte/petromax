---
name: grill-me
description: 'Helfer im Solutioning: den Lead zu einer Liste von Befunden befragen, eine Frage nach der anderen, Abhängigkeiten zuerst, je Frage mit Empfehlung, und eine Tabelle zurückgeben (Punkt, Antwort, intern oder an den Kunden). Gerufen von solution-design, solution-review, skill-create, auch direkt. Nutze das bei "grill mich zu EP-003", "geh die Lösungsansätze mit mir durch", "welche Lösung gibt nach". Schreibt NICHTS ins Repo, stellt KEINE Fragen an den Kunden und ersetzt KEINE Working Session.'
---

Verträge: keine.

# Den Lead zu den Befunden befragen

Am Ende steht **eine Tabelle**, je Befund eine Zeile: Punkt, Antwort, `intern entschieden` oder `an
den Kunden` (§287). Sie geht an den Skill, der dich gerufen hat, bzw. an den Lead; **du schreibst
nichts**, keine Datei, kein Sheet, keinen Commit. Geschrieben wird vom aufrufenden Skill bzw. von
`requirements-update`.

**Du fragst nur, was der Lead bzw. der Owner selbst entscheidet:** das Vorgehen, eine Empfehlung,
welche Lösung bei einem Konflikt nachgibt. Eine Frage, die nur der Kunde oder ein Dritter beantworten
kann, stellst du dem Lead nicht als Frage; sie wird `an den Kunden`, mit Adressat, und später eine
offene Frage in `gaps/`, mit `blocking: yes`, wenn die Lösung daran hängt. **Du sortierst sie nicht
still aus**: sie steht in der Tabelle, und der aufrufende Lauf zeigt sie vor seinem Ja in der Liste
der offenen Fragen, wo der Lead Adressat und Wortlaut korrigiert (§399). Der Lead beantwortet sie nicht stellvertretend. Kennt er die
Antwort aus einem Gespräch, gehört das Gespräch als Material ins Repo (`material-intake`), und die
Zeile bleibt `an den Kunden`.

**Wo du läufst, sagt `way-of-working.md`, Abschnitt „grill-me“** (§286, §287): im Standard im
Solutioning, in `solution-design` und `solution-review`, und in `skill-create` beim Klären eines
eigenen Skills (§290). Ein Projekt kann das mit einer Abweichung
ändern; dann gilt die Abweichung. Eine Working Session mit dem Kunden ersetzt du nicht.

### Step 1 — Die Liste der Befunde nehmen

**Gerufen von einem Skill** bekommst du von ihm die Liste der Befunde: je Punkt die Anforderung oder
das Epic, die Frage, seine Empfehlung mit Grund und was die Antwort ändert. Der aufrufende Skill hat
schon analysiert und den Stand gezogen; du liest nichts nach und hinterfragst nicht, was im Repo
erfasst oder schon klar ist.

**Direkt gerufen** ziehst du zuerst den Stand von `main` (`python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`; endet es
nicht mit Exit 0, nenne die Meldung wörtlich und halte an) und fragst den Lead, worum es geht: welches Epic, welche
Anforderungen, welche Stelle. Dann liest du nur deren Dateien in `requirements/` und `epics/`, die
offenen Fragen in `gaps/`, die sie nennen, und die Zeilen in `architecture.md`, auf die sie bauen,
und schreibst dir die Liste selbst, in derselben Form. Was dort schon entschieden oder als Frage
offen ist, kommt nicht auf die Liste.

### Step 2 — Ordnen

1. **Abhängigkeiten zuerst:** hängt die Antwort auf B an der auf A, kommt A vor B. Fällt mit einer
   Antwort eine spätere Frage weg, stellst du sie nicht.
2. **Fragen an andere mit Adressat festhalten.** Braucht ein Punkt eine Auskunft, die nur der Kunde
   oder ein Dritter hat, bekommt er `an den Kunden`, ohne Frage an den Lead, mit dem Satz, warum, und
   dem Adressaten, wie das Material ihn nennt: Kunde, Agentur oder ein anderer Dienstleister.
3. **Was bleibt, sind Fragen an den Lead**, je Punkt eine.

### Step 3 — Fragen, eine nach der anderen

Je Frage ein kurzer Block, und dann wartest du auf die Antwort:

```
‹n› von ‹gesamt› — ‹REQ-012 bzw. EP-003›: ‹die Frage›
a) ‹Möglichkeit› b) ‹Möglichkeit› c) Offene Frage
Empfehlung: ‹Möglichkeit›, weil ‹Grund›.
Die Antwort ändert: ‹was danach anders ist›.
```

**Die letzte Antwort heißt immer „Offene Frage“** (englisch „Open question“), in `AskUserQuestion`
wie im Chat. Wählt der Lead sie, wird der Punkt `an den Kunden`; an wen die Frage geht, Kunde,
Agentur oder ein anderer Dienstleister, steht in `Antwort` und später im Feld `to` der offenen Frage.

- **Eine Frage je Nachricht.** Ein Block mit fünf Fragen bekommt fünf halbe Antworten.
- **Die Empfehlung ist Pflicht.** Ohne sie wird der Lead zum Rechercheur.
- Antwortet der Lead mit „überspringen“, bleibt der Punkt offen und steht so in der Tabelle; mit
  „stopp“ endest du und gibst die Tabelle mit dem Stand zurück, die übrigen Punkte offen.
- **Sagt eine Antwort, dass der Kunde entscheiden muss**, wird der Punkt `an den Kunden`, ohne
  Nachfrage.
- **Ist eine Antwort unklar oder widerspricht sie einer früheren**, fragst du genau einmal nach und
  nennst beide Stellen.
- Bringt eine Antwort einen neuen Punkt auf, der zu den Befunden gehört, hängst du ihn hinten an
  und sagst das.

### Step 4 — Die Tabelle zurückgeben

```
| Punkt | Antwort | Art |
|---|---|---|
| REQ-012: Bundles über App oder eigene Logik | App, weil … | intern entschieden |
| REQ-031: Obergrenze für Gutscheine | Gilt eine Obergrenze je Bestellung? – an Kunde | an den Kunden |
| REQ-020: Edge Case Teillieferung | übersprungen | offen |
```

`Art` ist `intern entschieden`, `an den Kunden` oder `offen` (übersprungen oder nach „stopp“ nicht
gefragt). Bei `an den Kunden` steht in `Antwort` die Frage, wie sie hinausgeht, in einem Satz, und
dahinter, an wen: „– an Kunde“, „– an SEO-Agentur“.

Gerufen von einem Skill, endest du mit der Tabelle; er macht weiter. Direkt gerufen, nennst du
danach, wer schreibt: `intern entschieden` hält der Skill fest, aus dem der Punkt stammt (meist
`solution-design` bzw. `solution-review`), `an den Kunden` wird über diesen Skill oder
`requirements-update` eine Frage in `gaps/`; jeweils „in einer neuen Sitzung“.

## Was dieser Lauf nicht tut

Er schreibt keine Datei und nichts nach außen, legt keine Frage in `gaps/` an, ruft keinen anderen
Skill und stellt dem Kunden keine Frage. Er läuft nicht in Discovery, `material-intake`,
`requirements-review`, `solution-approach`, `epic-structure`, `solution-critical-path`,
`ticket-factory`, `solution-estimate` oder `solution-proposal`, solange `way-of-working.md` es nicht
anders sagt.
