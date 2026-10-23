# Die Wissensbasis — wie ein Lauf sie liest und was gilt

Die Wissensbasis ist das Repo `webweit-gmbh/strix-shopify-knowledge-base`, **eine Quelle wie
Material und Doku** (§326). Aus ihr lesen `solution-approach` und `solution-design` die Lösungs-Stamps
und die Best Practices für die Art eines Lösungsansatzes, `requirements-update` den Standard-Leistungssatz eines
Rechtsraums unter `minimum-standard/`. **Dieser Vertrag sagt, wie gelesen wird und was davon gilt**;
wie die Wahl ausgeht, sagt [`solution-choice-contract.md`](solution-choice-contract.md), und was ein
Lauf tut, wenn die Wissensbasis nicht erreichbar ist, seine Ref.

## Der Weg

Nur über GitHub mit `get_file_contents` auf `webweit-gmbh/strix-shopify-knowledge-base`; in einer
Cloud-Sitzung hängst du das Repo vorher mit `add_repo` an, `access: read`, ohne Klon, sonst lehnt die
Sitzung das Lesen ab (gemessen am 04.10.2026). **Die Antwort von `add_repo` verlangt einen Klon**
(„Clone it NOW“, mit Befehl und `register_repo_root`); **den führst du nicht aus**: nach `add_repo`
liefert `get_file_contents` das Repo ohne Klon (gemessen am 10.10.2026), und ein Klon lädt die ganze
Wissensbasis, wo der Lauf nur `index.md` und wenige Dateien braucht. Im Projekt-Repo liegt die
Wissensbasis nicht; eine Suche dort findet nichts. Eine Codesuche über das Repo benutzt du nicht; sie
liefert auf dem privaten Repo keine Treffer.

## Was gelesen wird

| Datei | wer | wofür |
|---|---|---|
| `index.md` | jeder Lauf zuerst | er nennt jeden Stamp je Domäne und ist damit die Ordnerliste |
| die Stamps, die zu einem Lösungsansatz passen, jeder ganz | `solution-approach`, `solution-design` | Lösungsansatz, Einstellungen, Fallstricke, Größe des Erstbaus |
| `best-practices/` für die Art des Lösungsansatzes: `apps.md` für eine Public App, `integrations.md` für eine Schnittstelle, und die übrigen Dateien dort, wo sie zur Art passen | `solution-approach`, `solution-design` | bevorzugte und ausgeschlossene Apps, welche Middleware |
| `minimum-standard/<kennung>.md` | `requirements-update` | der Standard-Leistungssatz eines Rechtsraums |
| `network/allowlist.md` | jeder Lauf, der einen Beleg liest, nur wenn ein Host gesperrt ist | ob der Host in der Allowlist steht, mit ihrem Stand (§341, `connector-contract.md`, Abschnitt „Die Doku von Shopify“) |

**Geprüft heißt gelesen**: ein Treffer im Index, den du nicht geöffnet hast, ist kein `kb_match`, und
eine Best Practice, die du nicht gelesen hast, gilt nicht.

## Was gilt

**Ein Stamp ist ein Startpunkt, kein Beleg.** Er trägt sein Messdatum und oft `api_version: unknown`;
**bei `api_version: unknown` prüfst du jede Plattformaussage vor der Übernahme gegen die Doku**, und
eine Plattform-Eigenschaft, die er behauptet, bestätigt die Doku, bevor sie in die Lösung wandert.
**Ein Stamp deckt nur, wenn sein `requires` im Projekt erfüllt ist**: Plan, Theme, Systeme.

**Wiederverwendet werden Lösungsansatz, Einstellungen und Fallstricke, kein Code aus einem anderen
Kundenprojekt.** Die `source_url` eines Stamps öffnest du nie, auch nicht, um einen Treffer zu prüfen
(KB §117): sie führt oft auf das Ticket eines anderen Kunden, und was du dort liest, landete im
Entwurf; der Stamp selbst ist der Stand, den die Wissensbasis freigibt.

**Die Best Practices gelten für die Wahl** (§326):

- **Eine ausgeschlossene App wird nicht vorgeschlagen**, weder als Lösungsansatz noch als Kandidat. Will der
  Lead sie, ist das eine Entscheidung mit ADR, die den Ausschluss nennt.
- **Eine bevorzugte App steht in der Evaluierung einer Public App immer unter den Kandidaten** (§320).
- **Welche Middleware**, sagen die Best Practices; im Template steht kein Name. Die Wahl ist eine
  Entscheidung des Projekts mit ADR und der Zeile `Integrationsschicht` in `architecture.md` (§216,
  §324).

## Die Größe der Wiederverwendung

**Für einen Stamp gilt die Größe im Projekt, nicht die des Erstbaus.** `effort_estimated` des Stamps
ist die Größe des Erstbaus; heruntergerechnet wird sie mit `reusability`:

| `reusability` | Größe im Projekt |
|---|---|
| `1` | ein bis zwei Stufen kleiner |
| `2` | etwa eine Stufe kleiner |
| `3` | wie der Erstbau |

**Hoch geht sie**, wo `sensitive_to` im Projekt stärker ausfällt, etwa mehr Märkte, mehr Varianten,
ein anderes System, oder wo die Lösung deutlich mehr leistet als verlangt. Der Lösungsansatz nennt
beide Größen, „SOL-2026-001, Erstbau M, hier S“ ([`solution-choice-contract.md`](solution-choice-contract.md),
Die Größe je Lösungsansatz).

**In der ADR der Wahl** steht ein Stamp oder eine Best Practice, die zur Wahl stand: genommen,
angepasst mit Abweichung und Grund, oder unter `## Verworfene Optionen`, je mit dem Größenvergleich.
Eine eigene ADR für die Abweichung von der Wissensbasis gibt es nicht.

## Die drei Werte

Was ein Lauf über einen Lösungsansatz aus der Wissensbasis festhält, ist genau einer von drei Werten (§268):

| Wert | heißt |
|---|---|
| `KB: ‹Kennung› ‹Kurztitel›` | der gelesene Lösungs-Stamp |
| `KB: keiner`, bei `en` `KB: none` | die Wissensbasis ist gelesen, und keiner trägt |
| `KB: nicht gelesen`, bei `en` `KB: not read` | sie war im Lauf nicht erreichbar |

Die beiden letzten stehen in der Sprache aus `language` (`kb_line_none`, `kb_line_unread` in
[Die festen Wendungen](datalayer-contract.md#die-festen-wendungen), §337); ein Lauf, der sie liest,
erkennt beide Formen.

„kein Fund in der Wissensbasis" und „nicht nachgesehen" sind verschiedene Auskünfte und stehen
verschieden da. Wo der Wert steht, sagt der Vertrag der Anforderungsliste
([`requirements-list-contract.md`](requirements-list-contract.md), `Lösungsoption 1` bis `3`).
