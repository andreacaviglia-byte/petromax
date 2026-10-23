#!/usr/bin/env python3
"""Gibt je Anforderung im Umfang eine Zeile aus requirements/ aus, als Grundlage für die
Lösungsansätze je Anforderung (§275, §280).

Aufruf:
    approach-list.py <repo> [--umfang alle|<Cluster>|REQ-001,REQ-002] [--cluster <datei>]
    approach-list.py <repo> --zeile <ID>

<repo> ist die Wurzel des Projekt-Repos. Der Cluster ist ein Feld der Menschen und steht nur im Sheet
(§280, Regel 5): ein Umfang nach Cluster braucht --cluster, eine CSV oder TSV mit Kopfzeile und den
Spalten `ID` und `Cluster`. Anforderungen mit `status` rejected oder duplicate werden nur gezählt; eine
mit `scope: out_of_scope` steht in der Liste, denn sie bekommt ein Ticket in der Wunschliste (§284).
Die Standard-Anforderungen des Design-Epics (`standard: design-concept` und `design-qa`) bekommen
keinen Lösungsansatz (§297): sie stehen nicht in der Liste und zählen nicht zum Umfang, sondern in
einer Zeile „ohne Lösungsansatz (Design-Epic, §297)“ mit ihren IDs.

Ausgabe, Tab-getrennt, je Anforderung: ID, Cluster, status, scope, title (100 Zeichen), Description
(160 Zeichen, der erste Absatz), Lösungsansatz: bei `solution_status` decided oder blocked
„entschieden:“ bzw. „blockiert:“ und `classification`, bei proposed „vorgeschlagen:“ und der Name des
ersten Lösungsansatzes aus `## Approach`, bei mehreren dahinter die Zahl der übrigen als „(+2)“ (§401),
sonst leer. Am Ende die Zahl im Umfang und die Zahl außerhalb, darunter die IDs ohne Lösungsansatz.
--zeile gibt `## Description`, `## Acceptance criteria`, `## Current state` und `## Approach` einer
Anforderung ganz aus.

Prüfungen, je eine Zeile `<prüfung> — <Satz>` und Exit 1: object (eine Datei in requirements/ ist
nicht lesbar), umfang (eine ID oder ein Cluster gibt es nicht; mit den vorhandenen Clustern), header
(der Datei von --cluster fehlt eine Spalte). Exit 0: Liste ausgegeben. Exit 2: falscher Aufruf. Nur
Standardbibliothek, Python 3.9.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import repo_objects  # noqa: E402

AUSSERHALB = {"rejected", "duplicate"}
OHNE_ANSATZ = {"design-concept", "design-qa"}  # §297


class Abbruch(Exception):
    pass


def kurz(text, n):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def lies_cluster(pfad):
    text = Path(pfad).read_text(encoding="utf-8-sig")
    trenner = "\t" if "\t" in text.split("\n", 1)[0] else ","
    zeilen = list(csv.reader(text.splitlines(), delimiter=trenner))
    kopf = zeilen[0] if zeilen else []
    fehlt = [s for s in ("ID", "Cluster") if s not in kopf]
    if fehlt:
        raise Abbruch(f"header — der Datei von --cluster fehlen die Spalten: {', '.join(fehlt)}")
    c = {k: i for i, k in enumerate(kopf)}
    out = {}
    for z in zeilen[1:]:
        z += [""] * (len(kopf) - len(z))
        if z[c["ID"]].strip():
            out[z[c["ID"]].strip()] = z[c["Cluster"]].strip()
    return out


def ansatz(head, body):
    status = head.get("solution_status", "")
    cls = head.get("classification") or []
    cls = [cls] if isinstance(cls, str) else cls
    if status in ("decided", "blocked"):
        return ("entschieden: " if status == "decided" else "blockiert: ") + (" + ".join(cls) or "offen")
    if status == "proposed":
        if not cls:
            # Ohne Empfehlung steht kein Lösungsansatz zuerst (ref-approach.md, „Ist keiner zu empfehlen“)
            return "vorgeschlagen: offen"
        teile = re.split(r"(?m)^### ", repo_objects.sections(body).get("Approach", ""))[1:]
        weitere = f" (+{len(teile) - 1})" if len(teile) > 1 else ""
        return "vorgeschlagen: " + (teile[0].split("\n", 1)[0].strip() if teile else "") + weitere
    return ""


def main(argv):
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("repo")
    p.add_argument("--umfang", default="alle")
    p.add_argument("--cluster")
    p.add_argument("--zeile")
    try:
        a = p.parse_args(argv[1:])
    except SystemExit:
        return 2
    repo = Path(a.repo)
    if not repo.is_dir():
        return 2
    try:
        reqs = repo_objects.load(repo)["requirements"]
        kaputt = [r for r in reqs if "error" in r]
        if kaputt:
            raise Abbruch(f"object — {kaputt[0]['name']}: {kaputt[0]['error']}")
        if a.zeile:
            r = next((x for x in reqs if x["key"] == a.zeile), None)
            if r is None:
                raise Abbruch(f"umfang — die ID {a.zeile} steht nicht in requirements/")
            teile = repo_objects.sections(r["body"])
            print(f"{r['key']} · {r['head'].get('status', '')} · {r['head'].get('title', '')}")
            for s in ("Description", "Acceptance criteria", "Current state", "Approach"):
                print(f"\n## {s}\n{teile.get(s, '')}")
            return 0
        cluster = lies_cluster(a.cluster) if a.cluster else {}
        kennungen = {r["key"] for r in reqs}
        if a.umfang == "alle":
            drin = kennungen
        elif a.umfang.startswith("REQ-"):
            drin = {i.strip() for i in a.umfang.split(",") if i.strip()}
            unbekannt = drin - kennungen
            if unbekannt:
                raise Abbruch(f"umfang — diese IDs stehen nicht in requirements/: {', '.join(sorted(unbekannt))}")
        else:
            werte = sorted({v for v in cluster.values() if v})
            if a.umfang not in werte:
                raise Abbruch(f"umfang — den Cluster '{a.umfang}' gibt es nicht; vorhanden: "
                              f"{', '.join(werte) or 'keiner'}")
            drin = {k for k, v in cluster.items() if v == a.umfang}
    except Abbruch as e:
        print(str(e), file=sys.stderr)
        return 1

    im, aus, ohne = 0, 0, []
    print("ID\tCluster\tstatus\tscope\ttitle\tDescription\tLösungsansatz")
    for r in reqs:
        h, k = r["head"], r["key"]
        if k not in drin:
            continue
        if h.get("status") in AUSSERHALB:
            aus += 1
            continue
        if h.get("standard") in OHNE_ANSATZ:
            ohne.append(k)
            continue
        im += 1
        beschreibung = repo_objects.first_paragraph(repo_objects.sections(r["body"]).get("Description", ""))
        print("\t".join([k, cluster.get(k, ""), str(h.get("status", "")), str(h.get("scope", "")),
                         kurz(str(h.get("title", "")), 100), kurz(beschreibung, 160), ansatz(h, r["body"])]))
    print(f"\n{im} Anforderungen im Umfang, {aus} verworfen oder Duplikat nur gezählt.")
    if ohne:
        print(f"ohne Lösungsansatz (Design-Epic, §297): {', '.join(ohne)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
