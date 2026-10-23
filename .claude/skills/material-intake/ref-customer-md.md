# Die Kundensicht `customer.md`

`customer.md` ist die Sicht auf den Kunden über alle Quellen, ein Arbeitsstand, keine Faktenquelle.
Sie wird am Ende jedes Laufs ganz überschrieben, oder angelegt, wenn sie fehlt, mit diesem Kopf in
der ersten Zeile, wenn in `project.yml` `requirements_sheet` gesetzt ist:

```
Stand ‹TT.MM.JJJJ›. Arbeitsstand, keine Faktenquelle. Massgeblich sind `notes/` und `decisions/`.
```

Sonst, weil ohne das Add-on `solutioning` keine ADR entsteht und `decisions/` fehlen darf (Datalayer-Vertrag):

```
Stand ‹TT.MM.JJJJ›. Arbeitsstand, keine Faktenquelle. Massgeblich ist `notes/`.
```

## Was hineingehört

| Abschnitt | Inhalt |
|---|---|
| `## Ziele` | was der Kunde mit dem Shop erreichen will, je Ziel eine Zeile mit Quelle |
| `## Rahmenbedingungen` | Termine, Organisation, Märkte und Sprachen, wie das Material sie nennt, je mit Quelle |
| `## Systemlandschaft` | **nur, wenn es `architecture.md` nicht gibt**: die Systeme, die das Material nennt, nach den Regeln in `${CLAUDE_SKILL_DIR}/../../docs/system-landscape-contract.md` |

**Mit `architecture.md` steht die Systemlandschaft dort und nur dort** (§215, §216); dort trägt sie
`requirements-update` ein. Steht in `customer.md` noch ein Abschnitt `Systemlandschaft` und gibt es
inzwischen `architecture.md`, lässt du ihn Zeichen für Zeichen stehen und nennst ihn im Bericht: ihn
zu übertragen ist Arbeit von `requirements-update`.

**Nicht hinein** gehören Personen, ein Budget (§352), eine Liste der Anforderungen und der Plan eines
Shops: der steht in `project.yml`.

## Fortschreiben

- Der Text, den du direkt davor liest, ist die Grundlage. **Was dieser Lauf nicht berührt,
  bleibt Zeichen für Zeichen stehen**, auch ein Eintrag, den ein Mensch von Hand ergänzt hat.
- Eine neue Angabe ist eine neue Zeile unter ihrem Abschnitt, mit Quelle. Widerspricht sie einer
  bestehenden, bleiben beide stehen, und die neue nennt die alte: welche gilt, sagt die jüngere Quelle
  nur, wenn beide dieselbe Frage beantworten.
- Die Quelle ist der Dateiname der Notiz in `notes/`.
- Nur der Kopf bekommt das Datum dieses Laufs.
