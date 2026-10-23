"""Die Bezeichnungen von Entwurf und Req Page in beiden Sprachen, gelesen aus draft-and-epic-page-contract.md (§255).

Die Quelle ist allein docs/draft-and-epic-page-contract.md: die Tabelle unter "## Die Bezeichnungen"
(Spalten Schlüssel, en, de) und je Sprache der Markdown-Block unter "### Vorlage `en`" und
"### Vorlage `de`" im Abschnitt "## Die Vorlage". check-page.py prüft gegen die Vorlage der Sprache,
check-solution-doc.py nimmt aus der Tabelle die Bezeichnungen, die es im Dokument zitiert. Keine
der beiden kennt eine Bezeichnung aus einer eigenen Liste.

`drift()` misst, dass die deutsche Vorlage die englische mit den Bezeichnungen der Tabelle ist,
Zeichen für Zeichen; dev/tests/check-page.py ruft es.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "docs" / "draft-and-epic-page-contract.md"
LANGUAGES = ("en", "de")


def _section(text, heading):
    """Der Rumpf unter "## heading" bis zur nächsten "## "-Überschrift außerhalb eines Code-Blocks."""
    out, inside, fence = [], False, False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            if inside:
                break
            inside = line.strip() == f"## {heading}"
            continue
        if inside:
            out.append(line)
    if not inside:
        raise SystemExit(f"{REF.name}: kein Abschnitt '## {heading}'")
    return "\n".join(out)


def _cell(text):
    t = text.strip()
    return t[1:-1] if len(t) >= 2 and t.startswith("`") and t.endswith("`") else t


def labels(path=REF):
    """{"en": {schlüssel: bezeichnung}, "de": {...}} aus der Tabelle unter "## Die Bezeichnungen"."""
    body = _section(Path(path).read_text(encoding="utf-8"), "Die Bezeichnungen")
    rows = [line for line in body.split("\n") if line.startswith("|")]
    if len(rows) < 3:
        raise SystemExit(f"{Path(path).name}: unter '## Die Bezeichnungen' steht keine Tabelle")
    head = [_cell(c) for c in rows[0].strip().strip("|").split("|")]
    if head != ["Schlüssel", *LANGUAGES]:
        raise SystemExit(f"{Path(path).name}: die Tabelle der Bezeichnungen hat die Spalten {head}, "
                         f"verlangt sind Schlüssel, {', '.join(LANGUAGES)}")
    out = {lang: {} for lang in LANGUAGES}
    for line in rows[2:]:
        cells = [_cell(c) for c in line.strip().strip("|").split("|")]
        key = cells[0]
        if key in out["en"]:
            raise SystemExit(f"{Path(path).name}: Schlüssel '{key}' steht zweimal in der Tabelle")
        for lang, value in zip(LANGUAGES, cells[1:]):
            out[lang][key] = value
    return out


def templates(path=REF):
    """{"en": block, "de": block}: je Sprache der Markdown-Block der Vorlage."""
    body = _section(Path(path).read_text(encoding="utf-8"), "Die Vorlage")
    out = {}
    for lang in LANGUAGES:
        m = re.search(rf"^### Vorlage `{lang}`\s*\n.*?```markdown\n(.*?)^```", body, re.S | re.M)
        if not m:
            raise SystemExit(f"{Path(path).name}: unter '## Die Vorlage' fehlt der Block '### Vorlage `{lang}`'")
        out[lang] = m.group(1)
    return out


def translate(text, table, src, dst):
    """Ersetzt jede Bezeichnung der Sprache src durch die von dst, in einem Durchgang, die längste zuerst."""
    pairs = {table[src][k]: table[dst][k] for k in table[src] if table[src][k] != table[dst][k]}
    if not pairs:
        return text
    pattern = re.compile("|".join(re.escape(s) for s in sorted(pairs, key=len, reverse=True)))
    return pattern.sub(lambda m: pairs[m.group(0)], text)


def drift(path=REF):
    """Befunde, wenn Tabelle und Vorlagen auseinanderlaufen; leer, wenn sie zusammenpassen."""
    table, blocks = labels(path), templates(path)
    problems = []
    for key in table["en"]:
        for lang in LANGUAGES:
            if not table[lang][key]:
                problems.append(f"label_empty: '{key}' hat in {lang} keine Bezeichnung")
    for lang in LANGUAGES:
        seen = {}
        for key, value in table[lang].items():
            if value in seen and table["en"][key] != table["de"][key]:
                problems.append(f"label_duplicate: '{value}' steht in {lang} für '{seen[value]}' und '{key}'")
            seen.setdefault(value, key)
    want = translate(blocks["en"], table, "en", "de")
    if want != blocks["de"]:
        w, g = want.split("\n"), blocks["de"].split("\n")
        n = next((i for i in range(max(len(w), len(g)))
                  if (w[i] if i < len(w) else None) != (g[i] if i < len(g) else None)), 0)
        problems.append(f"template_drift: Zeile {n + 1} der Vorlage `de` ist "
                        f"'{g[n] if n < len(g) else '(Ende)'}', aus der Vorlage `en` und der Tabelle folgt "
                        f"'{w[n] if n < len(w) else '(Ende)'}'")
    return problems
