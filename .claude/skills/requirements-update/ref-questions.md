# Wann eine offene Stelle eine Frage wird, und wie sie in `gaps/` steht und geschlossen wird

**Lies das ungekürzte Material noch einmal auf das hin, was nicht dasteht:** auf die Angabe, die ein
späterer Lauf verlangen wird, an den neuen Anforderungen und an denen, die schon stehen. Nicht
abhaken, durchdenken.

## Fünf Sichten

| Sicht | Die Frage, die sie stellt |
|---|---|
| **Menge und Grenze** | die Zahl, die niemand nennt und jeder annimmt: wie viele Kundengruppen, Produkte, Optionswerte, wie oft am Tag. Die Größe der Lösung hängt daran |
| **Der Fehlerfall** | was passiert, wenn es schiefgeht, und wer es merkt. Er kommt im Gespräch nie vor und in der Umsetzung immer |
| **Der Rand** | was ausdrücklich **nicht** dazugehört. Gefragt wird er, solange beide Seiten einverstanden sind |
| **Die andere Seite des Ladentischs** | merkt der Kunde des Shops etwas, das der Betreiber nicht gemeint hat, oder umgekehrt |
| **Der Entwurf** | was der Entwurf je Anforderung brauchen wird: welche Einstellung an welchem Shop, welche Ansicht mit welcher Design-Referenz, welche Felder in welcher Richtung mit welchem Auslöser. Sie hängt an keiner Ebene und legt keinen Lösungsansatz fest. Ob der Plan eine Einstellung hergibt, wird nachgeschlagen, nicht gefragt |

Die vierte Sicht bringt oft einen Kandidaten statt einer Frage; der geht zurück in Step 6. **Mehr als
zwei Durchgänge gibt es nicht**: der dritte erfindet Anforderungen, statt sie zu finden.

## Vier Prüfsteine, alle bestanden, sonst keine Frage

1. **Ändert die Antwort etwas Späteres?** Die Anforderung, den Scope, den Lösungsansatz im Entwurf, die
   Schätzung. Sonst ist sie Neugier, und wer zwanzig Fragen bekommt, beantwortet die ersten fünf.
2. **Wer kann sie beantworten?** Ohne Adressat ist sie eine Klage. Was im Haus zu beantworten ist,
   wird im Haus beantwortet.
3. **Beantwortet die Dokumentation sie?** Dann ist sie Lesearbeit für `solution-design`. Es gibt keine
   API-Version des Shops, die wählt der Aufrufer; gefragt wird nur, welche ein fremdes System anspricht.
   Ob der Plan eine Einstellung hergibt, schlägst du über die Doku-Wege aus `${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md` nach (§340); bleibt es offen,
   wird es eine Frage.
4. **Ist sie schon beantwortet?** Vor jeder neuen Frage suchst du in den Notizen in `notes/`, in
   `decisions/` und in `gaps/`, auch unter `## Answer` geschlossener Fragen (§215). Steht die Antwort
   dort, ist sie keine Frage, sondern eine Antwort mit dieser Quelle. Steht dieselbe Frage schon offen
   da, legst du sie nicht noch einmal an; betrifft sie eine weitere Anforderung, wächst ihr `concerns`.

Zwei Quellen, die Verschiedenes sagen, ohne dass eine sicher die jüngere ist, sind eine Frage, keine
Korrektur.

## Die Frage in `gaps/`

**Je Frage eine Datei `gaps/GAP-NNN.md`** (§279). Form und Felder setzt der Datalayer-Vertrag,
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt `gaps/GAP-NNN.md`, „Eine Frage
anlegen“; dieser Lauf stellt Fragen der Art `discovery` und `decision`, das Datum in `opened` ist das
dieses Laufs. `to` nimmst du aus dem Material, nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-open-questions.md`, 1; bei einer Frage an den Kunden beginnt es
mit `Kunde` (`to_customer`, `en`: `Customer, ERP support`). Rumpf und feste Wendungen stehen in der Sprache aus `language`, nach dem Abschnitt „Die
festen Wendungen“ desselben Vertrags (§337):

```markdown
---
id: GAP-014
kind: discovery
to: Kunde, ERP-Betreuung
concerns: [REQ-044, REQ-047]
blocking: no
status: open
opened: 2026-10-10
---

Welche Versandarten bietet das ERP je Markt an? Gemeint sind Standard und Express; die Antwort bestimmt die Kriterien von REQ-044.
```

**Eine Frage zur Lösung oder zur Architektur stellst du nicht.** Sie gehört an die treibende Anforderung,
und sie stellen `epic-structure` und `solution-design`; du nennst sie in der Notiz und im Bericht.
Ausgenommen ist ein Widerspruch in `architecture.md`: den findest du, und du legst die Frage dazu an
([ref-architecture.md](ref-architecture.md)).

## Frage an den Kunden oder Aufgabe bei uns

**Was der Kunde oder ein Dritter auf seiner Seite klären muss, ist eine Frage in `gaps/`; was jemand
bei uns tun muss, ist eine Aufgabe in `todo/`** (§279, §359), angelegt nach
`${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`. Eine Absprache aus dem Material, eine Zusage des Leads,
eine Klärung im Haus aus Prüfstein 2 wird eine Aufgabe.

| Im Material | wird |
|---|---|
| „Welche Felder die Warenwirtschaft für Händlerkunden braucht, klärt der Dienstleister des Kunden bis 10.10.“ | eine Frage in `gaps/`, `to: Kunde, ERP-Dienstleister`, die Frist als Satz im Rumpf |
| „Lead: Ich schicke euch die Anforderungsliste zur Durchsicht.“ | eine Aufgabe in `todo/` an den Lead, mit der Stelle als Quelle |

## Eine Frage schließen

**Geschlossen wird eine Frage nur aus Material**, das sie **ausdrücklich** beantwortet, auch eine
Frage, die ein anderer Lauf angelegt hat (§276, §279). Nie durch einen Eintrag im Sheet, auch nicht
durch einen des Leads: kennt er die Antwort aus einem Gespräch, ist sein Wortlaut im Chat das Material.

Du setzt `status: closed` und hängst unter den Rumpf an:

```markdown
## Answer

Standard und Express in allen Märkten, Express nur bis 14 Uhr. (Workshop Versand vom 02.10.2026)
```

in einem bis zwei Sätzen wie im Material, mit der Quelle in Klammern, als Wendung `source_workshop` oder
`source_chat` in der Sprache aus `language`; die Frage bleibt stehen. Steht
schon eine Antwort, die dasselbe sagt, schreibst du nichts; sagt sie anderes, schreibst du nichts und
meldest den Widerspruch. **Eine Teilantwort schließt nichts**; sie steht mit Zeitstempel in der Notiz.

**Ist die Antwort eine Entscheidung** mit einer Alternative, die nicht genommen wurde, entsteht dazu die ADR,
und die Antwort nennt sie (`… (Workshop … vom …), ADR-008`; [ref-adr.md](ref-adr.md)). Betrifft sie
eine Zeile in `architecture.md`, wechselt die Zeile auf `entschieden`
([ref-architecture.md](ref-architecture.md)).

Was aus der Antwort für die Lösung folgt, entscheidet `solution-design`. Ändert sie die Anforderung
selbst, ist das zusätzlich eine Korrektur ([ref-requirement.md](ref-requirement.md)). Mit dem Schließen
fällt die Frage aus den Spalten der Fragen und samt ihrer Zeile aus `Offene Punkte`; das tut die
Projektion.
