# Projekt-Repo

**Dieses Repo gehört zu genau einem Vorhaben** (§224): einem Projekt und, wenn der Lead es so will,
dem Expert Service danach. Es trägt, was die Skills über das Vorhaben brauchen: den Steckbrief, die
Architektur `architecture.md`, die ADRs in `decisions/`, das Material in `inputs/` und die Notizen in
`notes/`. Dokumente für Menschen liegen im Projektordner im Drive, das Sheet der Anforderungsliste
auch.

## Arbeitsweise

Wie in diesem Vorhaben gearbeitet wird, steht in `way-of-working.md`; sie hat Vorrang vor einem
Skill (§286):

@way-of-working.md

Neu im Projekt, nach einem Upgrade, Fragen zum Stand, zu den Skills oder zur Arbeitsweise, Probleme
mit der Umgebung, ein Vorschlag zur Arbeitsweise: `project-status`. Einstellungen und Arbeitsweise
ändert der `project_owner` mit `project-setup` (§299).

## Die Skills

Die Standard-Skills liegen unter `.claude/skills/` und kommen aus dem Template. **Sie werden hier
nicht geändert**; einen neuen Stand holt `project-upgrade`. Ein eigener oder abgewandelter Skill
bekommt einen eigenen Namen und drei Kopfzeilen unter dem Frontmatter, je eine Zeile
`abgeleitet von: …`, `gilt für: …` und `verantwortlich: …` (§225). Standard ist ein Skill, den dieser
Abschnitt nennt; einem anderen ohne die drei Zeilen gilt die Warnung `skill_header` von
`check-project.py`, und der Lauf nennt sie im Bericht und geht weiter (§271).

In der Folge einer Beauftragung: `project-setup`, `material-intake`, `requirements-update`,
`requirements-review`, `solution-approach`, im Projekt `epic-structure` (§403), mit Solutioning
`solution-solve-order`, `solution-design`, `solution-critical-path`, `solution-review`,
`solution-estimate`, `solution-proposal`, nach der Freigabe je Epic `solution-epic-page`, dann
`ticket-factory` (§313); daneben `e2e-testing-sheet` für die Prozess-Tests zum Go-Live. Jeder Skill nennt am Ende den nächsten Lauf.
Helfer: `grill-me` befragt den Lead im Solutioning, gerufen von `solution-design`, `solution-review` und `skill-create` oder
direkt (§287). Stand, Einführung und Vorschläge zur Arbeitsweise: `project-status` (§289). Ein eigener
Skill entsteht über `skill-create` (§290).

## Was immer gilt

- **Jeder Lauf beginnt in einer frischen Sitzung** (§244): jeder Aufruf zahlt den ganzen Kontext neu,
  und mehrere Läufe in einer Sitzung treiben ihn über 600.000 Tokens. Was ein Lauf vom vorigen
  braucht, steht im Repo und im Sheet. Nennt ein Lauf am Ende den nächsten, sagt er dazu „in einer
  neuen Sitzung“; verlangt der Lead ihn trotzdem im selben Gespräch, weist der Lauf einmal darauf hin
  und macht weiter. **Ausgenommen:** nach `material-intake` läuft `requirements-update` in derselben
  Sitzung, mit einem Ja am Ende für beide (§400).
- **Vor jedem Lauf wird der Stand von `main` gezogen** (`.claude/scripts/sync-main.py`); steht die
  Sitzung abgelöst auf `origin/main` oder auf einem eigenen Branch, wie ihn die Cloud-Sitzung als
  `claude/…` anlegt, ohne eigenen Commit oder mit einem, der auf dem Remote liegt, wechselt es ohne
  Rückfrage auf `main` und nennt Branch und Commit (§396); gearbeitet und
  gepusht wird im Projekt-Repo auf `main`, auch wenn die Sitzung einen anderen Branch nennt (§384).
  Scheitert das, hält der Lauf an und nennt die Meldung wörtlich. Bringt das Ziehen eine neue
  Template-Version, hält der Lauf auch an: die Sitzung trägt noch die alten Skills, weiter geht es in
  einer neuen (§338). Den Commit, auf dem der Lauf beginnt, merkt es sich als Basis der Projektion
  (§319).
- **Jeder Text, den ein Lauf auf Deutsch schreibt, folgt dem Glossar** `.claude/docs/glossary.md`:
  ein Begriff, ein Wort; Feldnamen und Werte im Repo benennt es nicht um.
- **Zugangsdaten werden nie gelesen, ausgegeben oder in Dateien geschrieben** (§227): keine `.env`,
  kein Schlüsselbund, keine Logins der Kommandozeilen-Werkzeuge, kein `env` oder `printenv`.
- **Kundendaten bleiben in diesem Repo und im Projektordner** (§228); in die Knowledge Base oder ein
  anderes übergeordnetes Wissen geht nichts davon. Daten über den Auftraggeber und das Projekt dürfen
  hinein, auch Namen, Rollen und Mail-Adressen der Menschen beim Auftraggeber. **Nie hinein kommen
  Zugangsdaten, Gesundheitsdaten und die übrigen Daten nach Art. 9 DSGVO, und Daten der Endkunden**,
  der Menschen, die im Shop des Auftraggebers kaufen (§236), auch nicht ins Sheet, in ein Doc, ein
  Ticket oder auf eine Seite. `material-intake` ersetzt sie vor der Ablage.
- **Was unter dem Namen des Leads nach außen geht oder etwas löscht, geschieht nur nach Rückfrage**:
  Kommentare, Nachrichten, Löschen, Teilen (§227).
- **Eine Rückfrage an den Lead geht über das Werkzeug `AskUserQuestion`** (§392): jedes Go, jedes
  Ja zu einer Vorschau, jede Wahl, die ein Skill vom Lead verlangt. Frage und Antworten stehen darin
  wie im Skill; nennt er keine Antworten, sind es „Ja“ und „Nein“, und eine Empfehlung steht nur
  zuerst, wo der Skill eine gibt, mit „(Empfehlung)“ hinter der Antwort. **Die Antworten sind kurz,
  ein bis drei Wörter, ohne Beschreibung darunter**: Hinweis, Vorschau, Diff und Warnung und was eine
  Antwort bewirkt, stehen vorher in der Nachricht, in ganzen Sätzen (§396). **Sind
  mehrere Fragen zugleich offen**, etwa fehlende Einstellungen oder die Lösungsansätze eines Epics, gehen bis
  zu vier in einen Aufruf, je mit ihren Antworten (§396). **Fehlt das Werkzeug, etwa in einem
  Unterlauf, oder sagt der Auftrag, im Chat zu fragen**, steht die Frage am Ende der Nachricht in
  einer eigenen Zeile `**❓ ‹Frage›**`, darunter die Antworten als Liste, und danach nichts mehr.
  Fragen an den Kunden bleiben offene Fragen in `gaps/`.
- **Der Bericht am Ende eines Laufs ist für einen Lead, der weder Technik noch GitHub kennt**
  (§397): in ganzen Sätzen, in der Sprache des Teams, in drei Teilen: ob der Lauf gelang; was sich
  geändert hat, mit Kennungen wie `REQ-012` und Links zu Sheet, Doc oder Seite; was als Nächstes zu
  tun ist, mit dem nächsten Lauf. Prüf-Scripts, Projektion, Commit, Branch, Pfade, Dateinamen,
  Feldnamen aus `project.yml` und Ausgaben von Scripts nennt er nur, wenn etwas scheiterte und der
  Lead etwas tun muss, dann die Meldung wörtlich, oder wenn der Lead danach fragt. Was ein Skill für
  den Bericht verlangt, sagt er in diesen Worten.
- **Im Auto-Modus einer Cloud-Sitzung prüft ein Klassifizierer jeden Aufruf und kennt nur, was im
  Auftrag steht.** Die Freigabe für das, was der Lauf schreiben soll (Sheet, Drive, Board,
  Confluence), gehört deshalb in den ersten Auftrag; eine Freigabe per Nachricht während des Laufs
  reicht nicht immer. Lehnt er einen Aufruf ab, nennt der Lauf die Meldung wörtlich und sucht keinen
  zweiten Weg. Änderungen an `.claude/settings.json` lehnt er ab, wenn ein Script sie schreibt oder
  die Freigabe nur im Auftrag steht; mit der ausdrücklichen Zustimmung des Leads in der Sitzung ging
  es mit dem Edit-Werkzeug durch (§347). Ein Lauf schreibt sie deshalb nur so, nach eigenem Ja.
  Legt ein Lauf eine weitere Sitzung an (`create_session`), gibt er
  `mcp__claude-code-remote__add_repo` in `extra_allowed_tools` mit, sonst darf sie kein Repo
  anhängen, und schreibt den ganzen Auftrag in ihren ersten Prompt, mit dem Satz „Frag im Chat,
  nicht mit `AskUserQuestion`.“: eine Antwort der anlegenden Sitzung käme erst nach dem Ende des
  Turns an, und die Kind-Sitzung hinge an der Frage.
- **Eine Sitzung, die ein Lauf anlegt (`create_session`), gehört zu diesem Repo** (§344):
  `source_url` ist die URL dieses Repos, `outcome_branch` ist `main`. Ohne `outcome_branch` steht
  sie in der App nicht beim Projekt. Ein weiteres Repo hängt sie mit `add_repo` an.
- **Ein Commit endet mit `Co-Authored-By: Claude …` und `Claude-Session: ‹Link›`** (§242), damit die
  Geschichte zeigt, welche Sitzung welchen Stand schrieb. **In Dokumenten für Menschen steht beides nie**:
  nicht im Sheet, im Entwurf, auf der Req Page, im Schätzdokument, im Proposal, im E2E-Sheet, im Ticket.
- **Am Ende jedes Laufs, nach seinen Prüfungen und direkt vor seinem Commit, schreibt die Sitzung
  Laufzeit und Kosten nach `.claude/metrics/runs.md`** (§246):
  `python3 .claude/metrics/run-metrics.py --skill <Name des Skills>`. In einer Cloud-Sitzung ruft sie
  vorher `get_session` ohne `session_id`, dann `run-metrics.py --open --ccr-session <ihre session_id>`,
  je genannte ID `get_session(session_id)` und `run-metrics.py --settle <id>=<cost_usd>`, und schreibt
  ihre Zeile mit `--cost <cost_usd> --ccr-session <ihre session_id>`. Die Zeile
  geht in den Commit des Laufs; committet ein Lauf sonst nichts (die Reviews, Schätzung, ein Proposal
  ohne Snapshot), geht sie allein in einen Commit `metrics: <Name des Skills>`. Kein Skill liest den Ordner.

## Das Vorhaben

Diesen Abschnitt füllt der Lead: worum es geht, wer beteiligt ist, was hier anders läuft als im
Standard.
