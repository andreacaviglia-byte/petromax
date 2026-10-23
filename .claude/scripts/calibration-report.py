#!/usr/bin/env python3
"""Misst die Modellschätzung eines Vorhabens gegen `Aufwand (h)`, je Bereich und je Größe (§357, Stufe 1).

Aufruf:
  calibration-report.py <projekt-repo> <hours.json>

<hours.json> ist die schmale Spalte `Aufwand (h)` (`Effort (h)`) des Tabs Solutioning mit `ID`, in
derselben Form, die `solution-estimate` liest: die Antworten von get_values in der Hülle
{"valueRanges": [...]}, oder eine Liste von Zeilen mit der Kopfzeile zuerst. Gelesen wird sie mit
dem Leser aus `check-solution-doc.py`; die Datei liegt im Temp-Ordner, nicht im Repo.

Ein Paar ist eine Anforderung mit Rohschätzung `effort_estimate_model` und `Aufwand (h)`, beide
größer 0. Ihr Bereich ist ihre Position der Schätzung (§355), zugeordnet wie in
`check-solution-doc.py` (`position_of`: die Domäne des Epics vor dem ersten Lösungsansatz). Je Bereich
steht eine Zeile `BEREICH` mit
  - der Zahl der Paare,
  - dem Median von Lead ÷ Roh, dem neuen Faktor,
  - dem aktuellen Faktor aus `.claude/docs/calibration.md`,
  - mit ihm dem Median der absoluten Abweichung kalibriert (Roh × Faktor) gegen Lead in Prozent,
  - der Spanne der Abweichungen, kleinste und größte, mit Vorzeichen,
und darunter je Paar eine Zeile `PAAR`. Ein Paar in „Lösungsansatz offen“ hat keinen Faktor und steht
unter `OHNE BEREICH`. Eine Anforderung mit nur einer der beiden Zahlen steht unter `OHNE PAAR`.

Danach zeigt der Bericht, wie gut das Modell Größen schätzt: je Größe (S, M, L, XL), getrennt für
`size` und für `size_estimate_approach`, eine Zeile `GRÖSSE` mit der Zahl der Anforderungen mit
`Aufwand (h)` größer 0 und dem Median, dem kleinsten und dem größten Wert von `Aufwand (h)`. Eine
Anforderung mit leerem Feld zählt für dieses Feld nicht; hat sie Stunden, steht sie unter
`OHNE GRÖSSE`. Ein Faktor entsteht daraus nicht, und kein Lauf hält die Stunden gegen die Größe.

Das Script schreibt nichts: die Faktoren trägt ein Mensch in `calibration.md` ein (§357). Exit 0 mit
der Ausgabe; verletzt eine Eingabe den Vertrag, steht je Befund eine Zeile `<prüfung> <detail>` da,
Exit 1; falscher Aufruf Exit 2.
"""
import importlib.util
import re
import sys
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CALIBRATION = HERE.parent / "docs" / "calibration.md"
COLUMNS = ["area", "factor", "pairs", "median_deviation", "basis", "source", "as_of"]
HOURS = re.compile(r"^\d+(?:\.\d+)?$")
NO_AREA = "approach_open"
SIZES = ["S", "M", "L", "XL"]
SIZE_FIELDS = ["size", "size_estimate_approach"]


def _doc():
    """check-solution-doc.py, die eine Stelle für Positionen und den Leser von hours.json."""
    spec = importlib.util.spec_from_file_location("check_solution_doc", HERE / "check-solution-doc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DOC = _doc()
Refused = DOC.Refused
AREAS = [k for k in DOC.POSITIONS if k != NO_AREA]


def factors(path=CALIBRATION):
    """Je Bereich der aktuelle Faktor aus der Tabelle in calibration.md; `calibration`, wenn sie nicht passt."""
    if not path.is_file():
        raise Refused(f"calibration {path.name} fehlt")
    rows = [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    head = next((i for i, l in enumerate(rows) if [c.strip() for c in l.strip("|").split("|")] == COLUMNS), None)
    if head is None:
        raise Refused(f"calibration keine Tabelle mit den Spalten {', '.join(COLUMNS)}")
    out = {}
    for line in rows[head + 2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(COLUMNS):
            break
        area, raw = cells[0], cells[1]
        if area not in AREAS:
            raise Refused(f"calibration {area}: kein Bereich; es gibt {', '.join(AREAS)}")
        if area in out:
            raise Refused(f"calibration {area}: steht zweimal in der Tabelle")
        if not HOURS.match(raw) or float(raw) <= 0:
            raise Refused(f"calibration {area}: Faktor „{raw}“ ist keine Zahl größer 0 mit Dezimalpunkt")
        out[area] = float(raw)
    missing = [a for a in AREAS if a not in out]
    if missing:
        raise Refused(f"calibration es fehlt der Bereich {', '.join(missing)}")
    return out


def load(repo, hours_path):
    """project.yml, die Anforderungen mit ihrem Bereich und die Stunden des Leads je Anforderung."""
    import repo_objects
    repo, hours_path = Path(repo), Path(hours_path)
    if not (repo / "project.yml").is_file():
        raise Refused(f"repo {repo}: dort liegt keine project.yml; gemeint ist die Wurzel des Projekt-Repos")
    try:
        project = repo_objects.read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
    except repo_objects.ObjectError as e:
        raise Refused(f"input project.yml nicht lesbar: {e}")
    lang = str(project.get("language", "") or "").strip()
    if lang not in ("de", "en"):
        raise Refused(f"input project.yml: language „{lang}“ ist weder de noch en")
    objects = repo_objects.load(repo)
    for kind in ("requirements", "epics"):
        for o in objects[kind]:
            if "error" in o:
                raise Refused(f"object {o['name']}: {o['error']}")
    domains = {o["key"]: str(o["head"].get("domain", "")).strip() for o in objects["epics"]}

    sheet = DOC._sheet()
    id_col, h_col = (sheet.column("solutioning", k, lang) for k in ("id", "hours"))
    if not hours_path.is_file():
        raise Refused(f"input {hours_path.name} fehlt")
    try:
        rows = DOC.rows_from_json(DOC.json.loads(hours_path.read_text(encoding="utf-8")))
    except (ValueError, AttributeError, TypeError) as e:
        raise Refused(f"input {hours_path.name} nicht lesbar: {e}")
    head = [h.strip() for h in rows[0]] if rows else []
    missing = [c for c in (id_col, h_col) if c not in head]
    if missing:
        raise Refused(f"header {hours_path.name}: es fehlt {', '.join(repr(c) for c in missing)}")
    lead = {}
    for r in rows[1:]:
        r = list(r) + [""] * (len(head) - len(r))
        i, raw = r[head.index(id_col)].strip(), r[head.index(h_col)].strip()
        if not i or not raw:
            continue
        if DOC.number(raw) is None:
            raise Refused(f"hours {i}: {h_col} „{raw}“ ist keine Zahl")
        lead[i] = DOC.number(raw)

    reqs = []
    for o in objects["requirements"]:
        h = o["head"]
        raw = h.get("effort_estimate_model", "")
        if not isinstance(raw, str) or (raw and not HOURS.match(raw)):
            raise Refused(f"effort_estimate {o['key']}: effort_estimate_model „{raw}“ ist weder leer noch "
                          f"eine Stundenzahl mit Dezimalpunkt (§357)")
        area = DOC.position_of(h, domains.get(str(h.get("epic", "")), ""))
        sizes = {}
        for field in SIZE_FIELDS:
            v = h.get(field, "")
            if not isinstance(v, str) or (v and v not in SIZES):
                raise Refused(f"size {o['key']}: {field} „{v}“ ist weder leer noch {', '.join(SIZES)}")
            sizes[field] = v
        reqs.append({"id": o["key"], "area": area, "model": float(raw) if raw else None, "lead": lead.get(o["key"]),
                     "sizes": sizes})
    return lang, h_col, reqs


def pct(x):
    return f"{x:+.0f} %".replace("+0 %", "0 %").replace("-", "−")


def num(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def report(repo, hours_path, calibration=CALIBRATION):
    current = factors(calibration)
    lang, h_col, reqs = load(repo, hours_path)
    names = {k: v[0 if lang == "de" else 1] for k, v in DOC.POSITIONS.items()}
    pairs = [r for r in reqs if r["model"] and r["lead"]]
    lines = [f"PAARE {len(pairs)} von {len(reqs)} Anforderungen; Faktoren aus {Path(calibration).name}"]
    for area in AREAS:
        mine = [r for r in pairs if r["area"] == area]
        f = current[area]
        if not mine:
            lines.append(f"BEREICH {area} ({names[area]}): Paare 0; Faktor aktuell {num(f)}")
            continue
        new = median(r["lead"] / r["model"] for r in mine)
        dev = [(r["model"] * f - r["lead"]) / r["lead"] * 100 for r in mine]
        lines.append(f"BEREICH {area} ({names[area]}): Paare {len(mine)}; Faktor neu {num(new)} "
                     f"(Median Lead ÷ Roh); Faktor aktuell {num(f)}; Abweichung kalibriert gegen Lead "
                     f"{median(abs(d) for d in dev):.0f} % (Median, absolut); Spanne {pct(min(dev))} bis {pct(max(dev))}")
        for r, d in zip(mine, dev):
            lines.append(f"  PAAR {r['id']}: Roh {num(r['model'])} h; Lead {num(r['lead'])} h; "
                         f"kalibriert {num(r['model'] * f)} h; Abweichung {pct(d)}")
    no_area = [r["id"] for r in pairs if r["area"] == NO_AREA]
    if no_area:
        lines.append(f"OHNE BEREICH ({names[NO_AREA]}, kein Faktor): {', '.join(no_area)}")
    single = [r["id"] for r in reqs if bool(r["model"]) != bool(r["lead"])]
    if single:
        lines.append(f"OHNE PAAR (nur eine der beiden Zahlen, oder 0): {', '.join(single)}")
    lines += by_size(reqs, h_col)
    return "\n".join(lines) + "\n"


def by_size(reqs, h_col):
    """Je Feld und Größe die Stunden des Leads: Zahl, Median, kleinster und größter Wert."""
    lines = []
    with_hours = [r for r in reqs if r["lead"]]
    for field in SIZE_FIELDS:
        for size in SIZES:
            hours = [r["lead"] for r in with_hours if r["sizes"][field] == size]
            line = f"GRÖSSE {field} {size}: Anforderungen mit {h_col} {len(hours)}"
            if hours:
                line += f"; Median {num(median(hours))} h; kleinster {num(min(hours))} h; größter {num(max(hours))} h"
            lines.append(line)
        empty = [r["id"] for r in with_hours if not r["sizes"][field]]
        if empty:
            lines.append(f"OHNE GRÖSSE {field} (mit {h_col}, Feld leer): {', '.join(empty)}")
    return lines


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        text = report(argv[1], argv[2])
    except Refused as e:
        print(str(e))
        return 1
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
