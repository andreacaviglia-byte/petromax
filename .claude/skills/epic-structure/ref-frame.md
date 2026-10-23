# Die Fundament-Fragen: fragen, einordnen, fortschreiben

**`architecture.md` trägt den geltenden Stand der Architektur, eine Aussage je Zeile** (§216), mit den
Spalten `Aussage | Status | Quelle/ADR | gestützt von`. Das Fundament besteht aus vier Zeilen, die in jeder
Datei stehen: Shops, Bauform der Storefront, Integrationsschicht, Systemlandschaft. Du liest die
Datei, bevor du schneidest, und wartest nicht auf sie.

## Welche Frage fehlt

| Zeile des Fundaments | fehlt, wenn |
|---|---|
| Shops, Pläne, Markets oder Expansion Stores | `shops` in `project.yml` ist leer oder ein `plan` darin; die Werte gehören dem Steckbrief: du fragst nicht und trägst nichts ein, die Zeile bleibt `offen`, und der Bericht nennt `project-setup` zum Ergänzen |
| Bauform der Storefront | die Zeile ist `offen`, und `Quelle/ADR` ist leer |
| Integrationsschicht: ob, welche, wer betreibt | ebenso |
| Systemlandschaft: welche Systeme angebunden sind und welches führt | ebenso |

**Vor jeder Frage suchst du**, ob eine Anforderung, eine Frage in `gaps/` oder eine Notiz sie schon
beantwortet oder schon stellt. Steht sie schon als offene Frage in `gaps/`, fragst du nicht neu; du
trägst deren treibende Anforderung in `Quelle/ADR` ein, wenn die Zeile sie noch nicht nennt.

## Der Block

Eine Nachricht, alle fehlenden Fragen darin, je Frage ein Absatz: die Frage, was Repo und Notizen
dazu sagen, mit Kennung oder Dateiname, und die Anforderung, die sie nach deinem Urteil treibt. Dazu der
Satz: „Was du nicht beantworten kannst, bleibt offen; ich schneide trotzdem."

| Antwort des Leads | wird |
|---|---|
| ein Wert mit Quelle aus dem Material, oder vom Lead selbst gesagt | eine Zeile `belegt` in `architecture.md`, Quelle ist die Fundstelle. Sagt der Lead ihn selbst, ist sein Wortlaut Material (§287): die Notiz `notes/JJJJ-MM-TT-chat-‹thema›.md` nach dem Schema aus `${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, und sie ist die Quelle |
| eine Teilantwort, eine Vermutung, „gehen wir mal von … aus“ | die Frage bleibt offen, mit ihrem Text, wie er war; der Wortlaut des Leads steht nur in der Chat-Notiz. Einen Status „Annahme“ hat `architecture.md` nicht (§216), und eine Frage an den Kunden beantwortet der Lead nicht stellvertretend (§287) |
| offen, mit dem, der entscheidet | eine Architekturfrage in `gaps/` an der treibenden Anforderung (unten); die Zeile bleibt `offen` und nennt die Anforderung in `Quelle/ADR` |
| zwei Antworten, die sich widersprechen | die Zeile wird `widersprüchlich`, `Quelle/ADR` nennt beide Fundstellen und die Anforderung mit der Frage |
| offen, und keine Anforderung treibt die Frage | kein Eintrag; es fehlt eine Anforderung, die über `requirements-update` ins Repo kommt (§216) |

**Eine Entscheidung legst du nicht fest.** Was der Lead als entschieden nennt, ohne dass es eine ADR
gibt, ist eine Vorgabe mit Quelle: `belegt`, und sie braucht keine ADR. `entschieden` mit ADR schreibt
`solution-design` erst, wenn ein Epic dort an dieser Zeile etwas entscheidet (§216). Der Bericht
kündigt für eine `belegt`e Zeile deshalb keine ADR an.

## Fortschreiben

**Du schreibst `architecture.md` fort**, die ganze Datei, gebaut aus der gelesenen Fassung:

- Neue Zeilen stehen am Ende; gilt eine nur für einen Shop von mehreren, steht sein Schlüssel vorne,
  `b2b: …` (§231). Das gilt nur für Zeilen in `architecture.md`; Anforderung und ADR tragen den Bezug
  im Feld `shops` (§307).
- **Ein Wert zu einer Zeile des Fundaments** ersetzt ihre Aussage an ihrer Stelle (§231):
  `Bauform der Storefront: Theme`, mit Status und Quelle; `gestützt von` bleibt. Den alten Stand
  hält Git.
- **Die Zeile zu den Shops** bekommt keinen Wert in der Datei (§180): ist `shops` in `project.yml`
  gefüllt, mit `plan` je Shop, wird sie `belegt` mit `project.yml, shops` in `Quelle/ADR`, die
  Aussage bleibt.
- **Eine offene Frage** ändert nur `Quelle/ADR` der Zeile: die ID der treibenden Anforderung.
- `gestützt von` verliert keinen Eintrag; den trägt `solution-design` ein.

**Geprüft wird vor jedem Schreiben gegen die gelesene Fassung:** Kopf und Kopfzeile unverändert;
jede gelesene Zeile steht noch an ihrer Stelle, neue nur am Ende; ein Status ist einer der vier,
`belegt`, `entschieden`, `offen`, `widersprüchlich`; in `gestützt von` fehlt kein Eintrag, der
dastand. Hält die neue Fassung das nicht, wird sie nicht geschrieben.

**Ersetzt du eine Zeile, deren `gestützt von` Epics nennt**, markierst du jedes davon in seiner
Datei: `clarification` endet mit `Nachprüfen: ‹Datum›, Architektur „‹ersetzte Aussage›“` (`clar_recheck`,
bei `en` `Recheck: ‹Datum›, architecture “‹statement›”`; §216, §231, §337); du zeigst es im Plan und nennst die ersetzte Aussage im Commit.

## Die Frage in `gaps/`

**Die Architekturfrage ist eine Datei in `gaps/`** (§279), in der Form des
Datalayer-Vertrags `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
`gaps/GAP-NNN.md`, „Eine Frage anlegen“: `kind: decision`, `to` der, der entscheidet, als Rolle, `concerns` die treibende Anforderung zuerst, dann jede Anforderung und jedes
Epic, deren Lösung an der Frage hängt, `blocking: "yes"`, `opened` das Datum des Laufs. Der Rumpf
beginnt mit „Architektur: ‹Frage›“ (`question_frame`, bei `en` „Architecture: ‹question›“) und nennt, was Repo und Notizen dazu sagen. Die Kennung ist die nächste
freie, von der höchsten in `gaps/`.

Welche Anforderungen an der Frage hängen, ist dein Urteil, und der Lead sieht es im Plan. **Ihre Epics
tragen die Frage in `clarification`**: „‹GAP-…› offen“ (`clar_gap_open`, bei `en` „‹GAP-…› open“). Die
Wendungen stehen in der Sprache aus `language`, nach dem Abschnitt „Die festen Wendungen“ des
Datalayer-Vertrags (§337). Geschlossen wird die Frage nur über
`requirements-update`, aus Material (§276).
