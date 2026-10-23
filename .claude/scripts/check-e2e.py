#!/usr/bin/env python3
"""Gleicht die geplanten Prozess-Tests gegen den Tab `Testfälle` des E2E-Sheets ab (§159, §220 W15, §256).

Aufruf:
  check-e2e.py <testcases.csv> [--language de|en]
  check-e2e.py <testcases.csv> --plan <plan.json> --shops <key>[,<key>…] [--out <update.json>]
               [--tests <tests/>] [--language de|en]

<testcases.csv> ist der Tab `Testfälle` (`en`: `Test cases`) als CSV-Export, direkt vor dem Aufruf
gelesen. Das E2E-Sheet steht in der Sprache aus `language` in project.yml (§337): Tabs, Kopfzeile,
Werte der Dropdowns, der Wert für alle Shops und die Übersicht kommen aus der Tabelle unten (TABS,
COLUMNS, STATUS_VALUES, SEVERITY_VALUES, ALL_SHOPS, TEXTS), je Sprache eine Spalte; sheet-format.py
liest dieselbe. --language nennt die Sprache des Projekts; ohne gilt die Sprache, deren Kopfzeile
Zeile 1 trägt. <plan.json> ist
eine Liste der geplanten Tests, je `{"testcase": …, "shop": …, "role": …, "steps": …, "expected": …}`.
--shops nennt die `key` aus `shops` in `project.yml`, in ihrer Folge. Erlaubt in `shop` ist mit einem
Shop dessen Key, mit mehreren jeder Key und `alle` (`en`: `all`); dieselbe Liste trägt das Dropdown
der Spalte.

Ohne Plan: je Zeile `<n> | <ID> | <Testfall> | <Status>` (leer zählt als `Offen`, `en` `Open`). Steht in
`Getestet am` ein Text, der nicht die Form der Sprache hat (`11.10.2026`, `en` `11 Oct 2026`, §337), folgt
`DATUM <n> | <Wert> | erwartet wie …`: ein Hinweis, kein Befund; das Feld gehört den Testenden. Mit Plan dazu je
geplantem Test eine Zeile `NEU <ID>`, `GLEICH <n>` oder `ERSETZT <n>`, je Bestandszeile ohne Plan
`NICHT-MEHR <n>`, und je ersetzter Zeile, die schon einen Status außer `Offen` (`Open`) oder ein Ist-Ergebnis
trägt, `ERGEBNIS <n>`: für genau diese fragt der Skill den Lead. Ein neuer Test bekommt die nächste
Nummer über der höchsten `ID` im Bestand; ein ersetzter behält seine.
`--out` schreibt den einen Aufruf für `Google_Sheets.update_values` als `{"range": …, "values": …}`,
jeder Wert mit führendem Hochkomma, damit das Sheet ihn als Text hält; `range` ist `null`, wenn nichts
zu schreiben ist. Er trägt nur die Spalten A bis F; G bis L gehören den Testenden.

`--tests` schreibt je geplantem Test seine Datei `<ordner>/E2E-NNN.md` in den Datalayer (§280), Form
im Datalayer-Vertrag: im Kopf `id`, `testcase`, die Anforderungen, die der Test verkettet, und die
Quellen, aus denen er abgeleitet ist; im Rumpf, was der Lauf ins Sheet projiziert, unter `## Shop`,
`## Role`, `## Steps` und `## Expected result`. Dafür trägt jeder geplante Test zusätzlich `requirements` (Liste von
`REQ-…`) und `sources` (je Quelle `epic`, `kind` `page` oder `draft`, `version`, `link`); ins Sheet
geht davon nichts. Geschrieben wird nur aus dem Rücklauf: jeder geplante Test meldet `GLEICH`, damit
die ID die des Sheets ist. Die Datei eines Tests, den der Plan nicht trägt, bleibt unberührt. Status,
Runde und Ergebnisse sind Felder der Menschen und stehen nur im E2E-Sheet (§280, Regel 5).

Prüfungen, je eine Zeile `<prüfung> <detail>` und Exit 1:
  header        Zeile 1 ist nicht wörtlich die Kopfzeile einer Sprache unten (COLUMNS), oder nicht die
                der Sprache aus --language
  duplicate_key ein Text in `Testfall` steht zweimal, im Bestand oder im Plan
  duplicate_id  eine `ID` steht im Bestand zweimal
  forbidden_id  ein Textfeld eines geplanten Tests trägt eine Kennung (REQ-, EP-, ADR-) oder eine Adresse
  empty_field   ein geplanter Test hat ein leeres Feld (testcase, shop, role, steps, expected)
  shop_unknown  `shop` eines geplanten Tests ist keiner der erlaubten Werte aus --shops
  test_file_field mit --tests: einem geplanten Test fehlen `requirements` oder `sources`, oder ein
                Eintrag hat nicht die Form oben
  test_file_not_back mit --tests: ein geplanter Test meldet nicht `GLEICH` oder trägt im Sheet keine
                ID der Form E2E-…, oder eine Datei liest sich nicht so zurück, wie sie geschrieben
                wurde; die Dateien entstehen erst aus dem Rücklauf, sonst bleibt der Ordner unverändert
Exit 2 bei falschem Aufruf.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

LANGUAGES = ("de", "en")
# Die Tabelle des E2E-Sheets (§256, §337): je Eintrag sein Schlüssel und seine Form in de und en,
# wörtlich wie in e2e-testing-sheet/ref-sheet.md, Abschnitt „Die Sprache des Sheets“;
# dev/tests/check-e2e.py hält beide gleich. Die deutschen Formen bleiben in 1.x, wie sie sind.
TABS = {"testcases": ("Testfälle", "Test cases"), "overview": ("Übersicht", "Overview")}
COLUMNS = [
    ("id", "ID", "ID"),
    ("testcase", "Testfall", "Test case"),
    ("shop", "Shop", "Shop"),
    ("role", "Rolle", "Role"),
    ("steps", "Ablauf", "Steps"),
    ("expected", "Erwartetes Ergebnis", "Expected result"),
    ("status", "Status", "Status"),
    ("round", "Runde", "Round"),
    ("result", "Ist-Ergebnis / Beobachtung", "Actual result / observation"),
    ("severity", "Schweregrad", "Severity"),
    ("tested_by", "Getestet von", "Tested by"),
    ("tested_on", "Getestet am", "Tested on"),
]
# Die Werte der Dropdowns (§256); sheet-format.py liest sie von hier.
STATUS_VALUES = [
    ("open", "Offen", "Open"),
    ("passed", "Bestanden", "Passed"),
    ("failed", "Fehlgeschlagen", "Failed"),
    ("blocked", "Blockiert", "Blocked"),
    ("retest", "Erneut testen", "Retest"),
    ("not_applicable", "Nicht anwendbar", "Not applicable"),
]
SEVERITY_VALUES = [
    ("blocker", "Blocker", "Blocker"),
    ("high", "Hoch", "High"),
    ("medium", "Mittel", "Medium"),
    ("low", "Niedrig", "Low"),
]
ROUNDS = ["1", "2", "3", "4", "5"]
ALL_SHOPS = ("alle", "all")
# Die übrigen Texte des Sheets: Übersicht, Schutz, die Form des Datums in `Getestet am` (ein Beispiel; das
# Datum steht dort als Text, nicht als Datumswert, damit es nicht vom Gebietsschema des Sheets abhängt),
# Präfix im Ablauf.
TEXTS = {
    "metric": ("Kennzahl", "Metric"),
    "value": ("Wert", "Value"),
    "total": ("Testfälle gesamt", "Total test cases"),
    "progress": ("Fortschritt (nicht Offen / gesamt)", "Progress (not Open / total)"),
    "pass_rate": ("Bestanden-Quote (ohne Nicht anwendbar)", "Pass rate (excluding Not applicable)"),
    "open_blockers": ("Offene Blocker (Fehlgeschlagen und Blocker)", "Open blockers (Failed and Blocker)"),
    "round_count": ("Testfälle", "Test cases"),
    "protection": ("Geschrieben vom E2E-Testlauf; Änderungen von Hand ersetzt der nächste Lauf",
                   "Written by the E2E test run; the next run replaces manual changes"),
    "date_form": ("11.10.2026", "11 Oct 2026"),
    "precondition": ("Voraussetzung:", "Precondition:"),
}


def _of(pair, language):
    return pair[LANGUAGES.index(language)]


def tab(key, language):
    return _of(TABS[key], language)


def head(language):
    """Die Kopfzeile von `Testfälle` in der Sprache."""
    return [c[1 + LANGUAGES.index(language)] for c in COLUMNS]


def column(key, language):
    return head(language)[[c[0] for c in COLUMNS].index(key)]


def status(language):
    return [v[1 + LANGUAGES.index(language)] for v in STATUS_VALUES]


def status_value(key, language):
    return status(language)[[v[0] for v in STATUS_VALUES].index(key)]


def severity(language):
    return [v[1 + LANGUAGES.index(language)] for v in SEVERITY_VALUES]


def severity_value(key, language):
    return severity(language)[[v[0] for v in SEVERITY_VALUES].index(key)]


def text(key, language):
    return _of(TEXTS[key], language)


def all_shops(language):
    return _of(ALL_SHOPS, language)


# Die Form eines Datums in `Getestet am` je Sprache (§337), wie TEXTS["date_form"] sie zeigt.
DATE_FORMS = {"de": re.compile(r"^\d{2}\.\d{2}\.\d{4}$"),
              "en": re.compile(r"^\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}$")}


def header_language(row, language=None):
    """Die Sprache, deren Kopfzeile `row` ist; None, wenn keine oder nicht die aus `language`."""
    cells = [h.strip() for h in row]
    for lang in ([language] if language else LANGUAGES):
        want = head(lang)
        if cells[:len(want)] == want and not any(cells[len(want):]):
            return lang
    return None


# Die Spalten, die der Lauf schreibt (A bis F), und die Felder des Plans dazu.
WRITTEN = 6
FIELDS = ("testcase", "shop", "role", "steps", "expected")
# Die Überschriften im Rumpf von tests/E2E-NNN.md, englisch wie jede im Repo (§295), zu Spalte C bis F.
BODY_HEADS = ("Shop", "Role", "Steps", "Expected result")
ID_FORM = re.compile(r"^E2E-(\d{3,})$")
FORBIDDEN = re.compile(r"\b(?:REQ|EP|ADR)-\d{3}\b|https?://")
REQ_ID = re.compile(r"^REQ-\d{3}$")
EPIC_ID = re.compile(r"^EP-\d{3}$")
KINDS = ("page", "draft")
TEST_FILE = re.compile(r"^E2E-\d{3,}\.md$")


def shop_values(keys, language="de"):
    """Die erlaubten Werte der Spalte `Shop`: ein Shop sein Key, mehrere jeder Key und `alle` (`all`)."""
    return list(keys) if len(keys) == 1 else list(keys) + [all_shops(language)]


def test_file_findings(t, key):
    """Die Form von `requirements` und `sources` eines geplanten Tests."""
    out = []
    reqs = t.get("requirements")
    if not isinstance(reqs, list) or not reqs or not all(isinstance(r, str) and REQ_ID.match(r) for r in reqs):
        out.append(f"test_file_field „{key}“: requirements ist keine Liste von Kennungen REQ-…: {reqs!r}")
    sources = t.get("sources")
    if not isinstance(sources, list) or not sources:
        out.append(f"test_file_field „{key}“: sources fehlt oder ist leer")
        return out
    for src in sources:
        ok = isinstance(src, dict) and EPIC_ID.match(str(src.get("epic", ""))) \
            and src.get("kind") in KINDS and str(src.get("version", "")).strip() \
            and str(src.get("link", "")).startswith("http")
        if not ok:
            out.append(f"test_file_field „{key}“: eine Quelle trägt nicht epic EP-…, kind page oder draft, "
                       f"version und link: {src!r}")
    return out


def q(value):
    return json.dumps(value, ensure_ascii=False)


def test_file(rid, t):
    """Die Datei `tests/E2E-NNN.md` eines Tests (Datalayer-Vertrag): im Kopf Kennung, Schlüssel und
    Zuordnung, im Rumpf, was der Lauf ins Sheet projiziert, je Spalte C bis F unter ihrer englischen Überschrift."""
    lines = ["---", f"id: {rid}", f"testcase: {q(str(t['testcase']).strip())}",
             f"requirements: [{', '.join(q(r) for r in t['requirements'])}]", "sources:"]
    for src in t["sources"]:
        lines += [f"  - epic: {q(src['epic'])}", f"    kind: {q(src['kind'])}",
                  f"    version: {q(str(src['version']).strip())}", f"    link: {q(src['link'])}"]
    lines.append("---")
    body = [str(t["shop"]).strip(), str(t["role"]).strip(), str(t["steps"]).strip(), str(t["expected"]).strip()]
    for head, value in zip(BODY_HEADS, body):
        lines += ["", f"## {head}", "", value]
    return "\n".join(lines) + "\n"


def write_test_files(folder, entries):
    """Schreibt oder ersetzt je Test-ID ihre Datei und liest sie zurück; die Datei eines anderen
    Tests bleibt unberührt. Gibt die IDs zurück, deren Datei sich anders zurückliest, und die Zahl
    der unberührten Dateien."""
    folder = Path(folder)
    others = {p.name for p in folder.iterdir() if TEST_FILE.match(p.name)} if folder.is_dir() else set()
    others -= {f"{rid}.md" for rid in entries}
    folder.mkdir(parents=True, exist_ok=True)
    for rid, t in entries.items():
        (folder / f"{rid}.md").write_text(test_file(rid, t), encoding="utf-8")
    bad = [rid for rid, t in entries.items()
           if (folder / f"{rid}.md").read_text(encoding="utf-8") != test_file(rid, t)]
    return bad, len(others)


def usage(sentence):
    print(f"Aufruf: {sentence}", file=sys.stderr)
    return 2


def option(args, name):
    if name not in args:
        return None
    i = args.index(name)
    return args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else ""


def pad(r):
    return list(r) + [""] * (len(COLUMNS) - len(r))


def main(argv):
    args = argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    plan_path, out_path, shops_arg = option(args, "--plan"), option(args, "--out"), option(args, "--shops")
    tests_path, language = option(args, "--tests"), option(args, "--language")
    if "" in (plan_path, out_path, shops_arg, tests_path, language):
        return usage("--plan, --out, --shops, --tests und --language brauchen einen Wert")
    if language is not None and language not in LANGUAGES:
        return usage(f"--language ist {' oder '.join(LANGUAGES)}, wie `language` in project.yml")
    if tests_path and not plan_path:
        return usage("--tests braucht --plan: die Zuordnung steht im Plan")
    if tests_path and Path(tests_path).exists() and not Path(tests_path).is_dir():
        return usage("--tests nennt den Ordner tests/ des Datalayers, keine Datei")
    if plan_path and shops_arg is None:
        return usage("mit --plan nennt --shops die Keys aus shops in project.yml, etwa --shops b2c,b2b")
    keys = [k.strip() for k in (shops_arg or "").split(",") if k.strip()]
    if shops_arg is not None and (not keys or len(set(keys)) != len(keys) or set(ALL_SHOPS) & set(keys)):
        return usage("--shops nennt jeden Key aus shops einmal, durch Komma getrennt, ohne „alle“ oder „all“")

    rows = list(csv.reader(open(args[0], encoding="utf-8-sig")))
    findings = []
    lang = header_language(rows[0], language) if rows else None
    if lang is None:
        want = " oder ".join(repr(head(l)) for l in ([language] if language else LANGUAGES))
        print(f"header Zeile 1 ist {rows[0] if rows else '(leer)'!r}, erwartet {want}")
        return 1
    open_ = status_value("open", lang)
    stock = {}
    seen = collections.defaultdict(list)
    ids = collections.defaultdict(list)
    numbers = []
    for n, r in enumerate(rows[1:], start=2):
        r = pad(r)
        rid, key = r[0].strip(), r[1].strip()
        if rid:
            ids[rid].append(n)
            m = ID_FORM.match(rid)
            if m:
                numbers.append(int(m.group(1)))
        if not key:
            continue
        seen[key].append(n)
        stock[key] = (n, r)
        print(n, rid or "-", r[1], r[6].strip() or open_, sep=" | ")
        tested_on = r[11].strip()
        if tested_on and not DATE_FORMS[lang].match(tested_on):
            # ein Feld der Menschen: gemeldet, nicht abgelehnt und nie geschrieben
            print(f"DATUM {n}", tested_on, f"erwartet wie {text('date_form', lang)}", sep=" | ")
    for key, lines in seen.items():
        if len(lines) > 1:
            findings.append(f"duplicate_key Bestand „{key}“ in Zeile {', '.join(map(str, lines))}")
    for rid, lines in ids.items():
        if len(lines) > 1:
            findings.append(f"duplicate_id Bestand „{rid}“ in Zeile {', '.join(map(str, lines))}")

    if plan_path:
        allowed = shop_values(keys, lang)
        plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
        planned = collections.Counter()
        for t in plan:
            key = str(t.get("testcase", "")).strip()
            planned[key] += 1
            for field in FIELDS:
                value = str(t.get(field, ""))
                if not value.strip():
                    findings.append(f"empty_field „{key}“: {field} ist leer")
                hit = FORBIDDEN.search(value)
                if hit:
                    findings.append(f"forbidden_id „{key}“: {field} trägt „{hit.group(0)}“; "
                                    f"ins E2E-Sheet geht keine Kennung und keine Adresse")
            if tests_path:
                findings += test_file_findings(t, key)
            shop = str(t.get("shop", "")).strip()
            if shop and shop not in allowed:
                findings.append(f"shop_unknown „{key}“: shop ist „{shop}“, erlaubt ist "
                                f"{', '.join(allowed)}")
        for key, count in planned.items():
            if count > 1:
                findings.append(f"duplicate_key Plan „{key}“ steht {count}-mal")
    if findings:
        for f in findings:
            print(f)
        return 1
    if not plan_path:
        return 0

    next_number = max(numbers, default=0) + 1
    replaced, new, back = {}, [], {}
    for t in plan:
        key = str(t["testcase"]).strip()
        body = [str(t["shop"]).strip(), str(t["role"]).strip(), str(t["steps"]), str(t["expected"])]
        if key not in stock:
            rid = f"E2E-{next_number:03d}"
            next_number += 1
            new.append([rid, key] + body)
            print(f"NEU {rid}", key, sep=" | ")
            continue
        n, r = stock[key]
        if r[2:WRITTEN] == body:
            print(f"GLEICH {n}", key, sep=" | ")
            if ID_FORM.match(r[0].strip()):
                back[key] = r[0].strip()
            continue
        rid = r[0].strip()
        if not rid:  # eine Zeile ohne ID, von Hand angelegt, bekommt beim Ersetzen die nächste
            rid = f"E2E-{next_number:03d}"
            next_number += 1
        replaced[n] = [rid, key] + body
        print(f"ERSETZT {n}", key, sep=" | ")
        status, result = r[6].strip(), r[8].strip()
        if (status and status != open_) or result:
            print(f"ERGEBNIS {n}", key, status or open_, result or "-", sep=" | ")
    keys_planned = {str(t["testcase"]).strip() for t in plan}
    for key, (n, _) in sorted(stock.items(), key=lambda kv: kv[1][0]):
        if key not in keys_planned:
            print(f"NICHT-MEHR {n}", key, sep=" | ")

    last = len(rows)
    if replaced:
        values = []
        for n, r in enumerate(rows[1:], start=2):
            values.append(replaced.get(n, pad(r)[:WRITTEN]))
        values += new
        update = {"range": f"'{tab('testcases', lang)}'!A2:F{1 + len(values)}", "values": values}
    elif new:
        update = {"range": f"'{tab('testcases', lang)}'!A{last + 1}:F{last + len(new)}", "values": new}
    else:
        update = {"range": None, "values": []}
    # update_values deutet Eingaben wie getippt: "=…" und "+…" werden Formeln, "0042" wird 42, ein
    # Datum wird eine Zahl. Ein führendes Hochkomma hält jeden Wert als Text, und get_values liefert
    # ihn ohne Hochkomma zurück (gemessen am 04.10.2026).
    update["values"] = [[f"'{c}" if c else c for c in row] for row in update["values"]]
    if out_path:
        Path(out_path).write_text(json.dumps(update, ensure_ascii=False, indent=1), encoding="utf-8")
    print("SCHREIBEN", update["range"] or "nichts", f"{len(update['values'])} Zeile(n)", sep=" | ")
    if tests_path:
        missing = [str(t["testcase"]).strip() for t in plan if not back.get(str(t["testcase"]).strip())]
        if missing:
            print(f"test_file_not_back {len(missing)} geplante(r) Test(s) nicht GLEICH oder ohne ID im Sheet, "
                  f"etwa „{missing[0]}“; die Dateien entstehen erst aus dem Rücklauf, {tests_path} bleibt "
                  f"unverändert")
            return 1
        bad, kept = write_test_files(tests_path, {back[str(t["testcase"]).strip()]: t for t in plan})
        if bad:
            print(f"test_file_not_back {tests_path}: zurückgelesen ist nicht das Geschriebene, "
                  f"{', '.join(rid + '.md' for rid in bad)}")
            return 1
        print("TESTS", tests_path, f"{len(plan)} Datei(en) geschrieben, {kept} Datei(en) anderer Tests unberührt",
              sep=" | ")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
