# Die Prüfungen und der Bericht

Jede Prüfung läuft über **alle** gelesenen Lösungen des Vorhabens. Im Umfang steht ein Befund, wenn
mindestens eine seiner Stellen zu einem Epic im Umfang gehört; ein Befund zwischen zwei Epics
außerhalb steht nur, wenn der Umfang „alle“ ist. **Summen und Grenzen je Shop (1) und
Wechselwirkungen (2) prüft nur der Lauf über alle** (§305): eine Summe hängt an keiner Anforderung,
und eine Wechselwirkung bewertet die Lösung eines anderen Workstreams mit. Ausgenommen ist der
„Verweis ins Leere“ aus 2: er hängt an einer Anforderung und läuft in jedem Umfang. Gezählt und
geprüft werden nur die Anforderungen, die [ref-read.md](ref-read.md) dafür nennt.

**Ein Befund nennt immer zwei gelesene Stellen**: Epic und Überschrift im Rumpf von
`epics/EP-NNN.md`, Anforderung und Abschnitt oder Feld ihrer Datei, die Zeile in `architecture.md`,
eine Datei in `gaps/` oder `todo/`, eine Zeile in `epics/critical-path.md` oder eine Zelle des Sheets. Was du nur vermutest, steht als Frage an den Lead, nie als Befund.

## 1 — Summen und Grenzen je Shop (§110), nur im Lauf über alle

**Gezählt wird, was die Lösungen zusammen anlegen, je Shop aus `shops` in `project.yml`.** Der Shop
selbst wird nicht gelesen: die Zahl, die zählt, ist die, die wir erzeugen. Ist `shops` leer, zählst
du einmal für das Vorhaben, Spalte `Shop` „noch offen“, gegen beide Pläne. Eine Anforderung zählt für
die Shops, die ihr Feld `shops` nennt; ist es leer, für alle (§307).

| Gegenstand | Gezählt aus |
|---|---|
| Metafeld-Definitionen, je Eigentümer (Produkt, Variante, Kunde, Bestellung, …) | `## Details` und `## Approach`, die ein Metafeld anlegen |
| Metaobjekt-Definitionen | wie oben |
| Varianten je Produkt und Optionen je Produkt | Lösungsansätze, die eine Achse oder Variante hinzufügen |
| installierte Apps | jede App, die ein Lösungsansatz einführt, einmal je Shop, auch wenn mehrere Epics sie nennen |
| Erweiterungen am Checkout und Functions | je Art und Zielpunkt |
| Aufrufe gegen ein Ratenlimit | Lösungsansätze mit Synchronisation oder Import, mit der Menge, die `## Details` nennt |

Je Summe hältst du die Grenze aus der Dokumentation dagegen, mit Fundstelle. **Hängt eine Grenze am
Plan**, nimmst du `plan` des Shops aus `project.yml`; ist er leer, gilt die Summe gegen beide Pläne
und der Bericht sagt das. Eine Summe über 80 Prozent der Grenze nennst du als Hinweis, eine darüber
als Befund. **Ohne gefundene Grenze** steht die Summe mit „Grenze nicht gefunden“; sie ist eine
Beobachtung, kein Befund.

## 2 — Wechselwirkungen, nur im Lauf über alle

| Befund | Woran du ihn erkennst |
|---|---|
| dieselbe Stelle, zwei Absichten | zwei Lösungsansätze ändern dasselbe Objekt, Feld, Template, denselben Checkout-Schritt oder dieselbe Datenstrecke, und die Änderungen schließen sich aus oder hängen voneinander ab, ohne dass `depends_on` es nennt |
| Aufbau auf ungelöstem Grund | ein Lösungsansatz baut laut `Relations and Prerequisites` oder `depends_on` auf einem Epic, dessen Anforderungen `solution_status` leer, `proposed` oder `blocked` tragen, oder das keine Lösung hat. **„Baut auf“ heißt: ohne das andere Epic trägt der Lösungsansatz nicht** („folgt der Migration in EP-004“, „setzt die B2B-Preise aus EP-002 voraus“). Eine gemeinsame Stelle ohne Aufbau zählt nur als „dieselbe Stelle, zwei Absichten“ |
| Reihenfolge ohne Richtung | zwei Lösungsansätze setzen einander voraus |
| Verweis ins Leere | `depends_on` nennt eine Kennung oder ADR, die es im Repo nicht gibt |

**Eine Berührung** ist der leichte Fall der ersten Zeile: eine Anforderung eines Epics fasst eine
Stelle an, die ein anderes Epic trägt, ohne dass sich die Absichten ausschließen, und weder
`depends_on` noch `Relations and Prerequisites` des anderen Epics nennt sie. Sie steht im Bericht
gesondert und wird nach dem Ja eine Aufgabe in `todo/` (Step 6 der SKILL.md).

**Gegen die Reihenfolge** (§267): baut ein Lösungsansatz auf einem anderen Epic, und `epics/critical-path.md`
trägt diese Kante nicht, hat sich die Abhängigkeit im Design neu gezeigt. Du nennst sie mit der Stelle
in der Lösung und den Stufen beider Epics laut Datei und sagst, ob sie die Reihenfolge verschiebt: ja,
wenn das wartende Epic in derselben oder einer früheren Stufe steht als das, auf das es wartet. **Neu
geplant wird nicht**; eine Verschiebung führt `solution-critical-path`. Gibt es die Datei nicht, steht unter
dem Abschnitt „Keine Reihenfolge gelesen.“

## 3 — Dasselbe Problem verschieden gelöst

| Befund | Woran du ihn erkennst |
|---|---|
| zwei Apps für einen Zweck | zwei Lösungsansätze führen verschiedene Apps für dieselbe Aufgabe ein (Bewertungen, Filter, Übersetzung, Abonnements, …) |
| zwei Muster für eine Art Daten | dieselbe Art Daten liegt in einem Lösungsansatz als Metafeld, in einem anderen als Metaobjekt oder in einer App |
| zwei Schlüssel oder zwei Master | zwei Lösungsansätze führen für dasselbe Objekt verschiedene Kennungen oder verschiedene führende Systeme |
| ein Lösungsansatz, zwei Formen | dieselbe Anbindung oder Logik steht in einem Lösungsansatz als Function, in einem anderen als App oder Theme-Logik |

Im Bericht nennst du beide Lösungen mit ihren Owner, ohne zu sagen, welche sich anpasst; das klärt der
Lead mit `grill-me` (Step 6 der SKILL.md).

## 4 — Jede Lösung gegen `architecture.md` (§216)

| Befund | Woran du ihn erkennst |
|---|---|
| Architektur fehlt | `architecture.md` gibt es nicht, oder eine der vier Zeilen des Fundaments fehlt |
| baut auf einer überholten Zeile | die Lösung nennt eine ersetzte Aussage, und `clarification` ihres Epics trägt `Nachprüfen:` ohne `Nachgeprüft:`, bei `en` `Recheck:` ohne `Rechecked:` (§337) |
| baut auf offenem Grund | der Lösungsansatz setzt eine Zeile mit Status `offen` oder `widersprüchlich` als gegeben, ohne zu nennen, unter welcher Variante er gilt |
| widerspricht der Architektur | der Lösungsansatz sagt anderes als eine Zeile mit Status `belegt` oder `entschieden` |
| legt fest, ohne Zeile | der Lösungsansatz legt etwas fest, das andere Epics betrifft (ein Master, ein Muster, eine App, eine Function, ein Schlüssel), und `architecture.md` trägt keine Zeile dazu (§216) |
| fehlt unter `gestützt von` | der gewählte Lösungsansatz baut auf einer Zeile, und sein Epic steht dort nicht unter `gestützt von`; dieselbe Regel, nach der `solution-design` ein Epic dort einträgt (Datalayer-Vertrag, `architecture.md`). Nennt die Lösung eine Zeile nur als offen, als Variante oder als Berührung, oder ist noch kein Lösungsansatz gewählt, ist das kein Befund |
| Architekturfrage ohne Ziel | eine Zeile `offen` oder `widersprüchlich` nennt in `Quelle/ADR` keine Frage `GAP-NNN`, oder die genannte ist geschlossen oder nennt in `concerns` keine Anforderung |

## 5 — Epic-Datei gegen Anforderung

`Technical Information` einer Zeile im Rumpf und der erste Lösungsansatz in `## Approach` derselben
Anforderung nennen verschiedene Lösungsansätze; oder eine Anforderung, deren `epic` das Epic nennt, fehlt unter
`Requirements` und steht nicht unter `Discarded`; oder eine Zeile nennt eine Anforderung, deren `epic`
ein anderes Epic nennt. Beide Stellen schreibt `solution-design`; der Befund geht an ihn.

## 6 — Lösungsansätze ohne gelesene Wissensbasis (§268)

Jeder Lösungsansatz in `## Approach` einer Anforderung im Umfang, dessen Zeile `KB: nicht gelesen` oder `KB: not
read` ist (`kb_line_unread` in beiden Sprachen, §337), ist ein
Befund: der Lösungsansatz wurde ohne die Wissensbasis gewogen, und ein Stamp kann die Empfehlung noch ändern,
bevor sie ins Proposal geht. Dieser Befund hat nur eine Stelle, den Lösungsansatz: was ihm fehlt, ist gerade
die zweite Lesung. `führt` ist `solution-design`, in einer Sitzung, die die Wissensbasis erreicht.

## 7 — Offen vor dem Proposal

| Befund | Woran du ihn erkennst |
|---|---|
| blockierende Frage | eine Frage in `gaps/` mit `status: open` und `blocking: yes`, deren `concerns` eine Anforderung oder ein Epic im Umfang nennt |
| offene Aufgabe | eine Datei in `todo/` mit `status: open`, deren `concerns` eine Kennung im Umfang nennt; beim Umfang „alle“ jede offene |
| Must-have, aber Out of Scope | eine Anforderung im Umfang mit `status` `open` oder `confirmed`, `priority: must-have` und `scope: out_of_scope` (§327): der Kunde braucht sie, und sie wird nicht gebaut |

Dieser Befund hat eine Stelle, die Datei. `führt` ist bei einer Frage `to` aus ihrem Kopf, geschlossen
wird sie nur über `requirements-update` aus Material (§276, §279); bei einer Aufgabe `to` aus ihrem Kopf;
bei „Must-have, aber Out of Scope“ der Lead, der es mit dem Kunden klärt: ändern tut sich `priority`
oder `scope` nur über Material und `requirements-update`, und das Proposal nennt sie unter „Nicht im
Scope“ mit Grund.
Ein Vorschlag zur Arbeitsweise an den `project_owner` (§289) gehört nicht zum Umfang.

## Der Bericht

Die Form steht in `${CLAUDE_SKILL_DIR}/../../docs/ref-run-scope.md`, 5; die Abschnitte dieses Laufs:

```markdown
# Solution Review ‹Vorhaben› — ‹Umfang›

Stand vom ‹TT.MM.JJJJ HH:MM›; Anforderungsliste gelesen am ‹TT.MM.JJJJ HH:MM Zeitzone› oder „keine Anforderungsliste“.
Gelesen: ‹n› Lösungen. Im Umfang: ‹Epic-IDs›.

## Im Umfang

### Summen und Grenzen je Shop
‹ist der Umfang nicht alle, statt der Tabelle: „Nur im Lauf über alle (§305).“›
| Shop | Gegenstand | Summe | aus | Grenze | Fundstelle | Befund |

### Wechselwirkungen
‹ist der Umfang nicht alle: nur Zeilen „Verweis ins Leere“, darunter „Übrige Wechselwirkungen, Berührungen und neue Abhängigkeiten nur im Lauf über alle (§305).“, und die zwei folgenden Abschnitte entfallen›
| Befund | Stelle 1 | Stelle 2 | Epics und Owner | führt |

### Berührungen
| Anforderung und Epic | Stelle im anderen Epic | Epic und Owner | führt |

### Neue Abhängigkeiten gegen die Reihenfolge
| Abhängigkeit | Stelle in der Lösung | Stufen laut critical-path.md | verschiebt | führt |

### Dasselbe Problem verschieden gelöst
| Befund | Stelle 1 | Stelle 2 | Epics und Owner | führt |

### Gegen architecture.md
| Befund | Zeile in architecture.md | Stelle in der Lösung | Epic und Owner | führt |

### Epic-Datei gegen Anforderung
| Befund | Stelle im Epic | Stelle in der Anforderung | Epic und Owner | führt |

### Wissensbasis nicht gelesen
| Anforderung | Lösungsansatz | Epic und Owner | führt |

### Offen vor dem Proposal
| Datei | Art | Kurztext | betrifft | führt |

## Aus dem Rest, berührt den Umfang
| Befund | Stellen | Epic und Owner, von dem er kommt | führt |

## Nicht geprüft
| Epic, Anforderung oder Grenze | Grund |

## Fragen an den Lead
- ‹Frage, mit der Stelle, an der sie entstand›
```

`führt` nennt den Skill oder Menschen, dem die Stelle gehört (Step 7 der SKILL.md). Der Owner eines
Epics ist `Owner Strix` aus dem Tab `Epics`; ist die Zelle leer oder gibt es kein Sheet, steht „ohne
Owner“. Ein Abschnitt ohne Befund trägt statt der Tabelle den Satz „Kein Befund.“; ist der Umfang
alle, entfällt „Aus dem Rest“. Die Tabellen bleiben im Chat; in eine Datei oder ein Dokument schreibst
du sie nicht. Ins Repo gehen daraus nur Fragen und Aufgaben, nach Step 6 der SKILL.md.
