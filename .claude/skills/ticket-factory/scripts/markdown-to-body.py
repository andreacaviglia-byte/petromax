#!/usr/bin/env python3
"""Setzt einen Ticket-Text aus der Vorlagenform in den Body des Kanals um.

Aufruf: markdown-to-body.py <datei|->

Die Vorlage in 'ref-ticket-templates.md' ist Markdown ('## Kunde', '- Punkt'),
das Feld des Kanals ist Rich Text. **Dazwischen fehlte das Stück, das
umsetzt** — und ohne es landet die Auszeichnung als Zeichenkette auf einem
Board, das der Kunde sieht: gemessen an elf Tickets, die als '## Kunde'
dastanden (v0.1, 16.08.2026).

Drei Regeln des Kanals, alle gemessen (ref-asana.md):
  * genau EIN Wurzelelement '<body>'; ein '\\n' hinter '</h2>' erzeugt in der
    Ansicht eine Leerzeile, weil Asana den Text mit 'white-space: pre-wrap'
    zeigt (developers.asana.com/docs/rich-text);
  * '<br/>' wird abgelehnt, Umbrüche entstehen über Blöcke und Listen —
    ungeordnet über '- ', geordnet über '1. ' — und über ein '\\n' zwischen
    zwei Zeilen Fließtext, das im Kanal als Zeilenwechsel ankommt;
  * '&', '<' und '>' müssen maskiert sein, sonst scheitert die Anlage mit
    'XML is invalid' und ohne Angabe der Stelle.

Was nicht in der erlaubten Liste steht, entsteht hier auch nicht. Links dagegen
verlangt der Vertrag: eine Angabe ohne Ziel kommt nicht ins Ticket. '[Text](URL)'
und eine nackte URL werden zu Ankern — die Zeile des Schlüssels bleibt nackt und
ein Link darin ist ein Abbruch, weil der Kanal im Plaintext-Feld den Linktext
durch die URL ersetzt und der Abgleich den Schlüssel dort nicht mehr findet.
"""

import re
import sys
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
NACKTE_URL = re.compile(r"(?<![\"=])(https?://[^\s<]+?)(?=[.,;:]?(?:\s|$))")


def maskieren(text):
    # Das Anführungszeichen kommt aus dem Kanal als '&quot;' zurück
    # (gemessen). Es hier selbst zu maskieren hält Gesendetes und
    # Gespeichertes gleich — sonst sieht jeder Vergleich eine Änderung.
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def verlinken(maskiert):
    """Aus '[Text](URL)' und aus einer nackten URL wird ein Anker.

    Der Kanal führt Links, und der Vertrag verlangt sie: eine Angabe ohne
    Ziel kommt nicht ins Ticket. Eine nackte URL wird mit sich selbst als
    Linktext verlinkt — dann geht im Plaintext-Feld nichts verloren, wo der
    Kanal den Linktext durch die URL ersetzt (ref-asana.md).
    """
    maskiert = MARKDOWN_LINK.sub(
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', maskiert)
    return NACKTE_URL.sub(nackt_verlinken, maskiert)


def nackt_verlinken(treffer):
    """Eine nackte URL wird ein Anker; eine schließende Klammer dahinter bleibt Text.

    Steht die URL in Klammern ('(siehe https://…)'), gehört die Klammer zum
    Satz, nicht zur Adresse: gemessen am 30.09.2026, dort landete sie im href.
    Eine Klammer, die in der URL selbst geöffnet wurde ('…/Foo_(Bar)'), bleibt
    drin.
    """
    url, rest = treffer.group(1), ""
    while url.endswith(")") and url.count(")") > url.count("("):
        url, rest = url[:-1], ")" + rest
    return f'<a href="{url}">{url}</a>{rest}'


def inhalt(zeile):
    """Maskieren, dann verlinken — die Zeile des Schlüssels bleibt nackt.

    Der Schlüssel darf nie in einem Linktext stehen: im Plaintext-Feld
    ersetzt der Kanal den Linktext durch die URL, und der Abgleich fand ihn
    dort nicht mehr.
    """
    maskiert = maskieren(zeile)
    if "Schlüssel:" in zeile:
        if MARKDOWN_LINK.search(zeile) or NACKTE_URL.search(zeile):
            raise ValueError("die Schlüssel-Zeile trägt einen Link — der "
                             "Schlüssel wäre im Plaintext des Kanals durch "
                             "die URL ersetzt und für den Abgleich unsichtbar")
        return maskiert
    return FETT.sub(r"<strong>\1</strong>", verlinken(maskiert))


# Die Überschrift einer Anforderung im Epic-Ticket ('**REQ-001 · Titel**',
# ref-ticket-templates.md). 'strong' steht auf der Liste des Kanals.
FETT = re.compile(r"\*\*(.+?)\*\*")


# Ein Punkt einer geordneten Liste. Der Block 'Schritte' eines Arbeitsschritts
# ist immer eine: '1. 2. 3.'. Ohne diese Zeile fielen die Punkte in den
# Fließtext-Zweig und standen im Ticket als EINE Zeile hintereinander --
# der Kanal bricht nur an Blöcken und Listenpunkten um (ref-asana.md). Drei
# Schritte lasen sich dann als ein Satz, und keine der zwei Prüfungen sah es:
# die Blockfolge stimmte, das XML war gültig (v0.1, 28.08.2026).
GEORDNET = re.compile(r"^(\d+)\.\s+(.*)$")

def umsetzen(markdown):
    teile = []
    liste_offen = None  # None | "ul" | "ol"
    # Was zuletzt entstand: None | "h2" | "text" | "liste". Fließtext hinter
    # Fließtext oder hinter einer Liste bekommt ein '\n' davor. Ohne es liefen
    # im Epic-Ticket die Überschrift einer Anforderung und der Text darunter in
    # eine Zeile, und die nächste Anforderung klebte an den Kriterien der
    # vorigen.
    vorher = None

    def liste_schliessen():
        nonlocal liste_offen
        if liste_offen:
            teile.append(f"</{liste_offen}>")
            liste_offen = None

    def liste_oeffnen(art):
        nonlocal liste_offen
        if liste_offen != art:
            liste_schliessen()
            teile.append(f"<{art}>")
            liste_offen = art

    for zeile in markdown.split("\n"):
        z = zeile.rstrip()
        if not z.strip():
            continue
        geordnet = GEORDNET.match(z.lstrip())
        if z.startswith("## "):
            liste_schliessen()
            teile.append(f"<h2>{maskieren(z[3:].strip())}</h2>")
            vorher = "h2"
        elif z.lstrip().startswith("- "):
            liste_oeffnen("ul")
            teile.append(f"<li>{inhalt(z.lstrip()[2:].strip())}</li>")
            vorher = "liste"
        elif geordnet:
            # Die Nummer selbst fällt weg: '<ol>' zählt, und eine mitgeschriebene
            # Nummer stünde doppelt da.
            liste_oeffnen("ol")
            teile.append(f"<li>{inhalt(geordnet.group(2).strip())}</li>")
            vorher = "liste"
        else:
            # Freie Zeilen sind Fließtext. Sie werden zu Listenpunkten NICHT
            # umgedeutet — was die Vorlage als Satz führt, bleibt ein Satz.
            # Ein eigener Absatz-Block existiert im Kanal nicht; der Text
            # hängt deshalb unter seiner Überschrift.
            liste_schliessen()
            if vorher in ("text", "liste"):
                teile.append("\n")
            teile.append(inhalt(z.strip()))
            vorher = "text"
    liste_schliessen()
    return "<body>" + "".join(teile) + "</body>"


def main():
    if len(sys.argv) != 2:
        print("Aufruf: markdown-to-body.py <datei|->", file=sys.stderr)
        return 2
    quelle = sys.argv[1]
    text = sys.stdin.read() if quelle == "-" else \
        Path(quelle).read_text(encoding="utf-8")
    try:
        body = umsetzen(text)
    except ValueError as fehler:
        print(f"Identität — {fehler}", file=sys.stderr)
        return 1
    if "<br" in body or re.search(r"</h[12]>\n|<body>\n|\n</body>", body):
        print("Der Body trägt einen Umbruch hinter einer Überschrift oder am "
              "Rand — der Kanal zeigt dort eine Leerzeile", file=sys.stderr)
        return 1
    sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
