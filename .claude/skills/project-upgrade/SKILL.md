---
name: project-upgrade
description: 'Den neuesten Stand des Templates ins Projekt-Repo holen, Sache des project_owner: Standard-Dateien im Drei-Wege-Abgleich zusammenführen, Anpassungen des Leads erhalten, erst zeigen, was sich ändert, dann nach einem Go schreiben, committen. Nutze das bei "Upgrade", "neuen Stand des Templates holen", "Skills aktualisieren", "neue Template-Version". Richtet KEIN Vorhaben ein (project-setup) und fasst KEINE Datei an, die nicht im Template liegt: kein Material, keine Abweichung, keinen eigenen Skill.'
---

Verträge: keine.

# Das Projekt-Repo auf den neuesten Stand des Templates bringen

Am Ende steht das Repo auf der neuesten Version des Templates, in einem Commit auf `main`: die
Standard-Dateien in der neuen Fassung, **jede Anpassung des Leads darin erhalten**, und
`.claude/template-version` nennt die neue Version (§225, §237). Gefragt wird einmal, nachdem der
Lead gesehen hat, was sich ändert (§394); was geschrieben wurde, nennt der Bericht, nichts geht
still verloren.

**Je Datei vergleicht der Lauf drei Fassungen:** das Template beim Tag der eigenen Version (alt),
beim Tag der neuen (neu) und die Datei im Projekt. Was zwischen alt und neu anders ist, kommt vom
Standard; was zwischen alt und Projekt anders ist, hat der Lead geändert. Geraten wird keine
Herkunft. Die Wurzel-`CLAUDE.md` mit „Das Vorhaben“ und `project.yml` laufen durch denselben
Abgleich. **Eine Datei, die im Template nicht liegt, fasst der Lauf nie an**: `inputs/`, `notes/`,
`decisions/`, `architecture.md`, `customer.md`, die Abweichungen in `way-of-working/` und jeden
eigenen Skill mit eigenem Namen. **Den Standard der Arbeitsweise ersetzt er** und projiziert
`way-of-working.md` danach neu (§286); einen Abgleich dieser Datei gibt es nicht.

**Upgraden ist Sache des `project_owner`** aus `project.yml` (§294): ein Upgrade tauscht den Standard
aus, der das Projekt bindet. Ein Projekt-Admin, Admin am Repo bei GitHub, hat dieselben Rechte
(§390). Wer keines von beiden ist, wird an den Owner verwiesen, und der Lauf endet (§350).

Die Adresse des Templates, sie kommt mit jedem Release neu:
`https://github.com/webweit-gmbh/strix-shopify-project-template.git`

Geholt wird mit git, ohne Connector. Arbeitsdateien und Klone legst du in einen eigenen Temp-Ordner
außerhalb des Repos (`mktemp -d`); ins Repo kommt nur, was der Plan schreibt (§233).

### Step 1 — Den Owner prüfen

Zuerst, ob die Person dieser Sitzung der `project_owner` ist, mit derselben Quelle wie der Hook
`wow-guard` (§350):

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --owner .
```

Exit 0: weiter. Exit 2 heißt: die Person ist nicht der Owner, ihr Name lässt sich nicht ermitteln,
oder das Feld ist leer. Dann **endest du sofort**, ohne Rückfrage, ohne etwas zu holen oder zu
schreiben, und nennst die Meldung von `wow-guard` wörtlich. Dazu holst du den Kontakt des Owners:

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --contact .
```

- Exit 0: „Ein Upgrade führt nur der Projekt-Owner aus: ‹Ausgabe›. Bitte wende dich an ihn.“ Die
  Ausgabe trägt die Mail-Adresse aus seinem GitHub-Profil, wenn er sie dort öffentlich führt, sonst
  nur den Namen.
- Exit 1: „Ein Upgrade führt nur der Projekt-Owner aus, und in `project.yml` ist noch keiner
  eingetragen. Das macht `project-setup`.“

Exit 0: weiter, ohne Frage. Steps 2 bis 5 lesen nur und schreiben nichts ins Repo; gefragt wird
einmal, in Step 6, wenn der Lead sieht, was sich ändert (§394).

### Step 2 — Prüfen, dass das Repo aus dem Template stammt und sauber ist

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py . --template-only
```

Meldet es `template_version`, **halte an** und sag: „Dieses Repo stammt nicht aus dem Template
`strix-shopify-project-template`; die Datei `.claude/template-version` fehlt. Ein Projekt-Repo legt
der GitHub-Admin aus dem Template an (§225, §232)." Du legst die Datei nicht an.

Dann `git status --porcelain`: **trägt die Arbeitskopie Änderungen, halte an** und nenne sie; der
Lead committet oder verwirft sie selbst. Gearbeitet wird auf `main` (§233); steht das Repo auf
einem anderen Branch, `git switch main`. Dann
`python3 ${CLAUDE_SKILL_DIR}/../../scripts/sync-main.py`; endet es nicht mit Exit 0, nenne die
Meldung wörtlich und halte an.

### Step 3 — Die neueste Version finden

In einer Cloud-Sitzung hängst du das Template zuerst mit `add_repo` an (`owner`
`webweit-gmbh`, `repo` `strix-shopify-project-template`, `access: read`), ohne Klon und ohne
`register_repo_root`; ohne das scheitert schon dieser Schritt an der Anmeldung (gemessen am
04.10.2026). Auf dem Rechner trägt die git-Anmeldung des Leads.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/upgrade.py latest <adresse>
```

Die Ausgabe ist die höchste Version unter den Tags `vX.Y.Z`. **Gleicht sie der eigenen aus
`.claude/template-version`, sag „Das Repo steht auf der neuesten Version ‹Version›." und ende.** Ist
sie niedriger, halte an und nenne beide. Scheitert der Aufruf, gilt Step 4 für die Meldung.

### Step 4 — Alt und neu holen

```
tmp=$(mktemp -d)
git clone --depth 1 --branch v<alt> <adresse> $tmp/old
git clone --depth 1 --branch v<neu> <adresse> $tmp/new
```

Scheitert ein Klon am Zugriff, **halte an** und sag: „Das Template ist aus dieser Sitzung nicht
erreichbar. Auf dem Rechner trägt das die git-Anmeldung; in einer Cloud-Sitzung muss das
Template-Repo an der Sitzung hängen." Einen zweiten Weg suchst du nicht (§237).

### Step 5 — Den Plan rechnen

```
python3 ${CLAUDE_SKILL_DIR}/scripts/upgrade.py plan . $tmp/old $tmp/new $tmp/work
```

Exit 1 heißt **anhalten** und die Meldung wörtlich nennen. Exit 0 oder 3: der Plan liegt in
`$tmp/work/plan.json`, die vorgeschlagene Fassung je Datei unter `$tmp/work/files/`. Exit 3 heißt,
der Plan trägt `conflict` oder `ask`. Die Fälle und ihre Folge (§237):

| Fall | heißt | Folge |
|---|---|---|
| `replace` | Projekt gleich alt | die neue Fassung kommt |
| `keep` | nur das Projekt weicht ab | die Fassung des Leads bleibt |
| `merge` | beide weichen ab, an verschiedenen Stellen | die neue Fassung mit der Änderung des Leads darin |
| `conflict` | beide weichen ab, an derselben Stelle, oder eine neue Datei trifft auf eine andere am selben Pfad | du schlägst eine Fassung vor (Step 6) |
| `add` | neu im Template | sie kommt dazu |
| `remove` | im Template entfernt, im Projekt gleich alt | sie geht |
| `ask` | im Template entfernt, im Projekt geändert | der Lead entscheidet: behalten oder löschen |
| `deleted` | im Projekt gelöscht | sie bleibt gelöscht |
| `projection` | `way-of-working.md`, eine Projektion (§286) | `apply` schreibt sie nicht; Step 7 projiziert sie neu |

`.claude/template-version`, `CHANGELOG.md` und der Standard `.claude/way-of-working-standard.md`
pflegt der Lead nicht; sie sind immer `replace`.

### Step 6 — Hinweis und Änderungen zeigen, dann das eine Go

**Erst zeigen, dann einmal fragen** (§394, §338). Eine Nachricht an den Lead, in ganzen Sätzen, ohne
Pfade, Fälle und Scripts:

1. **Der Hinweis:** „Das Upgrade tauscht die Standard-Dateien des Templates gegen den neuen Stand;
   Anforderungen, Material und Anforderungsliste fasst es nicht an. Jede andere Sitzung muss danach
   neu starten. Am besten passt es in ein ruhiges Fenster, nicht kurz vor einen Kundentermin.“
2. **Was sich ändert:** von welcher auf welche Version, und aus `$tmp/new/CHANGELOG.md` die Einträge
   nach der alten bis zur neuen Version, übersetzt in das, was das Team ab heute anders tut; neue
   oder umbenannte Skills mit dem alten Namen; was danach von Hand zu tun ist, wenn der `CHANGELOG`
   es nennt.
3. **Nur wenn der Plan es trägt**, je ein kurzer Absatz:
   - **Bei `conflict`**: was der Lead geändert hat (`git diff --no-index $tmp/old/<pfad> <pfad>`)
     und was der Standard ändert (`git diff --no-index $tmp/old/<pfad> $tmp/new/<pfad>`). Du schlägst
     eine Fassung vor, **die die Absicht des Leads erhält** und den neuen Standard aufnimmt,
     schreibst sie nach `$tmp/work/files/<pfad>`, ohne Konfliktmarken, und sagst in einem Satz, was
     sie behält. Lässt sich beides nicht vereinen, sagst du das und welche Seite du vorschlägst.
   - **Bei `ask`**: dass der Standard die Datei entfernt, der Lead sie aber geändert hat; du schlägst
     vor, sie zu behalten.
   - **Bei `keep` oder `merge`**: ein Satz, dass die Anpassungen des Leads erhalten bleiben.
   - **Ändert der Plan `.claude/settings.json`** (jeder Fall außer `unchanged`; nennt eine Zeile
     `basis <version>`, ließ ein früheres Upgrade sie aus): in einem Satz, welche Rechte dazukommen
     oder entfallen, und ihren Diff (`git diff --no-index .claude/settings.json
     $tmp/work/files/.claude/settings.json`); sie trägt die Rechte des Projekts.

Die Nachricht endet mit einem Satz, was ein Ja bewirkt, etwa „Mit Ja tausche ich die
Standard-Dateien und behalte deine Anpassungen.“ Dann fragst du **einmal**, als Rückfrage nach
`CLAUDE.md`, mit genau zwei kurzen Antworten, Ja und Nein, ohne Beschreibung darunter: „Soll ich das
Upgrade jetzt durchführen?“ Den Zeitpunkt und ob das Team Bescheid weiß, entscheidet der Lead; du fragst es nicht ab.
**Nur auf ein ausdrückliches Ja läuft der Lauf weiter**, und es deckt alles, was die Nachricht nennt,
auch die vorgeschlagenen Fassungen. Auf Nein, auf eine Gegenfrage oder, im Chat, ohne Antwort endest
du, ohne etwas zu schreiben, und sagst, dass das Upgrade nicht gelaufen ist.

**Alles andere kommt als eigene Antwort** in derselben Frage, nie als dritte Antwort, die du
anbietest: will der Lead eine Datei aus `ask` löschen oder eine Fassung anders, schreibst du sie nach
`$tmp/work/files/<pfad>` (oder merkst dir `--delete <pfad>`), zeigst neu und fragst noch einmal; will
er die Dateien im Einzelnen sehen, zeigst du je Datei Pfad und Fall als Tabelle, ohne `unchanged`,
und den Diff jeder Fassung, die du vorschlägst, und fragst noch einmal.

### Step 7 — Schreiben

```
python3 .claude/skills/project-upgrade/scripts/upgrade.py apply . $tmp/work --delete <pfad>
```

**Genau so, von der Wurzel aus, mit diesem Pfad und als eigener Aufruf**, nicht mit einem anderen
schreibenden Befehl verkettet: `.claude/settings.json` gibt diesen Aufruf frei, und nur dann prüft
ihn der Auto-Modus nicht (§391). Er überschreibt Skills und `CLAUDE.md`, und der Auto-Modus liest das
sonst als „[Self-Modification]“, auch nach dem Go. Lehnt er ihn trotzdem ab, ist die Freigabe im
Projekt noch nicht angekommen, etwa im ersten Upgrade, das sie bringt: nenne die Meldung wörtlich,
such keinen zweiten Weg und sag dem Lead, er startet eine neue Sitzung mit dem ersten Prompt
„/project-upgrade – ich erlaube, dass der Lauf die Template-Dateien ins Repo schreibt (upgrade.py
apply) und auf main committet und pusht.“

`--delete` nur je Datei aus `ask`, die der Lead löschen will; ohne seine Antwort bleibt sie.
**`apply` schreibt auch `.claude/settings.json`**, ohne eigene Frage (§395): das Go aus Step 6 deckt
sie, und weil die Regel den Aufruf freigibt, prüft der Auto-Modus ihn nicht. Ließ ein früheres
Upgrade sie aus, nimmt `apply` sie aus `.claude/upgrade-pending.json` heraus. `apply` kopiert die Fassungen aus dem Arbeitsordner ins Repo, löscht, was `remove` trägt, und setzt
`.claude/template-version`. Meldet es `markers`, trägt eine Fassung noch Konfliktmarken: zurück zu
Step 6 für diese Datei; geschrieben ist dann nichts. Jede andere Meldung nennst du wörtlich und
hältst an.

Dann projizierst du `way-of-working.md` und `readme.md` neu, von der Wurzel aus, genau so und als
eigenen Aufruf; `.claude/settings.json` gibt ihn frei (§393):

```
python3 .claude/scripts/project-readme.py .
```

Meldet es `wow_section`, nennt eine Abweichung in `way-of-working/` einen Abschnitt, den der neue
Standard nicht hat; `way-of-working.md` bleibt dann, wie es war. Du nennst Datei und Abschnitt
wörtlich im Bericht als Befund für den `project_owner`; die Datei der Abweichung änderst du nicht.
Jede andere Meldung nennst du wörtlich und hältst an.

### Step 8 — Prüfen, committen, pushen

```
python3 .claude/scripts/check-project.py .
```

Der Pfad geht von der Wurzel aus, nicht vom Ordner dieses Skills: benennt das Upgrade ihn um, ist der
Ordner nach `apply` gelöscht.

Meldet es `project_yml` oder `project_folder` und war `project.yml` vor dem Lauf noch nicht
ausgefüllt, ist das kein Befund des Upgrades; der nächste Lauf ist dann `project-setup`. Jede andere
Meldung kommt aus dem Abgleich von `project.yml`: nenne sie wörtlich, korrigiere die Datei mit dem
Lead und prüf neu, **vor** dem Commit.

Dann `git diff --stat` gegen den Plan lesen: jede geänderte Datei muss im Plan stehen, dazu
`way-of-working.md` und `readme.md` aus der Projektion und `.claude/upgrade-pending.json`, wenn eine
Datei ausgelassen blieb. Commit aller
Änderungen mit der Nachricht `project-upgrade: v<alt> auf v<neu>`, direkt auf `main`, und
pushen; wird der Push abgelehnt, holst du den Stand und pushst erneut, nie mit Force (§233). Zum
Schluss `rm -rf $tmp`.

### Step 9 — Berichten

**Der Bericht ist für den Lead, nicht für Technik** (§394): er will wissen, ob das Upgrade gelang
und was sich für das Team ändert. Ohne Tabelle der Dateien, ohne Fälle, Pfade, Scripts, Commit und
Meldungen, außer wenn etwas zu tun bleibt. Drei Teile, in ganzen Sätzen, in der Sprache des Teams:

1. **Ergebnis**, ein Satz: „Das Upgrade auf ‹neu› ist durch.“ Blieb etwas aus (ein abgelehnter
   Aufruf), sagst du in einem Satz, was fehlt und was der Lead tun muss.
2. **Was sich ändert**: aus `CHANGELOG.md` die Einträge nach der alten bis zur neuen Version,
   übersetzt in das, was das Team ab heute anders tut; neue oder umbenannte Skills mit dem alten
   Namen. Hatte der Lead Anpassungen in Standard-Dateien, sagst du in einem Satz, dass sie
   erhalten blieben, und nennst, wie er jede `ask` entschied.
3. **Was von Hand zu tun ist**, nur wenn der `CHANGELOG` oder der Lauf etwas nennt; sonst entfällt
   der Teil.

Zum Schluss ein Satz: der nächste Lauf beginnt in einer neuen Sitzung, damit er die neuen Skills
lädt. Fragt der Lead nach Details, nennst du Dateien, Fälle und den Commit. Einen anderen Lauf
stößt du nicht an.

## Was dieser Lauf nicht tut

Er fasst keine Datei an, die im Template nicht liegt, auch keine in `way-of-working/`, und legt
`.claude/template-version` nie an. Vor dem Go aus Step 6 schreibt er nichts ins Repo (§338, §394). Für
jemanden außer dem `project_owner` läuft er nicht, auch nicht auf Nachfrage (§350).
Er wählt keine andere als die neueste Version, schreibt nichts in den Drive, auf das Board oder nach
Confluence und pusht nie mit Force. Er ändert das Template nicht; was dort falsch ist, meldet der
Lead dem Team, das das Template pflegt.
