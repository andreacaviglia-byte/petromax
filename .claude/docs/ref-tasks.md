# Aufgaben in `todo/`: lesen, schließen, anlegen

**Jeder Lauf, der ins Repo schreibt, schließt die Aufgaben, deren Arbeit er tut, und legt eine an für
interne Arbeit, die er findet und nicht selbst tut** (§359). Die Form der Datei steht in
[`datalayer-contract.md`](datalayer-contract.md), Abschnitt `todo/JJJJ-MM-TT-<slug>.md`. Fragen an
den Kunden sind keine Aufgabe, sie gehen nach `gaps/` (§279).

## 1. Lesen

Mit deinem Scope liest du die offenen Aufgaben dazu: jede Datei in `todo/` mit `status: open`, deren
`concerns` eine Kennung aus deinem Scope nennt (`REQ-…`, `EP-…`); beim Scope „alle“ jede offene.
`repo_objects.py` liest `todo/` mit den übrigen Objekten. **Ein Vorschlag zur Arbeitsweise**
(`todo/…-wow-…`) gehört nie dazu: ihn schließt nur `project-setup` (§299).

## 2. Schließen

Du schließt eine Aufgabe, wenn dein Lauf **genau die Arbeit** tut, die ihr Rumpf nennt. Ist das nicht
eindeutig, bleibt sie offen, und die Vorschau sagt, warum. Schließen heißt, im Commit des Laufs
`status: done`, `done_by` (der GitHub-Name aus `python3 "$(git rev-parse --show-toplevel)"/.claude/scripts/wow-guard.py
--whoami`, sonst der Name, den die Person nennt), `done_at` (das Datum von heute, `date +%F`) und am
Ende des Rumpfs eine Zeile `Erledigt <TT.MM.JJJJ>: <was herauskam, mit Kennung>`. Nie löschen.

Beispiel: `solution-design` über EP-007 nimmt die Anzeige des Abo-Plans im Checkout in seine Lösung
auf. Die offene Berührung wird:

```
---
title: REQ-034 (EP-009) berührt den Abo-Warenkorb in EP-007
to: so-shop
status: done
concerns: [REQ-034, EP-007]
done_by: so-shop
done_at: 2026-10-16
---

REQ-034 (EP-009) nimmt an, dass der Checkout bei einem Abo den Abo-Plan in der Positionszeile zeigt.
Prüfen, ob die Lösung in EP-007 diese Anzeige trägt; Lauf `solution-design`.

Erledigt 16.10.2026: EP-007 trägt die Anzeige des Abo-Plans in der Positionszeile (ADR-031).
```

## 3. Anlegen

Du legst eine Aufgabe an für interne Arbeit, **die nirgends sonst steht** und die ein anderer Lauf
oder ein Mensch tun muss: eine Teilung, eine Berührung zwischen Epics, eine Entscheidung, die ein
anderer Lauf nachziehen muss, eine Absprache aus dem Material. Der Rumpf sagt, was zu tun ist, warum,
mit Quelle, und welcher Lauf es tut, wenn es einer ist. Pfad `todo/<Datum>-<slug>.md`, das Datum von
heute, der Slug kurz, klein, mit `-`; `status: open`.

**Keine Aufgabe** für das, was sich aus dem Zustand der Objekte ergibt: eine Anforderung ohne
Lösungsansatz, ein Epic ohne Lösung oder Prüfpunkt, eine Frage mit `blocking: yes`, ein fehlendes
Ticket. Das zeigen `readme.md` und `project-status` selbst; als Aufgabe stünde es doppelt da und
bliebe offen, wenn der Zustand sich ändert.

Beispiel: das Transkript eines Kickoffs sagt „[00:11:48] Lead: Gut. Ich schicke euch die
Anforderungsliste zur Durchsicht.“ Daraus wird:

```
---
title: Anforderungsliste dem Kunden zur Durchsicht schicken
to: lead-a
status: open
concerns: []
---

Zugesagt im Kickoff (notes/2026-09-29-kickoff-transkript.md, 00:11:48): der Lead schickt dem Kunden
die Anforderungsliste zur Durchsicht.
```

Dagegen ist „Welche Felder die Warenwirtschaft für Händlerkunden braucht, klärt der Dienstleister des
Kunden bis 10.10.“ eine Frage an die Seite des Kunden: eine Datei in `gaps/`, keine Aufgabe. Und eine
neue Anforderung ohne Lösungsansatz im selben Lauf ist keine Aufgabe; das zeigt `readme.md`.

## 4. An wen: `to`

`to` ist der GitHub-Name einer Person aus `team` in `project.yml`, sonst ihre Projektrolle (§360). Du
löst sinngemäß auf, bevor du schreibst:

| Was du weißt | `to` |
|---|---|
| ein Name aus dem Material | `github` der Person, deren `name` ihn trägt |
| eine Rolle | `github` der Person mit dieser `role`, wenn es genau eine gibt |
| das Epic, dessen Lösung es betrifft | `Owner Strix` des Epics im Tab `Epics` über `name` auf `github`; sonst der Solution Owner, wenn es genau einen gibt |
| ein Vorschlag zur Arbeitsweise | der `project_owner` |

Gelingt es nicht, fragst du in der Vorschau nach dem GitHub-Namen. Bleibt er offen, schreibst du die
Rolle und nennst im Bericht `project-setup`, damit die Person ins Team kommt. **Jede Aufgabe hat einen
Adressaten:** fehlt er, ist das die erste Frage der Vorschau.

## 5. Vorschau und Commit

Die Vorschau hat einen Block **Aufgaben** mit drei Zeilen, leer als „keine“:

```
Aufgaben
- schließt: todo/2026-10-10-req-034-beruehrt-ep-007.md – EP-007 trägt die Anzeige des Abo-Plans
- legt an: todo/2026-10-16-anforderungsliste-durchsicht.md an lead-a
- bleibt offen: todo/2026-10-10-req-041-beruehrt-ep-007.md – Folgebestellungen nicht entschieden
```

Geschrieben wird nach dem Ja, mit den übrigen Dateien des Laufs. Die Commit-Nachricht nennt sie in
einer Zeile `Aufgaben: schließt <Datei>, …; legt an <Datei>, …`, nur wenn es eine gibt.
