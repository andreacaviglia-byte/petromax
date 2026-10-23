#!/usr/bin/env python3
"""Rechnet aus den belegten Abhängigkeiten zwischen Epics die Stufen des Lösens (§215).

Aufruf: order-stages.py <repo> <deps.tsv>

Die Epics sind die Dateien in <repo>/epics/ außer critical-path.md, ohne die mit `status` merged oder
dissolved. <deps.tsv> hat die Kopfzeile `wartet<TAB>auf<TAB>Beleg`, je Kante eine Zeile: das Epic
links wartet auf das rechts. Eine Kante ohne Beleg lehnt das Script ab; eine Abhängigkeit trägt nur
mit Richtung (`depends_on` einer Anforderung, ein ausdrückliches Wort im Text) oder aus einer Zeile in
architecture.md (§215).

Ausgabe: je Stufe eine Zeile `Stufe N: EP-… (wartend: k), …`, die erste Stufe ist 1. Was in keine
Stufe fällt, steht in einer Zeile `Zyklus oder hängt an einem Zyklus:`; das Script löst ihn nicht auf.
Darunter `Kritischer Pfad:` mit jeder längsten Kette belegter Kanten (`EP-001 → EP-002`), ohne Kante
`keiner`, und `Zeile im Epic-Ticket:` mit je Epic einer Zeile `EP-…<TAB>Stufe N · wartet auf EP-…, EP-…`;
ohne Kante steht nur `Stufe N`, ein Epic ohne Stufe trägt `keine Stufe`. Diese Zeile übernimmt
epics/critical-path.md und aus ihr `ticket-factory` ins Epic-Ticket, Zeichen für Zeichen (§267); sie
steht darum in der Sprache aus `language` in <repo>/project.yml (§337), mit den Wendungen `stage`,
`stage_waits` und `stage_none` aus dem Datalayer-Vertrag, Abschnitt „Die festen Wendungen“: bei `en`
`Stage N · waits for EP-…`, `Stage N`, `no stage`. Ohne `language` gilt `de`. Die übrigen Zeilen
der Ausgabe sind für den Lauf und bleiben deutsch.
Exit 0 mit Stufen, 1 bei einer Kante ohne Beleg, mit unbekanntem Epic oder einer unlesbaren
Epic-Datei, 2 bei falschem Aufruf. Nur Standardbibliothek, Python 3.9.
"""
import csv
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import repo_objects  # noqa: E402  Die Objekte des Repos, eine Datei je Objekt (§280)

GONE = ("merged", "dissolved")


def stufen(epics, kanten):
    """Liefert (Stufen, Rest): Stufen als Listen, Rest als {Epic: Epics, auf die es noch wartet}."""
    auf = {e: set() for e in epics}
    for wartet, ziel in kanten:
        if wartet != ziel:
            auf[wartet].add(ziel)
    offen, fertig, out = dict(auf), set(), []
    while offen:
        jetzt = sorted(e for e, v in offen.items() if v <= fertig)
        if not jetzt:
            break
        out.append([(e, sum(e in v for v in auf.values())) for e in jetzt])
        fertig |= set(jetzt)
        for e in jetzt:
            del offen[e]
    return out, {e: sorted(v - fertig) for e, v in sorted(offen.items())}


def pfade(stufen_, kanten):
    """Jede längste Kette belegter Kanten, vom Epic ohne Vorgänger bis zum letzten (§267).

    Die Länge einer Kette ist die Zahl ihrer Stufen; ein Epic der letzten Stufe liegt am Ende jeder
    längsten Kette. Rückwärts wird je Schritt nur ein Vorgänger der Stufe direkt davor genommen.
    """
    if len(stufen_) < 2:
        return []
    stufe = {e: n for n, s in enumerate(stufen_) for e, _ in s}
    auf = {}
    for wartet, ziel in kanten:
        if wartet != ziel and wartet in stufe and ziel in stufe:
            auf.setdefault(wartet, set()).add(ziel)

    def rueckwaerts(e):
        vor = sorted(v for v in auf.get(e, ()) if stufe[v] == stufe[e] - 1)
        if not vor:
            return [[e]]
        return [k + [e] for v in vor for k in rueckwaerts(v)]

    return [k for e, _ in stufen_[-1] for k in rueckwaerts(e)]


def zeilen(epics, stufen_, kanten, sprache="de"):
    """Je Epic die Zeile für das Epic-Ticket: `Stufe N · wartet auf EP-…, EP-…` oder `Stufe N`, in der
    Sprache des Projekts (§337)."""
    w = repo_objects.phrases()[sprache]
    stufe = {e: n for n, s in enumerate(stufen_, start=1) for e, _ in s}
    auf = {e: set() for e in epics}
    for wartet, ziel in kanten:
        if wartet != ziel:
            auf[wartet].add(ziel)
    out = []
    for e in epics:
        if e not in stufe:
            out.append((e, w["stage_none"]))
        elif auf[e]:
            out.append((e, w["stage_waits"].replace("‹n›", str(stufe[e]))
                        .replace("‹EPs›", ", ".join(sorted(auf[e])))))
        else:
            out.append((e, w["stage"].replace("‹n›", str(stufe[e]))))
    return out


def ids(repo):
    """Die Kennungen der Epics in <repo>/epics/, ohne merged und dissolved; None bei einer kaputten Datei."""
    epics = repo_objects.load(repo)["epics"]
    kaputt = [e["name"] for e in epics if "error" in e]
    if kaputt:
        print(f"Epic-Datei nicht lesbar: {', '.join(kaputt)}")
        return None
    return [e["key"] for e in epics if str(e["head"].get("status") or "").strip() not in GONE]


def sprache(repo):
    """`language` aus project.yml, `de` ohne Datei oder Wert; None bei einem anderen Wert."""
    p = repo / "project.yml"
    if not p.is_file():
        return "de"
    try:
        lang = str(repo_objects.read_yaml(p.read_text(encoding="utf-8")).get("language") or "de").strip()
    except repo_objects.ObjectError as e:
        print(f"project.yml nicht lesbar: {e}")
        return None
    if lang not in repo_objects.LANGUAGES:
        print(f"project.yml: language '{lang}' ist weder de noch en")
        return None
    return lang


def main():
    args = sys.argv[1:]
    if len(args) != 2 or args[0].startswith("-"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    epics, lang = ids(Path(args[0])), sprache(Path(args[0]))
    if epics is None or lang is None:
        return 1
    kanten = []
    for z in csv.reader(open(args[1], encoding="utf-8"), delimiter="\t"):
        if not z or z[0] == "wartet":
            continue
        z += [""] * (3 - len(z))
        if z[0] not in epics or z[1] not in epics:
            print(f"unbekanntes Epic in deps.tsv: {z[0]} -> {z[1]}")
            return 1
        if not z[2].strip():
            print(f"Abhängigkeit ohne Beleg: {z[0]} -> {z[1]}")
            return 1
        kanten.append((z[0], z[1]))
    out, rest = stufen(epics, kanten)
    for n, stufe in enumerate(out, start=1):
        print(f"Stufe {n}: " + ", ".join(f"{e} (wartend: {w})" for e, w in stufe))
    if rest:
        print("Zyklus oder hängt an einem Zyklus: " + ", ".join(
            f"{e} wartet auf {', '.join(v)}" for e, v in rest.items()))
    ketten = pfade(out, kanten)
    print("Kritischer Pfad: " + ("; ".join(" → ".join(k) for k in ketten) if ketten else "keiner"))
    print("Zeile im Epic-Ticket:")
    for e, zeile in zeilen(sorted(epics), out, kanten, lang):
        print(f"{e}\t{zeile}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
