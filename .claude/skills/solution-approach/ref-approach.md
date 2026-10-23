# Die Lösungsansätze je Anforderung, ihr Fit, die Datei und die Notiz

**Die Lösungsansätze entstehen hier, vor dem Schnitt** (§275, §401), für jede Anforderung im
Umfang, in jedem Vorhaben gleich: **je Anforderung für sich**, der Fit gegen den Standard und bis zu
drei Lösungsansätze mit Größe, Fit, KB und einer Empfehlung, ohne Belege. Gewählt wird mit dem
Add-on `solutioning` in `solution-design`, im Expert Service hier vom Lead.

## Die Werte

Ein Lösungsansatz trägt eine oder zwei der acht Klassifizierungen aus dem Datalayer-Vertrag, Abschnitt
„Die Klassifizierung“ (`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, §324): in der Datei
als Wert von `classification`, englisch (§295), in Notiz und Bericht in der Anzeige des Projekts von
dort; zwei mit `+`. Ein drittes Vokabular gibt es nicht. `classification` trägt die des empfohlenen
Lösungsansatzes, im Expert Service die des gewählten. Ist keiner zu empfehlen, bleibt
`classification` `[]`, angezeigt als `offen`, mit den Kandidaten und der Frage. Eine Migration ist
keine Klassifizierung: sie trägt die ihres Lösungsansatzes. In den Worten des Leads heißen sie:

| `classification` | in den Worten des Leads |
|---|---|
| `shop`, `theme_native` | Standard |
| `app` | App |
| `theme`, `custom_app` | Custom |
| `integration_connector`, `integration_middleware`, `integration_custom` | Schnittstelle |

## Bis zu drei Lösungsansätze

**Zuerst der Fit gegen den Standard**: trägt Shopify-nativ oder Theme-nativ die Anforderung, ist das
der erste Lösungsansatz. **Er zählt als einer der drei.** **Einen weiteren nimmst du nur auf, wenn er
nach dem Vertrag der Wahl gewinnen könnte**: wenn er kleiner sein kann, bei gleicher Größe ein Stamp
ihn trägt, oder der Standard ein Kriterium nicht sicher deckt. Ein Lösungsansatz, der in jeder Folge
verliert, steht nicht da; eine Variante ohne eigenen Aufwandstreiber oder eigene Grenze ist keiner.
**Höchstens drei**; trägt der Standard alles und kann keiner ihn schlagen, steht er allein.

## Die Wahl, die Größe und die Empfehlung

**Gewogen wird nach dem Vertrag der Wahl** (§326, §401,
`${CLAUDE_SKILL_DIR}/../../docs/solution-choice-contract.md`): harte Grenzen streichen zuerst, dann
gewinnt die kleinere Größe im Projekt, bei gleicher Größe der Stamp, dann die Stufe, dann die
bevorzugte App und die Passung zur Gesamtlösung. **Was der Plan des Shops nicht trägt**
(`shops[].plan` in `project.yml`), fällt: Shopify Functions in einer Custom App und Checkout-UI auf
Information, Versand und Zahlung hängen an Plus; eine Public App mit Functions läuft auf jedem Plan.
Ein Eintrag in `shopify-limits.md` mit `ungeprüft` streicht keinen Lösungsansatz. Ist `plan` leer,
ist die Abhängigkeit vom Plan eine Frage, keine Annahme. Weitere Grenzen, die eine Zahl je Shop sind,
stehen in `${CLAUDE_SKILL_DIR}/../../docs/shopify-limits.md`.

**Du schätzt die Größe je Lösungsansatz grob** nach der Größentabelle im Vertrag, aus Bau,
Konfiguration und Pflege, für einen Stamp die Größe der Wiederverwendung
(`${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`), und schreibst sie als Zeile `Größe:` unter den
Lösungsansatz, mit den drei Teilen in Klammern. **Die Größe des empfohlenen schreibst du als
Vorschlag in `size`** der Anforderung und mit demselben Wert in `size_estimate_approach` (§357): dort
bleibt deine frühe Größe stehen, wenn `solution-design` später `size` entscheidet. Im Expert Service
gilt die Größe des Lösungsansatzes, den der Lead wählt. Eine App, die die Best Practices ausschließen,
schlägst du nicht vor.

**Die Empfehlung** steht bei mehr als einem Lösungsansatz als Zeile `Empfehlung: ‹Grund›` unter dem
empfohlenen, der zuerst steht: der Schritt des Vertrags, an dem er gewinnt, etwa „kleinere Größe (S
gegen M)“ oder „gleiche Größe, Stamp“. Belege sammelst du dafür nicht; das tut `solution-design`.

**Die Wahl setzt eine Anforderung voraus, die scharf genug ist**, nicht vollständige Kriterien.
Trägt die Zeile das Wollen nicht, gibt es keine Empfehlung, mit der Frage nach dem Wollen. **An einer
kaufmännischen Präferenz wählt die Empfehlung keine Seite**: monatliche Gebühr gegen einmaligen Bau
ist `offen`, mit beiden Kandidaten.

## Die Wahl im Expert Service

**Mit dem Add-on `solutioning` wählt in diesem Lauf niemand**; `solution-design` belegt und wählt.
**Im Expert Service wählt der Lead hier**, vor der Vorschau: je Anforderung mit mehr als einem
Lösungsansatz eine Frage „Welcher Lösungsansatz für ‹REQ-NNN›?“, die Lösungsansätze mit ihrem Namen
als Antworten, der empfohlene zuerst mit „(Empfehlung)“, bis zu vier Fragen in einem Aufruf (§396).
Vorher stehen in der Nachricht je Frage die Anforderung in einem Satz und die Lösungsansätze mit
Größe und Empfehlung. Eine Anforderung mit einem Lösungsansatz fragst du nicht; ihr Ja ist das Ja der
Vorschau. Eine offene ohne Empfehlung fragst du auch: die Antwort des Leads wählt.

Nach jeder Runde hältst du die Antworten in der Notiz einer Runde fest
(`${CLAUDE_SKILL_DIR}/../../docs/inputs-and-notes-contract.md`, Die Notiz einer Runde). **Der gewählte
steht danach zuerst**, mit der Zeile `Gewählt: Chat mit dem Lead vom ‹Datum›` (`source_chat`, in der
Sprache aus `language`, §337); `classification` und `size` folgen ihm, und `solution_status` bleibt
`proposed`: `ticket-factory` nimmt ihn mit dem Ja zur Vorschau der Tickets als Grundlage. Die Zeile
`Empfehlung:` bleibt bei dem, den du empfohlen hast.

## Der Fit

**Der Fit sagt, ob die Plattform den Lösungsansatz trägt, und woher du das weißt.** Eine
Plattformaussage aus dem Gedächtnis ist kein Beleg; eine leere Trefferliste heißt „nicht gemessen",
nicht „gibt es nicht".

| Fit | wann |
|---|---|
| `belegt: ‹Adresse› (‹Datum›, ‹Stufe›)` | die Dokumentation von Shopify oder des Herstellers trägt den Lösungsansatz; bei einer API mit Version (§340) |
| `Grenze: ‹was› (‹Adresse›, ‹Datum›)` | die Dokumentation zeigt eine Grenze, die den Lösungsansatz streicht oder an den Plan bindet; der nächste, der trägt, folgt |
| `Plan: ‹Frage›` | der Lösungsansatz hängt am Plan, und `plan` ist leer |
| `nicht nachgeschlagen` | ein Lösungsansatz ohne unklare Plattformfrage, etwa eine Einstellung, die jeder Plan trägt; `solution-design` belegt ihn |

**Nachgeschlagen wird nur, wo der Fit unklar ist**: ein Lösungsansatz über `Custom App` oder eine
Schnittstelle, eine Grenze, die am Plan oder an einer Zahl je Shop hängt, eine Fähigkeit, die du der
Plattform nicht sicher zuschreiben kannst. Gefragt ist nicht „geht das", sondern welche Ressource es
trägt, ab welcher API-Version und was am Plan hängt. `nicht nachgeschlagen` und `belegt` sind
verschiedene Auskünfte und stehen verschieden da; `solution-design` belegt jeden Lösungsansatz, den es
wählt, neu.

## Der Stamp

Die Zeile `KB:` unter jedem Lösungsansatz trägt genau einen dieser Werte (§268):

- `KB: ‹Kennung› ‹Kurztitel›`: der Stamp ist gelesen und trägt den Lösungsansatz.
- `KB: keiner`: die Wissensbasis ist gelesen, und kein Stamp trägt ihn.
- `KB: nicht gelesen`: die Wissensbasis war in diesem Lauf nicht erreichbar.

Die beiden letzten sind feste Wendungen (`kb_line_none`, `kb_line_unread`) und stehen in der Sprache aus
`language`, bei `en` `KB: none` und `KB: not read`, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt „Die festen Wendungen“ (§337).

Gelesen wird nach `${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`: nur über GitHub mit
`get_file_contents` auf `webweit-gmbh/strix-shopify-knowledge-base`; in einer Cloud-Sitzung hängst
du das Repo vorher mit `add_repo` an, `access: read`, und klonst es nicht, auch wenn die Antwort es
verlangt.
**Zuerst `index.md`**, dann die Stamps, deren Eintrag zu einem Lösungsansatz passt, jeden ganz.
**Geprüft heißt gelesen**: ein Treffer im Index, den du nicht geöffnet hast, ist kein Stamp in der
Notiz. Die `source_url` eines Stamps öffnest du nie (KB §117); sie führt oft auf das Ticket eines
anderen Kunden. Ein Stamp ist ein Startpunkt, kein Beleg für Shopify.

## Wenn eine Quelle fehlt

**Die Wissensbasis nicht erreichbar** (`get_file_contents` auf `index.md` scheitert zweimal gleich,
oder die Sitzung lehnt ab, auch nach `add_repo`): du arbeitest weiter (§268). Jeder Lösungsansatz
trägt `KB: nicht gelesen`, der Vorrang eines Stamps entfällt, und Notiz und Bericht nennen die
Wissensbasis als ungelesene Quelle mit der Meldung.

**Die Dokumentation fehlt nie still** (§339, §340): trägt ein Weg aus dem Connector-Vertrag nicht,
versuchst du einen anderen; trägt keiner, arbeitest du weiter. Eine Plattformaussage ohne Beleg steht mit „(noch zu verifizieren)“ da, in der Projektsprache;
die blockierende offene Frage für ein Muss-Kriterium ohne Beleg legt erst `solution-design` an, wenn
der Lösungsansatz gewählt wird (§326). Notiz und Bericht nennen den Weg, der nicht trug, mit der
Meldung.

## Projekt-Hinweis (im Expert Service)

**Im Expert Service läuft die Arbeit ohne Solutioning über Tickets** (§275, §282). Trägt das Material
mehr, als diese Strecke früh genug prüft, steht in der Notiz ein Projekt-Hinweis: die Empfehlung, die
Arbeit als Projekt mit Solutioning aufzusetzen. Er steht, wenn mindestens einer dieser Gründe belegt
ist:

| Grund | belegt durch |
|---|---|
| groß | mehrere Anforderungen der Größe `XL`, auf `Custom App` oder einer Schnittstelle, eine Migration aus mehreren Quellen, oder eine Lösung, die viele Anforderungen zugleich trägt |
| mehrere Systeme | die Lösungsansätze berühren mehr als ein Fremdsystem neben Shopify, oder es ist offen, welches System führt |
| architekturkritisch offen | ein Lösungsansatz hängt an einer offenen Frage der Bauform, der Integrationsschicht oder der Systemlandschaft, den Zeilen des Fundaments von `architecture.md` |

Je Grund nennt der Hinweis die Anforderungen und die Fundstelle. **Die Entscheidung trifft der
Lead**; der Hinweis empfiehlt nur. Trägt kein Grund, steht „Kein Projekt-Hinweis.“ mit einem Satz,
warum. Mit dem Add-on `solutioning` entfällt der Abschnitt: dort läuft Solutioning schon.

## Die Gewerke

Weder die Datei noch die Notiz trägt Gewerke: `ticket-factory` leitet sie aus dem gewählten
Lösungsansatz ab, nach dem Gewerk je Klassifizierung im Datalayer-Vertrag (§324), und die Datei der
Anforderung bleibt ohne Gewerk (§280, Regel 2).

## Die Lösungsansätze in der Datei

**Die Lösungsansätze stehen ungeprüft in der Datei der Anforderung** (§275, §280): unter
`## Approach`, mit `solution_status: proposed` und der Art in `classification`. Ein Lösungsansatz mit
`proposed` erscheint nicht im Sheet, in keinem Entwurf, auf keiner Seite und keinem Board; ein
Lösungsansatz, den der Kunde liest, gilt ihm als zugesagt. Die Form setzt der Datalayer-Vertrag
(`requirements/REQ-NNN.md`): je Lösungsansatz ein Unterabschnitt `### <Name>` mit einem Satz,
höchstens drei, der empfohlene oder gewählte zuerst, darunter die Zeilen `Fit:`, `Größe:` und `KB:`,
unter dem ersten `Empfehlung:` oder `Gewählt:`; `size` trägt die Größe des ersten. Eine Datei mit
einem Lösungsansatz und ohne diese Zeilen bleibt gültig. Das Beispiel zeigt `de`; bei `en` steht
`KB: none`.

```markdown
## Approach

### Versandprofile je Markt

Versandprofile in Shopify Markets, je Markt eigene Sätze.

Fit: belegt: https://shopify.dev/docs/apps/build/markets (11.10.2026, Doku)

Größe: S (Bau nichts, Konfiguration Sätze je Markt, Pflege nichts)

KB: keiner

Empfehlung: kleinere Größe (S gegen M)

### Versandkosten-App „Intuitive Shipping“

Versandsätze je Markt und Gewicht aus einer Public App.

Fit: nicht nachgeschlagen

Größe: M (Bau nichts, Konfiguration Regeln je Markt, Pflege Updates der App)

KB: keiner
```

**Ist keiner zu empfehlen**, stehen die Kandidaten als Lösungsansätze, keiner zuerst bevorzugt,
`classification`, `size` und `size_estimate_approach` bleiben leer, und unter dem letzten steht ein
Satz `Offen: ‹die Frage, an der es hängt›`.

**Ein Lösungsansatz `Public App` trägt in `### ‹Name›` den Namen einer App**, eine Schnittstelle den
Namen des Konnektors oder der Middleware, keinen Sammelposten wie „eine Abo-App eines Drittanbieters“.
Belegt und evaluiert werden die Apps in `solution-design`, mit mindestens zwei Kandidaten (§320).

**Geschrieben wird nur in eine Datei, deren `solution_status` leer ist.** Steht dort `proposed`, ist
der Vorschlag eines früheren Laufs; du ersetzt ihn nur, wenn der Lead es für diese Anforderung sagt.
Steht `decided` oder `blocked`, hat `solution-design` den Lösungsansatz gesetzt: du schreibst nichts,
und widerspricht er einer Grenze, die du findest, ist das ein Befund im Bericht. **Nur `## Approach`,
`classification`, `size`, `size_estimate_approach` und `solution_status`** ändert dieser Lauf (§280, Regel 3); das Was,
`depends_on` und `## Details` bleiben Zeichen für Zeichen.

## Die Notiz

`notes/JJJJ-MM-TT-solution-approach.md`, das Datum des Laufs; bei gleichem Namen am selben Tag `-2`
vor der Endung. Sie ist die Übergabe an `epic-structure` und trägt, was keine einzelne Anforderung
trägt; die Lösungsansätze selbst stehen in den Dateien. In der Sprache des Vorhabens (`language`):

```markdown
# Lösungsansätze, ‹TT.MM.JJJJ›

Vorhaben ‹key›, ‹Zahl› Anforderungen aus requirements/. Umfang: ‹alle | Workstream ‹Name› | IDs›. Shops: ‹key (plan)›, …
Ungeprüfter Vorschlag für die Arbeit im Team, kein Stand für den Kunden. Den Lösungsansatz wählt ‹solution-design | der Lead›.

## Lösungsansätze
‹je Art des ersten Lösungsansatzes die Zahl und die IDs, mit der Zahl der Anforderungen mit mehreren; die ohne Empfehlung mit ihrer Frage; die Anforderungen, deren Lösungsansatz schon entschieden war, mit „aus solution-design“; die IDs aus der Zeile des Scripts mit „ohne Lösungsansatz (Design-Epic, §297)“›

## Lösungen über mehrere Anforderungen
| Lösung | Lösungsansatz | trägt | KB |
‹je Lösung, die mehr als eine Anforderung trägt: ihr Name, die Art, die IDs; ohne solche „Keine.“›

## Grenzen
‹je harte Grenze, die einen Lösungsansatz gestrichen oder an den Plan gebunden hat: Grenze, Beleg, betroffene IDs; ohne „Keine gefunden.“›

## Projekt-Hinweis
‹nur im Expert Service: Empfehlung, je Grund die Anforderungen und die Fundstelle, „Die Entscheidung trifft der Lead.“›

## Ungelesen
‹Quellen, die nicht gelesen wurden, mit Meldung; sonst „Keine.“›
```

**Ohne Beleg keine Aussage**: eine Lösung über mehrere Anforderungen steht nur, wenn die
Lösungsansätze der Anforderungen sie tragen; ein Grund für den Projekt-Hinweis nur mit Fundstelle.
