# Grenzen der Plattform, gegen die eine Anforderung läuft

**Diese Datei ist der Startbestand, kein Wissensstand.** Sie trägt Grenzen, die eine Anforderung
unmöglich oder teuer machen und die im Gespräch niemand nennt. Von elf Einträgen aus sechs
Szenarien sind drei in achtzehn Monaten gekippt — deshalb trägt jeder Eintrag seinen Beleg und sein
Prüfdatum, und deshalb steht hier keine Prosa im Skilltext.

**So liest du sie:** im Gegencheck je Anforderung des Epics (§206), bevor ein Lösungsansatz gewogen wird.
Ein Treffer ist kein Verdikt, sondern eine Frage. Sie steht mit Eintrag und Prüfdatum als Datei in
`gaps/`, `kind: solutioning`, mit der betroffenen Anforderung in `concerns`
([datalayer-contract.md](datalayer-contract.md), `gaps/GAP-NNN.md`) — nie eine stille Ausklammerung. Ob die
Anforderung fällt, entscheidet der Kunde.

**Ein Eintrag ist verbindlich, solange sein Prüfdatum jünger als sechs Monate ist.** Ist er älter
oder trägt er `ungeprüft`, hältst du ihn vor dem Gebrauch gegen die Dokumentation
(Wege nach `connector-contract.md`, Abschnitt „Die Doku von Shopify“, §340) und nennst Beleg und Datum der Nachprüfung in der Frage und im Bericht; diese Datei
liegt im Template und wird im Dev-Repo fortgeschrieben, nicht im Lauf. Antwortet die Dokumentation
nicht, bleibt der Eintrag ungeprüft, und kein Befund stützt sich allein auf ihn. **Ein Eintrag ohne
Beleg wird nicht zitiert**; ein gekippter geht als Fund in den Bericht.

| Grenze | Was sie kostet | Beleg | geprüft |
|---|---|---|---|
| Ein eigener Identitätsanbieter über OpenID Connect gibt es nur auf Plus | Single Sign-on gegen ein Kundenkonto-System hängt am Plan; Multipass und der Storefront-Token-Weg tragen die neuen Kundenkonten nicht | shopify.dev/docs/api/customer-authentication | 22.09.2026 |
| Ein Produkt trägt höchstens drei Optionen | jede Anforderung, die eine vierte Achse aufmacht — Größe, Farbe, Material und dann noch eine — braucht einen anderen Lösungsansatz | shopify.dev/docs/api/admin-graphql/2026-04/mutations/productOptionsCreate (`OPTIONS_OVER_LIMIT`) | 22.09.2026 |
| Eine Custom App mit Shopify Functions läuft nur auf Plus; öffentliche Apps aus dem App Store mit Functions laufen auf jedem Plan | eine Rabatt-, Versand- oder Zahlungslogik als Custom App ist auf einem Shop ohne Plus kein Lösungsansatz; es bleibt eine Public App oder der Plan | shopify.dev/docs/apps/build/functions | 25.09.2026 |
| Checkout-UI-Extensions auf den Schritten Information, Versand und Zahlung gibt es nur auf Plus, unabhängig vom Vertriebsweg | jede Anforderung, die in diese Schritte etwas einblendet, hängt am Plan, auch mit einer Public App; Danke- und Bestellstatusseite sind ausgenommen | shopify.dev/docs/api/checkout-extensions | 25.09.2026 |
| Eine Post-Purchase-Extension als Custom App läuft nur auf Plus | ein Upsell nach dem Kauf als Custom App hängt auf einem Shop ohne Plus am Plan; es bleibt eine Public App | **ungeprüft** — steht im Architektur-Skill des Custom-App-Werkzeugs; auf shopify.dev am 25.09.2026 nicht gefunden | gelesen 14.08.2026 |
| Die alten Kundenkonten heißen `legacy` und sind für neue Stores nicht mehr zu haben | eine Migration, die sie voraussetzt, hat keinen Zielzustand; ein Enddatum ist angekündigt, aber nicht genannt | shopify.dev/changelog/legacy-customer-accounts-are-deprecated (26.02.2026) | 22.09.2026 |
| Expansion Stores teilen weder Kunden noch Produkte noch App- und Theme-Lizenzen | jede Anforderung über mehrere Stores hinweg trägt eine Übertragung, die niemand eingeplant hat | **ungeprüft** — die Auskunft steht im Help Center, gelesen am 08.09.2026 noch nicht; seit §340 über `WebFetch` lesbar | Messung 08.09.2026 |
| Managed Markets schließt Shopify Payments über mehrere Rechtsträger und die automatische Steuermeldung aus | eine Konzernstruktur mit mehreren Gesellschaften verliert entweder Managed Markets oder die Meldung | **ungeprüft** — wie oben | Messung 08.09.2026 |
| Ein Kunde ist B2B oder B2C, nicht beides | jeder Händler, der denselben Menschen geschäftlich und privat kaufen lässt, braucht zwei Konten oder einen zweiten Store | **ungeprüft** — `customer.b2b?` ist ein Boolean je Kunde und damit ein Indiz, kein Beleg | Messung 08.09.2026 |

**Was hier nicht hineingehört:** eine Grenze, die eine Zahl ist und sich je Shop misst — installierte
Apps, Metafeld-Definitionen, Rate-Limits. Die schlägt `solution-design` je Shop nach, und eine Zahl in
dieser Datei wäre am nächsten Shop falsch.
