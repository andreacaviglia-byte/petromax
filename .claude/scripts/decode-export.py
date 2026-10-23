#!/usr/bin/env python3
"""Schreibt den Export von Google_Drive.download_file_content als Datei: CSV eines Sheets, HTML eines Docs.

Aufruf:
    decode-export.py <antwort> <ziel>

<antwort> ist entweder die Datei, als die die Sitzung eine große Antwort ablegt (JSON mit dem Feld
content), oder eine Datei, in die der Lauf den Wert von content einer kleinen Antwort geschrieben hat.
<ziel> wird mit den dekodierten Bytes überschrieben.

Ein Script statt jq und base64 auf der Kommandozeile, weil jq nicht auf jedem Rechner liegt und
base64 je System andere Schalter hat; Python braucht die Strecke ohnehin. Das Ziel schreibt das
Script selbst, nicht eine Umleitung der Shell, damit keine Shell die Kodierung ändert.

Prüfungen: usage, content, base64. Exit 0: geschrieben. Exit 1: nichts geschrieben, die Meldung nennt
die Prüfung. Exit 2: falscher Aufruf.
"""
import base64
import binascii
import json
import sys
from pathlib import Path


def main(argv):
    if len(argv) != 3:
        print("usage: decode-export.py <antwort> <ziel>", file=sys.stderr)
        return 2
    quelle, ziel = Path(argv[1]), Path(argv[2])
    text = quelle.read_text(encoding="utf-8").strip()
    if text.startswith("{"):
        try:
            daten = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"content: {quelle} ist kein lesbares JSON: {e}")
            return 1
        if not isinstance(daten.get("content"), str) or not daten["content"]:
            print(f"content: {quelle} trägt kein Feld content mit Text")
            return 1
        text = daten["content"]
    try:
        roh = base64.b64decode("".join(text.split()), validate=True)
    except (binascii.Error, ValueError) as e:
        print(f"base64: der Inhalt von {quelle} ist kein Base64: {e}")
        return 1
    ziel.write_bytes(roh)
    print(f"geschrieben: {ziel} ({len(roh)} Bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
