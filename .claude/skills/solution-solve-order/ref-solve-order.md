# Die Reihenfolge des Lösens: was den größten Fehler verbergen kann

**Gelöst wird zuerst, was den größten Fehler verbergen kann** (§318); gebaut wird später in einer
eigenen Reihenfolge (`solution-critical-path`). Je Epic setzt du `solve_order`, eine Zahl ab `1`,
über alle Epics des Vorhabens, nach jedem Schnitt und Nachschnitt neu geprüft; Epics verschiedener
Workstreams dürfen dieselbe Zahl tragen. In dieser Folge:

1. **Fundament-Epics zuerst**: Epics, deren Anforderungen eine Zeile des Fundaments in
   `architecture.md` treiben oder an einer offenen Fundament-Frage hängen (§17): Shops, Bauform der
   Storefront, Integrationsschicht, Systemlandschaft, die `epic-structure` aufnimmt (§216).
2. **Dann Epics mit einer blockierenden offenen Frage**: eine Frage in `gaps/` mit `blocking: yes`,
   die eine Anforderung des Epics oder das Epic in `concerns` nennt.
3. **Riskante Themen schmal vorn**: ein Epic, dessen Lösungsansatz an einer Grenze der Plattform, einem
   Fremdsystem oder einer Lieferung von Dritten scheitern kann, mit einer Stelle im Repo oder in einer
   Notiz; ist es breit, nennst du im Plan einen Durchstich, die schmalste Strecke durch das Risiko.
4. **Dann die übrigen**, Kernprozesse vor Features.

Ein Grund zählt nur mit seiner Stelle; der Plan nennt sie je Epic. Die Reihenfolge ist eine
Empfehlung für `solution-design`, kein Tor (§148).
