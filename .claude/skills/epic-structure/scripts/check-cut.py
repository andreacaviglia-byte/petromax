#!/usr/bin/env python3
"""Prüft den Schnitt nach §252 und §303 im Projekt-Repo, nach dem Schreiben der Epics und vor der
Projektion.

Aufruf: check-cut.py <repo>

Prüfungen, je eine Zeile `<prüfung> <Kennung> <Satz>`:
    domain      ein Epic trägt eine `domain`, die nicht in der festen Liste steht (§252)
    epic_size   ein Epic trägt mehr als 12 Anforderungen, und `summary` endet nicht mit „Größe
                bestätigt“ bzw. „Size confirmed“ (§252)
    add_on      das Add-on `design` aus project.yml (`add_ons`) hat kein Epic der Domäne design (§303)
    design_qa   mit dem Add-on `design` steht keine Anforderung mit `standard: design-qa`, die
                UX/UI-QA, in einem Epic der Domäne design (§285, §303)

Gezählt werden die Anforderungen, deren `epic` das Epic nennt; ein Epic mit `status` merged oder
dissolved zählt für `add_on` und `design_qa` nicht. Liste, Grenze, Vermerk und Add-ons kommen aus check-sheet.py,
das dieselben Regeln am Sheet hält; es gibt sie nur einmal.

Exit 0 ohne Befund, 1 mit Befund, 2 bei falschem Aufruf oder unlesbarem Repo. Nur Standardbibliothek,
Python 3.9.
"""
import importlib.util
import sys
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
import repo_objects  # noqa: E402  Die Objekte des Repos, eine Datei je Objekt (§280)

GONE = ("merged", "dissolved")


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(repo):
    sheet = load("check-sheet")
    objects = repo_objects.load(repo)
    broken = [o["name"] for kind in ("requirements", "epics") for o in objects[kind] if "error" in o]
    if broken:
        raise ValueError(f"nicht lesbar: {', '.join(broken)}; das meldet check-repo.py")
    counts = Counter(str(o["head"].get("epic") or "").strip() for o in objects["requirements"])
    domains = set(sheet.VALUES[sheet.DOMAIN])
    out, live, domain_of = [], set(), {}
    for epic in objects["epics"]:
        head, key = epic["head"], epic["key"]
        domain = str(head.get("domain") or "").strip()
        if domain not in domains:
            out.append(("domain", key, f"domain '{domain}' steht nicht in der Liste des Vertrags (§252)."))
        n = counts.get(key, 0)
        summary = str(head.get("summary") or "").strip()
        if n > sheet.EPIC_LIMIT and not any(summary.endswith(v) for v in sheet.SIZE_OK.values()):
            out.append(("epic_size", key, f"trägt {n} Anforderungen, mehr als {sheet.EPIC_LIMIT}; teilen oder "
                                          f"„{sheet.SIZE_OK['de']}“ bzw. „{sheet.SIZE_OK['en']}“ am Ende von summary."))
        if str(head.get("status") or "").strip() not in GONE:
            live.add(domain)
            domain_of[key] = domain
    project = Path(repo) / "project.yml"
    if project.is_file():
        for add_on in sheet.add_ons(project):
            if add_on not in sheet.ADD_ON_DOMAIN:
                continue
            if sheet.ADD_ON_DOMAIN[add_on] not in live:
                out.append(("add_on", add_on, f"verkauft, aber kein Epic mit domain "
                                              f"'{sheet.ADD_ON_DOMAIN[add_on]}' (§303)."))
            if add_on == "design" and not any(
                    str(o["head"].get("standard") or "").strip() == "design-qa"
                    and domain_of.get(str(o["head"].get("epic") or "").strip()) == "design"
                    for o in objects["requirements"]):
                out.append(("design_qa", "design", "Das Add-on design ist verkauft, aber keine Anforderung mit "
                                                   "standard: design-qa steht in einem Epic der Domäne design; "
                                                   "requirements-update legt die UX/UI-QA an (§285, §303)."))
    return out


def main(argv):
    if len(argv) != 1 or argv[0].startswith("-"):
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    try:
        found = check(Path(argv[0]))
    except ValueError as e:
        print(f"Aufruf: {e}", file=sys.stderr)
        return 2
    for name, key, text in found:
        print(f"{name} {key} {text}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
