# Lösungsansätze, Belege, Klassifizierung, Größe und die Tiefe der Lösung

Ein fester Satz oder Status, der von hier in den Entwurf geht, etwa „Lösungsansatz offen; die Frage
steht im Sheet." oder „(zu bestätigen)", steht dort in der Sprache des Entwurfs, nach
`${CLAUDE_SKILL_DIR}/../../docs/draft-and-epic-page-contract.md`, Die Bezeichnungen (§255).

## Die Lösungsansätze, solange die Wahl offen ist

**Du beginnst mit den Lösungsansätzen, die `solution-approach` in die Datei der Anforderung
geschrieben hat** (§275, §401): `## Approach` mit `solution_status: proposed`, bis zu drei, je mit
`Fit:`, `Größe:` und `KB:`, der empfohlene zuerst mit `Empfehlung:`. Sie sind ein Vorschlag ohne
Belege, nicht die Wahl. Ein Stamp dort ist ein Hinweis, welchen du liest; ein `Fit` dort ist kein
Beleg, und jede Plattformaussage belegst du neu. Die Notiz `notes/…-solution-approach.md` nennt dazu
die Lösungen, die mehrere Anforderungen tragen.

**Je Epic belegst du sie**, mit Doku, der Wissensbasis je Lösungsansatz und bei einer App mindestens
zwei Apps mit Namen (unten), und dann:

- **Streichen mit Grund**: einen, der eine harte Grenze verletzt oder ein Kriterium nachweislich
  nicht deckt; der Grund steht in der ADR.
- **Einen besseren aufnehmen, mit Beleg**: einen, der nach dem Vertrag der Wahl gewinnen könnte und
  in der Datei fehlt. **Höchstens drei** stehen in `## Approach`; eine Variante ohne eigenen
  Aufwandstreiber oder eigene Grenze ist keiner.
- **Einen Fit gegen den Standard nur bestätigen**: trägt Shopify-nativ oder Theme-nativ alles und
  steht der Lösungsansatz zuerst, belegst du ihn und suchst keine weiteren.

Gibt es nur einen gangbaren Lösungsansatz, steht der Satz da, der das sagt, und warum die anderen
nicht gehen. Fehlt `## Approach` in der Datei, beginnst du ohne und nimmst bis zu drei auf.

Je Lösungsansatz hältst du fest:

- **was sie ist**, in der Sprache des Kunden, und welche Anforderungen sie deckt;
- **was sie nicht kann**, die Grenze, die daraus eine Abgrenzung oder eine Annahme wird;
- **was den Aufwand treibt**: Mengengerüst, Zahl der betroffenen Elemente, Abhängigkeiten, keine Stunden;
- **`kb_match`**: die Kennung des gelesenen Lösungs-Stamps mit Kurztitel, „keiner", wenn die
  Wissensbasis gelesen ist und keiner trägt, oder „nicht gelesen", wenn sie nicht erreichbar war
  ([ref-sources.md](ref-sources.md), §268);
- **welche Zeile aus `architecture.md` sie voraussetzt**, mit ihrem Status;
- **die Belege** der tragenden Aussagen, unten.

**Wo das steht** (W16): in der Datei der Anforderung unter `## Approach` je Lösungsansatz ein
Unterabschnitt `### <Name>` mit einem Satz und darunter den Zeilen `Fit:`, `Größe:` und `KB:`, der
empfohlene zuerst mit `Empfehlung:`; die Projektion zeigt die drei in `Lösungsoption 1` bis `3` und den
ersten in `Empfehlung`, sobald er entschieden ist. Im Entwurf in `Technical Information` der Zeile:
„Wahl offen.", die Lösungsansätze je in einem Satz, dann „Empfehlung: ‹Lösungsansatz›, ‹Stufe und
Grund›", in der Sprache des Entwurfs
(`choice_open`, `recommendation` im Vertrag von Entwurf und Epic Page, Die Bezeichnungen). **`kb_match` steht
nur in der Datei, im Sheet und im Plan**, nicht im Entwurf, weil der Kunde mitliest: `KB: ‹Kennung›
‹Kurztitel›`, `KB: keiner` oder `KB: nicht gelesen` (`kb_line_none`, `kb_line_unread`; bei `en` `KB: none`,
`KB: not read`, §337). Die Architekturzeile oder ADR, die ein
Lösungsansatz voraussetzt, steht in `depends_on`; im Entwurf steht nur die Aussage mit ihrem Status,
ohne Dateinamen (Vertrag von Entwurf und Epic Page, Relations and Prerequisites). Eine Datei aus
einer älteren Version mit mehr als drei bleibt gültig; du schreibst sie mit den drei stärksten
zurück. **Nach der Wahl** steht der gewählte zuerst, im Entwurf nur er; die verworfenen stehen mit
Grund in der ADR.

## Wie du die Empfehlung wiegst

**Vorher stehen zwei Dinge fest.** Die Akzeptanzkriterien sind vollständig; ein offenes Kriterium ist
eine Frage, keine Annahme. Und die Fakten des Shops sind gelesen: Plan und Rechtsraum aus
`project.yml`, die Architektur aus `architecture.md`, installierte Apps und Theme aus dem Material. Einen
Shop liest das Solutioning nicht (§339).

**Nennt das Material installierte Apps oder Theme nicht**, sind sie unbekannt. Dann zählt beim
Gleichstand keine App als „läuft schon im Shop"; ein Lösungsansatz, der auf einem Stand des Shops baut,
trägt ihn als Annahme unter `Assumptions and delimitations`. Die Stufe `Messung` gibt es nur mit einer
Messung aus dem Material.

**Gewogen wird nach dem Vertrag der Wahl** (§326,
`${CLAUDE_SKILL_DIR}/../../docs/solution-choice-contract.md`, §401): harte Grenzen streichen, dann
gewinnt die kleinere Größe im Projekt, bei gleicher Größe der Stamp, dann die Stufe, dann die
bevorzugte App aus den Best Practices und die Passung zur Gesamtlösung. Je Lösungsansatz prüfst du
seine Größe aus Bau, Konfiguration und Pflege nach der Größentabelle dort, für einen Stamp die Größe
der Wiederverwendung (`${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`), und er trägt die Zeile
`Größe:` mit den drei Teilen. Eine App, die die Best Practices ausschließen, schlägst du nicht vor.
Eine akzeptierte ADR oder eine `entschieden`e Zeile in der Architektur streicht nicht: der
Lösungsansatz steht mit dem, was er bricht, und den Kosten des Umbaus.

**Lässt sich nicht belegen, ob ein Lösungsansatz ein Kriterium deckt**, weil die Doku es nicht sagt
und nichts gemessen ist, ist er weder gestrichen noch gedeckt, sondern ein **Lösungsansatz unter
Vorbehalt**: sein Satz nennt das Kriterium mit „(zu bestätigen)". **Für den Lösungsansatz, den du
empfiehlst oder den der Lead wählt, ist jedes unbelegte Muss-Kriterium eine blockierende Frage** (§326, erweitert §320), für
jede Klassifizierung: eine Frage in `gaps/` mit `blocking: yes` an den, der es belegen kann
(Consultant, Anbieter), und die Anforderung trägt `solution_status: blocked`
([ref-questions.md](ref-questions.md)). Zeigt die Antwort, dass das Kriterium nicht gedeckt ist, ist
das eine neue Wahl mit `supersedes`.

**Steht eine Public App zur Wahl, evaluierst du sie vor dem Wiegen** (§320), unten.

**Hängt die Wahl an einer kaufmännischen Präferenz**, wählt die Empfehlung keine Seite; die Frage des
Lösungsansatzes geht an den Kunden ([ref-questions.md](ref-questions.md), „Offene Frage").

## Eine Public App evaluieren

**Trägt die Empfehlung oder ein Lösungsansatz die Klassifizierung `app`, evaluierst du Apps mit Namen** (§320).
Eine bevorzugte App aus den Best Practices steht immer unter den Kandidaten, eine ausgeschlossene nie
(`${CLAUDE_SKILL_DIR}/../../docs/kb-contract.md`):

- **Mindestens zwei Kandidaten**, jeder eine App mit ihrem Namen im App Store. Ein Sammelposten wie
  „eine Abo-App eines Drittanbieters" ist kein Kandidat. Je Kandidat, der unter den drei steht, ein
  Lösungsansatz `### ‹Name der App›`; von dort nimmt das Ticket den Namen (§312); die übrigen stehen
  in der Tabelle der ADR. Gibt es für die Fähigkeit nur eine App, zählt ein Lösungsansatz ohne App als
  zweiter Kandidat, mit eigenen Zeilen in der Tabelle; der Satz dazu nennt die Suche, die nur eine App
  fand.
- **Die Muss-Kriterien** sind die Akzeptanzkriterien der Anforderung und die Pflichten aus dem
  Standard-Leistungssatz, die sie berühren (§249), etwa ein Kündigungsbutton. Je Kandidat belegst du
  jedes, mit Quelle, Stufe und Datum.
- **Die Stufen der Belege**, stärkste zuerst; in der Tabelle der ADR steht der Wert in Klammern:

  | Stufe | Quelle |
  |---|---|
  | getestet auf einem Dev-Store (`dev_store`) | was an welchem Store getestet wurde |
  | App-Listing oder Doku des Herstellers (`vendor`) | die Adresse auf `apps.shopify.com` oder beim Hersteller |
  | Help Center von Shopify (`help_center`) | die Adresse auf `help.shopify.com` |
  | Doku auf shopify.dev (`shopify_dev`), für einen Lösungsansatz ohne App | die Adresse auf `shopify.dev` |
  | Annahme (`assumption`) | wer es annimmt; eine Annahme belegt nichts, das Ergebnis bleibt `unproven` |

  Wie du App Store und Help Center liest, sagt [ref-sources.md](ref-sources.md), Die Recherche draußen.
- **Ein Muss-Kriterium ohne Beleg ist eine blockierende Frage**, nie ein Vorbehalt: für den Kandidaten,
  den du empfiehlst oder den der Lead wählt, eine Frage in `gaps/` mit `blocking: yes` an den, der es
  belegen kann (Consultant mit Dev-Store, Anbieter der App), und die Anforderung trägt
  `solution_status: blocked` ([ref-questions.md](ref-questions.md)). Wählt der Lead trotzdem, steht die
  ADR auf `proposed`, bis jede dieser Fragen beantwortet ist ([ref-adr.md](ref-adr.md)). Ein Kandidat,
  der ein Muss-Kriterium nachweislich nicht erfüllt, ist kein Lösungsansatz.
- **Dann wiegst du nach dem Vertrag der Wahl**, wie bei jedem Lösungsansatz; die Evaluierung
  ersetzt das Wiegen nicht.

Die Evaluierung steht als Tabelle Kandidat × Kriterium mit Ergebnis, Stufe, Quelle und Datum in
einer ADR auf `proposed`, schon vor der Wahl ([ref-adr.md](ref-adr.md)); der Plan zeigt sie.

## Klassifizierung

`classification` in der Datei der Anforderung nennt die Art des Lösungsansatzes, eine oder zwei der acht Werte aus
dem Datalayer-Vertrag, Abschnitt „Die Klassifizierung“
(`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, §324); dort stehen auch Anzeige, Gewerk und
die Abgrenzung zwischen Public App und Standard-Konnektor. Eine Migration ist keine Klassifizierung:
sie trägt die ihres Lösungsansatzes, und das Thema trägt die Domäne des Epics. Gesetzt wird sie mit der Wahl;
solange die Wahl offen ist, trägt sie die Art der Empfehlung, und das Sheet zeigt sie nicht. Eine
Middleware wählst du nach den Best Practices; die Wahl bekommt eine ADR und die Zeile
`Integrationsschicht` in `architecture.md` ([ref-adr.md](ref-adr.md), §216).

## Die Größe

`size` in der Datei der Anforderung trägt `S`, `M`, `L` oder `XL`, gesetzt mit der Wahl; im Sheet
steht sie in `Aufwand`. `solution-approach` hat sie als Vorschlag geschrieben; **du prüfst sie und
setzt sie endgültig**, nach der Größentabelle im Vertrag der Wahl
(`${CLAUDE_SKILL_DIR}/../../docs/solution-choice-contract.md`), aus Bau, Konfiguration und Pflege,
für einen Stamp mit der Größe der Wiederverwendung. Stunden setzt nur ein Mensch, in `Aufwand (h)` (§280, Regel 10). `size_estimate_approach` fasst du nie an (§357): es hält die Größe aus `solution-approach` fest.

**Die Modellschätzung `effort_estimate_model`** setzt du mit der Wahl nach
[ref-model-estimate.md](ref-model-estimate.md) (§357).

Bei einem Seitentyp setzt du mit der Größe die Annahme zu den eigenen Sections, `own_sections`, aus
Anforderungen, Theme-Demo, Wissensbasis und der Zuarbeit von UX/UI; der Lead bestätigt sie im Plan,
und sie steht im Entwurf unter `Assumptions and delimitations` (§285).

**Im Epic der Domäne `design` gibt es weder `classification` noch `size`** (§297): die Anker tragen
keine Designarbeit.

## Wie tief die Lösung geht

**Die Lösung geht nur so tief, wie kein nachgelagertes Werkzeug es besser weiß.**

| Art des Lösungsansatzes | Tiefe in `Technical Information` |
|---|---|
| Shopify-nativ | dünn: welche Einstellung, an welchem Shop, ob der Plan sie hergibt |
| Theme-nativ | dünn: welche Section, welcher Block oder welche Einstellung des Theme |
| Public App | dünn: welche Fähigkeit, welche App, was sie nicht kann |
| Theme-Anpassung | Anforderung und Design-Referenz, kein CSS, keine Werte; bei einem Seitentyp die Annahme zu den eigenen Sections, kein Inventar (§285) |
| Custom App | Anforderung und Ausschlüsse, keine Bauform |
| Standard-Konnektor, Middleware, Custom Schnittstelle | tief: System, Konnektor oder Middleware mit Namen, Felder, Richtung, Auslöser, Fehlerfall, Wiederholung |
| eine Migration, gleich über welchen Lösungsansatz | tief: Quelle, Menge, Abbildung, Prüfung |

Theme-Anpassung und Custom App bleiben dünn, weil die Umsetzungs-Werkzeuge Pakete, Aufwand und
Kriterien selbst schneiden; was wir vorwegschneiden, konkurriert mit ihrer Aufteilung. Schnittstellen
und Migrationen gehen tief, weil den Vertrag eines fremden Systems kein nachgelagertes Werkzeug
erschließt. **Keine Datei, kein Metafeld, kein Extension-Target, kein Arbeitspaket** im Lösungsansatz, außer bei
Schnittstellen und Migrationen.

**Vor dem gewählten Lösungsansatz die Tiefenprüfung, je Anforderung und je Sicht:** am Shop (welche Einstellung,
an welchem Shop, gibt der Plan sie her), an der Ansicht (welche Ansicht, mit welcher Design-Referenz),
an den Daten (welche Felder, in welcher Richtung, mit welchem Auslöser). Jede Sicht ist beantwortet
oder „nicht betroffen" mit einem Satz Grund. Fehlt eine Antwort, wird sie eine Frage in `gaps/`, und
die Zeile trägt „Lösungsansatz offen; die Frage steht im Sheet."

## Belege und ihre Stufe

Jede tragende Aussage in `Assumptions and delimitations`, `Relations and Prerequisites` und
`Technical Information` trägt einen Beleg, und der Beleg eine Stufe. Die festen Wendungen der Form
stehen in der Sprache aus `language`, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`,
Abschnitt „Die festen Wendungen“ (§337); die Tabelle zeigt `de`:

| Stufe | Form |
|---|---|
| Doku | die gelesene Fundstelle auf shopify.dev oder beim Hersteller mit vollständiger Adresse, bei einer API mit Version, und das Datum des Lesens (§340) |
| Messung | was gemessen wurde, mit „gemessen am ‹Datum› an ‹Shop›" (`evidence_measured`, `en`: „measured on ‹date› at ‹Shop›") |
| Workshop | „Workshop ‹Titel› vom ‹Datum›" (`source_workshop`) oder „Chat mit dem Lead vom ‹Datum›" (`source_chat`) |
| Wissensbasis | der `kb_match` des Lösungsansatzes, in der Datei der Anforderung; der Stamp trägt den Lösungsansatz, den wir gegangen sind |
| Community | der Beitrag mit Adresse und „(noch zu verifizieren)" (`evidence_community`, `en`: „(to be verified)") |
| Annahme | keine tragende Aussage: sie steht unter `Assumptions and delimitations` oder wird eine Frage |

**Jede Plattformaussage wird gegen die Dokumentation geprüft**, nie aus dem Gedächtnis behauptet, auch
das Selbstverständliche. **Ein Stamp ist ein Startpunkt, kein Beleg für Shopify:** trägt er
`api_version: unknown` oder ein altes Messdatum, bestätigst du seine Plattformaussage über die
Dokumentation, bevor sie in den Lösungsansatz wandert. **Kein Fund ist kein Beleg:** eine leere Trefferliste
heißt „nicht gemessen", nicht „gibt es nicht".

**Der Belegpass** läuft vor dem Plan, über alles, was dieser Lauf schreibt: jede Aussage ohne Beleg
bekommt eine Quelle, geht unter `Assumptions and delimitations` oder wird eine Frage. Eine Aussage, die
sich als falsch erweist, auch eine aus einem früheren Lauf, benennt der Plan als Korrektur; still
ersetzt wird sie nicht.
