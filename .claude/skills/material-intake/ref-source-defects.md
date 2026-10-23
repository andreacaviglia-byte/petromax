# Woran du merkst, dass eine Quelle unvollständig oder defekt ist

**Vier Fehler sehen aus wie gültiges Material.** Ein gekappter Text hört auf, ohne es zu sagen; eine
maschinelle Mitschrift liest sich flüssig, während ihre Substantive falsch sind; eine Datei mit fünf
Besprechungen darin sieht aus wie eine Quelle; und der Abzug eines laufenden Systems sieht aus wie ein
Dokument. Deshalb steht hier je eine Prüfung und keine Warnung.

## Die Datei, die mehrere Quellen trägt

**Eine Quelle ist eine Besprechung oder ein Dokument**, und eine gelieferte Datei ist meistens genau
das. Getrennt wird nur, was **mehrere** trägt: eine Mitschrift mit fünf Terminen hintereinander, ein
Sammeldokument aus drei Sitzungen. Der Beleg der Schnittkante sind **zwei** Kriterien, die
übereinstimmen müssen: eine Titelzeile ohne Zeitstempel und ein Rücksetzer der Zeitmarke gegenüber der
Vorzeile. Stimmen sie nicht überein, wird **nicht** getrennt, sondern die Abweichung benannt. **Eine
Titelzeile, nach der die Zeitmarke weiterläuft**, ist ein Abschnitt desselben Termins, etwa ein
Nachgespräch: die Datei bleibt eine Quelle, und die Notiz nennt den Abschnitt mit Titel und erster
Zeitmarke, damit eine Aussage von dort als Teil dieses Termins zu finden ist. Nach der
Trennung zählst du die Wörter gegen die Ausgangsdatei (`wc -w`); die Summe muss gleich sein, sonst ist
Material verloren oder doppelt.

**Der Grund ist die Beweiskraft der Spalte `Quelle`.** „Workshop ‹Titel› vom ‹Datum›" (bei `en`
„Workshop ‹title› on ‹date›", die Wendung `source_workshop`, §337) belegt nur, wenn
genau dieser Termin in genau einer Datei steht.

## Der stille Deckel

**Die gelieferte Textmenge wird gegen die Größe der Quelle geprüft**, wo beide dasselbe messen: bei
einer Textdatei, die du mit `Google_Drive.download_file_content` ohne `exportMimeType` so herunterlädst,
wie sie liegt. Die Größe steht in der Antwort von `Google_Drive.search_files`; weicht die Datei im
Temp-Ordner des Laufs davon ab, ist gekappt worden. Für Text, den `Google_Drive.read_file_content`
liefert (Google-Doc, PDF, Office), und für ein exportiertes Sheet gibt es keine vergleichbare Größe:
die Größe der Datei ist die des Originals, nicht die des Textes. Dort prüfst du, ob die letzte Zeile
ein Ende ist und der letzte Zeitstempel zur Dauer des Termins passt.

Gemessen am Drive-Connector: `read_file_content` kappt bei rund 467.000 Zeichen **ohne Meldung**.
Kommt ein Text in dieser Länge zurück, gilt er als gekappt. Gezählt werden Zeichen (`wc -m`), nicht
Bytes (`wc -c`): ein Umlaut ist ein Zeichen und zwei Bytes, und ein Vergleich in Bytes meldet einen
deutschen Text als gekappt, der es nicht ist; die Größe aus `search_files` gilt für ein Google-Doc nie. Ein Google-Doc liest du dann mit
`download_file_content` und `exportMimeType: text/plain` auf die Platte ([ref-read.md](ref-read.md)).
Bei PDF und Office liefert `download_file_content` das Original, keinen Text; eine solche Quelle steht
im Bericht als gekappt, mit der gelesenen Länge.

**Dasselbe Misstrauen gilt beim Auflisten:** bringt die Antwort von `search_files` eine weitere Seite,
holst du sie mit `pageToken`, bis keine mehr kommt.

## Die maschinelle Mitschrift

**Ist eine Quelle maschinell mitgeschrieben, ist ihr Wortlaut an den tragenden Substantiven
unzuverlässig**: Systemnamen, Fachbegriffe und Mengen, nicht die Füllwörter.

- **Löse auf, was der Zusammenhang sicher hergibt**, und schreib die Auflösung in die Notiz und in die
  Zeile, die sie braucht. Der Text in `inputs/` bleibt wörtlich; eine geglättete Kopie machte das
  Sichere und das Geratene ununterscheidbar.
- **Was nicht sicher ist, wird nicht geraten**; es steht unter `Offen` in der Notiz.
- **Ein Personenname an der Stelle eines Sachworts ist derselbe Fehler.** Gemessen an einem echten
  Projekt: „Bei uns gibt es \[Name]" meinte den Baukasten, „Add to \[Name]" meinte Add to Cart. Solche
  Stellen werden je Vorkommen entschieden, nie über die Zeichenkette.
- **Dieselbe Menge in zwei Lesarten ist keine Menge.** Gesprochen „8, 9" wurde zu „89". In einer
  Anforderung wäre das falsch, als offener Punkt der Notiz ist es richtig.

## Die Zuschreibung an einen Sprecher

**Zeitmarke und Wortlaut tragen, die Person davor nicht.** In maschinellen Mitschriften sitzt der
Sprecherwechsel an mehreren Stellen eine Zeile zu früh oder zu spät. Wer etwas wollte, steht deshalb
nur dort in der Notiz, wo der Wortlaut es trägt.

## Der Abzug eines laufenden Systems

**Ein Board, ein Ticketsystem, ein Export zeigt seinen Stand am Tag des Lesens.** Er ist kein
Dokument: ein Dokument hält fest, was zu seinem Datum gesagt wurde, ein Abzug hält fest, wie weit
jemand seither gekommen ist. Zu erkennen ist er an Feldern, die es in einem Dokument nicht gibt: ein
Zähler erledigter Zeilen, eine Spalte, ein Status.

**Seine Zeilen belegen Arbeit, nicht Wollen.** Ein solcher Abzug **beantwortet deshalb keine Frage,
die eine andere Quelle offen führt**. Was er trägt, ist der Rand: dass ein Thema vorkommt, wie es dort
heißt, und welche Wünsche unstrukturiert dort liegen. In der Notiz steht ein Wunsch daraus unter
`Berührt`, mit Schlüssel oder Zeile als Beleg, was er als erledigt führt, unter `Heute`, und nie etwas
davon unter `Entschieden`.

Ein Jira-Ticket ist ein solcher Abzug, und ein Sheet eines früheren Vorhabens auch: seine
ausgeklammerten Zeilen sind Material des neuen, keine Vorlage. Die Notiz nennt das alte Sheet und seine
IDs, damit `requirements-update` die Herkunft in der `Quelle` führen kann.
