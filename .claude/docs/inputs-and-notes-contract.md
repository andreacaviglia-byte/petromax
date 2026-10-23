# Material und Notiz: `inputs/` und `notes/`

**Dieser Vertrag setzt die Form von Material und Notiz** (§325): `material-intake` legt Material in
`inputs/` ab und schreibt je Quelle die Notiz, `requirements-update` und `epic-structure`
legen die Notiz einer Eingabe des Leads im Chat an, `solution-approach` und `solution-design` die
Notiz einer Runde, und jeder Lauf, der für Kunde oder Dritte
schreibt, liest an `Intern: ja` und `## Intern`, was nicht nach außen geht.

`inputs/` trägt das Fremde als Text, `notes/` unsere Auslegung. **Fakt und Auslegung
stehen nie in derselben Datei:** nur so bleibt nachlesbar, ob eine Anforderung im Material stand oder
in unserer Lesart entstand.

## Das Material bleibt, wie es ist

**Das Rohe wird nicht gekürzt und nicht geglättet, auch nicht um die Namen der Menschen beim
Auftraggeber** (§228, §236). Ein Transkript
bleibt im Zeilenformat mit Zeitstempel, eine Zeile je Beitrag: `[hh:mm:ss] Sprecher: Text`. Hat die
Vorlage ein anderes Zeilenformat mit Zeitstempel, bleibt es. Widersprüche und Versprecher bleiben, auch ein offensichtlich falsch
erkanntes Wort; aufgelöst wird es in der Notiz. **Was als Binärdatei kommt**, PDF, Office, Folien,
wird Text; was sich nicht überführen lässt, wird benannt und nicht ersetzt.

**Drei Sorten Daten gehen trotzdem nicht ins Material** (§236): du ersetzt sie vor der Ablage,
wörtlich durch den Platzhalter der Sorte, in der Sprache aus `language`
([Die festen Wendungen](datalayer-contract.md#die-festen-wendungen), §337).

| Sorte | Platzhalter |
|---|---|
| Zugangsdaten jeder Art: Passwort, API-Key, Secret, Token, Schlüssel, ein Endpunkt, der eines trägt (§227) | „‹Zugangsdatum entfernt›", bei `en` „‹credential removed›" |
| Gesundheitsdaten und die übrigen Daten nach Art. 9 DSGVO über erkennbare Menschen | „‹Gesundheitsdaten entfernt›", bei `en` „‹health data removed›" |
| Daten der Endkunden des Auftraggebers, der Menschen, die in seinem Shop kaufen: Namen, Adressen, Mail-Adressen, Telefonnummern, Bestellungen und Kundenkonten, die einem Menschen zuzuordnen sind | „‹Endkundendaten entfernt›", bei `en` „‹end-customer data removed›" |

**Struktur und Zweck bleiben, nur der Wert geht**: Spaltenköpfe, Anzahl der Zeilen, was eine Angabe
belegen sollte. Du sagst vor der Ablage an, was du ersetzt hast. Welcher Zugang für welches System
gebraucht wird, ist Inhalt. Eine Anforderung über eine Produktgruppe, etwa rezeptpflichtige Artikel,
ist keine Angabe über einen Menschen und bleibt. Namen, Rollen und Mail-Adressen der Menschen beim
Auftraggeber bleiben.

## Dateiname

`<JJJJ-MM-TT>-<slug>.md`, das Datum ist das des Termins oder Dokuments, der Slug klein, kebab-case, aus
dem Titel. Die Notiz trägt denselben Namen in `notes/`. Eine Datei mit mehreren Terminen wird vor
der Ablage getrennt, nach der Prüfung aus Step 5 von `material-intake`; jeder Termin bekommt seine Datei. Ein Jira-Ticket
heißt `<JJJJ-MM-TT>-<schlüssel>.md` mit dem Datum des Lesens, weil es ein Abzug ist.

Der Kopf einer Datei in `inputs/`:

```
Quelle: Workshop ‹Titel› vom ‹TT.MM.JJJJ›
Herkunft: ‹Dateiname im Projektordner›
Abgelegt: ‹TT.MM.JJJJ›
Intern: ja
```

Die Zeile `Intern: ja` steht nur bei einer internen Quelle (unten); sonst fehlt sie.

## Interne Quellen

**Interne Inhalte gehen nie nach außen, auch nicht sinngemäß** (§278). Damit jeder spätere Lauf das
sieht, ohne die Quelle neu zu beurteilen, markierst du beim Ablegen:

- **Eine ganze Quelle ist intern**, wenn sie ein internes Gespräch oder eine interne Übergabe
  festhält: Transkript oder Notiz eines Termins ohne den Kunden, eine Übergabe, das
  Pre-Sales-Briefing. Ihre Datei in `inputs/` und ihre Notiz tragen im Kopf `Intern: ja`.
- **Eine Quelle mit internen Stellen**, etwa ein Kundentermin mit einem Nachgespräch ohne den Kunden
  oder eine Mail mit einem Absatz nur für uns, bleibt in `inputs/`, wie sie ist. Die Notiz führt
  diese Stellen unter `## Intern`, mit Zeitstempel oder Abschnitt, und nicht unter den übrigen
  Abschnitten.

Was als intern gilt, steht in `way-of-working.md`, Abschnitt „Interna“: Preisfindung und
Verhandlungstaktik, Budgetpuffer, Einschätzungen zu Kunde und Personen, Potenzial für
Folgeaufträge, saloppe Formulierungen und Zitate aus internen Gesprächen. **Eine Anforderung, die
nur in einer internen Quelle steht, ist trotzdem Material**: `requirements-update` nimmt sie auf, in
sachlichen Worten, und nennt die interne Quelle nirgends, wo Kunde oder Dritte lesen.

## Die Notiz

Eine Notiz je Quelle, neu angelegt, nie überschrieben. **Sie sagt, was die Quelle berührt, ohne
REQ-Nummern** (§209): die Zuordnung zu Anforderungen ist Arbeit von `requirements-update` (§282). Sie
trägt:

```
Quelle: ‹wie im Kopf der Datei in inputs/›
Gelesen: ‹TT.MM.JJJJ›, vollständig | gekappt bei ‹Stelle›
Intern: ja

## Berührt
- ‹Thema›: was gewünscht wird, mit Zeitstempel oder Abschnitt
## Heute
- ‹Thema›: was über den heutigen Shop oder ein System gesagt wird
## Entschieden oder ausgeklammert
- ‹Wahl›, die Alternative, die nicht genommen wurde, und wer entschied, mit Zeitstempel
## Offen
- eine Tendenz, eine Teilantwort, ein „klären wir intern", mit Zeitstempel
## Systeme
- ‹name›: wie das Material es nennt, jede Variante der Schreibweise
## Aufgelöst
- was eine maschinelle Mitschrift falsch erkannt hat und wofür es steht, je Vorkommen
## Intern
- eine interne Stelle einer Quelle, die sonst nicht intern ist, mit Zeitstempel oder Abschnitt
```

`Intern: ja` steht wie in `inputs/` nur bei einer internen Quelle; dann gibt es keinen Abschnitt
`Intern`, denn die ganze Notiz ist es. Ein Abschnitt ohne Inhalt fällt weg. **Was die Quelle nur andeutet, steht unter `Offen`, nicht unter
`Berührt`**: aus einer Tendenz macht kein späterer Lauf eine Anforderung. Eine Messung trägt ihr
Datum, ein Eintrag seinen Grund. **Was dem Werkzeug gilt statt dem Kunden**, etwa ein Aufruf, der
scheiterte, gehört in den Bericht, nicht in die Notiz.

Bei einer Eingabe des Leads im Chat heißt die Notiz `<JJJJ-MM-TT>-chat-<thema>.md` und trägt seinen
Wortlaut, die drei Sorten oben ersetzt. **Dieses Schema gilt für jedes Material aus dem Chat**, in `inputs/` wie
in `notes/` und in jedem Skill: das Datum des Laufs in ISO-Form, das Thema klein und kebab-case, in
wenigen Wörtern (`2026-09-30-chat-roesttag-hinweis.md`). Steht der Name am selben Tag schon, bekommt
die neue Datei `-2` vor der Endung, die nächste `-3`; eine stehende wird nie überschrieben, außer
der Notiz einer Runde, unten.

## Die Notiz einer Runde

**`solution-approach` und `solution-design` halten die Antworten des Leads nach jeder Runde im Repo
fest, vor dem Ja** (§401): eine Runde ist ein Aufruf mit bis zu vier Fragen oder eine Antwort in
Worten. Endet die Sitzung vor dem Ja, sind die Antworten sonst verloren. Es ist eine Chat-Notiz nach
dem Schema oben, **eine je Sitzung und Epic**, bei `solution-approach` eine je Sitzung:
`<JJJJ-MM-TT>-chat-loesung-ep-003.md`, `<JJJJ-MM-TT>-chat-loesungsansatz.md`. Dieselbe Sitzung
schreibt sie nach jeder Runde fort; eine andere Sitzung legt eine neue an.

```
Quelle: Chat mit dem Lead vom ‹TT.MM.JJJJ›
Lauf: ‹solution-approach | solution-design EP-NNN›
Lead: ‹GitHub-Name›
Stand: offen
Fortgesetzt aus: ‹Dateiname der Notiz der abgebrochenen Sitzung›

## Antworten
- ‹Kennung›: ‹Frage› – ‹Antwort, wörtlich›
```

- **`Lead:`** ist der GitHub-Name aus `python3 .claude/scripts/wow-guard.py --whoami`; endet der
  Aufruf mit Exit 1, steht dort `unbekannt`.
- **Nach jeder Runde** schreibst du die Notiz, committest nur sie, mit der Nachricht
  `‹Skill›: Antworten ‹Umfang›`, und pushst. Anforderungen, Epics und Entwurf ändern sich erst nach
  dem Ja. Im Commit des Laufs steht `Stand: abgeschlossen`; endet der Lauf mit Nein, ebenso.
- **Beantwortet der Lead eine offene Frage selbst** ([`ref-open-questions.md`](ref-open-questions.md),
  2), steht sein Wortlaut hier; eine zweite Chat-Notiz entsteht nicht. Eine Antwort zum Was ist
  Material für `requirements-update` (§280, Regel 6), und der Bericht nennt den Lauf.
- **Ein Lauf, der nach einer abgebrochenen Sitzung beginnt**, sucht in `notes/` die Notiz seines
  Laufs mit `Stand: offen`, die keine spätere in `Fortgesetzt aus` nennt. Findet er eine, nennt er
  dem Lead ihr Datum und `Lead:`, übernimmt ihre Antworten, statt neu zu fragen, und schreibt seine
  Notiz mit `Fortgesetzt aus:`; die alte bleibt, wie sie ist. Ohne Vorgängerin fällt die Zeile weg.

## Wegweiser

Ist eine Notiz falsch, bleibt ihr Text. Über die erste Zeile der Notiz kommt genau eine Zeile
Wegweiser, „Überholt durch ‹Dateiname der neuen Notiz›, ‹TT.MM.JJJJ›."; der alte Text folgt Zeichen
für Zeichen. Die neue Notiz nennt die alte und was an ihr falsch war.
