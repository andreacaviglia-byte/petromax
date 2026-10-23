# Die Systemlandschaft

**Dieser Vertrag setzt die Regeln der Systemlandschaft** (§325): `requirements-update` schreibt sie
in `architecture.md`, `material-intake` in `customer.md`, solange es `architecture.md` nicht gibt.

Die Systemlandschaft sind die Systeme, die das Material nennt: die Plattform und was um sie herum
steht, bevor eine Lösung ein einzelnes davon anfasst. Je System eine Aussage: Name, was es in
**diesem** Projekt tut, und was mit ihm geschieht. **Sie steht in `architecture.md`**, eine
Zeile je System ([datalayer-contract.md](datalayer-contract.md), `architecture.md`), in jedem Vorhaben (§282). Nur solange es
die Datei nicht gibt, steht sie in `customer.md` unter der Überschrift `Systemlandschaft`, mit der
Quelle am Ende; das schreibt `material-intake`.

```
| System business_central: führt Artikelstamm und Bestände, liefert beides an den Shop. Bleibt | belegt | Workshop ‹Titel› vom ‹Datum› | |
```

Die Quelle steht als feste Wendung in der Sprache aus `language` (`source_workshop`, bei `en`
„Workshop ‹title› on ‹date›“, [datalayer-contract.md](datalayer-contract.md), Die festen Wendungen, §337).

## Sechs Kanten, an denen die Liste sonst schrumpft oder anschwillt

- **Die Plattform selbst gehört hinein.** Ohne ihre Mitte stünde bei einem abgelösten System der
  Nachfolger nirgends.
- **Eigentum entscheidet nicht.** Das ERP, das der Kunde selbst betreibt und das bleibt, ist genau das,
  an dem die erste Frage nach einer Schnittstelle hängt.
- **Shopify-Apps gehören nicht hinein.** Sie laufen im Shop; eine Bewertungs-App wird eine Anforderung.
- **Werbe- und Trackingplattformen gehören hinein.** Eigenes Konto, eigener Datenweg.
- **Ein Werkzeug, das einmal läuft, gehört nicht hinein**, etwa ein Migrationswerkzeug. Es steht in der
  `Beschreibung` der Anforderung, die es benutzt.
- **Ein Kandidat gehört nicht hinein.** Ein Name, den das Material einmal als Alternative nennt, steht
  in der Frage, in der über ihn entschieden wird.

## Was mit einem System geschieht

Eines von fünf Wörtern: **bleibt** · **abgelöst durch ‹System›** · **entfällt** (ersatzlos) · **neu**
(kommt mit dem Projekt) · **offen**. Führe nie eine Ist- und eine Soll-Liste nebeneinander; sie driften.

- „abgelöst", „entfällt" und „neu" sagen, dass jemand entschieden hat: dazu gibt es eine ADR oder eine
  Quelle, die es sagt. **Ohne Beleg ist es „offen"**, und ob ein Altsystem abgelöst wird, ist eine
  Frage an den Kunden, die Notiz und Bericht nennen.
- **„entfällt" und „abgelöst" sind nicht dasselbe:** beim Wegfall ohne Nachfolger fällt beim Umschalten
  auf, was das System nebenbei noch tat. Der Nachfolger darf der Shop selbst sein.
- **Nur im Ist genannt und über die Zukunft schweigend heißt „offen"**, nur im Soll genannt heißt „neu".
- **„bleibt" ist kein Nullfall.** Nennt das Material einen Lösungsansatz, der nicht genommen wurde, etwa ein
  erwogenes und verworfenes Werkzeug, eine gesparte Anbindung oder die Grenze einer Migration, ist
  auch „bleibt" eine gefallene Wahl und bekommt eine ADR; die Zeile trägt dann `entschieden`.
  Nur wo das Material über jede Alternative schweigt, genügt die Quelle in der Zeile.
- **Eine Antwort, die zeigt, ist eine Antwort.** „siehe oben", „dito", „wie bisher", „unverändert",
  „alle" tragen die Liste, auf die sie zeigen, in voller Länge: du löst den Zeiger auf und schreibst
  das Wort an jedes System darin. Auf die Frage nach dem Sollzustand ist „wie bisher" ein „bleibt" für
  den ganzen Stapel, keine Wiederholung des Ist.
- **Prüf jede Angabe gegen die jüngste Quelle, die das System nennt**, und nenne sie in der Zeile.
  Jünger schlägt älter nur, wo beide dieselbe Frage beantworten.
- **Schweigen ist keine Antwort.** Nennt eine jüngere Quelle ein System nur beiläufig, gilt weiter, was
  die ältere über seine Zukunft sagt; ausschließen müsste die jüngere es ausdrücklich. Eine Antwort, die
  vier von acht Systemen aufzählt, beantwortet die Frage für vier und schließt die anderen nicht aus.
  Wo keine Quelle über die Zukunft spricht, bleibt „offen" richtig.
- **Zwei Quellen derselben Sitzung trennt kein Alter.** Ein Dokument, das im Termin gezeigt, und die
  Mitschrift dieses Termins sind gleich alt; widersprechen sie sich, ist das eine Frage, keine
  Korrektur.

**Eine Wahl schneidet den Lösungsansatz, nicht das System.** „Wir binden den Tag Manager ein, alles Weitere steuert
der Kunde daraus" legt den Lösungsansatz für jedes Werkzeug im Container fest: sie tragen dasselbe Wort, und eine
ADR nennt sie alle.

## Der Name

Klein, mit `_` verbunden, dieselbe Schreibweise in jeder Anforderung, jeder ADR und jeder Notiz. Trägt das
Material mehrere Namen für dasselbe System, entscheidest du **eine** Form, und die Varianten stehen in
der Notiz der Quelle. Welches Produkt gemeint ist, wird nie geraten: ohne Beleg entsteht eine Frage.
