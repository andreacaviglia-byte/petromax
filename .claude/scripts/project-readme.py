#!/usr/bin/env python3
"""Projiziert das Repo in `readme.md` (§288) und `way-of-working.md` (§286), in eine Richtung, am Ende
jedes schreibenden Laufs nach `check-repo.py` (§280).

Aufruf:
    project-readme.py <repo>            schreibt beide Dateien neu und liest sie zurück
    project-readme.py <repo> --check    schreibt nichts; meldet, welche Datei nicht die Projektion ist

`way-of-working.md` ist der Standard aus `.claude/way-of-working-standard.md` mit jeder Abweichung
aus `way-of-working/` am Ende ihres Abschnitts, in der Folge der Dateinamen; der Abschnitt ist die
Überschrift 2, die `section` wörtlich nennt. `readme.md` ist der Überblick aus `project.yml`,
`epics/`, `gaps/`, `todo/`, `decisions/` und `scope/`, in der Sprache aus `language` (`de`, sonst
`en`): Vorhaben und Shops, Links, Stand der Kette, offene Fragen mit `blocking: yes`, offene
Aufgaben, die fünf jüngsten Entscheidungen. Felder der Menschen stehen nicht im Repo und deshalb auch
hier nicht, auch nicht `Geprüft von` (§280, Regel 5). Eine Änderung von Hand ersetzt der nächste Lauf.

Prüfungen, je eine Zeile `<prüfung> <datei> <Satz>` und Exit 1:
    object        eine Datei in epics/, gaps/, todo/, decisions/ oder way-of-working/ ist nicht lesbar
    wow_section   eine Abweichung nennt einen Abschnitt, den der Standard nicht hat
    wow_drift     mit --check: way-of-working.md ist nicht die Projektion (eine Abweichung ohne Datei
                  in way-of-working/, oder eine Datei, die noch nicht projiziert ist)
    readme_drift  mit --check: readme.md ist nicht die Projektion
    readback      das Zurückgelesene ist nicht das Geschriebene
Exit 0: geschrieben oder gleich. Exit 2: falscher Aufruf. Nur Standardbibliothek, Python 3.9.
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import repo_objects  # noqa: E402  Die Objekte des Repos, eine Datei je Objekt (§280)

STANDARD = ".claude/way-of-working-standard.md"
WOW = "way-of-working.md"
README = "readme.md"
WOW_HEAD = ("<!-- Projektion aus .claude/way-of-working-standard.md und den Abweichungen in "
            "way-of-working/; nie von Hand ändern (§286). -->")
README_HEAD = ("<!-- Projektion aus project.yml, epics/, gaps/, todo/, decisions/ und scope/; "
               "nie von Hand ändern (§288). -->")
RECENT = 5

LABELS = {
    "de": {
        "project": "Vorhaben", "customer": "Kunde", "title": "Vorhaben", "shops": "Shops",
        "links": "Links", "folder": "Projektordner", "sheet": "Anforderungsliste", "e2e": "E2E-Sheet",
        "board": "Board", "confluence": "Confluence", "figma": "Figma",
        "chain": "Stand der Kette", "epic": "Epic", "status": "Status", "draft": "Entwurf",
        "epic_page": "Epic Page", "no_epics": "Noch kein Schnitt.", "released": "Freigegeben am {date} ({folder}).",
        "not_released": "Noch nicht freigegeben.", "requirements": "Anforderungen",
        "blocking": "Offene Fragen, an denen die Arbeit hängt", "question": "Frage", "to": "An",
        "concerns": "Betrifft", "none": "Keine.", "todo": "Offene Aufgaben", "task": "Aufgabe",
        "decisions": "Jüngste Entscheidungen", "decision": "Entscheidung",
        "wow": "Arbeitsweise", "wow_line": "Wie in diesem Vorhaben gearbeitet wird, steht in "
                                           "[`way-of-working.md`](way-of-working.md); Abweichungen vom Standard: {n}.",
        "yes": "ja",
    },
    "en": {
        "project": "Project", "customer": "Customer", "title": "Project", "shops": "Shops",
        "links": "Links", "folder": "Project folder", "sheet": "Requirements list", "e2e": "E2E sheet",
        "board": "Board", "confluence": "Confluence", "figma": "Figma",
        "chain": "State of the chain", "epic": "Epic", "status": "Status", "draft": "Draft",
        "epic_page": "Epic page", "no_epics": "No cut yet.", "released": "Released on {date} ({folder}).",
        "not_released": "Not released yet.", "requirements": "Requirements",
        "blocking": "Open questions that block work", "question": "Question", "to": "To",
        "concerns": "Concerns", "none": "None.", "todo": "Open tasks", "task": "Task",
        "decisions": "Recent decisions", "decision": "Decision",
        "wow": "Way of working", "wow_line": "How this project works is in "
                                             "[`way-of-working.md`](way-of-working.md); deviations from the standard: {n}.",
        "yes": "yes",
    },
}


class Refused(Exception):
    """Ein Befund; der Text beginnt mit dem Namen der Prüfung."""


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def readable(objects, kinds):
    for kind in kinds:
        for o in objects[kind]:
            if "error" in o:
                raise Refused(f"object {o['name']} {o['error']}")


# --- way-of-working.md --------------------------------------------------------------------------------

def deviation_block(o):
    h = o["head"]
    meta = [str(h.get("date", "")), str(h.get("by", ""))]
    if h.get("proposed_by"):
        meta.append(f"vorgeschlagen von {h['proposed_by']}")
    if h.get("skill"):
        meta.append(f"eigener Skill `{h['skill']}`")
    lines = [f"> **Abweichung in diesem Vorhaben** ({', '.join(m for m in meta if m)})", ">"]
    lines += [f"> {line}".rstrip() for line in o["body"].strip().split("\n")]
    lines += [">", f"> Grund: {h.get('reason', '')}"]
    return "\n".join(lines)


def render_wow(repo, objects):
    standard = (Path(repo) / STANDARD).read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=## )", standard)
    titles = [re.match(r"^## (.+?)\s*$", p.split("\n", 1)[0]).group(1) if p.startswith("## ") else None
              for p in parts]
    blocks = {t: [] for t in titles if t}
    for o in objects["way_of_working"]:
        section = str(o["head"].get("section", ""))
        if section not in blocks:
            raise Refused(f"wow_section {o['name']} nennt den Abschnitt „{section}“, den der Standard "
                          f"nicht hat")
        blocks[section].append(deviation_block(o))
    out = []
    for i, (title, part) in enumerate(zip(titles, parts)):
        if title and blocks[title]:
            part = part.rstrip("\n") + "\n\n" + "\n\n".join(blocks[title]) + "\n"
            if i < len(parts) - 1:
                part += "\n"
        out.append(part)
    return WOW_HEAD + "\n" + "".join(out)


# --- readme.md ----------------------------------------------------------------------------------------

def released(repo):
    """Die jüngste Freigabe aus scope/: (Datum, Ordner) oder None."""
    found = []
    for m in sorted((Path(repo) / "scope").glob("*/manifest.yml")):
        text = m.read_text(encoding="utf-8")
        dates = re.findall(r'^  - date: "([^"]+)"', text.split("\nreleases:", 1)[-1], re.M) \
            if "\nreleases:" in text else []
        for d in dates:
            found.append((d, f"scope/{m.parent.name}"))
    return max(found) if found else None


def cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


def render_readme(repo, objects, project, sheet):
    lang = "en" if project.get("language") == "en" else "de"
    L = LABELS[lang]
    title, customer = project.get("title") or "", project.get("customer") or ""
    out = [README_HEAD, f"# {' – '.join(x for x in (title, customer) if x) or L['project']}", ""]

    out += [f"## {L['project']}", ""]
    out.append(f"- {L['customer']}: {customer}")
    out.append(f"- {L['title']}: {title}" + (f" (`{project['key']}`)" if project.get("key") else ""))
    shops = project.get("shops") or []
    out.append(f"- {L['shops']}: " + ", ".join(
        f"`{s.get('key', '')}`" + (f" ({s['domain']})" if s.get("domain") else "") for s in shops))
    out.append("")

    links = []
    if project.get("project_folder"):
        links.append((L["folder"], f"https://drive.google.com/drive/folders/{project['project_folder']}"))
    for key, label in (("requirements_sheet", "sheet"), ("e2e_sheet", "e2e")):
        if project.get(key):
            links.append((L[label], f"https://docs.google.com/spreadsheets/d/{project[key]}"))
    board = project.get("board") or {}
    if isinstance(board, dict) and board.get("tool"):
        links.append((L["board"], f"{board['tool']} `{board.get('project', '')}`"))
    conf = project.get("confluence") or {}
    if isinstance(conf, dict) and conf.get("space"):
        links.append((L["confluence"], f"`{conf['space']}`"))
    if project.get("figma"):
        links.append((L["figma"], project["figma"]))
    out += [f"## {L['links']}", ""] + ([f"- {k}: {v}" for k, v in links] or [L["none"]]) + [""]

    out += [f"## {L['chain']}", ""]
    reqs_of = {}
    for r in objects["requirements"]:
        if "head" in r and r["head"].get("epic"):
            reqs_of.setdefault(str(r["head"]["epic"]), []).append(r["key"])
    epics = [e for e in objects["epics"] if "head" in e]
    if epics:
        out += [f"| {L['epic']} | {L['status']} | {L['requirements']} | {L['draft']} | {L['epic_page']} |",
                "|---|---|---|---|---|"]
        for e in epics:
            h = e["head"]
            status = sheet.display(sheet.EPIC_STATUS, str(h.get("status", "")), lang) or cell(h.get("status", ""))
            link = lambda u, t: f"[{t}]({u})" if u else ""
            out.append(f"| {e['key']} {cell(h.get('title', ''))} | {status} | "
                       f"{len(reqs_of.get(e['key'], []))} | {link(h.get('draft'), L['draft'])} | "
                       f"{link(h.get('epic_page'), L['epic_page'])} |")
    else:
        out.append(L["no_epics"])
    rel = released(repo)
    out += ["", L["released"].format(date=rel[0], folder=rel[1]) if rel else L["not_released"], ""]

    out += [f"## {L['blocking']}", ""]
    gaps = [g for g in objects["gaps"] if "head" in g and g["head"].get("status") == "open"
            and g["head"].get("blocking") == "yes"]
    if gaps:
        out += [f"| GAP | {L['question']} | {L['to']} | {L['concerns']} |", "|---|---|---|---|"]
        for g in gaps:
            h = g["head"]
            question = repo_objects.first_sentence(repo_objects.sections(g["body"])[""])
            out.append(f"| {g['key']} | {cell(question)} | {cell(h.get('to', ''))} | "
                       f"{cell(', '.join(h.get('concerns') or []))} |")
    else:
        out.append(L["none"])
    out.append("")

    out += [f"## {L['todo']}", ""]
    todos = [t for t in objects["todo"] if "head" in t and t["head"].get("status") == "open"]
    if todos:
        out += [f"| {L['task']} | {L['to']} |", "|---|---|"]
        out += [f"| [{cell(t['head'].get('title', ''))}]({t['name']}) | {cell(t['head'].get('to', ''))} |"
                for t in todos]
    else:
        out.append(L["none"])
    out.append("")

    out += [f"## {L['decisions']}", ""]
    adrs = sorted((d for d in objects["decisions"] if "head" in d), key=lambda d: d["key"], reverse=True)
    if adrs:
        out += [f"- [{d['key']} {cell(d['head'].get('title', ''))}]({d['name']}) ({d['head'].get('status', '')})"
                for d in adrs[:RECENT]]
    else:
        out.append(L["none"])
    out.append("")

    out += [f"## {L['wow']}", "", L["wow_line"].format(n=len(objects["way_of_working"]))]
    return "\n".join(out) + "\n"


# --- Aufruf ---------------------------------------------------------------------------------------------

def project_of(repo):
    path = Path(repo) / "project.yml"
    if not path.is_file():
        raise Refused("object project.yml fehlt")
    try:
        return repo_objects.read_yaml(path.read_text(encoding="utf-8"))
    except repo_objects.ObjectError as e:
        raise Refused(f"object project.yml {e}")


def render(repo):
    objects = repo_objects.load(repo)
    readable(objects, ("requirements", "epics", "gaps", "todo", "decisions", "way_of_working"))
    return {WOW: render_wow(repo, objects),
            README: render_readme(repo, objects, project_of(repo), load("check-sheet"))}


def main(argv):
    if not argv or argv[0].startswith("-") or any(a != "--check" for a in argv[1:]):
        print("Aufruf: project-readme.py <repo> [--check]", file=sys.stderr)
        return 2
    repo, check = Path(argv[0]), "--check" in argv[1:]
    if not (repo / STANDARD).is_file():
        print(f"Aufruf: {STANDARD} fehlt in {repo}", file=sys.stderr)
        return 2
    try:
        files = render(repo)
        if check:
            drift = [f for f, text in files.items()
                     if not (repo / f).is_file() or (repo / f).read_text(encoding="utf-8") != text]
            for f in drift:
                name = "wow_drift" if f == WOW else "readme_drift"
                print(f"{name} {f} ist nicht die Projektion; der nächste Lauf ersetzt sie"
                      + ("; eine Abweichung gehört als Datei nach way-of-working/ (§286)" if f == WOW else ""))
            if not drift:
                print("GLEICH | readme.md und way-of-working.md sind die Projektion")
            return 1 if drift else 0
        for f, text in files.items():
            (repo / f).write_text(text, encoding="utf-8")
            if (repo / f).read_text(encoding="utf-8") != text:
                raise Refused(f"readback {f} ist nicht das Geschriebene")
            print(f"GESCHRIEBEN {f}")
        return 0
    except Refused as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
