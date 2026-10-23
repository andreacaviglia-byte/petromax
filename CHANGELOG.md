# Änderungsprotokoll

## 1.0.11 (23.10.2026)

Der Schnitt in Epics gehört in jedem Projekt zur Discovery, und die Läufe fragen weniger und nur dort, wo ohne den Lead ein Fehler erst später auffiele; jede Rückfrage ist eine echte Frage mit kurzen Antworten, und jeder Bericht ist ohne Technik.

- **`epic-structure` in jedem Projekt:** `solution-epic-structure` heißt wieder `epic-structure` und ist im Projekt Pflicht in der Discovery, mit und ohne Solutioning. Er schneidet die Anforderungen in Epics und stellt die Fundament-Fragen (Shops, Systeme, Datenhoheit); er läuft nach `solution-approach` und vor `ticket-factory`. Bisher kam ein Projekt ohne Solutioning so nicht zu Tickets. Im Expert Service gibt es keinen Schnitt.
- **Neu: `solution-solve-order`:** der erste Lauf im Solutioning, nur mit dem Add-on `solutioning`. Er legt die Reihenfolge des Lösens der Epics fest, zuerst, was den größten Fehler verbergen kann. Ohne ihn gilt die Nummer des Epics.
- **Rückfragen über `AskUserQuestion`:** jedes Go, jedes Ja zu einer Vorschau und jede Wahl, die ein Skill verlangt, kommt als Frage mit kurzen Antworten, bis zu vier Fragen in einem Aufruf. Hinweis, Vorschau und was eine Antwort bewirkt, stehen vorher in der Nachricht, in ganzen Sätzen. Fehlt das Werkzeug, steht die Frage als eigene Zeile am Ende der Nachricht.
- **Weniger Rückfragen:** ein Lauf fragt nur, wenn er die Antwort nicht aus Repo, Einstellungen oder Arbeitsweise wissen kann und ein Fehler sonst erst im Sheet, auf dem Board oder beim Bauen sichtbar würde. Sieben Fragen entfallen, drei werden zusammengelegt. Das Ja vor dem Schreiben und die Frage vor allem, was nach außen geht oder etwas löscht, bleiben.
- **Bericht ohne Technik:** jeder Lauf berichtet in drei Teilen, ob er gelang, was sich geändert hat (mit Kennungen und Links) und was als Nächstes zu tun ist. Prüf-Scripts, Commit, Pfade und Feldnamen nennt er nur, wenn der Lead etwas tun muss.
- **`material-intake` und `requirements-update` in einem Rutsch:** nach dem Ablegen läuft `requirements-update` in derselben Sitzung weiter, in jedem Vorhaben, mit einem Ja am Ende für beide. Beim ersten Einlesen kommt weiter zuerst `project-setup` „Steckbrief“ in einer neuen Sitzung.
- **Vorschau und offene Fragen gleich gebaut:** jede Vorschau zeigt, was entsteht, die offenen Fragen, die Aufgaben und „Interna: keine“, und fragt mit Zahlen, etwa „Soll ich die 12 Anforderungen und 5 offenen Fragen so in die Anforderungsliste übernehmen?“. Neue offene Fragen stehen vor dem Ja als Liste mit Adressat (Kunde, Agentur oder anderer Dienstleister); der Lead korrigiert nur, was nicht stimmt.
- **Ohne Angabe fragt der Lauf nach dem Umfang:** braucht ein Lauf Material, Anforderungen oder Epics und nennt der Auftrag keine, fragt er danach, statt einen Umfang anzunehmen. Die Reviews und `e2e-testing-sheet` fragen ebenso, mit Mehrfachauswahl; `ticket-factory` fragt je Epic. Der Umfang begrenzt, was ein Lauf schreibt, nicht was er liest.
- **Bis zu drei Lösungsansätze:** `solution-approach` schlägt je Anforderung bis zu drei Lösungsansätze mit Größe, Fit und Empfehlung vor, ohne Belege. Mit dem Add-on `solutioning` belegt `solution-design` sie je Epic, und der Lead wählt dort; im Expert Service wählt der Lead schon in `solution-approach`. Die Größe zählt Bau, Konfiguration und Pflege. Die Antworten des Leads stehen nach jeder Runde als Chat-Notiz im Repo.
- **„Lösungsansatz“ überall:** Skills, Verträge und die festen Wendungen sagen „Lösungsansatz“ statt „Weg“ oder „Option“, wie im Glossar; im Glossar heißt es „Umfang eines Laufs“ statt „Scope eines Laufs“. Spalten und Tabs der Anforderungsliste bleiben, auch `Lösungsoption 1` bis `3`.
- **`project-upgrade`:** der Lauf zeigt zuerst, was sich für das Team ändert, und fragt dann einmal; das Ja deckt auch die Änderung an `.claude/settings.json`, die eigene Frage dazu entfällt. Der Bericht ist ohne Technik.
- **`sync-main.py`:** steht die Sitzung auf einem eigenen Branch mit einem Commit, der schon auf dem Remote liegt, wechselt es ohne Rückfrage auf `main` und nennt Branch und Commit.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich. Eine Anforderung mit einem Lösungsansatz und ohne die neuen Zeilen bleibt gültig. Neue Texte in den festen Wendungen erscheinen erst, wenn ein Lauf sie neu schreibt.

**Von Hand nachzuziehen:** nichts; das Upgrade mit `project-upgrade` macht der `project_owner` und entfernt dabei den alten Skill-Ordner `solution-epic-structure`. Eine Reihenfolge des Lösens, die schon in den Epics steht, bleibt. Das Upgrade läuft noch mit dem Skill aus 1.0.10; `.claude/settings.json` ändert sich in 1.0.11 nicht.

## 1.0.10 (22.10.2026)

Das Upgrade schreibt auch `settings.json` und die Projektion im Auto-Modus.

- **Freigabe für die Projektion:** `.claude/settings.json` gibt `python3 .claude/scripts/project-readme.py .` frei, mit relativem und mit absolutem Pfad, wie seit 1.0.9 `upgrade.py apply`. Damit lehnt der Auto-Modus die Projektion nach dem Upgrade nicht mehr als „[Self-Modification]“ ab, und `way-of-working.md` kommt auf den neuen Stand.
- **`project-upgrade`, `settings.json`:** Step 7 fragt nicht mehr „ja/nein“. Der Lauf bittet den Lead, mit genau diesem Satz zu antworten: „Ich erlaube ausdrücklich, dass du `.claude/settings.json` mit dem Edit-Werkzeug mit dem gezeigten Diff schreibst.“ Ein „ja“ trug die Änderung im Auto-Modus nicht. Lehnt der Auto-Modus trotzdem ab, nennt der Lauf den Weg von Hand: die Datei mit dem gezeigten Diff auf GitHub ändern und `.claude/upgrade-pending.json` löschen.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich.

**Von Hand nachzuziehen:** nichts. Das Upgrade auf 1.0.10 bringt die Zeilen für die Projektion in `.claude/settings.json` selbst mit; bei der Frage dazu antwortet der `project_owner` mit dem Satz oben. Die Projektion dieses einen Upgrades kann noch abgelehnt werden, weil die Freigabe erst danach in der Datei steht; der Standard der Arbeitsweise ist zwischen 1.0.9 und 1.0.10 gleich, es fehlt also nichts.

## 1.0.9 (22.10.2026)

Das Upgrade läuft im Auto-Modus durch, wenn der `project_owner` das Go gibt.

- **Freigabe für den Schreibschritt:** `.claude/settings.json` gibt `upgrade.py apply` von `project-upgrade` frei, mit relativem und mit absolutem Pfad. Damit prüft der Auto-Modus diesen Aufruf nicht mehr und lehnt ihn nicht als „[Self-Modification]“ ab, auch wenn das Go erst im Lauf kommt. Owner-Prüfung und Go bleiben.
- **`project-upgrade`:** Step 7 ruft `apply` von der Wurzel aus mit genau diesem Pfad und als eigenen Aufruf. Lehnt der Auto-Modus trotzdem ab, nennt der Lauf den ersten Prompt für eine neue Sitzung.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich.

**Von Hand nachzuziehen:** das Upgrade auf 1.0.9 selbst bringt die Freigabe erst mit und läuft deshalb noch ohne sie. Der `project_owner` startet es in einer neuen Sitzung mit dem ersten Prompt: „/project-upgrade – ich erlaube, dass der Lauf die Template-Dateien ins Repo schreibt (upgrade.py apply) und auf main committet und pusht.“ Die Änderung an `.claude/settings.json` zeigt der Lauf mit Diff und schreibt sie nach seinem Ja. Ab dem nächsten Upgrade greift die Freigabe von selbst.

## 1.0.8 (21.10.2026)

Der Projektstart fragt weniger ab, ein Admin am Projekt-Repo hat die Rechte des `project_owner`, und die Kosten jedes Laufs werden in `runs.md` genau nachgetragen.

- **Steckbrief aus dem Material:** `project-setup` fragt im ersten Lauf nur, was nie im Material steht: Projektordner, Sprache, Board, Confluence-Space und Team, alle in einer Nachricht. Kunde, Titel, Kennung, Shops, Projekttyp und Add-ons schlägt der Lauf „Steckbrief“ nach dem ersten `material-intake` vor, je Feld mit Fundstelle in `inputs/`. Der Lead bestätigt eine Tabelle in Klartext statt YAML. Ein Feld ohne Fundstelle bleibt „noch offen“.
- **`material-intake`:** beim ersten Einlesen nennt es als nächsten Lauf `project-setup` „Steckbrief“ vor `requirements-update`, wenn Kunde, Titel oder Projekttyp noch leer sind.
- **Projekt-Admin:** wer bei GitHub Admin-Rechte am Projekt-Repo hat, gilt bei jeder Prüfung von `wow-guard.py` wie der `project_owner`: er führt `project-upgrade` aus und ändert Einstellungen und Arbeitsweise ohne Rückfrage. Kein neues Feld in `project.yml`; liefert GitHub kein klares Ja, gilt die Person nicht als Admin.
- **Kosten in `runs.md`:** ein Lauf, der in einem Turn durchläuft, bekommt von `get_session` noch keine Kosten und schreibt `ungemessen`. `run-metrics.py --open` nennt solche Zeilen jetzt auch, und `--settle` trägt den genauen Wert nach, wie bisher bei der Untergrenze „mind. …“.
- **Glossar:** `.claude/docs/glossary.md` legt die Begriffe fest; jeder Text, den ein Lauf auf Deutsch schreibt, folgt ihm (`CLAUDE.md`).
- **Kalibrierung:** `calibration.md` sagt, dass ein Aufschlag in `Aufwand (h)` in den Faktor eingeht und vorher erfragt wird.

**Bestand bleibt, wie er ist:** `project.yml` behält seine Form; Anforderungen, Epics, offene Fragen und Sheets ändern sich nicht. Zeilen mit `ungemessen` in `runs.md` trägt der nächste Lauf nach, soweit `get_session` die alte Sitzung noch findet.

**Von Hand nachzuziehen:** nichts; das Upgrade mit `project-upgrade` macht der `project_owner`.

## 1.0.7 (21.10.2026)

Ein Lauf fragt nicht mehr bei jedem Start, ob er auf `main` wechseln soll.

- **Sitzungs-Branch:** eine Cloud-Sitzung startet heute auf einem eigenen Branch `claude/…` statt abgelöst auf `origin/main`. `sync-main.py` wechselt von dort jetzt ohne Rückfrage auf `main`, wenn der Branch keinen eigenen Commit und keine Änderung an getrackten Dateien trägt, und nennt den alten Branch in einer Zeile. Trägt er eigene Arbeit, fragt der Lauf weiter, bevor er wechselt.
- **`CLAUDE.md`:** gearbeitet und gepusht wird im Projekt-Repo auf `main`, auch wenn die Sitzung einen anderen Branch nennt.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich.

**Von Hand nachzuziehen:** nichts; das Upgrade mit `project-upgrade` macht der `project_owner`.

## 1.0.6 (15.10.2026)

Aufgaben in `todo/` werden geschlossen, wenn ihre Arbeit getan ist, und jede Person im Projekt kann sie abhaken; `project.yml` kennt das Team.

- **Schließen und anlegen:** jeder schreibende Lauf liest die offenen Aufgaben seines Scopes, schließt im selben Commit, was er erledigt, und legt eine Aufgabe an für interne Arbeit, die er findet und nicht selbst tut. Die Vorschau nennt sie im Block „Aufgaben“. Wie, steht in `.claude/docs/ref-tasks.md`.
- **Aufgaben aus Material:** `requirements-update` legt eine Absprache oder Zusage aus dem Material als Aufgabe an; Fragen an den Kunden bleiben in `gaps/`.
- **Abhaken:** „Aufgabe … ist erledigt“ an `project-status`; die Aufgabe bekommt `status: done`, `done_by`, `done_at` und eine Zeile `Erledigt <Datum>: <Ergebnis>`. Den Vorschlag zur Arbeitsweise schließt weiter nur `project-setup`.
- **Berührungen:** was `solution-design` an einem anderen Epic findet, wird eine Aufgabe an dessen Owner statt nur ein Satz im Bericht.
- **Das Team:** das optionale Feld `team` in `project.yml` nennt je Person Name, Projektrolle, GitHub-Name und beim Solution Owner den Workstream. `project-setup` fragt es im Onboarding und ergänzt es in den Einstellungen; darüber geht eine Aufgabe an die richtige Person. Geprüft wird nur die Form.
- **Prüfung:** `check-repo.py` meldet `done_by` oder `done_at` an einer Aufgabe, die nicht `done` ist (`task_done`).

**Bestand bleibt, wie er ist:** Aufgaben ohne die neuen Felder und mit `to: Lead` oder `to: Owner Strix EP-…` bleiben gültig.

**Von Hand nachzuziehen:** das Team, wenn gewünscht, mit `project-setup` („Team eintragen“).

## 1.0.5 (15.10.2026)

Die Knowledge Base und das Projekt-Repo-Template liegen in der Organisation `webweit-gmbh`.

- **Knowledge Base:** `solution-approach`, `solution-design`, `requirements-update` und `project-status` lesen sie aus `webweit-gmbh/strix-shopify-knowledge-base`.
- **Upgrade:** `project-upgrade` holt den neuen Stand aus `webweit-gmbh/strix-shopify-project-template`.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich.

**Von Hand nachzuziehen:** nichts.

## 1.0.4 (15.10.2026)

Das Solution Proposal nennt keine Stunden mehr, das interne Schätzdokument gliedert die Stunden nach Positionen und kennt kein Budget, und das Modell schätzt im Solutioning Stunden, die nur der Kalibrierung dienen.

- **Proposal ohne Stunden:** `solution-proposal` nennt keinen Aufwand, keine Zeilen für Projektmanagement und Testing, kein Gesamt und kein Budget. Es bleiben Stand, Scope, die geprüften Epics nach Domäne mit Zielen und Annahmen, „Nicht im Scope“, „Blocker“ und „Vor Beauftragung zu klären“. Eine blockierte Anforderung ohne Frage an den Kunden steht unter „Blocker“ mit „in interner Klärung“. Vor dem Snapshot liest der Lauf den Tab `Solutioning` neu.
- **Schätzdokument je Position:** `solution-estimate` gliedert die Stunden aus `Aufwand (h)` in Shop-Setup, Erweiterte Shop-Features, UX/UI, Custom-Erweiterungen, Schnittstellen, Daten-Migration und Content-Migration, je mit Bullets in Kundensprache, darunter Summe Umsetzung, Projektmanagement und Testing als Satz und das Gesamt. Eine Anforderung mit Schnittstelle zählt immer zu Schnittstellen, auch ein Konnektor aus dem App Store; eine ohne Lösungsansatz steht in „Lösungsansatz offen“, statt den Lauf anzuhalten.
- **Kein Budget in der Strecke:** das Schätzdokument nimmt kein verkauftes Budget an und gleicht nichts damit ab; den Vergleich machen PM oder Sponsor außerhalb der Strecke. Ins Repo kommt das Budget nie.
- **Modellschätzung:** mit dem Add-on `solutioning` setzt `solution-design` mit der Wahl einer Lösung `effort_estimate_model` je Anforderung, die Rohschätzung des Modells in Stunden, und schreibt ihre Zerlegung je Teil mit Begründung nach `.claude/metrics/estimates/`. `solution-approach` hält seine Größe zusätzlich in `size_estimate_approach` fest; ein offener Lösungsansatz hat keine Größe. Die Schätzungen des Modells stehen nur im Repo, nie in Sheet, Entwurf, Epic Page, Proposal, E2E-Sheet oder Ticket; das Schätzdokument rechnet nur mit `Aufwand (h)`.
- **Kalibrierung:** `.claude/docs/calibration.md` trägt je Position einen Korrekturfaktor, den ein Mensch setzt; `calibration-report.py` misst die Modellschätzung gegen `Aufwand (h)` und zeigt je Bereich den Faktor, der passen würde, und je Größe die Stunden.
- **Offene Fragen ohne Werkzeugsprache:** `check-repo.py` meldet eine Frage in `gaps/`, die Feldnamen oder Werte des Repos statt Worte für den Kunden trägt (`gap_jargon`).
- **Aufgeräumt:** Regeln und Prüfungen für Zustände aus Versionen vor 1.0.0 sind entfernt, etwa die alte Titelform `b2b: …` und das Nachziehen von Tickets aus Läufen vor 0.5.0.

**Bestand bleibt, wie er ist:** Anforderungen ohne die neuen Felder gelten als ohne Modellschätzung.

**Von Hand nachzuziehen:** nichts.

## 1.0.3 (13.10.2026)

Das Upgrade führt nur noch der Projekt-Owner aus, fragt einmal am Anfang und danach nur dort, wo eine Datei ein Urteil braucht.

- **Upgrade nur durch den `project_owner`:** wer es nicht ist, bekommt „Ein Upgrade führt nur der Projekt-Owner aus: ‹Name› (‹Mail›). Bitte wende dich an ihn.“, und der Lauf endet ohne Rückfrage. Die Mail-Adresse kommt aus dem GitHub-Profil des Owners, wenn er sie dort öffentlich führt; sonst steht nur der Name da. Ist kein Owner eingetragen, verweist die Meldung auf `project-setup`. `project-setup` und der Hook für `way-of-working/` fragen wie bisher nach.
- **Ein Go statt Bedingungen:** `project-upgrade` warnt kurz und fragt einmal „Soll ich das Upgrade starten?“. Phasengrenze und ruhiges Fenster stehen nur noch als Empfehlung darin; ob der Zeitpunkt passt und das Team Bescheid weiß, entscheidet der Owner.
- **Rückfrage nur bei Urteil:** nach dem Go schreibt das Upgrade ohne Ja zum Plan. Es fragt nur, wenn Lead und Template dieselbe Stelle geändert haben, wenn eine angepasste Datei im Template wegfällt, und bei `.claude/settings.json`. Der Bericht am Ende nennt jede Datei mit ihrem Fall. Wer den Plan vorher sehen will, sagt das beim Go.

**Bestand bleibt, wie er ist:** nichts an Anforderungen, Epics, offenen Fragen oder Sheets ändert sich.

**Von Hand nachzuziehen:** nichts. Das Upgrade auf 1.0.3 selbst läuft noch mit dem Skill von 1.0.2 (Rückfrage statt Sperre, Ja zum Plan); die neuen Regeln gelten ab dem Upgrade danach.

## 1.0.2 (12.10.2026)

Sitzungen, die ein Lauf startet, stehen in der App beim Projekt, und das Upgrade läuft vollständig durch, auch für `.claude/settings.json`.

- **Eine Sitzung, die ein Lauf anlegt, gehört zum Projekt-Repo:** `create_session` bekommt die URL des Projekt-Repos als `source_url` und `main` als `outcome_branch`; ein weiteres Repo hängt die Sitzung wie bisher mit `add_repo` an. Ohne `outcome_branch` stand eine solche Sitzung in der Sidebar der App unter „Sonstiges“, mit ihm steht sie beim Repo.
- **`project-upgrade` schreibt `.claude/settings.json` mit:** es zeigt ihren Diff, fragt eigens nach und schreibt sie auf das Ja des Leads mit dem Edit-Werkzeug. Lehnt der Lead oder der Auto-Modus ab, bleibt die Datei, und `.claude/upgrade-pending.json` merkt sich ihren Stand; das nächste Upgrade rechnet von dort und zeigt sie wieder, statt den alten Stand für eine Anpassung des Leads zu halten.

**Bestand bleibt, wie er ist:** schon gestartete Sitzungen behalten ihren Platz in der App.

**Von Hand nachzuziehen:** in einem Projekt, das auf 1.0.1 steht und `.claude/settings.json` beim Upgrade ausgelassen hat, gleicht der `project_owner` die Datei einmal mit der Fassung von v1.0.2 ab; das Upgrade auf 1.0.2 hält den alten Stand sonst für seine Anpassung (Fall `keep`). Ein Projekt, das neu aus 1.0.2 entsteht, betrifft das nicht.

## 1.0.1 (11.10.2026)

Das Template sagt jetzt, wie das Glossar der Agentur: `architecture.md` ist die Architektur, die vier Zeilen oben sind das Fundament.

- **Architektur statt Rahmen:** Skills, Verträge, `CLAUDE.md` und die Arbeitsweise sagen „Architektur“ und „Architekturfrage“, für die vier Zeilen oben „Fundament“ und „Fundament-Frage“. Eine neue `architecture.md` beginnt mit `# Architektur`.
- **Die zwei Wendungen dazu:** eine Frage zur Architektur in `gaps/` beginnt mit „Architektur: ‹Frage›“ (bei `en` „Architecture: ‹question›“); ersetzt eine Aussage der Architektur eine frühere, endet `clarification` des Epics mit „Nachprüfen: ‹Datum›, Architektur „‹Aussage›““ (bei `en` „Recheck: ‹date›, architecture “‹statement›”“).
- **Der englische Entwurf zeigt die Architektur englisch:** die Zeilen des Fundaments und ihr Status (`Storefront build`, `Integration layer`, `System landscape`; `evidenced`, `decided`, `open`, `contradictory`) stehen im Entwurf und auf der Epic Page in der Projektsprache. `architecture.md` selbst bleibt deutsch.

**Bestand bleibt, wie er ist:** eine `architecture.md` mit `# Rahmen` und Fragen, die mit „Rahmen:“ beginnen, bleiben stehen; kein Script liest die Wörter.

**Von Hand nachzuziehen:** nichts.

## 1.0.0 (11.10.2026)

Die erste Produktionsversion. Ab hier bleibt die Form stabil: Felder im Repo und Spalten, Kopfzeilen, Tabs und Auswahlwerte der Kundendokumente ändern sich in 1.x nicht mehr; neu dazukommen dürfen nur ein Feld, das ohne Eintrag als seine Vorgabe gilt, und eine Spalte am Ende, die die Projektion anlegt. Dazu jedes Kundendokument in der Projektsprache und die Doku von Shopify als Quelle statt als Pflicht.

- **Jedes Dokument, das der Kunde sieht, in der Projektsprache** (`language` in `project.yml`, `de` oder `en`): Anforderungsliste, E2E-Sheet, Entwurf je Epic, Epic Page, Solution Proposal und Tickets zeigen Überschriften, Spaltenköpfe, Tabs, Auswahlwerte, feste Sätze und Namen in dieser Sprache. Neu zweisprachig ist das E2E-Sheet (Kopfzeile, Tabs, Auswahlwerte, Übersicht) und die Stufenzeile im Epic-Ticket. Die festen Wendungen, die Läufe ins Repo schreiben (Quelle, Ist-Marker, KB-Zeile, Klärungsbedarf, Musterfragen, Belege), stehen im Datalayer-Vertrag unter „Die festen Wendungen“ in beiden Sprachen. Der Titel einer Anforderung und jede offene Frage in `gaps/` stehen in der Projektsprache. Datum bei `en`: „11 Oct 2026“. Fest in jeder Sprache bleiben die Gewerke (`DEV`, `Konfig`, `Schnittstelle`, `UX/UI`) und die Kennzeilen `Beauftragung:` und `Schlüssel:` im Ticket. Das interne Schätzdokument bleibt deutsch.
- **`Cluster` ist der Workstream** (etwa `SHOP`, `DATA`, `CX`); die Spalte behält ihren Namen. Eine Kategorie innerhalb eines Workstreams (Internationalisierung, B2B, UX/UI) gehört nicht hinein.
- **„Go-Live“** ist die eine Schreibweise, auch in der Standard-Anforderung „UX/UI-QA vor dem Go-Live“.
- **Die Doku ist im Solutioning eine Quelle, keine Voraussetzung:** `solution-approach`, `solution-design`, `solution-review` und `project-status` halten nicht mehr an, wenn sie fehlt, und der Shopify-Connector ist keine Voraussetzung mehr. Vier Wege ohne feste Reihenfolge, für die Doku von Shopify ebenso wie für die von Apps und Systemen des Kunden: `WebSearch` findet eine Seite, `WebFetch` liest sie, `curl` ist der Rückfall, der Shopify-Connector (`search_docs_chunks`) ist die Doku-Suche für shopify.dev, wenn er verbunden ist. `.claude/settings.json` erlaubt dazu `WebFetch` auf shopify.dev, help.shopify.com und apps.shopify.com und `curl` auf shopify.dev. Jeder Beleg nennt die gelesene URL, das Datum und die Stufe; trägt ein Weg nicht, versucht der Lauf einen anderen. Ist ein Host in der Umgebung gesperrt, schlägt der Lauf ihn in der Allowlist der Knowledge Base nach (`network/allowlist.md`) und sagt, ob die Umgebung den Block von dort braucht oder der Eintrag beim Kurator fehlt. Eine Plattformaussage ohne Beleg steht mit „(noch zu verifizieren)“ da; ein Muss-Kriterium des gewählten Wegs ohne Beleg bleibt eine blockierende offene Frage. Installierte Apps und Theme liest `solution-design` aus dem Material, nicht aus dem Shop.
- **Connector-Werkzeuge nach Zweck:** fehlt ein Werkzeugname, weil ein Connector in einer anderen Fassung angebunden ist, sucht der Lauf das Werkzeug nach seinem Zweck (Werkzeug-Suche, bei Atlassian `discover`) und hält erst an, wenn es keines dafür gibt. `ticket-factory` liest Projekt, Vorgangstypen, Pflichtfelder und Übergänge in Jira über `executeRead`, so wie der Atlassian-Connector sie heute anbietet. `.claude/settings.json` fragt jetzt auch vor einem Jira-Kommentar unter dem neuen Werkzeugnamen, vor einem Löschen in Atlassian und vor einem Kommentar auf GitHub.
- **Prüfungen:** `check-repo.py` lehnt `concerns` einer Frage und `depends_on` einer Anforderung ab, wenn sie keine Liste in eckigen Klammern sind; vorher fiel eine solche Frage still aus dem Proposal.
- **Upgrade:** `project-upgrade` warnt zu Beginn mit den Auswirkungen und läuft erst nach einem ausdrücklichen Go. Bringt das Ziehen von `main` vor einem Lauf eine neue Template-Version, hält der Lauf an: die Sitzung trägt noch die alten Skills, weiter geht es in einer neuen Sitzung.

**Bestand bleibt, wie er ist:** Werte, die frühere Läufe geschrieben haben (etwa „split from“ in einer Quelle oder „Go-live“ im Text), werden nicht umgeschrieben; der nächste Lauf, der die Stelle ohnehin schreibt, nimmt die neue Form.

**Von Hand nachzuziehen:** nichts. Meldet `check-repo.py` nach dem Upgrade `gap_target` oder `depends_on` mit „keine Liste“, kommt der Wert in eckige Klammern. Das Upgrade läuft an einer Phasengrenze oder in einem angekündigten ruhigen Fenster, nie mitten in einer Phase und nie kurz vor einem Termin beim Kunden.

## 0.5.0 (11.10.2026)

Das Projekt-Repo ist die Quelle der Wahrheit. Anforderungsliste, Entwurf, Schätzung, Proposal, E2E-Sheet und `readme.md` sind Projektionen daraus. Dazu eine überarbeitete Methodik: die User Story als Ableitung, acht Klassifizierungen, die Wahl des Wegs nach Größe, die Priorität je Anforderung und die Doku von Shopify als Pflicht im Solutioning.

- **Ein Objekt, eine Datei:** `requirements/REQ-NNN.md` (zugleich die Story), `epics/EP-NNN.md`, `gaps/GAP-NNN.md` für offene Fragen, `todo/` für interne Aufgaben, `decisions/ADR-NNN-….md`, `tests/E2E-NNN.md`. Jeder schreibende Lauf endet mit `check-repo.py` und der Projektion in die Anforderungsliste, `readme.md` und `way-of-working.md`. Was von Hand in diese drei geschrieben wird, überschreibt der nächste Lauf; Antworten kommen als Material.
- **Ein Weg für Projekt und Expert Service:** in jedem Vorhaben `material-intake` → `requirements-update` → `solution-approach` → `ticket-factory`. `project.yml` trägt `project_type` und `add_ons` (`solutioning`, `design`, `content_migration`, `e2e_testing`); mit `solutioning` kommen dazwischen `requirements-review`, `solution-epic-structure` → `solution-design` → `solution-critical-path` → `solution-review` → `solution-estimate` → `solution-proposal` und nach der Freigabe `solution-epic-page`.
- **Umbenannt:** `requirement-update` → `requirements-update`, `requirement-check` → `requirements-review`, `epic-structure` → `solution-epic-structure`, `critical-path` → `solution-critical-path`. **Neu:** `solution-epic-page`, `grill-me`, `project-status`, `skill-create`.
- **Reihenfolge:** die Reihenfolge des Lösens setzt `solution-epic-structure` beim Schnitt in `solve_order` der Epics. `solution-critical-path` läuft nach den Lösungen und ordnet nur das Bauen, aus `depends_on` der Anforderungen; Ergebnis in `epics/critical-path.md`.
- **Die User Story ist eine Ableitung** aus Ist, Soll, FC und UC der Anforderung, kein eigenes Feld in `requirements/`. Mit `solutioning` entsteht sie in `solution-design` in der Zelle `User Story / Description` des Epics, und `ticket-factory` schreibt sie ab; ohne `solutioning` leitet `ticket-factory` sie ab und legt sie in der Vorschau vor. Eine Story und ein Subtask tragen sie immer, nie leer und nie „offen“; `check-ticket-body.py` lehnt beides ab.
- **Acht Klassifizierungen, ein Vokabular:** Shopify-nativ, Theme-nativ, Public App, Theme-Anpassung, Custom App, Standard-Konnektor, Middleware, Custom Schnittstelle (`shop`, `theme_native`, `app`, `theme`, `custom_app`, `integration_connector`, `integration_middleware`, `integration_custom`). Jede hat ein Gewerk (Konfig, DEV, Schnittstelle) und eine typische Größe. Eine Migration ist ein Thema, keine Klassifizierung: `data_migration` geht an Schnittstelle, `content_migration` an Konfig.
- **Der Weg wird nach Größe gewählt:** harte Grenzen streichen, dann gewinnt die kleinere Größe im Projekt, bei gleicher Größe die Stufe (Shopify-nativ, Theme-nativ, Public App oder Theme-Anpassung gleichrangig, Custom App; bei Schnittstellen Standard-Konnektor, Middleware, Custom Schnittstelle), bei gleicher Größe und Stufe ein Stamp oder eine bevorzugte App der Knowledge Base. `solution-approach` schätzt die Größe je Option grob (S bis XL), `solution-design` setzt sie. Jedes Muss-Kriterium des gewählten Wegs braucht einen Beleg aus Doku, Listing oder Messung, sonst wird es eine blockierende offene Frage; das gilt für jede Klassifizierung, nicht nur für Apps.
- **Die Knowledge Base ist eine Quelle**, kein Vorrang: gelesen werden `index.md`, die passenden Stamps und die Best Practices für die Art des Wegs. Ein Stamp, der zur Wahl stand, steht in der ADR der Wahl; eine eigene ADR für die Abweichung gibt es nicht.
- **Priorität je Anforderung:** `priority` mit `must-have` oder `nice-to-have`. Must-have ist die Vorgabe; Nice-to-have nur, wenn der Kunde es ausdrücklich sagt, mit der Stelle in `source`. Geraten wird nie. In der Anforderungsliste steht die Spalte `Priorität` direkt vor `Scope`. `solution-review` meldet „Must-have, aber Out of Scope“, das Proposal nennt solche Anforderungen unter „Nicht im Scope“ mit Grund.
- **Die Anforderungsliste hat ein festes Format** in jedem Vorhaben: Tabs `Anforderungen`, `Solutioning`, `Epics`, `Offene Punkte`; `Status`, `Priorität` und `Scope` getrennt; neu die Spalte `Shops` am Ende; die Spalte des Epic-Tickets heißt `Board-Schlüssel`. Spalten der Menschen (`Cluster`, Owner, `Aufwand (h)`, `Kommentar`, `Geprüft von/am`, `Verantwortlich`, `Bis`) schreibt kein Lauf. Vor jeder Projektion zieht der Lauf `main`.
- **Shop-Bezug im Feld `shops`** von Anforderung und ADR statt im Titel; angezeigt hinten in Klammern, etwa `Staffelpreise (B2B)`.
- **Entwurf je Epic als Google-Doc**, einmal angelegt und danach gezielt fortgeschrieben; Kommentare des Kunden bleiben im Dokument und werden vor dem nächsten Lauf als Material gelesen. Geprüft wird je Epic von Hand (`Geprüft von`, `Geprüft am`).
- **Tickets:** Epic, eine Story je gültiger Anforderung, Subtasks nur bei mehreren Gewerken. Out of Scope geht in die Wunschliste. Mit `solutioning` bekommt ein freigegebenes Epic Tickets erst mit seiner Epic Page in Confluence.
- **Die Epic Page** trägt unter dem Titel nur „Freigegeben am ‹Datum›.“ und keinen Link aufs Board; `ticket-factory` schreibt nichts nach Confluence und verlinkt die Seite im Ticket.
- **Die Doku von Shopify ist im Solutioning Pflicht:** `solution-approach`, `solution-design` und `solution-review` prüfen zu Beginn den Shopify-Connector (`search_docs_chunks`, ein Shop ist nicht nötig) und `WebFetch` auf `shopify.dev`, `help.shopify.com` und `apps.shopify.com`; `.claude/settings.json` erlaubt diese drei Hosts. Ist shopify.dev auf keinem Weg erreichbar, hält der Lauf an. `graphql_schema` läuft nur mit angemeldetem Shop; ohne ihn arbeitet `solution-design` mit der Doku-Suche weiter. `project-status` prüft die Umgebung genauso.
- **Verträge und Refs getrennt:** was mehrere Skills lesen, steht als Vertrag unter `.claude/docs/` (neu unter anderem `user-story-contract.md`, `solution-choice-contract.md`, `draft-and-epic-page-contract.md`, `inputs-and-notes-contract.md`, `system-landscape-contract.md`, `shopify-limits.md`); die Refs eines Skills liest nur er selbst. Jede `SKILL.md` nennt in einer Zeile „Verträge:“, welche sie schreibt und liest.
- **Arbeitsweise:** `way-of-working.md` entsteht aus dem Standard des Templates und den Abweichungen in `way-of-working/`. Einstellungen und Abweichungen ändert `project-setup`, nach dem ersten Lauf der `project_owner`; andere bekommen eine Rückfrage. `project-upgrade` ist Sache des `project_owner`.
- **Schutz:** Werkzeuge des Shopify-Connectors, die Kunden oder Bestellungen eines Shops lesen, sind gesperrt. Neue Prüfungen in `check-repo.py`, `check-project.py` und `check-ticket-body.py`.

**Altbestand und bestehende Anforderungslisten werden nicht nachgepflegt:** alte Werte sind Fehler, und ein bestehendes Sheet wird von Hand auf die neue Spaltenfolge umgestellt.

**Von Hand nachzuziehen:**
- **Slash-Befehle:** `/requirements-update`, `/requirements-review`, `/solution-epic-structure`, `/solution-critical-path`, neu `/solution-epic-page`, `/grill-me`, `/project-status`, `/skill-create`. Die alten Ordner entfernt `project-upgrade`; ein angepasster alter Skill erscheint im Plan als `ask`.
- **`project_owner` in `project.yml` nachtragen** (GitHub-Name der Person, die das Repo eingerichtet hat); ohne das Feld fragen der Hook bei jeder Änderung in `way-of-working/` und `project-upgrade` nach. `project_type` und `add_ons` setzen über `project-setup`.
- **`priority` in jeder Anforderung:** `check-repo.py` meldet eine Anforderung ohne das Feld als `value`, und die Projektion unterbleibt. In jede Datei `priority: must-have` eintragen; Nice-to-have nur, wo der Kunde es ausdrücklich gesagt hat, mit der Stelle in `source`.
- **Alte Klassifizierungen umstellen:** `integration` wird `integration_connector`, `integration_middleware` oder `integration_custom`; `data` ist keine Klassifizierung mehr, die Anforderung bekommt den Weg der Migration (etwa `shop` für Export und Import im Admin, `app` für eine Migrations-App). `check-repo.py` meldet alte Werte.
- **Der Abschnitt `## User story`** in `requirements/` ist abgelöst; einen leeren Abschnitt löschen, einen gefüllten als Material behandeln.
- **Bestehende Anforderungsliste:** im Tab `Anforderungen` die Spalte `Priorität` direkt vor `Scope` einfügen (die Spalten danach rücken eine weiter) und die Spalte `Shops` am Ende anlegen (R); im Tab `Epics` die Spalte `Jira-Schlüssel` in `Board-Schlüssel` umbenennen (P). Danach einmal projizieren. Umbenannte Anzeigewerte der Klassifizierung (etwa „fremde App“ → „Public App“) meldet die erste Projektion als Abweichung; der Lead bestätigt sie.
- **Titel mit Shop-Präfix** (`b2b: Staffelpreise`) auf das Feld `shops` umstellen; `check-repo.py` meldet die alte Form als Fehler.
- **`depends_on` nennt nur Anforderungen, Epics und ADRs**, keine offenen Fragen (`GAP-…`); was an einer Frage hängt, nennt die Frage in `gaps/` unter `concerns`.
- **Epics brauchen `solve_order`:** einmal `solution-epic-structure` laufen lassen, danach `solution-critical-path`. Notizen `notes/…-critical-path.md` sind abgelöst.
- **Mit `solutioning` ist die Epic Page Pflicht:** für jedes freigegebene Epic ohne Seite vor `ticket-factory` einmal `solution-epic-page`.
- **Der Shopify-Connector muss in claude.ai verbunden sein**, ein Shop ist dafür nicht nötig. `solution-approach`, `solution-design` und `solution-review` halten ohne ihn an, wenn auch `WebFetch` auf `shopify.dev` nicht durchgeht.
- **Cloud-Sitzungen im Auto-Modus:** der Lauf braucht die Freigabe für das Schreiben in Anforderungsliste und Drive schon im ersten Auftrag; eine Freigabe per Nachricht während des Laufs reicht nicht immer. Sonst die Sitzung nicht im Auto-Modus starten. Was im Auto-Modus gilt, steht jetzt in der Wurzel-`CLAUDE.md`.
- **Eine von Hand geschriebene `readme.md`** überschreibt die erste Projektion; was bleiben soll, vorher als Material ablegen.
- **Eigene Skills** mit alten Namen oder Pfaden umstellen (Kopfzeile `abgeleitet von:`, Verweise im Text); ein Verweis auf einen verschobenen Ref zeigt jetzt auf den Vertrag unter `.claude/docs/`.
- **Das E2E-Sheet** zeigt Header-Zeile, Tabs und Auswahlwerte weiter deutsch, auch mit `language: en`.
- Nach dem Upgrade startet jedes Projektmitglied einmal `project-status`; er zeigt, was neu ist.

## 0.4.0 (08.10.2026)

Die Skills heißen nach ihrem Platz in der Kette; neu sind `solution-approach` und `critical-path`.

- Neue Kette (§274): `project-setup` → `material-intake` → `requirement-update` → `requirement-check` → `solution-approach` → `epic-structure` → `critical-path` → `solution-design` → `solution-review` → `solution-estimate` → `solution-proposal` → `ticket-factory`; daneben `e2e-testing-sheet` und `project-upgrade`.
- Umbenannt: `project-intake` → `material-intake`, `requirements-update` → `requirement-update`, `requirements-review` → `requirement-check`, `solution-epic-cut` → `epic-structure`, `solution-e2e-tests` → `e2e-testing-sheet`, `project-repo-upgrade` → `project-upgrade`.
- `epic-structure` schneidet nur noch; die Reihenfolge des Lösens leitet `critical-path` ab, nach jedem Schnitt und Nachschnitt neu, als Notiz in `notes/`. `ticket-factory` und `solution-review` lesen deren jüngste Notiz.
- Neu `solution-approach` (§275): je Anforderung Standard, App oder Custom, der Fit gegen die Grenzen von Shopify und die passenden Stamps der Wissensbasis, als Notiz in `notes/`, nicht im Sheet. Im Expert Service dazu ein Projekt-Hinweis; entscheiden tut der Lead. `epic-structure` und `solution-design` setzen auf der Notiz auf.
- Der Zugriff auf die Wissensbasis steht an einem Ort, in `.claude/docs/kb-contract.md`.
- `project-upgrade` prüft nach dem Übertragen über den Pfad ab der Wurzel.

**Von Hand nachzuziehen:**
- **Das Upgrade auf 0.4.0 läuft noch mit dem alten `project-repo-upgrade`.** Sein Step 7 meldet danach `can't open file …/project-repo-upgrade/../../scripts/check-project.py`, weil der Ordner umbenannt ist. Geschrieben ist dann, was der Plan zeigte: `python3 .claude/scripts/check-project.py .` aus der Wurzel aufrufen und mit Commit und Push weitermachen.
- **Slash-Befehle heißen anders:** `/material-intake`, `/requirement-update`, `/requirement-check`, `/epic-structure`, `/e2e-testing-sheet`, `/project-upgrade`, neu `/solution-approach` und `/critical-path`.
- **Eigene Skills mit alten Namen:** Kopfzeile `abgeleitet von:` und Verweise im Text auf die neuen Namen umstellen.
- **Ein angepasster Standard-Skill** erscheint im Plan als `ask`. Behalten heißt: die alte `SKILL.md` steht ohne ihre Refs neben dem neuen Skill. Die eigene Änderung in den neuen Skill übertragen, dann den alten Ordner löschen.
- **Die Reihenfolge der Epics:** nach dem Upgrade einmal `critical-path` laufen lassen, sonst fehlt die Stufenzeile im Epic-Ticket.
- Ältere Notizen in `notes/` mit „nächster Lauf: …“ behalten die alten Namen; das ist ohne Folgen.

## 0.3.0 (08.10.2026)

Der Stand je Freigabe, die Reihenfolge als Empfehlung und weniger harte Halte.

- Das Proposal hält den vorgelegten Stand als Snapshot unter `scope/` fest, „Kunde hat freigegeben“ trägt die Freigabe ein; `requirements-update` meldet danach jede Abweichung als mögliche Change Request (§266).
- `solution-epic-cut` gibt je Epic den kritischen Pfad und die Zeile fürs Epic-Ticket aus; `ticket-factory` schreibt „Stufe n · wartet auf EP-…“ ins Epic-Ticket, als Text, keine Verknüpfung. Ein Durchstich wird nur nach dem Ja des Leads eine eigene Story (§267).
- Ist die Wissensbasis nicht erreichbar, arbeitet `solution-design` weiter und schreibt `KB: nicht gelesen`; der Entwurf trägt dann „Noch nicht gegen Lösungen aus früheren Projekten geprüft.“, und `solution-review` meldet es vor dem Proposal (§268).
- `baselines.yml` trägt je Rechtsraum den geltenden Lesestand seiner Pflichtliste; `check-project.py` prüft die Datei (§269).
- `tests/trace.yml` verbindet Anforderung, Epic und E2E-Test (§270).
- `check-project.py` warnt mit `skill_header`, wenn ein eigener Skill die drei Kopfzeilen nicht trägt (§271).
- Das Schätzdokument ist in Poppins wie das Proposal; Dokumente für Menschen nennen keine Skill-Namen, auch der Schutz im E2E-Sheet nicht.

**Von Hand nachzuziehen:** nichts. `scope/`, `baselines.yml` und `tests/trace.yml` entstehen mit dem ersten Lauf, der sie schreibt.

## 0.2.10 (08.10.2026)

Lesbare Dokumente: Weißraum, Tabellen in Satzbreite, keine Hinweise zum Lauf.

- Schätzung und Proposal haben Abstand vor jeder Überschrift, auch direkt unter Tabellen; die Linie unter H2 fällt weg. Jede Tabelle passt in die Satzbreite.
- In Dokumenten für Menschen steht kein Hinweis zum Lauf (§264): oben nur „Stand: TT.MM.JJJJ“. Lesezeit und Fassung je Req Page stehen im Rumpf des Commits `metrics: ‹Skill›`. Eine Zeile „Geändert am“ ist ein kurzer Satz ohne Aufzählung.
- Die Übersicht im Schätzdokument zeigt nur noch `Aufwand (h)`; Abweichungen zwischen Sheet und Req Page stehen im Hinweis (§265).

**Von Hand nachzuziehen:** nichts. Bestehende Dokumente bekommen die neue Form mit der nächsten Fassung.

## 0.2.9 (08.10.2026)

Dokumentnamen in natürlicher Schreibweise.

- Die Hauptdokumente heißen `‹Art› ‹title› – ‹Kunde›`, etwa „Solution Proposal Relaunch Onlineshop – Nordlicht Tee“ (§263); das ersetzt die Form aus 0.2.8. Gilt für Schätzung, Proposal, Anforderungsliste und E2E-Sheet. `doc-name.py` liest dafür `customer` und `title`.
- Weiter gilt: jede Fassung von Schätzung und Proposal trägt denselben Namen, die vorige kommt nach `Archiv` (§262, §260).

**Von Hand nachzuziehen:** Dokumente mit dem Namen aus 0.2.8 behalten ihn. Wer aufräumen will, benennt sie im Drive um; IDs und Links bleiben gültig.

## 0.2.8 (08.10.2026)

Dokumentnamen nach Art, Vorhaben und Kunde.

- Die Hauptdokumente heißen `‹art›-‹key›-‹kunde›`, etwa `aufwandsschaetzung-relaunch-nordlicht-tee` (§262). Das gilt für Schätzung, Proposal, Anforderungsliste und E2E-Sheet. Den Namen bildet `.claude/scripts/doc-name.py` aus `customer` und `key` in `project.yml`.
- Jede Fassung von Schätzung und Proposal trägt denselben Namen. Ist die neue gleich zurückgelesen, kommt die vorige nach `Archiv` (§260); die Lesezeit steht im Dokument.
- `requirements-update` und `solution-e2e-tests` brauchen dafür `customer` und `key` in `project.yml`.

**Von Hand nachzuziehen:** Dokumente mit dem alten Namen behalten ihn. Wer aufräumen will, benennt sie im Drive um; die IDs in `project.yml` und die Links bleiben gültig.

## 0.2.7 (08.10.2026)

Ordnung im Ordner `Solutioning`, Titel mit der Epic-ID vorne.

- Flach in `Solutioning` liegen nur das Sheet, die aktuelle Schätzung und das aktuelle Proposal (§260). `solution-design` legt Entwürfe im Unterordner `Epics` an. `solution-estimate` und `solution-proposal` verschieben die vorige Fassung nach `Archiv`, sobald die neue gleich zurückgelesen ist.
- Entwurf und Req Page heißen `[EP-023] Barrierefreiheit`, in jeder Projektsprache gleich (§261). Ein Entwurf mit altem Titel meldet in `check-page.py` `title`; die Seite bekommt den neuen Titel beim nächsten „Seite neu übertragen“.

**Von Hand nachzuziehen:** Entwürfe aus früheren Läufen liegen weiter flach in `Solutioning` und tragen den alten Titel. Wer aufräumen will, verschiebt sie nach `Solutioning/Epics` und benennt Entwurf und Seite um; die Links im Sheet bleiben gültig.

## 0.2.6 (08.10.2026)

Aufräumen kaputter Dokumente, Nachprüfen nur an lebenden Epics.

- `solution-design`, `solution-estimate`, `solution-proposal` und `solution-e2e-tests` legen ein Doc oder Sheet, das sie selbst kaputt angelegt haben, in den Papierkorb, sobald die neue Fassung steht (§259). Die Sitzung fragt dabei einmal nach (`ask` auf `trash_file`, §227).
- `solution-design` markiert nach einer ersetzten Zeile in `architecture.md` keine Epics mit `Status` `Aufgelöst` oder `Zusammengeführt` mehr zum Nachprüfen.
- Korrektur zu 0.2.5: Ein E2E-Sheet im alten Format legt `solution-e2e-tests` nicht von selbst neu an. Der Lauf hält an. Der Lead stellt das Sheet um oder entscheidet, ein neues anzulegen.
- Die doppelte Überschrift „0.2.5“ in diesem Änderungsprotokoll ist entfernt.

**Von Hand nachzuziehen:** nichts.

## 0.2.5 (08.10.2026)

E2E-Sheet mit Status und Runden, Proposal mit Stunden je Block.

- `solution-e2e-tests` legt das E2E-Sheet mit ID, Shop, Rolle, Status, Runde und Übersicht an (§256).
- Das Proposal nennt die Stunden nur je Block: Shop-Features, Schnittstellen, Daten-Migration, Content-Migration (§257). Der Block folgt aus der `Domäne` des Epics; die Epic-Abschnitte stehen je Block ohne Stunden. Ein Epic ohne gültige Domäne lehnt `check-solution-doc.py` mit `domain` ab.
- Das Schätzdokument trägt zusätzlich eine Summe je Block und eine Spalte „Block“.
- Unter den Blöcken steht „Summe Umsetzung“, danach die Aufschläge. Projektmanagement (20 bis 25 %) und E2E-Testing (20 %, wenn E2E-Tests zum Vorhaben gehören) nennt der Lead als Aufschlag im Aufruf (§258).

**Von Hand nachzuziehen:** nichts. Ein bestehendes E2E-Sheet im alten Format legt `solution-e2e-tests` beim nächsten Lauf neu an.

## 0.2.4 (05.10.2026)

Req Page und Entwurf in der Projektsprache.

- Titel-Präfix, Kopf, Überschriften, Spaltenköpfe, Checkboxen und feste Sätze stehen in `language` aus `project.yml`. Bei `de` ist alles deutsch, bei `en` alles englisch (§255).
- `check-page.py` kennt `--language` und meldet `language_mismatch` und `language_mixed`.
- Schätzdokument und Proposal nennen Abschnitte und Spalten in der Sprache des Dokuments.

**Von Hand nachzuziehen:** nichts. Bestehende Seiten mit englischen Bezeichnungen stellt `solution-design` beim nächsten „Seite neu übertragen“ um (§251).

## 0.2.3 (05.10.2026)

Epics nach Domäne und Fähigkeit, verkaufte Bausteine, IST/SOLL/FC/UC, übertragene Seite fortschreiben.

- `solution-epic-cut` schneidet in zwei Ebenen (§252):
  - über den Epics eine `Domäne` aus einer festen Liste mit 16 Werten;
  - darunter ein Epic je Fähigkeit;
  - die Storefront je Seitentyp, eine Anbindung je Datenstrom;
  - ein Epic mit einer Anforderung ist erlaubt, ab 12 schlägt der Lauf eine Teilung vor.
- Neuschnitt für bestehende Vorhaben: ein dabei leer gewordenes Epic bekommt den Status `Aufgelöst`, Schätzung und Proposal zählen es nicht.
- Neue Prüfung `check-sheet.py --check cut`.
- `project.yml` trägt `services` (`setup`, `data_migration`, `content_migration`) aus dem unterschriebenen Angebot (§253). `project-setup` fragt sie ab, `requirements-update` legt je Baustein eine Anforderung an, `solution-epic-cut` das Fundament-Epic.
- `requirements-update` und `requirements-review` prüfen IST, SOLL, FC und UC je Zeile (§254):
  - Steht beim IST „ungeprüft“, entsteht eine Frage.
  - Eine Zeile trägt genau eine Fähigkeit; trägt sie mehrere, wird sie geteilt.
- `solution-design` schreibt eine übertragene Req Page nach dem Ja des Leads fort, mit „Geändert am …“ (§251).
- Eine Frage nach dem Nutzen entsteht nur noch, wo ohne ihn kein Kriterium prüfbar ist (§250).

**Von Hand nachzuziehen:**
- In `project.yml` die Zeile `services: []` eintragen; das Upgrade tut das im Drei-Wege-Abgleich.
- Bestehende Epics tragen eine freie `Domäne`. `solution-epic-cut` mit „Neuschnitt“ setzt sie nach der Liste.

## 0.2.2 (04.10.2026)

Kosten je Lauf genau, Strix-CI in den Dokumenten.

- `run-metrics.py` hält mit `--ccr-session` die ID der Cloud-Sitzung in der Spalte Sitzung fest. Der nächste Lauf fragt mit `--open`, welche Zeilen nur eine Untergrenze tragen, holt mit `get_session(session_id)` den genauen Wert und setzt ihn mit `--settle` ein (§246).
- Eine Sitzung, die eine andere per `send_message` steuert, zählt ihre Eingaben jetzt als Eingabe; „aktiv“ stand dort bisher auf 0:00.
- `Interface nötig?` gilt auch für Stammdaten aus PIM oder ERP (§205).
- Schätzdokument und Proposal tragen oben die Strix-Wortmarke, Links in #3540F8 (§248).
- Das E2E-Sheet bekommt beim Anlegen dasselbe Format wie die Anforderungsliste; das Zebra beider Sheets nimmt #F7F7F8. `sheet-format.py` liegt jetzt unter `.claude/scripts/`.

**Von Hand nachzuziehen:** ein bestehendes E2E-Sheet formatiert `solution-e2e-tests` auf „formatier das E2E-Sheet“. Zeilen in `runs.md` ohne ID der Cloud-Sitzung bleiben Untergrenzen.

## 0.2.1 (04.10.2026)

Die Pflichtbaseline gilt je Shop nach seiner Zielgruppe.

- `project.yml` trägt je Shop `audience: b2c | b2b | both`; `project-setup` fragt es mit den Shops, `requirements-update` fragt es, wenn es fehlt (§249).
- Eine Zeile des Standard-Leistungssatzes entsteht nur für Shops, deren Zielgruppe zur Spalte `für` der Wissensbasis passt; ein reiner Händlershop bekommt dafür die Zeile, die Verbraucher wirksam ausschließt. Im Sheet steht dazu keine Frage und kein Kommentar.
- `requirements-review` prüft Zeilen aus dem Leistungssatz nur noch, wenn ein Shop kein `audience` trägt.
- Kosten aus `get_session` stehen in `.claude/metrics/runs.md` als Untergrenze, weil der laufende Turn fehlt.

**Von Hand nachzuziehen:** in `project.yml` je Shop `audience` eintragen. Verbraucherzeilen, die ein Sheet schon ohne Schlüssel trägt, bestimmt kein Lauf neu.

## 0.2.0 (04.10.2026)

Stand nach der Simulation der ganzen Strecke an einem erfundenen Vorhaben.

- Jeder Lauf zieht zuerst `main` (`git pull --ff-only`), und jeder Lauf beginnt in einer frischen Sitzung (§244).
- Commits tragen `Co-Authored-By` und `Claude-Session`, Dokumente für Menschen nie (§242).
- Ein Lauf schreibt nach dem Ja des Leads, was in ihm entsteht, auch in Spalten anderer Skills (§243); ein lösender Lauf nur an Zeilen seines Epics, über Epic-Grenzen schreiben die Reviews.
- `requirements-review` prüft bei mehreren Shops den Shop-Bezug; der Standard-Leistungssatz trägt den Shop, wenn nur einer den Rechtsraum hat (§245).
- Laufzeit und Kosten je Lauf stehen in `.claude/metrics/runs.md` (§246).
- `requirements-update` formatiert die Anforderungsliste im Strix-Auftritt (§247).
- Schätzung und Proposal entstehen als Google-Doc aus HTML mit Strix-Stilen, A4 und Fußzeile; das Proposal ohne Abschnitt „Offene Fragen“, mit „Vor Beauftragung zu klären“ (§241, §248).
- Kleinere Korrekturen in Skills und Prüfern aus der Simulation.

**Von Hand nachzuziehen in einem bestehenden Sheet:** die Spalte F im Tab `Anforderungen` heißt jetzt `Interface nötig?` statt `MD Interface nötig?` (§205); `check-sheet.py` lehnt den alten Namen ab.

## 0.1.0 (04.10.2026)

Erster Stand des Templates. Ein Projekt-Repo je Vorhaben (§224), angelegt aus diesem Template.

- Elf Skills von `project-setup` bis `ticket-factory`, dazu `project-repo-upgrade` für neue Stände des Templates.
- Der Agent `project-sheet-writer` für die Anforderungsliste.
- Die Verträge unter `.claude/docs/`, die gemeinsamen Scripts unter `.claude/scripts/`.
- `project.yml` als leeres Gerüst; `project-setup` füllt es.
- `.claude/settings.json`: `deny` für Zugangsdaten, `ask` für alles mit Außenwirkung.
