# Der Umfang: worüber ein Lauf schreibt und berichtet

**Ein Lauf, der über eine Auswahl geht, läuft ohne Angabe nicht los, und der Umfang begrenzt, was er
schreibt und berichtet, nicht was er liest** (§215, §398, §402). Das gilt für `material-intake`,
`requirements-update`, `solution-approach`, `solution-design`, `solution-epic-page`,
`ticket-factory`, `requirements-review`, `solution-review` und `e2e-testing-sheet`. Was als Angabe
gilt, welche Antworten passen und welche empfohlen ist, sagt der Skill; hier stehen, wann du fragst,
die Form der Frage, wie mehrere Epics laufen und wie ein Review berichtet.

## 1. Nennt der Auftrag einen Umfang, fragst du nicht

Eine Angabe ist, was der Skill als Angabe nennt: Kennungen, ein Workstream, wie er in der Spalte
`Cluster` steht, ein Link, eine Datei, „alle“. Du nimmst sie, wie sie dasteht, und fragst nicht nach,
ob sie so gemeint ist. **Gibt es den genannten Workstream oder die Kennung nicht**, nennst du die
vorhandenen und fragst einmal.

## 2. Nennt er keinen, fragst du, mit den Antworten des Skills

Du nennst in einem Satz, was du gefunden hast, mit Zahlen, und dass einzelne Kennungen ins freie Feld
gehören, wo der Skill sie zulässt. Dann fragst du über `AskUserQuestion` in der Form der
Wurzel-`CLAUDE.md` (§392, §396):

- **Frage und Antworten sind die des Skills**, die Antworten kurz, die Zahl im Wortlaut, etwa
  „SHOP (12)“ oder „EP-003 (5 ohne Test)“. Wählt der Skill aus mehr Kandidaten, als Antworten
  passen, stehen die mit der größten Zahl zuerst, sonst die nach `solve_order`.
- **Mehrfachauswahl, wo der Skill sie nennt**: der Umfang ist dann alles Gewählte zusammen, und
  „Alle“ mit einer weiteren Antwort ist alle.
- **Eine Empfehlung nur, wo der Skill eine gibt**, mit „(Empfehlung)“ hinter der Antwort.
- **Trägt der Stand keine Auswahl**, etwa ohne Sheet keine Workstreams, sagt der Skill, ob du mit der
  einen Antwort fragst oder ohne Frage über alles läufst.

## 3. Geschrieben und berichtet wird im Umfang, gelesen darüber hinaus

Du liest, was eine Stelle im Umfang braucht, um zum Rest zu passen: die Liste über alle
Anforderungen, die Lösungsansätze der übrigen Epics, die Epics, durch die ein Prozess läuft.
**Geschrieben wird nur im Umfang.** Was aus dem Rest eine Stelle im Umfang berührt, steht im Bericht
gesondert, mit Kennung, Epic und `Owner Strix`; wohin ein Widerspruch zum Rest geht, eine Aufgabe in
`todo/` oder eine Notiz, sagt der Skill. Was an keiner Stelle hängt, etwa eine Summe über alle Epics,
prüft und berichtet nur der Lauf über alle (§305).

## 4. Mehrere Epics nacheinander, je mit eigenem Ja

Wo ein Skill Epics einzeln abarbeitet, `solution-design`, `solution-epic-page` und `ticket-factory`,
gehst du sie **nacheinander durch, in der Folge von `solve_order`**, ist es leer, nach der Nummer des
Epics: je Epic die Vorschau, die Frage
und das Schreiben nach [`ref-preview.md`](ref-preview.md), etwa „Soll ich die 14 Tickets für EP-003
so anlegen?“. Ein Ja über mehrere Epics gibt es nicht.

- **Nein** gilt dem einen Epic: du schreibst für es nichts und gehst zum nächsten; der Bericht nennt
  es.
- **Bricht die Sitzung ab**, bleibt stehen, was geschrieben ist. Der nächste Lauf beginnt beim ersten
  offenen Epic, das er im Stand findet, nicht in einer Liste im Chat.
- **Wird der Kontext knapp**, endest du nach einem Epic und nennst die übrigen als nächsten Lauf, in
  einer neuen Sitzung (§244).

## 5. Der Bericht eines Reviews

`requirements-review` und `solution-review` berichten in derselben Form, im Chat, nach der Regel für
Berichte (§397). Was je Sicht oder Prüfung in den Abschnitten steht, sagt der Skill.

```markdown
# ‹Requirements Review | Solution Review› ‹Vorhaben› — ‹Umfang›

Stand vom ‹TT.MM.JJJJ HH:MM›; Anforderungsliste gelesen am ‹TT.MM.JJJJ HH:MM Zeitzone› oder „keine Anforderungsliste“.
Gelesen: ‹was, mit Zahl›. Im Umfang: ‹Kennungen oder Workstreams›.

## Im Umfang
### ‹Sicht oder Prüfung›
‹Befunde mit Kennungen, oder „Kein Befund.“; was nur der Lauf über alle prüft: „Nur im Lauf über alle (§305).“›

## Aus dem Rest, berührt den Umfang
‹Befund, Stellen, Epic und Owner, von dem er kommt; oder „Kein Befund.“›

## Nicht geprüft
‹Kennung und Grund; oder „Alles gelesen.“›

## Fragen an den Lead
‹Frage mit der Stelle, an der sie entstand; oder „Keine.“›
```

**Ein Abschnitt ohne Befund trägt einen Satz**, nie nichts: ein leerer Bericht sieht aus wie einer, der
nicht lief. Ist der Umfang alle, entfällt „Aus dem Rest“. Die Tabellen bleiben im Chat; ins Repo gehen
daraus nur die Fragen und Aufgaben, die der Skill danach mit Vorschau und Ja anlegt.
