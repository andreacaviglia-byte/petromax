# Offene Fragen: an wen sie gehen und wie der Lead sie sieht

**Jede neue offene Frage steht vor dem Ja in einer Liste mit Adressat; einzeln fragst du den Lead nur
nach fester Regel** (§399). Das gilt für jeden Lauf, der offene Fragen anlegt: `requirements-update`,
`requirements-review`, `epic-structure`, `solution-design` und `solution-review`, auch für
die Punkte, die `grill-me` als `an den Kunden` zurückgibt. Wann eine offene Stelle eine Frage wird, sagt der Skill; die Form der
Datei setzt [`datalayer-contract.md`](datalayer-contract.md), Abschnitt `gaps/GAP-NNN.md`.

## 1. Der Adressat

`to` nennt, wer die Frage beantwortet, als Rolle: der Kunde (`to_customer`), eine Agentur oder ein
anderer Dienstleister des Kunden, etwa „Kunde, ERP-Betreuung“ oder „SEO-Agentur“. **Du nimmst ihn aus
dem Material**: wer dort für das Thema genannt ist, wer zugesagt hat, es zu klären, wessen System es
betrifft. Nennt kein Material einen, fragst du den Lead (3).

## 2. Die Liste in der Vorschau

Der Block **Offene Fragen** in der Vorschau ([`ref-preview.md`](ref-preview.md)) trägt je neue Frage
eine Zeile, die blockierenden zuerst: Kennung, die Anforderungen, die Frage und an wen sie geht.

```
Offene Fragen
- GAP-015, blockiert REQ-044: Welche Versandarten bietet das ERP je Markt an? – an Kunde, ERP-Betreuung
- GAP-016 zu REQ-051: Wie viele Rabattcodes sind gleichzeitig aktiv? – an Kunde
```

Eine Frage, die schon offen steht und nur eine weitere Anforderung bekommt, steht mit „wächst um
REQ-…“ in der Zeile. Der ganze Text jeder Frage folgt darunter, wo der Skill ihn verlangt.

**Der Lead liest die Liste und korrigiert nur, was nicht stimmt**: den Adressaten, ob sie blockiert,
den Wortlaut. Du übernimmst die Korrektur und zeigst die Vorschau neu. **Beantwortet er eine Frage
selbst**, entsteht sie nicht: sein Wortlaut wird eine Chat-Notiz `<JJJJ-MM-TT>-chat-<thema>.md` nach
[`inputs-and-notes-contract.md`](inputs-and-notes-contract.md), im Commit des Laufs. Sie ist Material
(§280, Regel 6): `requirements-update` gleicht sie im selben Lauf ab; jeder andere Lauf nennt im
Bericht `requirements-update` für sie.

## 3. Einzeln fragen, nur nach fester Regel

Bevor du die Vorschau zeigst, fragst du den Lead einzeln nach einer Frage, **wenn eines gilt**:

- **Kein Material nennt einen Adressaten** für ihr Thema.
- **Sie gilt einer Regel oder einem Ablauf beim Kunden**, wie er etwas heute handhabt oder handhaben
  will, etwa Preise, Rabatte, Versand, Retouren oder Freigaben; die kann der Lead aus einem Gespräch
  kennen.

Vorher stehen in der Nachricht die Frage, die Anforderung und der Adressat, den du vorschlägst. Dann
fragst du mit dem ersten Satz der Frage, ohne Empfehlung, mit drei Antworten, bis zu vier Fragen in
einem Aufruf (§396):

| Antwort | Folge |
|---|---|
| **Offene Frage** | sie entsteht, mit dem vorgeschlagenen Adressaten; ohne Vorschlag beginnt `to` mit `to_customer` |
| **Ich weiß es** | du bittest um die Antwort; sein Wortlaut wird eine Chat-Notiz wie in 2, und die Frage entsteht nicht |
| **Anderer Adressat** | du fragst, an wen; die Frage entsteht mit ihm in `to` |

**Jede andere Frage fragst du nicht einzeln**; sie steht nur in der Liste. Du lässt keine weg, weil du
meinst, der Lead kenne die Antwort, und beantwortest keine aus einer Annahme.
