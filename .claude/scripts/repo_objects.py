"""Liest die Objekte des Projekt-Repos, eine Datei je Objekt (§280), für check-repo.py und die
Projektionen. Die Form steht in .claude/docs/datalayer-contract.md, Abschnitt „Die Objekte“.

Gelesen wird ohne Fremdbibliothek, mit dem Leser aus check-project.py: ein Kopf in YAML zwischen
zwei Zeilen `---` in der Form von project.yml, darunter der Rumpf in Markdown.
"""
import importlib.util
import re
from pathlib import Path

# Ordner, Muster des Dateinamens und Präfix der Kennung je Art.
KINDS = {
    "requirements": ("requirements", re.compile(r"^(REQ-\d{3})\.md$")),
    "epics": ("epics", re.compile(r"^(EP-\d{3})\.md$")),
    "gaps": ("gaps", re.compile(r"^(GAP-\d{3})\.md$")),
    "tests": ("tests", re.compile(r"^(E2E-\d{3})\.md$")),
    "todo": ("todo", re.compile(r"^(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)\.md$")),
    "decisions": ("decisions", re.compile(r"^(ADR-\d{3})-[a-z0-9-]+\.md$")),
    "way_of_working": ("way-of-working", re.compile(r"^(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)\.md$")),
}
ID = re.compile(r"^(REQ|EP|GAP|E2E|ADR)-\d{3}$")


class ObjectError(Exception):
    """Eine Datei, die nicht der Form des Vertrags folgt; der Text nennt Datei und Stelle."""


def _project_reader():
    """Der Leser aus check-project.py: dieselbe Form wie project.yml, es gibt ihn nur einmal."""
    spec = importlib.util.spec_from_file_location("check_project", Path(__file__).with_name("check-project.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_PROJECT = _project_reader()


def read_yaml(text):
    """Ein dict aus der Form des Vertrags; ObjectError, wenn sie nicht passt."""
    try:
        return _PROJECT.lies(text)
    except _PROJECT.Fehler as e:
        raise ObjectError(str(e))


def read_object(path):
    """(Kopf, Rumpf) einer Datei; ObjectError, wenn der Kopf fehlt oder nicht lesbar ist."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        raise ObjectError(f"{Path(path).name}: kein Kopf zwischen zwei Zeilen ---")
    end = 1 + [l.strip() for l in lines[1:]].index("---")
    try:
        head = read_yaml("\n".join(lines[1:end]))
    except ObjectError as e:
        raise ObjectError(f"{Path(path).name}: {e}")
    return head, "\n".join(lines[end + 1:])


def sections(body):
    """Der Rumpf je Überschrift 2; der Text vor der ersten steht unter ""."""
    out, name = {"": []}, ""
    for line in body.split("\n"):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            name = m.group(1)
            out[name] = []
        else:
            out[name].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def first_paragraph(text):
    return re.split(r"\n\s*\n", text.strip(), maxsplit=1)[0].strip() if text.strip() else ""


def first_sentence(text):
    """Der erste Satz des ersten Absatzes. Ein Punkt hinter einer Zahl vor einem Wort ist eine
    Ordnungszahl und kein Satzende: in der zweiten Proberunde (10.10.2026) wurde „ab dem 51. Abo“ zu
    „ab dem 51.“, ebenso „Am 3. Oktober“."""
    para = " ".join(first_paragraph(text).split())
    for m in re.finditer(r"[.?!](?=\s|$)", para):
        after = para[m.end() + 1:m.end() + 2]
        if m.group(0) == "." and m.start() and para[m.start() - 1].isdigit() and after.isalpha():
            continue
        if m.group(0) == "." and ABBREVIATION.search(para[:m.end()]):
            continue
        return para[:m.end()]
    return para


# Abkürzungen, deren Punkt kein Satzende ist: „z. B.“, „ca.“, „inkl.“, „e.g.“ (Prüfung vor 1.0.0, 11.10.2026:
# „Gilt das z. B. auch …?“ wurde zu „Gilt das z.“).
ABBREVIATION = re.compile(r"(?:^|[\s(])(?:z\.\s?B|d\.\s?h|u\.\s?a|bzw|ca|inkl|exkl|ggf|evtl|vgl|bspw|usw|etc|"
                          r"Nr|Abs|e\.g|i\.e|incl|approx|vs|[zdue])\.$")


# Die Anzeige des Shop-Bezugs hinten am Titel (§307), je Sprache.
ALL_SHOPS = {"de": "alle Shops", "en": "all shops"}
SOME_SHOPS = {"de": "{n} Shops", "en": "{n} shops"}


def shop_keys(value):
    """Die Schlüssel aus dem Feld `shops` einer Anforderung oder ADR; leer heißt: alle Shops (§307)."""
    if value in ("", None):
        return []
    return [str(value)] if isinstance(value, str) else [str(v) for v in value if str(v)]


def project_shop_keys(project):
    """Die `key` aus `shops` in project.yml, in ihrer Folge."""
    shops = project.get("shops") or []
    return [str(s.get("key")) for s in shops if isinstance(s, dict) and s.get("key")] if isinstance(shops, list) else []


def shops_label(value, project_keys, language="de", sheet=False):
    """Der Shop-Bezug hinten am Titel nach §307, mit Leerzeichen davor, oder "": ein Shop `(B2B)`, zwei
    `(B2B & B2C)`, drei oder mehr `(3 Shops)`, alle `(alle Shops)`. Keine Klammer in einem Projekt mit
    einem Shop und, mit sheet, für alle Shops: dort sagt es die Spalte `Shops`."""
    lang = "en" if language == "en" else "de"
    if len(project_keys) <= 1:
        return ""
    keys = shop_keys(value)
    if not keys or set(project_keys) <= set(keys):
        return "" if sheet else f" ({ALL_SHOPS[lang]})"
    keys = [k for k in project_keys if k in keys] + [k for k in keys if k not in project_keys]
    if len(keys) > 2:
        return f" ({SOME_SHOPS[lang].format(n=len(keys))})"
    return f" ({' & '.join(k.upper() for k in keys)})"


def shops_title(title, value, project_keys, language="de", sheet=False):
    """Der Titel mit dem Shop-Bezug hinten (§307)."""
    return f"{title}{shops_label(value, project_keys, language, sheet)}"


def shops_cell(value, project_keys):
    """Die Spalte `Shops` der Anforderungsliste: alle Schlüssel, für die sie gilt, groß, mit Komma (§307)."""
    keys = shop_keys(value) or list(project_keys)
    keys = [k for k in project_keys if k in keys] + [k for k in keys if k not in project_keys]
    return ", ".join(k.upper() for k in keys)


CONTRACT = Path(__file__).resolve().parent.parent / "docs" / "datalayer-contract.md"
LANGUAGES = ("de", "en")
MONTHS_EN = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def phrases(path=CONTRACT):
    """{"de": {schlüssel: wendung}, "en": {...}} aus der Tabelle unter "## Die festen Wendungen" des
    Datalayer-Vertrags (§337); dort steht jede Wendung, die ein Lauf in ein Feld des Repos schreibt und
    die von dort in ein Dokument des Kunden wandert."""
    out, inside, fence, rows = {lang: {} for lang in LANGUAGES}, False, False, []
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            if inside:
                break
            inside = line.strip() == "## Die festen Wendungen"
            continue
        if inside and line.startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    if len(rows) < 3 or rows[0] != ["Schlüssel", *LANGUAGES]:
        raise SystemExit(f"{Path(path).name}: unter '## Die festen Wendungen' steht keine Tabelle "
                         f"Schlüssel, {', '.join(LANGUAGES)}")
    for cells in rows[2:]:
        key, *values = [c[1:-1] if len(c) >= 2 and c[0] == c[-1] == "`" else c for c in cells]
        if key in out["de"] or len(values) != len(LANGUAGES):
            raise SystemExit(f"{Path(path).name}: die Wendung '{key}' steht zweimal oder ohne beide Sprachen")
        for lang, value in zip(LANGUAGES, values):
            out[lang][key] = value
    return out


def date_text(value, language="de"):
    """Ein Datum in der Form der Sprache (§337): `de` 11.10.2026, `en` 11 Oct 2026. `value` ist ein
    date, ein datetime oder ein Text, der mit JJJJ-MM-TT beginnt."""
    text = value.isoformat() if hasattr(value, "isoformat") else str(value)
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)
    if not m:
        raise ValueError(f"'{value}' ist kein Datum der Form JJJJ-MM-TT")
    y, mo, d = m.groups()
    if not 1 <= int(mo) <= 12:
        raise ValueError(f"'{value}' hat keinen Monat 01 bis 12")
    if language == "en":
        return f"{int(d)} {MONTHS_EN[int(mo) - 1]} {y}"
    return f"{d}.{mo}.{y}"


# Ein Datum in einer der beiden Formen, etwa in einem Text, der keines tragen darf.
DATE_ANY = re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b|\b\d{4}-\d{2}-\d{2}\b"
                      r"|\b\d{1,2} (?:" + "|".join(MONTHS_EN) + r") \d{4}\b")


def load(repo):
    """Je Art eine Liste von dict(name, key, head, body) oder dict(name, error) in der Folge der Namen;
    ein Ordner, den es nicht gibt, ist leer."""
    repo = Path(repo)
    out = {}
    for kind, (folder, pattern) in KINDS.items():
        items = []
        base = repo / folder
        if base.is_dir():
            for f in sorted(base.iterdir()):
                if not f.is_file() or not f.name.endswith(".md"):
                    continue
                if kind == "epics" and f.name == "critical-path.md":
                    continue
                m = pattern.match(f.name)
                if not m:
                    items.append({"name": f"{folder}/{f.name}", "error": "Dateiname folgt nicht dem Vertrag"})
                    continue
                try:
                    head, body = read_object(f)
                except ObjectError as e:
                    items.append({"name": f"{folder}/{f.name}", "error": str(e)})
                    continue
                items.append({"name": f"{folder}/{f.name}", "key": m.group(1), "head": head, "body": body})
        out[kind] = items
    return out


def main(argv):
    """`repo_objects.py <repo> <Kennung>...`: je Anforderung oder ADR die Zeile `<Kennung> <Titel>` mit
    dem Shop-Bezug hinten (§307), in der Sprache aus project.yml, für einen Lauf, der den Titel in
    Ticket, Entwurf oder Epic Page von Hand schreibt. Exit 1 bei einer Kennung, die es nicht gibt, oder
    einer Datei, die nicht lesbar ist; 2 bei falschem Aufruf."""
    import sys
    if len(argv) < 2 or not Path(argv[0]).is_dir():
        print("Aufruf: repo_objects.py <repo> <REQ-NNN|ADR-NNN>...", file=sys.stderr)
        return 2
    repo = Path(argv[0])
    try:
        project = read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
    except (OSError, ObjectError) as e:
        print(f"project.yml: {e}")
        return 1
    keys, lang = project_shop_keys(project), project.get("language", "de")
    objects = load(repo)
    found = {o["key"]: o for kind in ("requirements", "decisions") for o in objects[kind] if "key" in o}
    broken = {o["name"]: o["error"] for kind in ("requirements", "decisions") for o in objects[kind] if "error" in o}
    rc = 0
    for wanted in argv[1:]:
        o = found.get(wanted)
        if o is None:
            print(f"{wanted}: nicht in requirements/ oder decisions/"
                  + (f"; nicht lesbar: {', '.join(sorted(broken))}" if broken else ""))
            rc = 1
            continue
        print(f"{wanted} {shops_title(str(o['head'].get('title', '')), o['head'].get('shops'), keys, lang)}")
    return rc


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
