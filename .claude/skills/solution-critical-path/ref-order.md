# Die Reihenfolge des Bauens: Abhängigkeiten, Stufen, `epics/critical-path.md`

**Nach den Lösungen leitest du die Reihenfolge ab, in der die Epics gebaut werden** (§318), über alle
Epics des Vorhabens, aus den gelösten Anforderungen, wie sie im Repo stehen. Sie steht in
`epics/critical-path.md`, nicht im Sheet. Die Reihenfolge des Lösens ist eine andere: sie steht in
`solve_order` der Epics und setzt `solution-solve-order`. **Die Reihenfolge des Bauens gilt als
Empfehlung für die Umsetzung; ob die Umsetzung ihr folgt, entscheiden die Fachleute** (§267). `ticket-factory` schreibt
aus der Datei je Epic-Ticket eine Zeile, und `solution-review` hält neue Abhängigkeiten aus den
Lösungen gegen sie.

## Je Anforderung

| Feld | Inhalt |
|---|---|
| Rolle | `Grundlage`, wenn andere Anforderungen auf ihr bauen; `Konsument`, wenn sie auf anderen baut; beides ist möglich |
| hängt ab von | IDs, mit dem Beleg |
| wird gebraucht von | IDs, mit dem Beleg |
| Blocker | was sie aufhält, mit Adressat und Belegstand: `belegt` (eine offene Frage in `gaps/` mit `blocking: "yes"`, die sie in `concerns` nennt, oder eine Stelle in einer Notiz) oder `vermutet` |

**Eine Kante kommt aus `depends_on` einer gelösten Anforderung** (`solution_status: decided`, §318):
sie baut auf den genannten Anforderungen, Epics und ADRs auf (Datalayer-Vertrag); das setzt
`solution-design` mit der Lösung. Eine Anforderung ohne Lösung trägt keine Kante. **Eine Kennung im Text von
`## Description` ist keine Kante**; sie steht in der Datei als Berührung. Eine offene Frage hält eine
Anforderung auf, ist aber keine Kante zwischen Epics: sie steht als Blocker da.

## Die Stufen

Aus den Abhängigkeiten der Anforderungen werden Kanten zwischen Epics: Epic A wartet auf Epic B, wenn
eine Anforderung von A von einer Anforderung von B abhängt. Du schreibst sie in `deps.tsv`
(Kopfzeile `wartet<TAB>auf<TAB>Beleg`), eine Kante je Zeile, jede mit Beleg, und rechnest die Stufen:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/order-stages.py . deps.tsv
```

Die Epics liest das Script aus `epics/`, ohne `merged` und `dissolved`; ein Epic, das dort fehlt, legt
`epic-structure` an, nicht dieser Lauf. Eine Kante ohne Beleg oder mit einem Epic, das nicht in `epics.tsv` steht,
lehnt das Script mit Exit 1 ab; du ergänzt den Beleg oder streichst die Kante und rechnest neu.

Die Stufen beginnen bei 1; ein Epic ohne Kante steht in Stufe 1. **Die Abhängigkeiten sind harte
Grenzen**: kein Epic steht vor einem, auf das es wartet, und kein Grund unten verschiebt eine Stufe.
**Innerhalb einer Stufe ordnest du** nach diesen Gründen, in dieser Folge, und nennst je Epic den
Grund mit seiner Stelle:

1. **Risiko zuerst.** Ein Epic, dessen Lösungsansatz scheitern oder andere Epics umwerfen kann, steht vor einem
   sicheren: eine offene Fundament-Frage, eine Anbindung an ein Fremdsystem, eine Grenze der Plattform,
   eine Lieferung von Dritten. Riskant ist ein Epic nur mit einer Stelle im Repo oder in einer Notiz.
2. **Schmal vor breit.** Ist ein riskantes Epic breit, schlägst du einen **Durchstich** vor: die
   schmalste Strecke durch das Risiko, eine Anforderung für ein Produkt, einen Markt oder einen
   Datenstrom von Anfang bis Ende, die zeigt, ob der Lösungsansatz trägt, bevor die Breite gelöst wird. Ein
   Durchstich ist ein Vorschlag in der Datei, kein Epic und kein Schnitt.
3. **Kernprozesse vor Features.** Ein Epic, ohne das der Shop nicht verkauft (`domain`
   `basic_setup`, `product_data`, `cart_checkout`, `markets_shipping`, `customer_account`), steht
   vor einem, das ihn ergänzt.
4. **Baselines gehen mit ihrem fachlichen Epic.** Eine Anforderung aus dem Standard-Leistungssatz wird
   mit dem Epic gelöst, dessen Ablauf sie betrifft, nicht als Block am Ende; ein Epic, das nur solche
   Anforderungen trägt, etwa in `legal_consent`, nennt in `Grund der Folge` das fachliche Epic, mit dem es
   gelöst wird.
5. **Migration in Stufen.** Datenmigration steht je Datenobjekt, nicht als Block am Ende: ein Objekt,
   auf das andere verweisen, vor ihnen (Produkte und Kunden vor der Bestellhistorie), die
   Weiterleitungen nach dem Epic, das die neuen Adressen festlegt. Als Kante zählt das nur mit Beleg;
   ohne ihn ist es ein Grund der Folge.
6. **Dann** die Zahl der wartenden Epics, die Vorlaufzeit externer Antworten und harte Termine.

**Einen Zyklus meldest du, du löst ihn nicht auf**: die Datei nennt die Kanten mit ihrem Beleg, und
der Lead entscheidet.

Das Script gibt unter den Stufen den **kritischen Pfad** aus, jede längste Kette belegter Kanten, und
je Epic die **Zeile im Epic-Ticket**: `Stufe ‹n› · wartet auf ‹EP-…›, ‹EP-…›`, ohne Kante nur
`Stufe ‹n›`, im Zyklus `keine Stufe`; bei `language: en` `Stage ‹n› · waits for ‹EP-…›`, `Stage ‹n›`,
`no stage` (`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Die festen Wendungen, §337). Das
Script liest die Sprache aus `project.yml`. Beide übernimmst du Zeichen für Zeichen in die Datei; die Zeile
schreibst du nie von Hand.

**Eine offene Fundament-Frage** zieht die Epics ihrer treibenden Anforderungen nach vorn. Ändert eine
Antwort die Kanten, rechnest du je Variante (`deps-theme.tsv`, `deps-headless.tsv`) und zeigst beide
Reihenfolgen; ändert sie nichts, reicht eine.

## Die Datei

`epics/critical-path.md`, je Lauf ganz neu geschrieben, auch wenn sich nichts geändert hat, in der
Form des Datalayer-Vertrags `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
`epics/critical-path.md`: `solution-review` und `ticket-factory` lesen sie (§325).
