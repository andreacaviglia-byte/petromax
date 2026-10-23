# Glossar

**Wir sind eine Shopify-Agentur, und so sprechen wir:** deutsch, mit den englischen Fachwörtern, die
im Team und beim Kunden üblich sind. Dieses Glossar gilt für jeden deutschen Text, den ein Lauf
schreibt: Antworten im Chat, Dateien im Repo, Anforderungsliste, Entwurf, Schätzdokument, Proposal,
Epic Page, E2E-Sheet und Tickets. Feldnamen und Werte im Repo bleiben, wie
[`datalayer-contract.md`](datalayer-contract.md) sie festlegt; das Glossar benennt nichts um, was
dort steht.

**Ein Begriff, ein Wort.** Steht ein Wort in der Spalte „nicht“, wird es für diesen Begriff nicht
geschrieben; wo es etwas anderes meint und dafür selbst ein Begriff ist, gilt seine Zeile. Fehlt ein
Begriff, fragt der Lauf, wie das Team ihn nennt. Die Fachsprache des Kunden steht in seinem Material
und gilt daneben, wo sie ein Wort des Kunden ist.

## Agentur und Rollen

| Begriff | nicht | Bedeutung |
|---|---|---|
| Kunde | Auftraggeber im Text, Mandant | wer uns beauftragt; Feldwert `kunde` |
| Endkunde | Shopkunde, Käufer | wer im Shop des Kunden kauft; Feldwert `shopkunde` |
| Lead | Projektleiter, PL | führt das Projekt und die Läufe der Strecke |
| Solution Owner | Stream-Owner, Cluster-Owner | Projektrolle: verantwortet einen Workstream und dessen Lösungen, von der Discovery bis in die Umsetzung |
| UX/UI-Designer | Designer allein | Specialist für das Gewerk UX/UI |
| Strix CI | Hausstil, Corporate Design | das Markensystem der Gruppe |
| Logo | Signet, Icon | das Strix-Logo: gelbes Quadrat mit schwarzem Zeichen |
| Wordmark | Wortmarke, Schriftzug | der Schriftzug „Strix“ |
| Projektrolle | Rolle allein, Funktion | was jemand in einem Projekt verantwortet: Sponsor, Lead, Solution Owner, Associate, Specialist; getrennt vom Titel in der Organisation |
| Projekt-Admin | Admin allein, Co-Owner | wer bei GitHub Admin-Rechte am Projekt-Repo hat; hat die Rechte des `project_owner`, ohne es zu sein (§390). „Admin“ allein ist die Verwaltungsoberfläche des Shops |
| Sponsor | Projektsponsor, Owner | wirtschaftlich und kundenstrategisch verantwortlich, Eskalationsinstanz |
| Associate | Assistenz, Junior-Lead | entlastet und vertritt den Lead |
| Specialist | Spezialist, Fachexperte | setzt die zugewiesenen Tickets eines Gewerks um |
| PM | Projektleitung, Projektmanager als Rolle | die Tätigkeit Projektmanagement, keine Projektrolle; meist beim Lead oder Associate. In der Umsetzung zugleich ein Gewerk |
| Sales | Vertrieb | bietet an und übergibt das Projekt an die Delivery |
| Delivery | Abwicklung, Projektgeschäft | wer Projekte nach der Übergabe löst und umsetzt |

## Projekt und Strecke

| Begriff | nicht | Bedeutung |
|---|---|---|
| Vorhaben | Mandat, Engagement | ein Projekt und, wenn der Lead es so will, der Expert Service danach; je Vorhaben ein Projekt-Repo |
| Projekt | Beauftragung, Mandat | ein Vorhaben mit Go-Live; `project_type: project` |
| Expert Service | Retainer, Wartung | die laufende Betreuung nach dem Go-Live; `project_type: expert_service` |
| Add-on | Zusatzmodul, Paket | vorab verkaufter Baustein: `solutioning`, `design`, `content_migration`, `e2e_testing` |
| Discovery | Aufnahme, Analyse | Anforderungen erfassen, bis sie eingefroren werden; dazu je Anforderung die Lösungsansätze und im Projekt der Schnitt in Epics mit den Fundament-Fragen (§403) |
| Solutioning | Konzeption, Lösungsphase | Reihenfolge des Lösens, Lösung je Epic, Reihenfolge des Bauens, Review, Schätzung, Solution Proposal |
| Scope | Umfang (als Schnitt) | was in diesem Projekt gebaut wird; „In Scope“, „Out of Scope“ |
| Scope-Freigabe | Abnahme, Beauftragung | der Kunde gibt den Scope frei; der Stand wird eingefroren |
| Solution Proposal | Angebot, Konzeptpapier | was wir dem Kunden vorlegen; kein Angebot |
| Schätzung | Kalkulation | das interne Schätzdokument mit Stunden |
| Go-Live | Go-live, GoLive, Launch, Livegang | der Shop geht online |
| Replay | Nachspiel | ein abgeschlossenes Projekt mit der Strecke nachspielen |
| Umsetzung | DEV als Sammelwort | alles nach der Scope-Freigabe; DEV ist ein Gewerk von mehreren |
| Workstream | Cluster, Stream, Fokusgruppe, Arbeitsbereich | die Gruppierung, in der wir arbeiten, vor allem in Discovery und Solutioning, aber auch in der Umsetzung; jeden Workstream verantwortet ein Solution Owner, und er läuft in seinem eigenen Tempo. Je Projekt geschnitten, üblich sind SHOP, DATA und CX. Nicht dasselbe wie die Kategorie einer Anforderung und das Gewerk eines Tickets. In der Anforderungsliste und im Budget-Tracking heißt es noch `Cluster` |
| SHOP | | der Workstream des Shopify-Expert-Teams: was Shopify nativ kann, mit UX/UI und DEV |
| DATA | | der Workstream des Integrations-Teams: Daten, Datenmigration, Systeme, Middleware |
| CX | Customer Experience | Custom Experience: der Workstream des Custom-Teams, alles, was als Custom App gebaut wird und nicht Shopify-nativ ist |
| Umfang eines Laufs | Scope eines Laufs | worüber ein Lauf geht: eine Auswahl von Anforderungen, ein Workstream, ein Epic oder alles; je Skill verschieden. „Scope“ allein ist der Schnitt des Projekts (§402) |
| Kette | Ablauf, Pipeline | die Abhängigkeit je Anforderung (Material, Anforderung, Lösungsansatz, Epic, Lösung, Ticket), kein Ablauf für das ganze Projekt; Workstreams laufen parallel |
| Pre-Sales | PreSales, Vorvertrieb | alles vor der Übergabe; Ergebnis ist das Angebot mit Budgetrahmen |
| Angebot | Solution Proposal | was Sales mit Preis verkauft; nicht das Solution Proposal |
| Festpreis | Pauschalprojekt | Projekt mit festem Scope, Budget und Timeline |
| Time and Material | Aufwandsabrechnung, Stundenbasis | Abrechnung nach geleisteten Stunden; kurz T&M |
| Übergabe | Handover, Sales-Übergabe | Sales übergibt das Projekt an die Delivery, der Lead nimmt an |
| Projektbriefing | Briefing allein, Steckbrief | die Vorlage der Übergabe |
| Kickoff | Kick-off, Auftaktmeeting | der Start, intern und extern; der externe ist der erste offizielle Termin mit dem Kunden |
| Working Session | Arbeitstermin, Workshop-Termin | Termin mit Kunde und Specialists je Workstream |
| Change Request | Nachtrag, Zusatzauftrag, Änderungswunsch | alles, was nicht im Angebot steht; schriftlich, mit Folgen für Zeit und Budget; kurz CR |
| Scope Creep | schleichende Erweiterung | Arbeit außerhalb des Scopes ohne Change Request |
| Abnahme | Freigabe für Geliefertes | der Kunde nimmt ein umgesetztes Ticket ab; nie für die Scope-Freigabe |
| Jour Fixe | Jour fixe, JF im Text | der wöchentliche Steuertermin, intern und extern |
| Status-Mail | Statusbericht, Statusmail | wöchentlich bei Festpreis; bei T&M und Expert Service der Monatsbericht |
| MvPM | PM-Regeln, PM-Standards | die Mindeststandards Projektmanagement 2.0 |

## Gegenstände im Projekt-Repo

| Begriff | nicht | Bedeutung |
|---|---|---|
| Anforderung | Requirement im Text, Feature | `REQ-NNN`, eine Datei je Anforderung, zugleich die Story |
| Anforderungsliste | Kundenblatt, Sheet allein | das Google Sheet mit den Anforderungen |
| Epic | Paket, Arbeitspaket | `EP-NNN`, ein Schnitt aus Anforderungen; gibt es in jedem Projekt, im Expert Service nur am Board (§403) |
| offene Frage | Gap im Text, Klärungspunkt | `GAP-NNN`; blockierend heißt `Blockiert` |
| Entscheidung | Beschluss, Festlegung | eine ADR (`ADR-NNN`) in `decisions/` |
| Architektur | Rahmen in neuem Text | `architecture.md`: das Fundament und die Entscheidungen, die mehrere Epics betreffen |
| Fundament | Kernfrage, Kernzeile, Kernsatz, Foundation | die vier Fragen oben in `architecture.md`: Shops, Bauform der Storefront, Integrationsschicht, Systemlandschaft; eine davon ist eine Fundament-Frage. „geklärt“ heißt belegt oder entschieden |
| Lösungsansatz | Weg, Lösungsweg, Approach im Text | wie eine Anforderung gelöst wird, angezeigt als Shopify-nativ, Theme-nativ, Public App, Theme-Anpassung, Custom App, Standard-Konnektor, Middleware, Custom Schnittstelle; `## Approach` in der Anforderung, vorgeschlagen oder entschieden, überall mit diesem einen Wort |
| Größe | Aufwand, Komplexität | S bis XL; schätzt die KI |
| Must-have | Pflicht, Muss | Priorität einer Anforderung, die der Kunde braucht; Vorgabe, solange er nichts anderes sagt. Nicht dasselbe wie In Scope |
| Nice-to-have | Kann, Wunsch | Priorität einer Anforderung, die der Kunde ausdrücklich als verzichtbar nennt, nie geraten. Nicht dasselbe wie Out of Scope |
| Aufwand | Größe | Stunden, nur von Menschen; bis 1.0.x nur im Sheet, ab 2.0 im Dashboard |
| Modellschätzung | KI-Aufwand, Vorschlag, Entwurf | Stunden, die das Modell je Anforderung schätzt, `effort_estimate_model`; zur Kalibrierung, keine Zusage |
| Ist-Aufwand | tatsächlicher Aufwand, Ist-Stunden | die am Board gebuchten Stunden, `effort_actual_hours` |
| Material | Input, Unterlagen | was neu ins Projekt kommt: Transkript, Mail, Antwort des Kunden |
| Entwurf | Konzept, Draft, Lösungsentwurf | das Google-Doc je Epic, Arbeitsstand; steht nie im Ticket |
| Epic Page | Req Page in neuem Text | das freigegebene Epic in Confluence |
| Snapshot | Kopie, Sicherung | der eingefrorene Stand in `scope/` |
| Kategorie | Themenbereich | die fachliche Gruppe, nach der Anforderungen und Tickets sortiert werden, etwa B2B, Internationalisierung, UX/UI |
| Aufgabe | To-do | interne Arbeit, die jemand im Projekt erledigen muss, ein Eintrag in `todo/` mit dem, an den sie geht; nie ein Ticket auf dem Board |
| Notiz | Memo, Vermerk | eine Datei in `notes/`: je Quelle des Materials eine, dazu Übergaben an den nächsten Lauf oder eine Person |
| Akzeptanzkriterium | Abnahmekriterium, AC im Text | was ein Ticket erfüllen muss, damit es abgenommen wird |

## Board

| Begriff | nicht | Bedeutung |
|---|---|---|
| Board | Tafel, Projektplan | Jira oder Asana, wo die Umsetzung läuft |
| Ticket | Karte, Aufgabe für ein Ticket | was auf dem Board liegt |
| Story | User-Story-Ticket | der Ticket-Typ, der eine Anforderung trägt |
| Subtask | Unterkarte, Unteraufgabe | ein Ticket unter einem anderen |
| Gewerk | Disziplin, Team | wonach die Tickets in der Umsetzung gruppiert sind: UX/UI, Konfig, DEV, Schnittstelle, PM; DATA ist ein Workstream, kein Gewerk |
| Wunschliste | Backlog | Spalte des Boards für Out of Scope |
| Bug | Fehlerticket, Defect | Ticket-Typ für einen Fehler, den wir verursacht haben; trägt Soll und Ist |
| Task | Aufgabe für den Ticket-Typ | Ticket-Typ für organisatorische Arbeit auf dem Board; die Aufgabe in `todo/` ist keiner |
| Support | Wartungsticket | Ticket-Typ für den laufenden Betrieb des Shops |
| Status | Zustand, Phase | wo ein Ticket auf dem Board steht |
| Done | Erledigt, Fertig | der letzte Status eines Tickets |
| Definition of Done | Fertig-Kriterien, Fertig-Spalte | wann ein Ticket Done ist: intern geprüft und dokumentiert |
| Blocker | Hindernis, Blockade | ein Ticket, an dem niemand weiterkommt; geht sofort an den Lead |
| Due Date | Fälligkeitsdatum, Deadline | bis wann ein Ticket fertig sein soll; überschritten heißt Overdue |
| Auffangbecken | Inbox, Eingang | Bereich des Boards für neue, noch nicht eingeordnete Themen |

## Shopify

Shopify-Begriffe heißen, wie Shopify sie auf englisch nennt.

| Begriff | nicht | Bedeutung |
|---|---|---|
| Plan | Tarif, Abo | die Stufe des Shops: Basic, Grow, Advanced, Plus |
| Admin | Backend, Shop-Backend | die Verwaltungsoberfläche des Shops |
| Storefront | Shopfront, Frontend allein | was der Endkunde im Shop sieht |
| Theme | Vorlage, Design | Aussehen und Aufbau der Storefront; ein Template im Theme ist eine Seitenvorlage, „Template“ allein meint das Projekt-Template |
| Section | Abschnitt, Modul | ein Bauteil eines Theme, im Theme Editor platzierbar |
| Block | Baustein, Element | ein Bauteil innerhalb einer Section |
| Theme Editor | Customizer, Baukasten | wo im Admin ein Theme angepasst wird |
| App | Plugin, Erweiterung | eine App aus dem Shopify App Store |
| Public App | App aus dem App Store, fremde App | eine App aus dem Shopify App Store als Lösungsansatz |
| Custom App | Eigenentwicklung, Individualentwicklung | eine App, die wir für einen Kunden bauen |
| Standard-Konnektor | Connector, Konnektor-App | ein fertiger Konnektor zu einem System der Systemlandschaft, etwa der Warenwirtschaft, als Lösungsansatz; nicht der Connector von Claude |
| Middleware | iPaaS, Integrationsplattform | eine Plattform, über die Daten zwischen Systemen laufen, als Lösungsansatz; welche, sagt die Knowledge Base |
| Custom Schnittstelle | Eigenbau-Schnittstelle, Individualschnittstelle | eigener Code, der Daten zwischen Systemen bewegt, laufend oder einmalig, als Lösungsansatz |
| Checkout Extensibility | Checkout-Anpassung | die Art, den Checkout zu erweitern |
| Shopify Functions | Function allein | serverseitige Logik für Rabatte, Versand, Zahlung und Prüfungen im Checkout |
| Metafield | Metafeld, Zusatzfeld, Custom Field | ein zusätzliches Feld an Produkt, Kunde, Bestellung und anderen Objekten |
| Metaobject | Metaobjekt | ein eigener Datentyp aus Metafields |
| Collection | Kollektion, Produktkategorie | eine Gruppe von Produkten im Shop |
| Variante | Variant im Text, Ausprägung | eine kaufbare Ausführung eines Produkts |
| Option | Merkmal, Auswahlmerkmal | was Varianten unterscheidet, etwa Größe; höchstens drei je Produkt |
| Markets | Länder-Setup | Shopify Markets: Länder, Sprachen, Währungen |
| PDP | Produktdetailseite, Artikelseite | die Seite eines Produkts |
| PLP | Kategorieseite, Listing | die Seite einer Collection |
| Kundenkonto | Customer Account im Text | das Konto des Endkunden im Shop |

## Technik

| Begriff | nicht | Bedeutung |
|---|---|---|
| Repo | Ablage, Projektordner | ein Git-Repository |
| Branch | Zweig | ein Entwicklungsstand neben `main` |
| Commit | Einspielung, Speicherstand | ein festgeschriebener Stand im Repo |
| Pull Request | Merge Request, Änderungsantrag | der Vorschlag, einen Branch zu mergen; kurz PR |
| Merge | Zusammenführen | einen Branch in einen anderen übernehmen |
| Release | Auslieferung, Veröffentlichung | ein getaggter Stand eines Werkzeugs |
| Deploy | Ausrollen, Einspielen | einen Stand auf eine Umgebung bringen |
| Staging | Testumgebung, Vorschau | die Umgebung vor Live |
| Live | Produktion, produktiv | die Umgebung, die der Endkunde sieht |
| Hook | Haken, Auslöser | ein Skript, das bei einem Ereignis läuft |

## Werkzeuge und Arbeit

| Begriff | nicht | Bedeutung |
|---|---|---|
| Skill | Befehl, Agent | ein Arbeitsschritt der Strecke, etwa `requirements-update` |
| Lauf | Run im Text, Durchgang | ein Skill, einmal ausgeführt, endet mit einem Commit |
| Sitzung | Chat, Konversation | eine Sitzung in Claude Code; jeder Lauf in einer neuen |
| Projekt-Repo | Kundenrepo, Datalayer im Text | das Repo eines Projekts, Quelle der Wahrheit |
| Template | Vorlage | das Projekt-Template, aus dem jedes Projekt-Repo entsteht |
| Template-Repo | Vorlagen-Repo | `strix-shopify-project-template`, das ausgelieferte Template; daraus entsteht jedes Projekt-Repo |
| Upgrade | Update | neuer Stand des Templates im Projekt-Repo |
| Projektion | Export, Sync | was ein Lauf aus dem Repo ins Sheet, Doc oder Board schreibt |
| Connector | Integration, Plugin | Anbindung von Claude an Drive, Sheets, Asana, GitHub |
| Artefakt | Seite allein, Webseite | eine veröffentlichte Seite auf claude.ai |
| Dashboard | Cockpit in neuem Text | das Artefakt eines Projekts mit Stand und Läufen |

## Oberfläche

Elemente einer Oberfläche heißen, wie sie in der Webentwicklung heißen.

| Begriff | nicht | Bedeutung |
|---|---|---|
| Button | Knopf, Schaltfläche | löst eine Aktion aus |
| Sidebar | Seitenleiste, Navigation links | die Navigation am Rand |
| Tab | Reiter | ein Umschalter zwischen Ansichten |
| Tab Bar | Tab-Leiste | die Navigation unten auf dem Smartphone |
| Card | Karte, Kachel | ein abgesetzter Block mit einem Inhalt |
| KPI | Kennzahl, Stat | eine Zahl, die den Stand zeigt |
| Detail-Panel | Inspektor, Seitenblatt | rechts die Details des gewählten Eintrags |
| Feed | Strom, Timeline | die Liste dessen, was passiert ist |
| Filter | Umschalter | schränkt eine Liste ein |
| Badge | Pille, Chip | kleines Etikett für einen Status |
| Toast | Popup, Meldung | kurze Rückmeldung nach einer Aktion |
| Modal | Dialog, Overlay | ein Fenster über der Seite |
| Übersicht | Startseite, Home | die erste Seite des Dashboards |
| mobil | am Handy | auf dem Smartphone |
| Header | Kopfzeile, Kopfbereich | der obere Bereich einer Seite oder Ansicht; im Sheet die Header-Zeile |
| Footer | Fußzeile | der untere Bereich einer Seite |
| Dropdown | Auswahlfeld, Aufklappmenü | eine Auswahl aus einer Liste |
| Checkbox | Kontrollkästchen, Haken | ein Feld zum An- und Abhaken |
| Toggle | Schalter | schaltet eine Einstellung an oder aus |
| Tooltip | Hinweisblase, Mouseover-Text | ein kurzer Text beim Hover |
| Icon | Symbol, Piktogramm | ein Bildzeichen; das Strix-Logo ist kein Icon |
| Link | Verknüpfung, Verweis | führt zu einer anderen Seite oder Stelle |
| Accordion | Klappbereich, Aufklapper | ein Abschnitt, der sich auf- und zuklappen lässt |
| Empty State | Leerzustand, leere Ansicht | was eine Ansicht zeigt, wenn nichts da ist |
| Layout | Anordnung | wie die Elemente einer Seite angeordnet sind |
| Breakpoint | Umbruchpunkt | die Breite, ab der das Layout wechselt |

## Wissen und Ablage

| Begriff | nicht | Bedeutung |
|---|---|---|
| Knowledge Base | Wissensbasis, Wissensdatenbank, Bestand als Sammelwort | `strix-shopify-knowledge-base`, das Shopify-Lösungswissen: Stamps gebauter Lösungen, Best Practices, Mindest-Standards nach Rechtsraum, Insights, Plattformgrenzen. Kein Prozesswissen, das steht in der WoW |
| Stamp | Eintrag, Karteikarte | die Einheit der Knowledge Base; einen Stamp gibt es nur dort |
| WoW | Handbuch, Wissensdatenbank allein | Way of Working: das Prozesswissen der Delivery als Prosa in Confluence, also Prozesse, Rollen, Regeln. Im Projekt-Repo heißt die Arbeitsweise des Projekts ebenso, `way-of-working.md` |
