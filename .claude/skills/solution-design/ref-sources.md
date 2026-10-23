# Die Quellen: Material, Wissensbasis, Dokumentation, Recherche

## Material des Vorhabens

**Erst suchen, dann fragen.** Vor jeder Frage suchst du die Antwort in allen Dateien von
`inputs/` und `notes/`, nicht nur in denen, die das Epic nennen, dazu in `customer.md`,
den ADRs in `decisions/`, in `architecture.md`, in den Kommentaren am Entwurf und in den offenen und
geschlossenen Fragen in `gaps/`. Eine Frage, die zweimal gestellt wird,
kostet zweimal Termin-Zeit.

**`inputs/` vor `notes/`.** Notizen verdichten und haben nachweislich zusammengezogen, was im Termin
getrennt gesagt wurde: eine Aussage über einen Bereich steht dort als Aussage über das Ganze, ein
bestrittener Punkt als geklärt. Führ je Aussage mit, welche Rolle sie gemacht hat und ob sie dafür
zuständig ist. Was ein späterer Termin bestreitet, ist wieder offen.

**Jede ADR mit `status: accepted` gilt, und jede `entschieden`e oder `belegt`e Zeile
in `architecture.md`.** Bricht ein Lösungsansatz eine davon, ist das ein Blocker mit der ADR in `depends_on`
oder, nach Option B, eine neue ADR mit `supersedes`; nie eine stille Abweichung. Eine `offen`e Zeile
ist keine Annahme: ein Lösungsansatz, der sie voraussetzt, sagt das, und die Architekturfrage steht in `gaps/`
([ref-questions.md](ref-questions.md)). Eine Quelle mit `Intern: ja` liest du mit; was aus ihr in den
Entwurf geht, folgt den Quellenregeln in `${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md` (§278).

**Wechselwirkungen findest du vom Gegenstand her**, nicht Epic für Epic: sammle die Gegenstände, die
in den Lösungen wiederkehren (ein Feld, eine Einwilligung, der Bestand, die Artikelnummer, ein
Mail-Werkzeug), und prüf je Gegenstand die Anforderungen, die ihn berühren. Der Test ist eng: eine
Antwort für die eine schränkt die Antwort für die andere ein. Gelesen werden die direkten Bezüge aus
`depends_on`, nicht ihre Fortsetzung. Was du findest, steht unter `Relations and Prerequisites`, als Text ohne Dateinamen.

## Die Wissensbasis

**Wie du sie liest und was davon gilt, sagt der Vertrag** `${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`
(§326): das Repo anhängen, zuerst `index.md`, die Stamps, die zum Lösungsansatz passen, jeden ganz, die Best
Practices für die Art des Lösungsansatzes, die `source_url` nie, die Größe der Wiederverwendung eines Stamps und
die drei Werte von `kb_match`. Lies ihn vor dem ersten Aufruf. Gesucht wird mit Fragen: haben wir das
schon gebaut, womit lösen wir es, was bauen wir in diesem Rechtsraum ohnehin.

Trägt ein Stamp für den Lösungsansatz zu wenig, ist das eine Lücke im Stamp, die der Bericht nennt, und die
Plattformaussage belegst du über die Dokumentation. Auch in den Entwurf kommt die `source_url` nicht.

**Ist die Wissensbasis nicht erreichbar, arbeitest du weiter** (§268): `get_file_contents` auf
`index.md` scheitert zweimal gleich, oder die Sitzung lehnt den Aufruf ab, auch nach `add_repo`. Dann
trägt jeder Lösungsansatz, den dieser Lauf schreibt, `KB: nicht gelesen` statt `KB: keiner` (`kb_line_unread`,
`kb_line_none`; bei `en` `KB: not read`, `KB: none`, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt „Die festen Wendungen“, §337): „kein Fund in
der Wissensbasis" und „nicht nachgesehen" sind verschiedene Auskünfte und stehen verschieden da. Der
Vorrang eines Stamps bei gleicher Größe und der bevorzugten App aus den Best Practices entfällt; die
Empfehlung wiegt die übrigen Lösungsansätze. Plan und Bericht nennen die Wissensbasis als ungelesene Quelle mit der Meldung, der
Entwurf mit dem Satz `kb_unread` unter `Assumptions and delimitations` (Vertrag von Entwurf und Epic Page),
und `solution-review` meldet jeden Lösungsansatz mit `KB: nicht gelesen` vor dem Proposal als Befund. **Ein
späterer Lauf, der die Wissensbasis erreicht, liest sie für diese Lösungsansätze nach**, ersetzt den Wert
durch den Treffer oder `KB: keiner` und nimmt den Satz aus dem Entwurf, nach der Übertragung mit
„Seite neu übertragen".

## Die Dokumentation

**Die Wege stehen im Connector-Vertrag** (`${CLAUDE_SKILL_DIR}/../../docs/connector-contract.md`,
Abschnitt „Die Doku von Shopify“, §340): `WebSearch` findet die Seite, `WebFetch` liest sie, `curl`
ist der Rückfall, und mit verbundenem Shopify-Connector sucht `search_docs_chunks` in shopify.dev;
eine feste Folge gibt es nicht. Jeder Beleg nennt die gelesene URL, das Datum und die Stufe. Trägt ein
Weg nicht, versuchst du einen anderen und nennst den Fehlschlag im Bericht; trägt keiner, steht die
Aussage mit „(noch zu verifizieren)“ da, und ein Muss-Kriterium des gewählten Lösungsansatzes ohne Beleg wird eine blockierende
offene Frage (§326). Eine fertige Abfrage oder ihre Validierung ist weder Pflicht noch Beleg: das
Solutioning nennt Objekte, Operationen, Scopes, Plan und Grenzen. **Gefragt ist nicht „geht das",
sondern:** welche Ressource trägt es, ab welcher API-Version, und was hängt am Plan des Shops aus
`plan` in `project.yml`. Ist `plan` leer, ist die Abhängigkeit vom Plan eine Frage, keine Annahme. Dazu das Changelog auf Abkündigungen und Termine, die ein Umsetzungsfenster begrenzen.

**Grenzen, die eine Zahl je Shop sind** (installierte Apps, Metafeld-Definitionen, Varianten je
Produkt, Ratenlimits), schlägst du nach und zählst, was die Lösungen des Shops zusammen anlegen. Ohne
Zahl ist die Zählung eine Beobachtung, kein Befund. Die Grenzen, gegen die eine Anforderung läuft, stehen
in `${CLAUDE_SKILL_DIR}/../../docs/shopify-limits.md`; ein
Eintrag mit altem Prüfdatum wird vor dem Gebrauch gegen die Dokumentation gehalten.

## Die Recherche draußen

- **Vergleichbare Händler und der heutige Shop des Kunden:** die Seite öffnen und festhalten, was dort
  passiert. Ohne Beleg steht es nicht da.
- **Die Community** trägt Grenzfälle, Umgehungen und bekannte Fehler. Beiträge sind Hinweise und stehen
  mit „(noch zu verifizieren)" (`evidence_community`, bei `en` „(to be verified)"), bis die Dokumentation
  sie trägt.
- **Die freie Suche** nach dem Epic-Titel und seinen Fachbegriffen findet Anbieter, Marktbewegungen und
  rechtliche Entwicklungen; bei einem Anbieterthema auch Übernahmen, Ablösungen und Datenresidenz.
- **App Store und Help Center** belegen die Muss-Kriterien einer Public App (§320): das Listing auf
  `apps.shopify.com` und die Doku, auf die es verweist, die Artikel auf `help.shopify.com`. Du liest
  sie über die Wege des Connector-Vertrags (§340), `WebFetch` auf beide Hosts ist ohne Rückfrage
  erlaubt; dazu die Doku des Herstellers, die `WebSearch` findet. Erreichst du sie nicht, nennt der Bericht Host und Meldung,
  und jedes Kriterium, das nur dort zu belegen war, bleibt `unproven` und wird eine Frage
  ([ref-options.md](ref-options.md), Eine Public App evaluieren). Die Suche über den Shopify-Connector
  ersetzt sie nicht.

Recherche ist Material dieses Laufs; was für die Entscheidung zählt, steht als Beleg am Lösungsansatz.
