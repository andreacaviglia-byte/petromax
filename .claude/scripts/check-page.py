#!/usr/bin/env python3
"""Prüft einen Entwurf oder eine Req Page gegen die Vorlage in docs/draft-and-epic-page-contract.md (§218, §255).

    check-page.py [--language de|en] [--title TITEL] <dokument.md|dokument.html> ...

Die Vorlage ist je Sprache der Markdown-Block unter "## Die Vorlage" im Vertrag und die
einzige Quelle: Titel, Überschriften und ihre Reihenfolge, die Beschriftungen des
Kopfs und die Tabellenköpfe je Abschnitt werden aus ihm gelesen (über page_labels.py),
nicht aus einer Liste in diesem Script. Eine umbenannte Überschrift bricht die Läufe,
die das Dokument lesen, und ohne diese Prüfung meldet das nichts.

Die Sprache: `--language` nennt die Projektsprache, und geprüft wird gegen ihre Vorlage.
Trägt das Dokument durchgehend die Bezeichnungen der anderen Sprache, meldet das
`language_mismatch`, und die Struktur wird ebenfalls gegen die Vorlage von `--language`
geprüft. Ohne `--language` gilt die Sprache, deren Bezeichnungen das Dokument trägt.
Trägt es Bezeichnungen beider Sprachen, meldet das `language_mixed`, und geprüft wird
gegen `--language` oder die Sprache mit den meisten Bezeichnungen. Bezeichnungen, die in
beiden Sprachen gleich sind (`Epic`, `ID`, seit §261 der Titel), zählen für keine.

Gelesen wird Markdown, HTML aus Confluence (getConfluenceContent, content_format html)
oder der HTML-Export eines Google-Docs; HTML erkennt das Script an <h2> oder
<table>. `--title` prüft den Titel, den Confluence nicht im Rumpf führt und den
ein Google-Doc als Dateinamen trägt.

Der Kopf ist die Tabelle vor der ersten Überschrift; geprüft werden seine
Beschriftungen in der ersten Spalte. Eine Tabelle, über der in der Vorlage eine
Zeile `‹optional›` steht, darf fehlen.

Das Datum (§337): ein Datum steht in der Form der Sprache, gegen die geprüft wird, bei `de`
`11.10.2026`, bei `en` `11 Oct 2026` (Datalayer-Vertrag, Die festen Wendungen); ein Datum in der
Form der anderen Sprache meldet `date_form`. Eine Adresse zählt nicht.

Prüfungen: language_mismatch, language_mixed, title, heading_missing, heading_unknown,
heading_duplicate, heading_order, head_labels, table_missing, table_header, date_form. Ausgabe je
Verstoß eine Zeile "<prüfung>: <detail>", Exit 1, sobald einer vorliegt, Exit 2 bei
falschem Aufruf.

Liegt unter .claude/scripts/, damit ein Skill es über ${CLAUDE_SKILL_DIR}/../../scripts/
aufrufen kann (§212). Gemessen wird es von dev/tests/check-page.py, in beiden Richtungen.
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_labels  # noqa: E402

TEMPLATE = page_labels.REF
LANGUAGES = page_labels.LANGUAGES
OPTIONAL = "‹optional›"
PLACEHOLDER = re.compile(r"‹[^›]*›")


def norm(text):
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def cell(text):
    return norm(text).strip("*_` ")


class Document:
    """Titel, Abschnitte (h2) in Folge, und je Abschnitt seine Tabellen."""

    def __init__(self):
        self.title = None
        self.sections = []            # h2-Überschriften in Folge
        self.tables = []              # (Abschnitt oder None, [Zeilen als Zelllisten], optional)

    def current(self):
        return self.sections[-1] if self.sections else None

    def heading(self, level, text):
        if level == 1 and self.title is None:
            self.title = text
        elif level == 2:
            self.sections.append(text)


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [cell(c) for c in s.split("|")]


def read_markdown(text):
    doc = Document()
    lines = text.split("\n")
    in_code = False
    optional = False                  # die letzte Zeile mit Text war `‹optional›`
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            doc.heading(len(m.group(1)), norm(m.group(2)))
            i += 1
            continue
        if (line.lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1])):
            rows = [split_row(line)]
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            doc.tables.append((doc.current(), rows, optional))
            optional = False
            continue
        if line.strip():
            optional = line.strip() == OPTIONAL
        i += 1
    return doc


class HtmlReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.doc = Document()
        self.head = None              # (Ebene, [Text])
        self.stack = []               # offene Tabellen
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r"h[1-6]", tag):
            self.head = (int(tag[1]), [])
        elif tag == "table":
            self.stack.append([])
        elif tag == "tr" and self.stack:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "br" and self.cell is not None:
            self.cell.append(" ")

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]", tag) and self.head:
            level, parts = self.head
            self.doc.heading(level, norm("".join(parts)))
            self.head = None
        elif tag in ("td", "th") and self.cell is not None:
            self.row.append(cell("".join(self.cell)))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.stack[-1].append(self.row)
            self.row = None
        elif tag == "table" and self.stack:
            rows = self.stack.pop()
            if rows:
                self.doc.tables.append((self.doc.current(), rows, False))

    def handle_data(self, data):
        if self.head:
            self.head[1].append(data)
        if self.cell is not None:
            self.cell.append(data)


def read(text):
    if re.search(r"<h2[\s>]|<table[\s>]", text, re.I):
        reader = HtmlReader()
        reader.feed(text)
        reader.close()
        return reader.doc
    return read_markdown(text)


def templates(path=TEMPLATE):
    """{"en": block, "de": block}, aus dem Vertrag von Entwurf und Epic Page."""
    return page_labels.templates(path)


def strip_mark(name):
    return name.replace(OPTIONAL, "").strip() if name else name


def title_pattern(tpl):
    return "^" + ".+".join(re.escape(t) for t in PLACEHOLDER.split(tpl.title)) + "$"


def label_set(doc):
    """Die Bezeichnungen eines Dokuments: Überschriften, Beschriftungen des Kopfs, Tabellenköpfe."""
    found = [strip_mark(s) for s in doc.sections]
    head = next((rows for s, rows, _ in doc.tables if s is None), None)
    found += [r[0] for r in head or [] if r]
    found += [c for s, rows, _ in doc.tables if s is not None and rows for c in rows[0]]
    return set(found)


def detect(doc, blocks, title=None):
    """Die Sprache der Bezeichnungen: {"en": [...], "de": [...]} je Sprache die Treffer, die nur sie hat."""
    tpls = {lang: read_markdown(b) for lang, b in blocks.items()}
    sets = {lang: label_set(t) for lang, t in tpls.items()}
    own = {lang: sets[lang] - set().union(*(sets[o] for o in sets if o != lang)) for lang in sets}
    have = label_set(doc)
    hits = {lang: sorted(have & own[lang]) for lang in sets}
    # Der Titel zählt nur für eine Sprache, deren Muster er allein trifft; seit §261 ist er in beiden gleich.
    patterns = {lang: title_pattern(tpl) for lang, tpl in tpls.items()}
    candidates = [c for c in (title, doc.title) if c is not None]
    for lang in tpls:
        others = [patterns[o] for o in patterns if o != lang]
        if any(re.match(patterns[lang], c) and not any(re.match(p, c) for p in others) for c in candidates):
            hits[lang].insert(0, "Titel")
    return hits


def check_language(doc, blocks, language=None, title=None):
    """Prüft die Sprache der Bezeichnungen und die Struktur gegen die Vorlage der geltenden Sprache."""
    hits = detect(doc, blocks, title)
    found = [lang for lang in LANGUAGES if hits[lang]]
    errors = []
    if len(found) > 1:
        errors.append("language_mixed: Bezeichnungen aus " + " und ".join(
            f"{lang} ({', '.join(hits[lang][:3])})" for lang in found))
        use = language or max(found, key=lambda lang: len(hits[lang]))
    elif found and language and found[0] != language:
        errors.append(f"language_mismatch: das Dokument trägt die Bezeichnungen von {found[0]}, "
                      f"verlangt ist {language}")
        use = language
    else:
        use = language or (found[0] if found else LANGUAGES[0])
    return errors + check(doc, blocks[use], title), use


def check(doc, block, title=None):
    tpl = read_markdown(block)
    errors = []
    order = [(strip_mark(s), OPTIONAL in s) for s in tpl.sections]
    names = [n for n, _ in order]

    # Titel: im Rumpf (Markdown-Entwurf) oder über --title (Confluence).
    pattern = title_pattern(tpl)
    for candidate in (t for t in (title, doc.title) if t is not None):
        if not re.match(pattern, candidate):
            errors.append(f"title: '{candidate}' folgt nicht '{tpl.title}'")

    seen = set()
    for s in doc.sections:
        if s not in names:
            errors.append(f"heading_unknown: '{s}' steht nicht in der Vorlage")
        elif s in seen:
            errors.append(f"heading_duplicate: '{s}' steht mehr als einmal")
        seen.add(s)
    for n, optional in order:
        if not optional and n not in doc.sections:
            errors.append(f"heading_missing: '{n}' fehlt")
    known = [s for s in dict.fromkeys(doc.sections) if s in names]
    expected = [n for n in names if n in known]
    if known != expected:
        errors.append(f"heading_order: {' > '.join(known)}; die Vorlage verlangt "
                      f"{' > '.join(expected)}")

    want, have = {}, {}
    tpl_head, doc_head = None, None
    for s, rows, optional in tpl.tables:
        if s is None:
            tpl_head = tpl_head or rows
        else:
            want.setdefault(strip_mark(s), []).append((rows, optional))
    for s, rows, _ in doc.tables:
        if s is None and doc_head is None:
            doc_head = rows
        else:
            have.setdefault(s, []).append(rows)

    for s, tables in want.items():
        heads = [t[0] for t in have.get(s, [])]
        for t, optional in tables:
            if s in doc.sections and not optional and t[0] not in heads:
                errors.append(f"table_missing: unter '{s}' fehlt die Tabelle "
                              f"'{' | '.join(t[0])}'")
    for s, tables in have.items():
        allowed = [t[0] for t, _ in want.get(s, [])]
        for t in tables:
            if t[0] not in allowed:
                where = f"unter '{s}'" if s else "vor der ersten Überschrift"
                known_heads = ", ".join(f"'{' | '.join(k)}'" for k in allowed)
                errors.append(f"table_header: {where} steht '{' | '.join(t[0])}', die "
                              f"Vorlage kennt dort {known_heads or 'nur den Kopf'}")

    # Die Beschriftungen des Kopfs: erste Spalte der Tabelle vor der ersten Überschrift.
    if tpl_head:
        labels = [r[0] for r in tpl_head]
        got = [r[0] for r in doc_head if r] if doc_head else []
        if got != labels:
            errors.append(f"head_labels: {', '.join(got) or 'kein Kopf vor der ersten Überschrift'}; "
                          f"die Vorlage verlangt {', '.join(labels)}")
    return errors


MONTHS_EN = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
# Je Sprache die Form eines Datums der jeweils anderen (§337); ISO-Daten (JJJJ-MM-TT) stehen in keinem Dokument
# des Kunden und bleiben hier ungeprüft.
FOREIGN_DATE = {"en": re.compile(r"(?<![\d./-])\d{1,2}\.\d{1,2}\.\d{4}(?![\d.]*\d)"),
                "de": re.compile(rf"(?<!\d)\d{{1,2}} (?:{MONTHS_EN}) \d{{4}}\b")}
URL = re.compile(r"https?://\S+")


def check_dates(text, language):
    """Ein Datum in der Form der anderen Sprache (§337), ohne Adressen."""
    hits = FOREIGN_DATE[language].findall(URL.sub(" ", html.unescape(text)))
    if not hits:
        return []
    want = "11.10.2026" if language == "de" else "11 Oct 2026"
    return [f"date_form: '{hits[0]}' steht in der Form der anderen Sprache; bei {language} heißt ein "
            f"Datum wie '{want}'" + (f" ({len(hits)} Stellen)" if len(hits) > 1 else "")]


def main(argv):
    title, language = None, None
    while len(argv) >= 2 and argv[0] in ("--title", "--language"):
        if argv[0] == "--title":
            title = argv[1]
        else:
            language = argv[1]
        argv = argv[2:]
    if not argv or (language is not None and language not in LANGUAGES):
        print(__doc__.strip())
        return 2
    blocks = templates()
    rc = 0
    for path in argv:
        text = Path(path).read_text(encoding="utf-8")
        errors, use = check_language(read(text), blocks, language, title)
        errors += check_dates(text, use)
        for e in errors:
            print(f"{path}: {e}")
        if errors:
            rc = 1
    if rc == 0:
        print(f"{len(argv)} Dokument(e) folgen der Vorlage {use}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
