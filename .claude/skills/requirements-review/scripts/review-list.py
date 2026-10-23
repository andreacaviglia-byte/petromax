#!/usr/bin/env python3
"""Die Liste zum Prüfen: eine Zeile je Anforderung aus requirements/, mit den Befunden, die sich zählen
lassen (§280).

Aufruf: review-list.py <repo> [--umfang alle|<Cluster>|source:<Text>|REQ-001,REQ-002] [--cluster <datei>]
                       [--shops <key>,<key>]
        review-list.py <repo> --zeile REQ-001

<repo> ist die Wurzel des Projekt-Repos. Die Anforderungen kommen aus requirements/, die offenen
Fragen aus gaps/, die ADRs aus decisions/ (.claude/docs/datalayer-contract.md). Der Cluster ist ein
Feld der Menschen und steht nur im Sheet (§280, Regel 5): ein Umfang nach Cluster braucht --cluster,
eine CSV oder TSV mit Kopfzeile und den Spalten `ID` und `Cluster`, gelesen aus dem Tab
`Anforderungen`. Gelesen wird am Spaltennamen. Ein Umfang `source:<Text>` ist der Input einer
Session (§305): die Anforderungen, deren `source` den Text enthält, ohne Unterschied in Groß- und
Kleinschreibung, etwa `source:Workshop Märkte vom 18.08.2026` oder der Dateiname einer Notiz.

Ausgabe je Anforderung: ID | umfang oder andere | Cluster | status | scope | title | source (40
Zeichen) | epic | Befunde. `title` trägt den Shop-Bezug aus dem Feld `shops` hinten, `(B2B)` oder
`(alle Shops)` (§307), mit den Schlüsseln aus --shops oder sonst aus `shops` in project.yml. Befunde:
    ohne_quelle              `source` ist leer
    duplikat_ohne_verweis    `status: duplicate` und `duplicate_of` ist leer
    ausklammerung_ohne_adr   `status: rejected` oder `scope: out_of_scope`, und keine ADR in decisions/
                             nennt die Kennung (die ADR trägt den Grund)
    fragen_offen=N           N offene Fragen in gaps/ nennen sie in `concerns`
    blockiert=N              davon N mit `blocking: yes`
    shop_unbekannt=<key>     mit --shops (die `key` aus `shops` in project.yml): das Feld `shops` nennt
                             einen Schlüssel, der nicht in der Liste steht (§245, §307)
    ist_ungeprueft_ohne_frage
                             `## Current state` ist „ungeprüft“ (oder „unchecked“), und keine offene
                             Frage, die sie nennt, fragt nach dem Ist-Zustand (§254)
    kriterien_leer_ohne_frage
                             `## Acceptance criteria` fehlt oder ist leer, und keine offene Frage, die
                             sie nennt, fragt nach einem Kriterium (§254)
Die beiden letzten gelten nicht für `status` rejected oder duplicate. Ob eine Frage nach dem
Ist-Zustand oder einem Kriterium fragt, liest das Script am Wortlaut (IST_FRAGE, KRITERIUM_FRAGE
unten); es zählt Kandidaten, das Urteil über Kriterien, die nicht leer und trotzdem nicht prüfbar
sind, bleibt beim Lauf.
Am Ende `ANFORDERUNGEN <n>, im Umfang <m>`.

Mit --zeile kommen `## Description`, `## Acceptance criteria` und `## Current state`
einer Anforderung, je unter ihrer Überschrift, dazu die offenen Fragen mit Kennung und erstem Satz.

Exit 0, 1 bei einer Kennung oder einem Cluster, den es nicht gibt, einem Text, den keine `source`
nennt, oder einer Datei des Repos, die nicht lesbar ist, 2 bei falschem Aufruf oder fehlender Spalte.
Nur Standardbibliothek, Python 3.9.
"""
import csv
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import repo_objects  # noqa: E402

UNGEPRUEFT = re.compile(r"^\W*(ungeprüft|unchecked)\W*$", re.I)
# Woran eine offene Frage als Frage nach dem Ist-Zustand oder nach einem Kriterium erkannt wird; die
# Musterfrage nach dem Ist-Zustand ist „Wie ist das heute im Shop gelöst?“ (ref-requirement.md, IST).
IST_FRAGE = re.compile(r"\bheute\b|ist-zustand|derzeit|\btoday\b|current state|currently", re.I)
KRITERIUM_FRAGE = re.compile(r"kriteri|akzeptanz|abgenommen|prüfbar|criteri|acceptance", re.I)


class Abbruch(Exception):
    def __init__(self, text, code):
        super().__init__(text)
        self.code = code


def lies_repo(repo):
    objekte = repo_objects.load(repo)
    for art in ("requirements", "gaps", "decisions"):
        for o in objekte[art]:
            if "error" in o:
                raise Abbruch(f"{o['name']}: {o['error']}", 1)
    return objekte


def lies_cluster(pfad):
    text = Path(pfad).read_text(encoding="utf-8-sig")
    trenner = "\t" if "\t" in text.split("\n", 1)[0] else ","
    zeilen = list(csv.reader(text.splitlines(), delimiter=trenner))
    if not zeilen:
        raise Abbruch("Spalte fehlt: ID", 2)
    c = {k: i for i, k in enumerate(zeilen[0])}
    for s in ("ID", "Cluster"):
        if s not in c:
            raise Abbruch(f"Spalte fehlt: {s}", 2)
    out = {}
    for z in zeilen[1:]:
        z += [""] * (len(zeilen[0]) - len(z))
        if z[c["ID"]]:
            out[z[c["ID"]]] = z[c["Cluster"]]
    return out


def als_liste(wert):
    if wert in ("", None):
        return []
    return [wert] if isinstance(wert, str) else list(wert)


def liste(repo, umfang="alle", cluster_pfad=None, shops=None):
    objekte = lies_repo(repo)
    try:
        projekt = repo_objects.read_yaml((Path(repo) / "project.yml").read_text(encoding="utf-8"))
    except (OSError, repo_objects.ObjectError):
        projekt = {}
    sprache = projekt.get("language", "de")
    schluessel = list(shops) if shops is not None else repo_objects.project_shop_keys(projekt)
    cluster = lies_cluster(cluster_pfad) if cluster_pfad else {}
    reqs = objekte["requirements"]
    kennungen = {r["key"] for r in reqs}
    if umfang == "alle":
        drin = kennungen
    elif umfang.startswith("source:"):
        text = umfang[len("source:"):].strip().casefold()
        if not text:
            raise Abbruch("umfang source: braucht einen Text", 2)
        drin = {r["key"] for r in reqs if text in str(r["head"].get("source", "")).casefold()}
        if not drin:
            werte = "; ".join(sorted({str(r["head"].get("source", "")) for r in reqs} - {""})) or "keine"
            raise Abbruch(f"umfang source „{umfang[7:].strip()}“ nennt keine Anforderung; "
                          f"vorhanden: {werte}", 1)
    elif umfang.startswith("REQ-"):
        drin = {s.strip() for s in umfang.split(",") if s.strip()}
        fehlt = sorted(drin - kennungen)
        if fehlt:
            raise Abbruch(f"umfang {', '.join(fehlt)} steht nicht in requirements/", 1)
    else:
        if not cluster_pfad:
            raise Abbruch("umfang nach Cluster braucht --cluster", 2)
        drin = {k for k, v in cluster.items() if v == umfang}
        if not drin:
            werte = ", ".join(sorted({v for v in cluster.values() if v})) or "keine"
            raise Abbruch(f"umfang Cluster „{umfang}“ gibt es nicht; vorhanden: {werte}", 1)
    offen = [g for g in objekte["gaps"] if g["head"].get("status") == "open"]
    adr_text = "\n".join(str(d["head"].get("title", "")) + "\n" + d["body"] for d in objekte["decisions"])
    out = []
    for r in reqs:
        h, k = r["head"], r["key"]
        status, scope = str(h.get("status", "")), str(h.get("scope", ""))
        fragen = [g for g in offen if k in als_liste(g["head"].get("concerns"))]
        blockiert = [g for g in fragen if g["head"].get("blocking") == "yes"]
        fremd = ",".join(s for s in repo_objects.shop_keys(h.get("shops")) if shops is not None and s not in shops)
        teile = repo_objects.sections(r["body"])
        gilt = status not in ("rejected", "duplicate")
        fragetexte = [g["body"] for g in fragen]
        ist_offen = gilt and bool(UNGEPRUEFT.match(teile.get("Current state", "").strip())) \
            and not any(IST_FRAGE.search(f) for f in fragetexte)
        kriterien_offen = gilt and not teile.get("Acceptance criteria", "").strip() \
            and not any(KRITERIUM_FRAGE.search(f) for f in fragetexte)
        befund = [b for b, ja in (
            ("ohne_quelle", not str(h.get("source", "")).strip()),
            ("duplikat_ohne_verweis", status == "duplicate" and not str(h.get("duplicate_of", "")).strip()),
            ("ausklammerung_ohne_adr", (status == "rejected" or scope == "out_of_scope")
             and not re.search(rf"\b{k}\b", adr_text)),
            (f"fragen_offen={len(fragen)}", fragen),
            (f"blockiert={len(blockiert)}", blockiert),
            (f"shop_unbekannt={fremd}", fremd),
            ("ist_ungeprueft_ohne_frage", ist_offen),
            ("kriterien_leer_ohne_frage", kriterien_offen)) if ja]
        out.append([k, "umfang" if k in drin else "andere", cluster.get(k, ""), status, scope,
                    repo_objects.shops_title(str(h.get("title", "")), h.get("shops"), schluessel, sprache),
                    str(h.get("source", ""))[:40], str(h.get("epic", "")),
                    " ".join(befund)])
    return out, len(drin)


def zeile(repo, req):
    objekte = lies_repo(repo)
    r = next((x for x in objekte["requirements"] if x["key"] == req), None)
    if r is None:
        raise Abbruch(f"{req} steht nicht in requirements/", 1)
    teile = repo_objects.sections(r["body"])
    out = [f"## {s}\n{teile.get(s, '')}" for s in ("Description", "Acceptance criteria", "Current state")]
    fragen = [f"{g['key']} {repo_objects.first_sentence(repo_objects.sections(g['body'])[''])}"
              for g in objekte["gaps"]
              if g["head"].get("status") == "open" and req in als_liste(g["head"].get("concerns"))]
    out.append("## Open questions\n" + "\n".join(fragen))
    return out


def main():
    args = sys.argv[1:]
    try:
        if "--zeile" in args:
            if len(args) != 3 or args[1] != "--zeile":
                raise Abbruch(__doc__.strip(), 2)
            print("\n\n".join(zeile(Path(args[0]), args[2])))
            return 0
        werte = {"--umfang": "alle", "--cluster": None, "--shops": None}
        for name in werte:
            if name in args:
                i = args.index(name)
                if i + 1 >= len(args):
                    raise Abbruch(__doc__.strip(), 2)
                werte[name] = args[i + 1]
                del args[i:i + 2]
        if len(args) != 1 or not Path(args[0]).is_dir():
            raise Abbruch(__doc__.strip(), 2)
        shops = werte["--shops"]
        if shops is not None:
            shops = [s.strip() for s in shops.split(",") if s.strip()]
        zeilen, n = liste(Path(args[0]), werte["--umfang"], werte["--cluster"], shops)
    except Abbruch as a:
        print(str(a), file=sys.stderr if a.code == 2 else sys.stdout)
        return a.code
    for z in zeilen:
        print(" | ".join(z))
    print(f"ANFORDERUNGEN {len(zeilen)}, im Umfang {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
