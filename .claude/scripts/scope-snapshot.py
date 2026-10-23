#!/usr/bin/env python3
"""Hält den Stand der Anforderungsliste am Ende der Discovery, bei Proposal und Freigabe fest und
vergleicht ihn (§266, §280 Regel 8).

Ein Snapshot ist Kontext, nie Wahrheit: was gilt, steht im Repo. Er zeigt, wogegen ein Kunde
freigegeben hat, damit eine spätere Änderung als mögliche Change Request sichtbar wird, bevor gebaut
wird.

Aufruf:
  scope-snapshot.py write <repo> --occasion discovery|proposal|release --sheet <id>
        --read-at <JJJJ-MM-TTThh:mmZ> --tab Anforderungen=<datei> --tab Solutioning=<datei>
        --tab Epics=<datei> --tab "Offene Punkte"=<datei> [--pages <pages.json>]
        [--proposal-id <id> --proposal-created <createdTime>]     nur und immer bei proposal, release
        [--estimate-id <id> --estimate-created <createdTime>]
        [--released-by <wer> --release-date <JJJJ-MM-TT>]        nur und immer bei release
  scope-snapshot.py release <repo> <ordner> --released-by <wer> --release-date <JJJJ-MM-TT>
  scope-snapshot.py latest <repo> [--released]
  scope-snapshot.py compare <repo> <ordner> --tab Anforderungen=<datei> --tab Solutioning=<datei>
        --tab Epics=<datei> --tab "Offene Punkte"=<datei>

--tab nennt einen Tab mit seinem Namen im Sheet, in `de` oder `en` (`Requirements`, `Open items`);
alle vier stehen in derselben Sprache, die die Kopfzeile von `Anforderungen` zeigt. Eine <datei> eines Tabs ist der CSV-Export (`.csv`), eine TSV (`.tsv`) oder die Antwort von
`Google_Sheets.get_values` über den ganzen Tab: als JSON, auch in der Hülle `valueRanges` mit genau
einem Bereich, oder die Datei, als die die Sitzung eine große Antwort ablegt. <pages.json> trägt je
Epic mit Epic Page oder Entwurf `source` (`page` | `draft`) und `version`, in der Form von
solution-proposal; weitere Felder liest das Script nicht. Ohne --pages gilt `{}`; dann darf kein Epic
eine Epic Page oder einen Entwurf tragen, wie am Ende der Discovery.

write   legt `scope/<JJJJ-MM-TT>-<anlass>/` an (das Datum aus --read-at; gibt es den Ordner, mit
        `-2`, `-3` …) mit `anforderungen.tsv`, `solutioning.tsv`, `epics.tsv`, `offene-punkte.tsv`
        und `manifest.yml`, liest
        alles zurück und gibt `SNAPSHOT scope/<ordner>` aus. Liegt `baselines.yml` in <repo>, steht ihr
        Inhalt im Manifest. Ein bestehender Ordner wird nie beschrieben.
release hängt an das Manifest eines Snapshots den Eintrag der Freigabe unter `releases` an; sonst
        ändert sich nichts.
latest  gibt den jüngsten Snapshot aus (nach `read_at`), mit --released den jüngsten freigegebenen.
compare listet je Tab neue, entfernte und geänderte Zeilen gegen den Snapshot, je geänderte Spalte
        eine Zeile: `NEU`, `ENTFERNT`, `GEÄNDERT`, `KOPF`, am Ende `ABWEICHUNGEN <n>` oder `GLEICH`.
        Er entscheidet nichts; jede Zeile ist eine mögliche Change Request.

Prüfungen, je eine Zeile `<prüfung> <detail>` und Exit 1, ohne dass etwas geschrieben ist:
  input        eine Datei fehlt oder trägt keine Zeilen eines Tabs
  header       die Kopfzeile eines Tabs ist nicht die aus requirements-list-contract.md in der Sprache
               des Tabs Anforderungen, oder eine Zeile trägt Werte rechts davon
  read_at      --read-at ist keine Lesezeit der Form JJJJ-MM-TTThh:mmZ
  sheet        --sheet ist leer
  epic         ein Epic mit Epic Page oder Entwurf hat in pages.json keine Fassung oder keinen Link im
               Sheet, oder pages.json nennt ein Epic, das der Tab nicht trägt; ein Epic mit Status
               `Zusammengeführt` darf ohne Fassung stehen
  document     Datei-ID oder `createdTime` des Proposals fehlt bei proposal oder release, beim
               Schätzdokument steht nur eins von beiden, oder bei discovery steht eines da
  released_by  bei release fehlt, wer freigegeben hat; bei proposal steht es da
  release_date das Datum der Freigabe hat nicht die Form JJJJ-MM-TT
  released     der Snapshot trägt schon eine Freigabe
  snapshot     der Ordner hat kein lesbares Manifest oder keine TSV eines Tabs
  readback     das Zurückgelesene ist nicht das Geschriebene; der neue Ordner wird wieder entfernt
Exit 0: geschrieben, gefunden oder gleich. Exit 3: latest fand keinen Snapshot, compare fand
Abweichungen. Exit 2: falscher Aufruf.

Nur Standardbibliothek: der Rechner eines Leads muss kein PyYAML haben. Das Manifest schreibt jeden
Wert als JSON-String, der zugleich gültiges YAML ist, und liest genau diese Form zurück.
"""
import argparse
import csv
import importlib.util
import io
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

SCOPE = "scope"
MANIFEST = "manifest.yml"
BASELINES = "baselines.yml"
OCCASIONS = ("discovery", "proposal", "release")
# Tab in check-sheet.py, Datei im Snapshot, Spalte mit dem Titel einer Zeile.
TABS = (("requirements", "anforderungen.tsv", "title"),
        ("solutioning", "solutioning.tsv", "title"),
        ("epics", "epics.tsv", "title"),
        ("open_items", "offene-punkte.tsv", "question"))
READ_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?Z$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CUT = 300


class Refused(Exception):
    """Ein Befund; der Text beginnt mit dem Namen der Prüfung."""


def contract():
    """Tabs, Kopfzeilen und Anzeigewerte aus check-sheet.py: es gibt sie nur einmal (§219, §247)."""
    spec = importlib.util.spec_from_file_location("check_sheet", Path(__file__).with_name("check-sheet.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SHEET = contract()


def name_of(tab, lang):
    return SHEET.tab_name(tab, lang)


def index_of(tab, key):
    return [c[0] for c in SHEET.TABS[tab][1]].index(key)


# --- Lesen ------------------------------------------------------------------------------------------

def find_values(node):
    """Die Zeilen einer get_values-Antwort, auch in einer Hülle oder als JSON in einem Textfeld."""
    if isinstance(node, dict):
        if isinstance(node.get("valueRanges"), list):
            ranges = node["valueRanges"]
            if len(ranges) != 1:
                raise Refused(f"input die Antwort trägt {len(ranges)} Bereiche; gelesen wird ein "
                              f"Bereich über den ganzen Tab")
            return ranges[0].get("values", [])
        if isinstance(node.get("values"), list):
            return node["values"]
        for v in node.values():
            found = find_values(v)
            if found is not None:
                return found
    elif isinstance(node, list):
        if node and all(isinstance(r, list) for r in node):
            return node
        for v in node:
            found = find_values(v)
            if found is not None:
                return found
    elif isinstance(node, str) and node.lstrip()[:1] in ("{", "["):
        try:
            return find_values(json.loads(node))
        except json.JSONDecodeError:
            return None
    return None


def load_rows(path):
    path = Path(path)
    if not path.is_file():
        raise Refused(f"input {path.name} fehlt")
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".csv":
        rows = list(csv.reader(io.StringIO(text)))
    elif path.suffix == ".tsv":
        rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    else:
        try:
            rows = find_values(json.loads(text))
        except json.JSONDecodeError as e:
            raise Refused(f"input {path.name} ist weder CSV noch eine lesbare Antwort von get_values: {e}")
        if rows is None:
            raise Refused(f"input {path.name} trägt keine Zeilen (`values`)")
    rows = [["" if c is None else str(c) for c in r] for r in rows]
    while rows and not any(c.strip() for c in rows[-1]):
        rows.pop()
    if not rows:
        raise Refused(f"input {path.name} ist leer")
    return rows


def language_of(path):
    """Die Sprache der Kopfzeile des Tabs Anforderungen."""
    got = [h.strip() for h in load_rows(path)[0]]
    while got and not got[-1]:
        got.pop()
    for lang in SHEET.LANGUAGES:
        if got == SHEET.columns("requirements", lang):
            return lang
    raise Refused(f"header {path.name}: Zeile 1 ist "
                  f"{' | '.join(got)!r}, die Kopfzeile von Anforderungen in keiner Sprache des Vertrags")


def table(name, path, head):
    """Die Zeilen eines Tabs, jede auf die Breite der Kopfzeile des Vertrags gebracht."""
    rows = load_rows(path)
    got = list(rows[0])
    while got and not got[-1].strip():
        got.pop()
    if [h.strip() for h in got] != head:
        raise Refused(f"header {name}: Zeile 1 ist {' | '.join(got)!r}, erwartet {' | '.join(head)!r}")
    out = []
    for n, r in enumerate(rows, start=1):
        if any(c.strip() for c in r[len(head):]):
            raise Refused(f"header {name}: Zeile {n} trägt Werte rechts der Spalte {head[-1]!r}")
        out.append((r + [""] * len(head))[:len(head)])
    out[0] = list(head)
    return out


def tsv(rows):
    buf = io.StringIO()
    csv.writer(buf, delimiter="\t", lineterminator="\n").writerows(rows)
    return buf.getvalue()


# --- Manifest -----------------------------------------------------------------------------------------

def q(value):
    return "null" if value is None else json.dumps(value, ensure_ascii=False)


def scalar(text):
    text = text.strip()
    if text in ("", "null", "~"):
        return None
    if text.startswith('"'):
        return json.loads(text)
    return text


def read_manifest(folder):
    """Die Felder oben und die Freigaben; genau die Form, die write schreibt."""
    path = Path(folder) / MANIFEST
    if not path.is_file():
        raise Refused(f"snapshot {folder}: {MANIFEST} fehlt")
    data, releases, last = {}, [], None
    try:
        for line in path.read_text(encoding="utf-8").split("\n"):
            if not line.strip() or line.startswith("#"):
                continue
            top = re.match(r"^([a-z_]+):(.*)$", line)
            if top:
                last, value = top.group(1), top.group(2).strip()
                data[last] = None if not value or value.startswith("|") else scalar(value)
                continue
            if last == "releases":
                item = re.match(r"^  - ([a-z_]+): (.*)$", line)
                more = re.match(r"^    ([a-z_]+): (.*)$", line)
                if item:
                    releases.append({item.group(1): scalar(item.group(2))})
                elif more and releases:
                    releases[-1][more.group(1)] = scalar(more.group(2))
                else:
                    raise Refused(f"snapshot {folder}: Zeile unter releases nicht lesbar: {line!r}")
    except json.JSONDecodeError as e:
        raise Refused(f"snapshot {folder}: {MANIFEST} nicht lesbar: {e}")
    if last != "releases":
        raise Refused(f"snapshot {folder}: {MANIFEST} endet nicht mit releases")
    for key in ("date", "occasion", "language", "read_at", "sheet"):
        if not data.get(key):
            raise Refused(f"snapshot {folder}: {MANIFEST} ohne {key}")
    data["releases"] = releases
    return data


def release_lines(by, date):
    return [f"  - date: {q(date)}", f"    released_by: {q(by)}"]


def manifest_text(a, lang, epics, tab_rows, baselines):
    lines = [
        "# Snapshot der Anforderungsliste am Ende der Discovery, bei Proposal oder Freigabe (§266).",
        "# Kontext, nie Wahrheit: es gilt, was im Repo steht. Geschrieben von",
        "# .claude/scripts/scope-snapshot.py; nie überschrieben, nur `releases` wächst.",
        f"date: {q(a.read_at[:10])}",
        f"occasion: {q(a.occasion)}",
        f"language: {q(lang)}",
        f"read_at: {q(a.read_at)}",
        f"sheet: {q(a.sheet)}",
        "tabs:",
    ]
    for (tab, fname, _), rows in zip(TABS, tab_rows):
        lines += [f"  - tab: {q(name_of(tab, lang))}", f"    file: {q(fname)}", f"    rows: {len(rows) - 1}"]
    lines.append("epics:" if epics else "epics: []")
    for e in epics:
        lines += [f"  - id: {q(e['id'])}", f"    source: {q(e['source'])}", f"    link: {q(e['link'])}",
                  f"    version: {q(e['version'])}"]
    if a.proposal_id:
        lines += ["documents:", "  proposal:", f"    file_id: {q(a.proposal_id)}",
                  f"    created_time: {q(a.proposal_created)}"]
    else:
        lines += ["documents:", "  proposal: null"]
    if a.estimate_id:
        lines += ["  estimate:", f"    file_id: {q(a.estimate_id)}",
                  f"    created_time: {q(a.estimate_created)}"]
    else:
        lines.append("  estimate: null")
    if baselines is None:
        lines.append("baselines: null")
    else:
        # Ein Literalblock mit fester Einrückung trägt den Inhalt Zeichen für Zeichen; `+` hält die
        # Zeilenumbrüche am Ende, `-` sagt, dass keiner da ist.
        body = baselines.split("\n")
        chomp = "+" if baselines.endswith("\n") else "-"
        if chomp == "+":
            body = body[:-1]
        lines.append(f"baselines: |2{chomp}")
        lines += [("  " + b) if b else "" for b in body]
    lines.append("releases:")
    if a.occasion == "release":
        lines += release_lines(a.released_by, a.release_date)
    return "\n".join(lines) + "\n"


def epic_entries(epics_rows, pages, lang):
    ids, draft, page, status = (index_of("epics", k) for k in ("id", "draft", "epic_page", "status"))
    merged = SHEET.display(SHEET.EPIC_STATUS, "merged", lang)
    seen, out = set(), []
    for r in epics_rows[1:]:
        eid = r[ids].strip()
        if not eid:
            continue
        seen.add(eid)
        page_link = r[page].strip()
        page_link = page_link if page_link.startswith("http") else ""
        draft_link = r[draft].strip()
        draft_link = draft_link if draft_link.startswith("http") else ""
        p = pages.get(eid)
        if p is not None:
            source = str(p.get("source", "")).strip()
            version = str(p.get("version", "") if p.get("version") is not None else "").strip()
            if source not in ("page", "draft"):
                raise Refused(f"epic {eid}: source in pages.json ist {source!r}, erwartet page oder draft")
            link = page_link if source == "page" else draft_link
            if not link:
                raise Refused(f"epic {eid}: pages.json nennt {source}, das Sheet trägt dafür keinen Link")
            if not version:
                raise Refused(f"epic {eid}: pages.json trägt keine Fassung")
        elif page_link or draft_link:
            if r[status].strip() != merged:
                raise Refused(f"epic {eid}: trägt {'eine Epic Page' if page_link else 'einen Entwurf'}, "
                              f"pages.json keine Fassung")
            source, link, version = ("page", page_link, "") if page_link else ("draft", draft_link, "")
        else:
            source, link, version = "none", "", ""
        out.append({"id": eid, "source": source, "link": link, "version": version})
    extra = sorted(set(pages) - seen)
    if extra:
        raise Refused(f"epic pages.json nennt {', '.join(extra)}, der Tab Epics nicht")
    return out


# --- Befehle ------------------------------------------------------------------------------------------

def tab_files(pairs):
    """Je Tab des Vertrags die Datei, dazu die Sprache aus der Kopfzeile von Anforderungen."""
    files = {}
    for p in pairs or []:
        name, _, path = p.partition("=")
        key, langs = SHEET.tab_of(name.strip())
        if key is None:
            raise Refused(f"input --tab {name.strip()!r} ist kein Tab des Vertrags")
        files[key] = (name.strip(), path, langs)
    missing = [name_of(t, "de") for t, _, _ in TABS if not files.get(t) or not files[t][1]]
    if missing:
        raise Refused(f"input --tab fehlt für {', '.join(missing)}")
    lang = language_of(Path(files["requirements"][1]))
    stray = [n for n, _, langs in files.values() if lang not in langs]
    if stray:
        raise Refused(f"header die Tabs {', '.join(stray)} heißen in {lang} anders als im Sheet")
    return {k: v[1] for k, v in files.items()}, lang


def cmd_write(a):
    repo = Path(a.repo)
    if not READ_AT.match(a.read_at or ""):
        raise Refused(f"read_at {a.read_at!r} ist keine Lesezeit der Form JJJJ-MM-TTThh:mmZ")
    if not (a.sheet or "").strip():
        raise Refused("sheet --sheet ist leer")
    proposal = (a.proposal_id or "").strip() or (a.proposal_created or "").strip()
    if a.occasion == "discovery":
        if proposal or (a.estimate_id or "").strip() or (a.estimate_created or "").strip():
            raise Refused("document am Ende der Discovery gibt es kein Proposal und keine Schätzung")
    elif not (a.proposal_id or "").strip() or not (a.proposal_created or "").strip():
        raise Refused("document Datei-ID und createdTime des Proposals gehören in jeden Snapshot "
                      "bei proposal und release")
    if bool((a.estimate_id or "").strip()) != bool((a.estimate_created or "").strip()):
        raise Refused("document beim Schätzdokument stehen Datei-ID und createdTime beide oder keins")
    if a.occasion == "release":
        if not (a.released_by or "").strip():
            raise Refused("released_by bei release nennt --released-by, wer freigegeben hat, wie der Lead es sagt")
        if not DATE.match(a.release_date or ""):
            raise Refused(f"release_date {a.release_date!r} hat nicht die Form JJJJ-MM-TT")
    elif a.released_by or a.release_date:
        raise Refused(f"released_by bei {a.occasion} gibt es keine Freigabe; die trägt release")
    files, lang = tab_files(a.tab)
    tab_rows = [table(name_of(tab, lang), files[tab], SHEET.columns(tab, lang)) for tab, _, _ in TABS]
    pages = {}
    if a.pages:
        pages_path = Path(a.pages)
        if not pages_path.is_file():
            raise Refused(f"input {pages_path.name} fehlt")
        try:
            pages = json.loads(pages_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise Refused(f"input {pages_path.name} ist kein JSON: {e}")
    epics = epic_entries(tab_rows[2], pages if isinstance(pages, dict) else {}, lang)
    base = repo / BASELINES
    baselines = base.read_text(encoding="utf-8") if base.is_file() else None

    stem = f"{a.read_at[:10]}-{a.occasion}"
    folder, n = repo / SCOPE / stem, 1
    while folder.exists():
        n += 1
        folder = repo / SCOPE / f"{stem}-{n}"
    folder.mkdir(parents=True)
    try:
        for (name, fname, _), rows in zip(TABS, tab_rows):
            (folder / fname).write_text(tsv(rows), encoding="utf-8")
        text = manifest_text(a, lang, epics, tab_rows, baselines)
        (folder / MANIFEST).write_text(text, encoding="utf-8")
        for (name, fname, _), rows in zip(TABS, tab_rows):
            if load_rows(folder / fname) != rows:
                raise Refused(f"readback {fname} ist nicht das Gelesene")
        back = read_manifest(folder)
        if (back["read_at"], back["occasion"], back["sheet"]) != (a.read_at, a.occasion, a.sheet) or \
                (folder / MANIFEST).read_text(encoding="utf-8") != text:
            raise Refused(f"readback {MANIFEST} ist nicht das Geschriebene")
    except Refused:
        shutil.rmtree(folder)
        raise
    rel = folder.relative_to(repo).as_posix()
    print(f"SNAPSHOT {rel}")
    for (tab, _, _), rows in zip(TABS, tab_rows):
        print(f"TAB {name_of(tab, lang)} | {len(rows) - 1} Zeile(n)")
    for e in epics:
        print(f"EPIC {e['id']} | {e['source']} | {e['version'] or '-'}")
    print(f"BASELINES {'übernommen' if baselines is not None else 'keine Datei'}")
    if a.occasion == "release":
        print(f"FREIGABE {a.release_date} | {a.released_by}")
    return 0


def resolve(repo, folder):
    path = Path(folder)
    return path if path.is_absolute() else Path(repo) / path


def cmd_release(a):
    folder = resolve(a.repo, a.folder)
    data = read_manifest(folder)
    if data["releases"]:
        r = data["releases"][0]
        raise Refused(f"released {a.folder} trägt schon die Freigabe vom {r.get('date')} durch "
                      f"{r.get('released_by')}; ein Snapshot wird nie überschrieben")
    if not (a.released_by or "").strip():
        raise Refused("released_by --released-by nennt, wer freigegeben hat, wie der Lead es sagt")
    if not DATE.match(a.release_date or ""):
        raise Refused(f"release_date {a.release_date!r} hat nicht die Form JJJJ-MM-TT")
    path = folder / MANIFEST
    before = path.read_text(encoding="utf-8")
    if not before.endswith("\n"):
        raise Refused(f"snapshot {a.folder}: {MANIFEST} endet nicht mit einem Zeilenumbruch")
    path.write_text(before + "\n".join(release_lines(a.released_by, a.release_date)) + "\n", encoding="utf-8")
    back = read_manifest(folder)
    if back["releases"] != [{"date": a.release_date, "released_by": a.released_by}] or \
            not path.read_text(encoding="utf-8").startswith(before):
        path.write_text(before, encoding="utf-8")
        raise Refused(f"readback {MANIFEST}: die Freigabe steht nicht wie geschrieben da")
    print(f"FREIGABE {Path(a.folder).as_posix()} | {a.release_date} | {a.released_by}")
    return 0


def snapshots(repo):
    out = []
    for m in sorted((Path(repo) / SCOPE).glob(f"*/{MANIFEST}")):
        out.append((m.parent, read_manifest(m.parent)))
    return out


def cmd_latest(a):
    found = [(d["read_at"], f.name, f) for f, d in snapshots(a.repo) if not a.released or d["releases"]]
    if not found:
        print(f"kein {'freigegebener ' if a.released else ''}Snapshot unter {SCOPE}/")
        return 3
    print(max(found)[2].relative_to(Path(a.repo)).as_posix())
    return 0


def one_line(text):
    text = text.replace("\r\n", "\n").strip().replace("\n", " ⏎ ")
    return text if len(text) <= CUT else text[:CUT] + " …"


def keyed(rows):
    head, out, count = rows[0], {}, Counter()
    for n, r in enumerate(rows[1:], start=2):
        r = (r + [""] * len(head))[:len(head)]
        key = r[0].strip()
        if not key:
            if not any(c.strip() for c in r):
                continue
            key = f"(ohne ID, Zeile {n})"
        count[key] += 1
        if count[key] > 1:
            key = f"{key} ({count[key]}. Vorkommen)"
        out[key] = dict(zip(head, r))
    return out


def cmd_compare(a):
    folder = resolve(a.repo, a.folder)
    data = read_manifest(folder)
    files, lang = tab_files(a.tab)
    rel = Path(a.folder).as_posix()
    rel_info = data["releases"][0] if data["releases"] else None
    print(f"SNAPSHOT {rel} | gelesen {data['read_at']} | "
          + (f"freigegeben {rel_info.get('date')} durch {rel_info.get('released_by')}" if rel_info
             else "nicht freigegeben"))
    lines = []
    if lang != data["language"]:
        lines.append(f"KOPF Sprache | Snapshot {data['language']}, Sheet {lang}")
    for tab, fname, title_key in TABS:
        name = name_of(tab, lang)
        title = SHEET.column(tab, title_key, lang)
        if not (folder / fname).is_file():
            raise Refused(f"snapshot {rel}: {fname} fehlt")
        old = load_rows(folder / fname)
        new = load_rows(files[tab])
        old_head = [h.strip() for h in old[0]]
        new_head = [h.strip() for h in new[0]]
        while new_head and not new_head[-1]:
            new_head.pop()
        old[0], new[0] = old_head, new_head
        for h in old_head:
            if h not in new_head:
                lines.append(f"KOPF {name} | Spalte „{h}“ entfernt")
        for h in new_head:
            if h not in old_head:
                lines.append(f"KOPF {name} | Spalte „{h}“ neu")
        common = [h for h in new_head if h in old_head]
        before, after = keyed(old), keyed(new)
        for key, row in after.items():
            if key not in before:
                lines.append(f"NEU {name} {key} | {one_line(row.get(title, ''))}")
        for key, row in before.items():
            if key not in after:
                lines.append(f"ENTFERNT {name} {key} | {one_line(row.get(title, ''))}")
        for key, row in after.items():
            if key not in before:
                continue
            for h in common:
                was, now = before[key][h], row[h]
                if was == now:
                    continue
                if was and now.startswith(was):
                    change = f"+ „{one_line(now[len(was):])}“"
                else:
                    change = f"„{one_line(was)}“ → „{one_line(now)}“"
                lines.append(f"GEÄNDERT {name} {key} | {h}: {change}")
    for line in lines:
        print(line)
    if not lines:
        print("GLEICH | kein Unterschied zum Snapshot")
        return 0
    print(f"ABWEICHUNGEN {len(lines)} | mögliche Change Requests; entschieden wird nicht hier")
    return 3


def parser():
    p = argparse.ArgumentParser(prog="scope-snapshot.py", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write")
    w.add_argument("repo")
    w.add_argument("--occasion", required=True, choices=OCCASIONS)
    w.add_argument("--sheet", required=True)
    w.add_argument("--read-at", required=True)
    w.add_argument("--tab", action="append")
    w.add_argument("--pages")
    w.add_argument("--proposal-id")
    w.add_argument("--proposal-created")
    w.add_argument("--estimate-id")
    w.add_argument("--estimate-created")
    w.add_argument("--released-by")
    w.add_argument("--release-date")
    r = sub.add_parser("release")
    r.add_argument("repo")
    r.add_argument("folder")
    r.add_argument("--released-by", required=True)
    r.add_argument("--release-date", required=True)
    lt = sub.add_parser("latest")
    lt.add_argument("repo")
    lt.add_argument("--released", action="store_true")
    c = sub.add_parser("compare")
    c.add_argument("repo")
    c.add_argument("folder")
    c.add_argument("--tab", action="append")
    return p


def main(argv):
    a = parser().parse_args(argv[1:])
    try:
        return {"write": cmd_write, "release": cmd_release, "latest": cmd_latest,
                "compare": cmd_compare}[a.cmd](a)
    except Refused as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
