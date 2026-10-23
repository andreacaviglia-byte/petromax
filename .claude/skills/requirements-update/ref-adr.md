# Eine Entscheidung aus dem Material anlegen

**Dieser Lauf hält fest, was das Material als entschieden nennt**, in jedem Material: im Kickoff, im
Call zum Proposal, in der Mail zur Req Page. **Jede Entscheidung bekommt eine ADR**, auch eine, die
genau eine Anforderung bindet; die Anforderung trägt dazu ihre `## Description`.

**Jede Ausklammerung ist eine Entscheidung und bekommt eine ADR**: `status: rejected` oder
`scope: out_of_scope`, auch eine Rücknahme. Die Frage ist, ob die Anforderung gilt oder in diesen Scope
gehört; verworfen ist der andere Stand; der Grund ist der aus dem Material. Holt eine Rücknahme eine
Anforderung zurück, trägt ihre ADR `supersedes` auf die der Ausklammerung.

**Die Gegenprobe hält das ehrlich:** sagt das Material die Entscheidung nicht, entsteht keine ADR,
sondern eine Frage in `gaps/` ([ref-questions.md](ref-questions.md)).

## Die Datei

In `decisions/` des Datalayers, flach, Name `ADR-<NNN>-<slug>.md`. Die Nummer
zählt von der höchsten `ADR-`, die die Liste von `decisions/` nennt. Du legst die Datei an und
überschreibst sie nie.

```
---
id: ADR-004
title: <Titel>
status: accepted
---

Frage: …
Entscheidung: … (Workshop ‹Titel› vom ‹Datum›)
Verworfen: … und warum
Betrifft: REQ-012, REQ-031
```

Die Quelle in Klammern ist die Wendung `source_workshop` oder `source_chat` in der Sprache aus
`language`, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen
Wendungen“ (§337); bei `en` „(Workshop ‹title› on ‹date›)“.

Gilt die Entscheidung nicht für alle Shops, trägt der Kopf dazu `shops` mit den Schlüsseln der Shops, `shops: [b2b]`; der Titel trägt keinen Schlüssel (§307).

**Dieser Lauf schreibt `accepted` oder nichts.** `proposed` ist der Status des Entwurfs in
`solution-design`. Löst die Entscheidung eine frühere ab, trägt die neue `supersedes: ADR-00N`, und in
der alten ADR änderst du nur die Zeile `status:`, auf `superseded`; der übrige Text bleibt Zeichen
für Zeichen. Das ist die einzige Änderung an einer bestehenden ADR.

## Die verworfene Alternative gehört dazu

Der Rumpf sagt die Frage, die Entscheidung und die Alternative, die nicht genommen wurde. Bei einer
Ausklammerung ist das immer der Umfang, den sie nicht hat. Findet sich sonst in keiner Quelle eine
Alternative, lag vermutlich keine Wahl vor, sondern eine Feststellung, und dann entsteht
keine ADR: „X ist im Einsatz und ist unser CRM" beschreibt, was da ist, und gehört als `belegt` in die
Systemlandschaft (`${CLAUDE_SKILL_DIR}/../../docs/system-landscape-contract.md`).

## Eine Entscheidung, kein Sammeleintrag

Je Wahl eine ADR. „Newsletter-Werkzeug und Zahlungsdienstleister werden abgelöst" sind zwei: zwei
Quellen, zwei verworfene Alternativen, getrennt zurückzunehmen. **Umgekehrt ist eine Wahl, die zehn
Systeme bindet, eine ADR**; der Schnitt läuft an der Wahl, nicht an der Zahl der Betroffenen. Unter
`Betrifft` steht die ganze gebundene Menge, nicht nur die laut genannte: zählt der Termin vier
Beispiele auf, wo das Papier acht führt, löst du die Menge an der Aufzählung auf, auf die sich die
Entscheidung bezieht.

Das Datum der Entscheidung ist das der Quelle, nicht das von heute.

## Was nach der ADR folgt

- **Beantwortet sie eine offene Frage**, wird die Frage geschlossen, und ihre Antwort nennt die ADR:
  `… (‹Quelle›), ADR-‹NNN›` ([ref-questions.md](ref-questions.md)).
- **Betrifft sie eine Zeile in `architecture.md`**, wechselt die Zeile auf `entschieden` und
  `Quelle/ADR` nennt die ADR ([ref-architecture.md](ref-architecture.md)).
- **Ist sie eine Ausklammerung**, trägt die Anforderung `status: rejected` oder `scope: out_of_scope`;
  den Grund trägt die ADR, nicht die Anforderung.

Die ADR legst du erst nach dem Ja an, mit der Nummer, die du im Block gezeigt hast. Ist die Nummer
inzwischen vergeben, nimmst du die nächste freie und nennst die Änderung im Bericht.
