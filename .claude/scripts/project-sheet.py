#!/usr/bin/env python3
"""Projiziert das Repo in die Anforderungsliste (§280, §283): berechnet aus den Objekten und der einen
Lesung je Tab (§280, Regel 7) die Tabelle `changes`, die der Lead bestätigt und der Agent
`project-sheet-writer` schreibt. Das Script schreibt selbst nichts ins Sheet.

Aufruf:
    project-sheet.py <repo> --tab Anforderungen=<datei> --tab Solutioning=<datei> --tab Epics=<datei>
                     --tab "Offene Punkte"=<datei> [--base <git-rev>] [--out <changes.json>]
    project-sheet.py <repo> --base <git-rev> --repo-only

--repo-only (§311) liest kein Sheet: es vergleicht die Zeilen, die das Repo im Stand --base und im
Arbeitsstand ergibt, nur in den Spalten des Repos. Ausgabe je Tab mit Änderung eine Zeile
`GEÄNDERT <Tab> | <Kennungen>`, am Ende `GEÄNDERT <n>` oder `KEINE | Sheet: keine Stelle geändert`;
dann unterbleiben Lesung und Schreiben.

--tab nennt jeden Tab mit seinem Namen im Sheet in der Sprache aus `language` in project.yml und die
Datei der Lesung: CSV, TSV oder die Antwort von `Google_Sheets.get_values` über den ganzen Tab (wie in
scope-snapshot.py). --base nennt den Stand des Repos, den die letzte Projektion geschrieben hat:
den Commit, auf dem der Lauf begann, `refs/strix/run-start` aus sync-main.py (§319); eine Zelle des Repos, die im Sheet weder diesem Stand
noch dem neuen gleicht, hat ein Mensch geändert, und sie wird als Abweichung vorgelegt. Die
Projektion übernimmt nichts aus dem Sheet (§280, Regel 6).

Geschrieben werden nur Spalten des Repos (requirements-list-contract.md); Spalten der Menschen und die
Formel nie. Jede Zeile findet die Projektion über ihre Kennung in Spalte A. Werte mit Vokabular gehen
als Anzeigewert in der Sprache des Projekts hinaus (§295).

Ausgabe je Stelle eine Zeile, in der Folge, in der der Agent schreibt:
    ÄNDERN <Tab> | <Stelle> | <heute> | <neu>          eine Zelle; `neu` leer heißt: die Zelle leeren
    ABWEICHUNG <Tab> | <Stelle> | <heute> | <neu>      dasselbe, aber die Zelle hat ein Mensch geändert;
                                                       eine leere Zelle nie, sie wird ÄNDERN
    NEU <Tab> | <Bereich> | leer | <Werte>             eine neue Zeile, je Bereich zwischen Spalten
                                                       der Menschen oder der Formel eine Stelle
    LÖSCHEN <Tab> | Zeile <n> (<Kennung>, löschen) | <Kennung> | leer
                                                       eine Zeile im Tab Offene Punkte, deren Frage
                                                       geschlossen ist; von unten nach oben, zuletzt
Am Ende `STELLEN <n>` oder `GLEICH`. --out schreibt dieselben Stellen als JSON
`{"language": …, "changes": [{"kind", "tab", "stelle", "heute", "neu"}]}`, `neu` bei NEU als Liste.

Prüfungen, je eine Zeile `<prüfung> <detail>` und Exit 1, ohne Ausgabe der Stellen:
    object        eine Datei des Repos ist nicht lesbar; das meldet sonst check-repo.py
    value         ein Wert hat keinen Anzeigewert im Vertrag
    input         ein Tab fehlt, ist keiner des Vertrags oder ist nicht lesbar
    header        die Kopfzeile eines Tabs ist nicht die des Vertrags in der Sprache des Projekts
    duplicate_id  eine Kennung steht in einem Tab zweimal; die Projektion fände ihre Zeile nicht
    base          --base ist kein Stand des Repos; fehlt refs/strix/run-start, nennt die Meldung
                  sync-main.py als Abhilfe
Exit 0: Stellen berechnet oder gleich. Exit 2: falscher Aufruf. Nur Standardbibliothek, Python 3.9.
"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import repo_objects  # noqa: E402  Die Objekte des Repos, eine Datei je Objekt (§280)

FOLDERS = ("requirements", "epics", "gaps")
START_REF = "refs/strix/run-start"  # der Startcommit aus sync-main.py (§319)
SHOWN = ("decided", "blocked")  # ein Lösungsansatz mit proposed oder ohne Status erscheint nicht (§275)


class Refused(Exception):
    """Ein Befund; der Text beginnt mit dem Namen der Prüfung."""


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SHEET = load("check-sheet")
SNAPSHOT = load("scope-snapshot")


# --- Die Zeilen, die das Repo ergibt -------------------------------------------------------------------

def shown(field, value, lang, where):
    if value in ("", None) and "" not in SHEET.VALUES[field]:
        return ""
    text = SHEET.display(field, value, lang)
    if text is None:
        raise Refused(f"value {where}: „{value}“ hat keinen Anzeigewert in {field}")
    return text


def options(body):
    """Die Lösungsansätze aus `## Approach`: je Unterabschnitt ### (Name, Text)."""
    approach = repo_objects.sections(body).get("Approach", "")
    out = []
    for part in re.split(r"(?m)^### ", approach)[1:]:
        name, _, text = part.partition("\n")
        lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
        kb = [l for l in lines if l.startswith("KB:")]
        prose = " ".join(l for l in lines if not l.startswith("KB:"))
        out.append((name.strip(), f"{name.strip()}: {repo_objects.first_sentence(prose)}"
                    + (f"\n{kb[0]}" if kb else "")))
    return out


def question_lines(gaps, rid, kinds):
    return "\n".join(f"{g['key']} {repo_objects.first_sentence(repo_objects.sections(g['body'])[''])}"
                     for g in gaps if g["head"].get("kind") in kinds and rid in (g["head"].get("concerns") or []))


def rows(objects, lang, shops=()):
    """Je Tab die Zeilen des Repos: Kennung → {Schlüssel der Spalte: Wert}, nur Spalten des Repos.
    shops sind die `key` aus project.yml: der Titel trägt den Shop-Bezug hinten, die Spalte `Shops`
    alle Schlüssel, für die die Anforderung gilt (§307)."""
    for kind in FOLDERS:
        for o in objects[kind]:
            if "error" in o:
                raise Refused(f"object {o['name']} {o['error']}")
    open_gaps = [g for g in objects["gaps"] if g["head"].get("status") == "open"]
    out = {"requirements": {}, "solutioning": {}, "epics": {}, "open_items": {}}
    members = {}
    for r in objects["requirements"]:
        h, k = r["head"], r["key"]
        parts = repo_objects.sections(r["body"])
        members.setdefault(str(h.get("epic", "")), []).append(k)
        title = repo_objects.shops_title(str(h.get("title", "")), h.get("shops"), shops, lang, sheet=True)
        out["requirements"][k] = {
            "id": k, "title": title,
            "description": repo_objects.first_paragraph(parts.get("Description", "")),
            "epic": str(h.get("epic", "")),
            "status": shown("status (Anforderung)", h.get("status"), lang, f"{k} status"),
            "priority": shown("priority", h.get("priority", ""), lang, f"{k} priority"),
            "scope": shown("scope", h.get("scope", ""), lang, f"{k} scope"),
            "design_needed": shown("design_needed, interface_needed", h.get("design_needed"), lang, f"{k} design_needed"),
            "interface_needed": shown("design_needed, interface_needed", h.get("interface_needed"), lang,
                                      f"{k} interface_needed"),
            "open_questions": question_lines(open_gaps, k, ("discovery",)),
            "source": str(h.get("source", "")),
            "live": shown("live", h.get("live", ""), lang, f"{k} live"),
            "current_state": repo_objects.first_paragraph(parts.get("Current state", "")),
            "shops": repo_objects.shops_cell(h.get("shops"), shops),
        }
        decided = h.get("solution_status") in SHOWN
        opts = options(r["body"]) if decided else []
        cls = h.get("classification") or []
        cls = [cls] if isinstance(cls, str) else cls
        out["solutioning"][k] = {
            "id": k, "title": title,
            "classification": " + ".join(shown("classification", c, lang, f"{k} classification") for c in cls)
            if decided else "",
            "size": shown("size", h.get("size", ""), lang, f"{k} size") if decided else "",
            "option_1": opts[0][1] if len(opts) > 0 else "",
            "option_2": opts[1][1] if len(opts) > 1 else "",
            "option_3": opts[2][1] if len(opts) > 2 else "",
            "recommendation": opts[0][0] if opts else "",
            "open_questions": question_lines(open_gaps, k, ("solutioning", "decision")),
            "depends_on": ", ".join(h.get("depends_on") or []) if decided else "",
            "solution_status": shown("solution_status", h.get("solution_status", ""), lang, f"{k} solution_status"),
        }
    for e in objects["epics"]:
        h, k = e["head"], e["key"]
        out["epics"][k] = {
            "id": k, "domain": shown(SHEET.DOMAIN, h.get("domain"), lang, f"{k} domain"),
            "title": str(h.get("title", "")), "summary": str(h.get("summary", "")),
            "requirements": ", ".join(sorted(members.get(k, []))),
            "status": shown(SHEET.EPIC_STATUS, h.get("status"), lang, f"{k} status"),
            "information": shown("information (Epic)", h.get("information"), lang, f"{k} information"),
            "clarification": str(h.get("clarification", "")), "draft": str(h.get("draft", "")),
            "epic_page": str(h.get("epic_page", "")), "board_key": str(h.get("board_key", "")),
        }
    for g in open_gaps:
        h, k = g["head"], g["key"]
        out["open_items"][k] = {
            "id": k, "kind": shown("kind (Frage)", h.get("kind"), lang, f"{k} kind"),
            "question": " ".join(repo_objects.sections(g["body"])[""].split()),
            "to": str(h.get("to", "")), "concerns": ", ".join(h.get("concerns") or []),
            "blocking": shown("blocking", h.get("blocking"), lang, f"{k} blocking"),
        }
    return out


# --- Der Stand vor dem Lauf ------------------------------------------------------------------------------

def objects_at(repo, rev, tmp):
    """Die Objekte, wie sie im Stand <rev> lagen."""
    def git(*args):
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").returncode != 0:
        if rev == START_REF:
            raise Refused(f"base {rev} fehlt: sync-main.py lief am Start des Laufs nicht und hat den Startcommit "
                          f"nicht gemerkt; die Projektion rechnet nicht ersatzweise mit HEAD und unterbleibt. "
                          f"Abhilfe: sync-main.py . am Start jedes Laufs (§319)")
        raise Refused(f"base {rev} ist kein Stand des Repos")
    for folder in FOLDERS:
        listing = git("ls-tree", "--name-only", rev, f"{folder}/")
        for path in listing.stdout.split():
            target = Path(tmp) / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(git("show", f"{rev}:{path}").stdout, encoding="utf-8")
    return repo_objects.load(tmp)


# --- Abgleich mit dem Gelesenen --------------------------------------------------------------------------

def letter(i):
    return chr(ord("A") + i)


def compare(tab, lang, read, want, before):
    """Die Stellen eines Tabs: Änderungen und Abweichungen, neue Zeilen, Löschungen."""
    name = SHEET.tab_name(tab, lang)
    cols = SHEET.TABS[tab][1]
    keys = [c[0] for c in cols]
    head = [h.strip() for h in read[0]]
    while head and not head[-1]:
        head.pop()
    if head != SHEET.columns(tab, lang):
        raise Refused(f"header {name}: Zeile 1 ist {' | '.join(head)!r}, erwartet "
                      f"{' | '.join(SHEET.columns(tab, lang))!r}")
    at, last = {}, 1
    for n, r in enumerate(read[1:], start=2):
        r = (list(r) + [""] * len(cols))[:len(cols)]
        key = r[0].strip()
        if any(c.strip() for c in r):
            last = n
        if not key:
            continue
        if key in at:
            raise Refused(f"duplicate_id {name}: {key} steht in Zeile {at[key][0]} und {n}")
        at[key] = (n, r)
    changes, deletes = [], []
    repo_cols = [i for i, c in enumerate(cols) if c[3] == SHEET.REPO]
    for key, values in sorted(want.items()):
        if key not in at:
            continue
        n, r = at[key]
        for i in repo_cols:
            today, new = r[i].strip(), values[keys[i]].strip()
            if today == new:
                continue
            old = (before or {}).get(key, {}).get(keys[i])
            # eine leere Zelle hat kein Mensch geändert, etwa eine neu angelegte Spalte
            kind = "ABWEICHUNG" if before is not None and old is not None and today and today != old.strip() else "ÄNDERN"
            changes.append({"kind": kind, "tab": name, "stelle": f"{letter(i)}{n} ({key}, {cols[i][1 + SHEET.LANGUAGES.index(lang)]})",
                            "heute": today, "neu": new})
    runs, start = [], None
    for i in range(len(cols) + 1):
        inside = i < len(cols) and cols[i][3] == SHEET.REPO
        if inside and start is None:
            start = i
        elif not inside and start is not None:
            runs.append((start, i))
            start = None
    for key in sorted(k for k in want if k not in at):
        last += 1
        for a, b in runs:
            changes.append({"kind": "NEU", "tab": name, "stelle": f"{letter(a)}{last}:{letter(b - 1)}{last} ({key}, neu)",
                            "heute": "", "neu": [want[key][keys[i]] for i in range(a, b)]})
    if tab == "open_items":
        for key, (n, _) in sorted(at.items(), key=lambda x: -x[1][0]):
            if key not in want:
                deletes.append({"kind": "LÖSCHEN", "tab": name, "stelle": f"Zeile {n} ({key}, löschen)",
                                "heute": key, "neu": ""})
    return changes, deletes


def repo_only(repo, base, lang, shops):
    """Die Kennungen je Tab, deren Zeile sich zwischen --base und dem Arbeitsstand ändert (§311)."""
    now = rows(repo_objects.load(repo), lang, shops)
    with tempfile.TemporaryDirectory() as tmp:
        before = rows(objects_at(repo, base, tmp), lang, shops)
    total = 0
    for tab in SHEET.TABS:
        keys = sorted(k for k in set(now[tab]) | set(before[tab]) if now[tab].get(k) != before[tab].get(k))
        if keys:
            total += len(keys)
            print(f"GEÄNDERT {SHEET.tab_name(tab, lang)} | {', '.join(keys)}")
    print(f"GEÄNDERT {total}" if total else "KEINE | Sheet: keine Stelle geändert")
    return 0


def one_line(text):
    return " ⏎ ".join(str(text).split("\n")) if text != "" else "leer"


def main(argv):
    p = argparse.ArgumentParser(prog="project-sheet.py", description=__doc__.split("\n")[0])
    p.add_argument("repo")
    p.add_argument("--tab", action="append")
    p.add_argument("--base")
    p.add_argument("--out")
    p.add_argument("--repo-only", action="store_true")
    a = p.parse_args(argv)
    if a.repo_only and not a.base:
        p.error("--repo-only braucht --base")
    repo = Path(a.repo)
    try:
        project = repo_objects.read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
        lang = "en" if project.get("language") == "en" else "de"
        shops = repo_objects.project_shop_keys(project)
        if a.repo_only:
            return repo_only(repo, a.base, lang, shops)
        files = {}
        for item in a.tab or []:
            name, _, path = item.partition("=")
            key, langs = SHEET.tab_of(name.strip())
            if key is None or lang not in langs:
                raise Refused(f"input --tab {name.strip()!r} ist kein Tab des Vertrags in {lang}")
            files[key] = path
        missing = [SHEET.tab_name(t, lang) for t in SHEET.TABS if t not in files]
        if missing:
            raise Refused(f"input --tab fehlt für {', '.join(missing)}")
        try:
            reads = {t: SNAPSHOT.load_rows(path) for t, path in files.items()}
        except SNAPSHOT.Refused as e:
            raise Refused(str(e))
        want = rows(repo_objects.load(repo), lang, shops)
        before = None
        if a.base:
            with tempfile.TemporaryDirectory() as tmp:
                before = rows(objects_at(repo, a.base, tmp), lang, shops)
        changes, deletes = [], []
        for tab in SHEET.TABS:
            c, d = compare(tab, lang, reads[tab], want[tab], before[tab] if before else None)
            changes += c
            deletes += d
    except (Refused, repo_objects.ObjectError) as e:
        print(str(e) if isinstance(e, Refused) else f"object project.yml {e}")
        return 1
    except OSError as e:
        print(f"input {e}")
        return 1
    stellen = changes + deletes
    for s in stellen:
        neu = " | ".join(one_line(v) for v in s["neu"]) if isinstance(s["neu"], list) else one_line(s["neu"])
        print(f"{s['kind']} {s['tab']} | {s['stelle']} | {one_line(s['heute'])} | {neu}")
    print(f"STELLEN {len(stellen)}" if stellen else "GLEICH | das Sheet zeigt den Stand des Repos")
    if a.out:
        Path(a.out).write_text(json.dumps({"language": lang, "changes": stellen}, ensure_ascii=False, indent=1),
                               encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
