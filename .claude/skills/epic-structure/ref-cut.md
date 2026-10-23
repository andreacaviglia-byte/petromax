# Der Schnitt: nach dem, was sich gemeinsam lösen lässt

**Ein Epic trägt eine Fähigkeit und ist eine Einheit, die der Kunde abnehmen kann** (§209). Der
Schnitt bündelt nach dem, was sich gemeinsam lösen lässt, nicht nach dem, was der Kunde in einem
Termin gesagt hat (§217). Er ist wiederholbar: ein zweiter Lauf schneidet die Anforderungen ohne Epic
und hängt nur um, was der Lead nennt.

## Zwei Ebenen: Domäne und Epic

**Jedes Vorhaben wird gleich geschnitten, gleich wie groß es ist** (§252). Über den Epics steht die
`domain`, eine aus der festen Liste unten; in der Datei steht der Wert, im Sheet sein Anzeigewert
(`.claude/docs/requirements-list-contract.md`, „Die Anzeigewerte“). Darunter steht das Epic, **eines
je Fähigkeit**: eine App, ein Prozess, ein Datenstrom. Weil die Körnung fest ist, folgt die Zahl der
Epics aus dem Umfang: ein großes Vorhaben hatte 50 Epics zu 296 Anforderungen, zwei mittlere rund 30
bis 36. Eine Zielzahl gibt es nicht.

| `domain` | Anzeige | was hineingehört |
|---|---|---|
| `basic_setup` | Basissetup | Einrichtung der Shops, Pläne, Expansion Stores, Grundeinstellungen, Kollektionen anlegen |
| `design` | Design | das Design-Epic: die Arbeit des Designers, nur mit dem Add-on `design` (siehe unten) |
| `storefront` | Storefront | das Theme-Epic: eine Anforderung je Seitentyp (siehe unten) |
| `product_data` | Produktdaten | Datenmodell, Metafelder, Varianten, Preisangaben am Produkt |
| `search_navigation` | Suche & Navigation | Suche, Filter, Empfehlungen, Mega-Menü |
| `cart_checkout` | Warenkorb & Checkout | Zahlarten, Checkout-Regeln, Pflichtangaben vor der Bestellabgabe, Geschenkkarten |
| `customer_account` | Kundenkonto | Login, Konto, Adressen, Bestellungen im Konto |
| `b2b` | B2B | Firmen, Registrierung, Kataloge und Preise, Zahlungsbedingungen, Bestellregeln |
| `subscription_loyalty` | Abo & Kundenbindung | Abo, Loyalty, Empfehlungs- und Partnercodes |
| `markets_shipping` | Märkte & Versand | Märkte, Währung und Steuer, Sprachen, Versand, Lieferzeiten |
| `legal_consent` | Recht & Consent | Rechtstexte und Pflichtseiten, Widerruf, Consent und Tracking, Barrierefreiheit |
| `marketing_crm` | Marketing & CRM | Newsletter, E-Mail-Marketing, Bewertungen, Pop-ups |
| `apps_features` | Apps & Features | eine Fähigkeit, die in keine Domäne oben gehört, etwa Wunschliste, Live-Chat, Produktvergleich |
| `interfaces` | Schnittstellen | je Datenstrom ein Epic: Artikel, Preise, Bestand, Aufträge, Status, Kunden, je System |
| `data_migration` | Datenmigration | je Datenobjekt ein Epic: Produkte, Kunden, Bestellhistorie, Weiterleitungen |
| `content_migration` | Content-Migration | Übernahme von Inhaltsseiten und Blog |

Der `Cluster` einer Anforderung ist ihr Workstream (§336), ein Feld der Menschen im Sheet, keine
Domäne; ein Epic darf Anforderungen aus zwei Workstreams tragen.

## Theme-Epic und Design-Epic

**Die Storefront ist ein Theme-Epic mit einer Anforderung je Seitentyp** (§285): Startseite,
Kollektionsseite, Produktseite, Warenkorb, Blog, Inhaltsseite. Der Kunde nimmt je Seitentyp ab, und
jede Anforderung wird eine Story. **Die erste ist „Design-System und globale Sections“**, ohne
das Add-on `design` „Theme-Einstellungen und globale Sections“ (bei `en` „Design system and global
sections“, „Theme settings and global sections“): Farben, Schriften, Abstände und was
jede Seite trägt (Header, Footer, Warenkorb). Die Seitentypen legt `requirements-update` aus der
UX/UI-Session an; ein Inventar der Sections gibt es vor der Freigabe nicht. Fehlt die erste, nennst
du `requirements-update`. Ein Epic „Design-System und globale Sections“ gibt es nicht.

**Schnitt nach Zweck, nicht nach Code-Schicht** (§285): Darstellung gehört ins Theme-Epic, Funktion
ins Epic ihrer Fähigkeit, auch wenn sie im Theme-Code steckt. Was es nur durch eine Fähigkeit gibt,
gehört zur Fähigkeit, auch ihr UI-Stück; was die Seite auch ohne sie hätte, zum Seitentyp. **Der
Checkout ist kein Theme:** angepasst wird er über seine Einstellungen und das Branding, über Apps mit
Checkout-Extensions, über Functions oder eine Custom App; seine Anforderungen gehören in das Epic der
Fähigkeit, die sie tragen. **Trägt eine Anforderung mehrere Seitentypen**, ist sie zu grob: ein Befund
an den Lead, und `requirements-update` teilt sie.

**Das Design-Epic gibt es nur mit dem Add-on `design`** (§285, §303). Es trägt die Arbeit des Designers:
Sessions, Konzept, Figma, Abnahme des Designs beim Kunden, die interne QS und die UX/UI-QA vor dem
Go-Live, getrennt vom Theme-Epic, das den Bau trägt. Seine Anforderungen bekommen ihre Story ohne Lösungsansatz
(§297). **Die UX/UI-QA erkennst du an `standard: design-qa`** (§303); sie gehört ins Design-Epic. Fehlt
sie, meldet `check-cut.py` `design_qa`, und du nennst `requirements-update`, der sie aus dem
Add-on anlegt. Ohne das Add-on `design` legst du kein Design-Epic an, und eine Anforderung, die Arbeit des
Designers beschreibt, ist ein Befund an den Lead.

## Anbindungen

**Eine Anbindung schneidest du je Datenstrom** (§215): Artikel, Preise, Bestand, Aufträge,
Versandstatus, Kunden, je System ein Epic. Ob es eine Middleware braucht, steht als Zeile zur
Integrationsschicht in `architecture.md`; ihren Aufbau schneidest du wie jedes Thema. **Trägt eine
Anforderung mehrere Datenströme, ist sie zu grob**: ein Befund an den Lead, und `requirements-update`
teilt sie. Bis dahin steht sie im Epic ihres ersten Datenstroms, und eine Aufgabe in `todo/` nennt
den Befund.

**Setup, Datenmigration und Content-Migration schneidest du wie jedes Thema** nach der Tabelle oben
(§303): ihre Anforderungen kommen aus dem Material, mit dem Add-on `content_migration` dazu die
Standard-Anforderung `standard: content-migration`. Ein Fundament-Epic je Baustein gibt es nicht; ein
Epic ohne Anforderung legst du nicht an.

## Weitere Regeln

- **Zwei Themen mit derselben Fähigkeit** schlägst du als ein Epic vor.
- **Lösungen über mehrere Anforderungen** aus der Notiz von `solution-approach`: trägt eine Lösung
  (dieselbe App, dieselbe Custom App, dieselbe Schnittstelle) Anforderungen derselben Fähigkeit, gehören
  sie in ein Epic. Tragen sie verschiedene Fähigkeiten, bleibt der Schnitt nach Fähigkeit, und **eine**
  Aufgabe in `todo/` je gemeinsamer Lösung nennt sie, mit allen ihren Epics und Anforderungen in
  `concerns`; steht sie schon offen da, ergänzt du dort `concerns` statt eine zweite anzulegen (Probe:
  9 Dateien für 4 Lösungen, als jedes Epic eine eigene bekam). Der Lösungsansatz ist
  ein ungeprüfter Vorschlag (§275): er ordnet zu, er steht in keiner Epic-Datei.
- **Ein Sammelthema, dessen Anforderungen je in ein anderes Epic gehören**, wird aufgelöst.
- **Ein Epic mit einer einzigen Anforderung ist erlaubt**, wenn die Fähigkeit für sich steht, etwa
  eine Wunschliste oder die Zahlarten.
- **Ein Epic mit mehr als 12 Anforderungen** schlägst du zur Teilung vor; behält der Lead es, endet
  `summary` mit „Größe bestätigt“ (`en`: „Size confirmed“).
- **Dubletten** kommen ins selbe Epic; als `duplicate` markiert sie `requirements-update`.
- **Eine Anforderung, die der Kunde weder sehen noch prüfen kann** (reine Technik, etwa Token oder ein
  Build-Schritt), ist ein Befund: frag, welcher Anforderung sie dient.
- **Eine Anforderung mit `rejected`, `duplicate` oder `out_of_scope`** bekommt das Epic, zu dem ihr
  Thema gehört; ihr Status bleibt.

Go-Live, Schulung, Qualitätssicherung und Projektleitung schneidest du nicht: sie tragen keine
Anforderung des Kunden und stehen in der Vorlage des Boards. Die UX/UI-QA ist davon ausgenommen; sie
ist eine Anforderung im Design-Epic (§285).

## Teilen, umhängen, berühren

**Teilen:** braucht eine Anforderung in zwei Epics echte Arbeit, legst du nach dem Ja des Leads eine
Aufgabe in `todo/` an (`${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`): `title` „‹ID› teilen: ‹Teil› nach ‹EP-…›“, `to` der Lead, `concerns` die
Anforderung und beide Epics; der Rumpf sagt, welcher Teil in welches Epic gehört, und nennt
`requirements-update`, der die neue Anforderung mit `source` „‹Quelle der alten›; aufgeteilt aus ‹ID›“ (bei `en` „; split from ‹ID›“)
anlegt. Die alte Anforderung bleibt, wie sie ist; die neue schneidet der nächste Lauf dieses Skills.

**Berühren:** berührt eine Anforderung ein zweites Epic nur, ist das keine Teilung. Die Berührung
wird eine Aufgabe in `todo/`, in der Form von `solution-review`: `title` „‹ID› (‹EP-…›) berührt
‹EP-…›“, `to` der Owner des berührten Epics, aufgelöst nach `ref-tasks.md`, `concerns` die Anforderung und das berührte
Epic. Steht dieselbe Aufgabe schon offen da, legst du sie nicht neu an.

**Umhängen:** nur die Anforderungen, die der Lead nennt. Trägt eines der beiden Epics `draft` oder
`epic_page`, sagst du vor dem Ja, dass beide Epics danach `solution-design` brauchen; trägt es
`board_key`, dass auf dem Board schon Tickets stehen und `ticket-factory` die Änderung dort vorlegt.

**Neuschnitt** (§252): verlangt der Lead, ein bestehendes Vorhaben nach dieser Regel neu zu schneiden,
schneidest du alle Anforderungen, als gäbe es keine Epics. Ein bestehendes Epic, das danach genau eine
Fähigkeit trägt, behält seine Kennung; `domain`, `title` und `summary` setzt du nach der Regel neu.
Alle übrigen Anforderungen kommen in neue Epics. Ein bestehendes Epic, dessen Anforderungen alle
woanders landen, bekommt `status: dissolved` und in `clarification` „Aufgelöst am ‹Datum›:
‹ID› → ‹EP-…›, …“ (`clar_dissolved`, bei `en` „Dissolved on ‹date›: …“). Trägt ein Epic schon `draft` oder `epic_page`, sagst du vor dem Ja, dass es
`solution-design` braucht.

## Die Datei des Epics

Neu angelegt als `epics/EP-NNN.md`, mit dem Kopf aus dem Datalayer-Vertrag und ohne Rumpf; den Rumpf
schreibt `solution-design`:

| Feld | beim Anlegen |
|---|---|
| `id` | die nächste freie Nummer, von der höchsten in `epics/`, drei Ziffern (`EP-013`) |
| `title` | der Titel, in der Sprache des Vorhabens |
| `domain` | ein Wert aus der Liste oben, wörtlich (§252) |
| `summary` | das Kriterium des Schnitts in einem Satz, ohne Lösungsansatz; den legt erst `solution-design` fest |
| `status` | `open` |
| `information` | `thin`, `partial` oder `solid`, dein Urteil: tragen die Anforderungen einen Lösungsansatz, oder fehlen Soll, Ist oder Antworten |
| `clarification` | was das Epic aufhält, etwa „GAP-004 offen“ (`clar_gap_open`) für eine Architekturfrage, sonst „Lösung offen“ (`clar_solution_open`); in der Sprache aus `language`, ohne Namen eines Skills, nach `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt „Die festen Wendungen“ (§337) |
| `solve_order` | `""`; die Reihenfolge des Lösens setzt `solution-solve-order` (§403) |
| `draft`, `epic_page`, `board_key` | `""`; sie schreiben andere Läufe |

An einem bestehenden Epic änderst du `information` und `clarification` nur, wenn sich
einer geändert hat. **Eine Epic-Kennung wird nie neu vergeben und nie umgewidmet**; ein Epic, dessen Anforderungen
alle umgehängt werden, bleibt als Datei, und der Bericht nennt es als leer.
