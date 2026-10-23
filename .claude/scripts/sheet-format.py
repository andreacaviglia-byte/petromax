#!/usr/bin/env python3
"""Die Anfragen, die die Anforderungsliste und das E2E-Sheet formatieren (§247, §248, §256), für genau
einen Aufruf von `Google_Sheets.update_spreadsheet` je Sheet, die Werte des Tabs `Übersicht` und die
Formel in `Aufwand (h)` des Tabs `Epics`.

Aufruf:
    sheet-format.py --sheet Anforderungen=0 --sheet Solutioning=<id> --sheet Epics=<id>
                    --sheet "Offene Punkte"=<id> [--no-banding <Tab>]... [--no-protect <Tab>]...
    sheet-format.py --sheet Testfälle=0 --sheet Übersicht=<id> --shops <key>[,<key>…]
    sheet-format.py --overview-values --shops <key>[,<key>…] --separator <,|;> --language <de|en>
    sheet-format.py --epic-hours --language <de|en> --separator <,|;>

--sheet nennt einen Tab mit seinem Namen im Sheet und seine `sheetId`, je Tab höchstens einmal;
mindestens einer. Die Tabs sind die aus .claude/docs/requirements-list-contract.md, in `de` oder
`en`, alle in derselben Sprache, und die Tabs `Testfälle` und `Übersicht` des E2E-Sheets (`en`:
`Test cases` und `Overview`, beide in derselben Sprache; §337). Ihre Namen, die Kopfzeile, die Werte der
Dropdowns und die Texte der Übersicht kommen aus der Tabelle in check-e2e.py, in der Sprache der Tabs;
--language muss dazu passen, wenn es steht.
--no-banding lässt das Zebra eines Tabs aus, der schon eines trägt; --no-protect ebenso die
Schutzbereiche eines Tabs, der sie schon trägt, etwa wenn an einem bestehenden Sheet eine neue
Spalte formatiert wird: `addProtectedRange` legt jeden Bereich ein weiteres Mal an. --shops nennt die `key` aus
`shops` in `project.yml`; daraus das Dropdown der Spalte `Shop` und die Zeilen der Matrix in
`Übersicht`, nach `shop_values` in check-e2e.py.

Je Tab der Anforderungsliste, in dieser Folge: Grundformat im ganzen Blatt (Poppins 10, Umbruch, oben
bündig), Kopfzeile nach dem Eigentümer der Spalte gefärbt (§283: Repo und Formel Strix-Gelb #FFDB32,
Mensch #FFF1B0; schwarz, fett, mittig), erste Zeile und erste Spalte fixiert, eine Breite je Spalte in
Pixeln, Zebra (Weiß und die Fläche #F7F7F8) ab Zeile 2 ohne Zeilenende, damit angehängte Zeilen es
tragen, und ohne Kopffarbe, weil sie die Füllung des Kopfs überdeckte (gemessen am 05.10.2026 im
E2E-Sheet); ein Schutz mit Warnung je zusammenhängendem Bereich von Spalten des Repos und der Formel
ab Zeile 2; im Tab `Anforderungen` Dropdowns für `Status`, `Priorität`, `Scope` und `Heute live?` aus den
Anzeigewerten des Vertrags. Feldmasken stehen als volle Pfade mit Komma: die Form
`userEnteredFormat(…)` lehnt der Connector mit `Invalid field` ab, und dann gilt kein Request
(gemessen am 04.10.2026).

Der Tab `Testfälle` dazu (§256): Kopf A–F Strix-Gelb (schreibt der Lauf), G–L heller (#FFF1B0,
schreiben die Testenden); fixiert Zeile 1 und Spalten A–B; Zebra erst ab Zeile 2 und ohne Kopffarbe;
ab Zeile 2 bis Tabellenende Dropdowns für
Shop, Status, Runde und Schweregrad (`ONE_OF_LIST`, `showCustomUi`, `strict`);
`Getestet am` als Text (Zahlenformat TEXT, keine Datumsprüfung: ein Datumswert hinge vom
Gebietsschema des Sheets ab), geschrieben wie `11.10.2026`, bei `en` `11 Oct 2026` (§337); bedingte Formate (Statuszelle je Wert gefärbt, Zeile grau
bei `Nicht anwendbar`, Zeile hellrot bei `Fehlgeschlagen` und `Blocker`); ein Schutz mit Warnung auf
A–F ab Zeile 2. Der Tab `Übersicht`: Grundformat, Köpfe in Strix-Gelb, Breiten, Prozent in Fortschritt
und Quote. --overview-values gibt statt der Anfragen `{"range": …, "values": …}` für einen Aufruf von
`Google_Sheets.update_values` aus: Beschriftungen mit Hochkomma, Formeln über offene Bereiche von
`Testfälle`, damit neue Zeilen mitzählen. --separator trennt die Argumente der Formeln so, wie das
Gebietsschema des Sheets es verlangt: `;` in de_DE, `,` in en_US. --language nennt die Sprache des
E2E-Sheets, aus der Beschriftungen und Statuswerte der Formeln kommen.

--epic-hours gibt ebenso `{"range": …, "values": …}` aus: die eine Formel in Zeile 2 der Spalte
`Aufwand (h)` im Tab `Epics`, die für jede Zeile die Stunden aus `Solutioning` über die IDs summiert,
deren `Epic` in `Anforderungen` die `Epic-ID` der Zeile ist. Die Spalten findet sie über die
Kopfzeilen des Vertrags in der Sprache aus --language. Ungemessen ist, ob `update_values` sie annimmt.

Die Kopfzeilen, ihre Eigentümer und die Werte der Dropdowns kommen aus check-sheet.py und
check-e2e.py daneben, denselben Quellen, gegen die die Läufe die Kopfzeilen prüfen. Die Breiten stehen
unten je Spalte.

Prüfungen, vor jeder Ausgabe:
    width_missing   eine Spalte des Vertrags hat keine Breite
    width_orphan    eine Breite gehört zu keiner Spalte des Vertrags

Ausgabe: das JSON der `requests` (oder der Werte) auf stdout. Exit 0; 1 mit Befund, je Zeile
`<prüfung> „<Spalte>“ <Satz>`, ohne JSON; 2 bei falschem Aufruf. Nur Standardbibliothek, Python 3.9.
"""
import importlib.util
import json
import sys
from pathlib import Path

CHECK_SHEET = Path(__file__).resolve().parent / "check-sheet.py"
CHECK_E2E = Path(__file__).resolve().parent / "check-e2e.py"

YELLOW = "#FFDB32"
YELLOW_LIGHT = "#FFF1B0"
STRIPE = "#F7F7F8"
WHITE = "#FFFFFF"
BLACK = "#000000"
FONT = "Poppins"
FONT_SIZE = 10

# Testfälle: die Spalten, die der Lauf schreibt (A bis F); der Rest gehört den Testenden.
E2E_WRITTEN = 6
E2E_FROZEN_COLS = 2
# Bedingte Formate: Hintergrund der Statuszelle je Wert, über den Schlüssel in check-e2e.py; Zeile grau
# und Zeile hellrot.
STATUS_COLORS = {
    "passed": "#C8E6C9",
    "failed": "#F4C7C3",
    "blocked": "#FCE0B2",
    "retest": "#CFE2F3",
    "not_applicable": "#E0E0E0",
}
ROW_GREY_TEXT = "#9E9E9E"
ROW_RED = "#FDECEA"
OVERVIEW_WIDTHS = [260, 120, 120, 120, 120, 120, 120]

# Breite je Spalte der Anforderungsliste in Pixeln, über ihren Schlüssel in check-sheet.py: dieselbe
# Spalte ist in jedem Tab und jeder Sprache gleich breit. Kennungen und Auswahl schmal, Text breit.
WIDTHS = {
    "id": 90,
    "title": 260,
    "description": 380,
    "epic": 90,
    "cluster": 140,
    "owner_customer": 140,
    "owner_strix": 140,
    "status": 130,
    "priority": 120,
    "scope": 120,
    "design_needed": 100,
    "interface_needed": 110,
    "open_questions": 320,
    "comment": 320,
    "source": 220,
    "live": 100,
    "current_state": 220,
    "shops": 120,
    "classification": 160,
    "size": 80,
    "hours": 100,
    "option_1": 260,
    "option_2": 260,
    "option_3": 260,
    "recommendation": 220,
    "depends_on": 180,
    "solution_status": 140,
    "domain": 140,
    "summary": 320,
    "requirements": 180,
    "information": 130,
    "clarification": 260,
    "reviewed_by": 140,
    "reviewed_on": 110,
    "draft": 220,
    "epic_page": 220,
    "board_key": 110,
    "kind": 120,
    "question": 380,
    "to": 140,
    "concerns": 160,
    "blocking": 100,
    "responsible": 140,
    "due": 110,
}
# Breite je Spalte des E2E-Sheets in Pixeln, über ihren Schlüssel in check-e2e.py: in jeder Sprache gleich.
E2E_WIDTHS = {
    "id": 90,
    "testcase": 260,
    "shop": 90,
    "role": 160,
    "steps": 380,
    "expected": 320,
    "status": 130,
    "round": 80,
    "result": 320,
    "severity": 110,
    "tested_by": 140,
    "tested_on": 110,
}
# Die Dropdowns im Tab Anforderungen: Spalte und Feld ihrer Anzeigewerte im Vertrag (§283).
DROPDOWNS = (("status", "status (Anforderung)"), ("priority", "priority"), ("scope", "scope"), ("live", "live"))
REPO_PROTECTION = {"de": "Geschrieben aus dem Repo; Änderungen von Hand legt der nächste Lauf als "
                         "Abweichung vor", "en": "Written from the repo; the next run reports manual "
                                                 "changes as deviations"}




def usage_error(sentence):
    print(f"Aufruf: {sentence}", file=sys.stderr)
    sys.exit(2)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or not path.is_file():
        usage_error(f"{path.name} fehlt neben sheet-format.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_contracts():
    return load(CHECK_SHEET, "check_sheet"), load(CHECK_E2E, "check_e2e")


def check_widths(sheet, e2e):
    out = []
    keys = set()
    for tab, (names, cols) in sheet.TABS.items():
        for key, de, _, _ in cols:
            keys.add(key)
            if key not in WIDTHS:
                out.append(("width_missing", de, f"Spalte im Tab {names[0]} hat keine Breite"))
    e2e_keys = [c[0] for c in e2e.COLUMNS]
    for key, de, _ in e2e.COLUMNS:
        if key not in E2E_WIDTHS:
            out.append(("width_missing", de, f"Kopf im Tab {e2e.tab('testcases', 'de')} hat keine Breite"))
    for key in WIDTHS:
        if key not in keys:
            out.append(("width_orphan", key, "Breite gehört zu keiner Spalte des Vertrags"))
    for key in E2E_WIDTHS:
        if key not in e2e_keys:
            out.append(("width_orphan", key, f"Breite gehört zu keinem Kopf des Tabs {e2e.tab('testcases', 'de')}"))
    return out


def rgb(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return {"rgbColor": {"red": round(r / 255, 4), "green": round(g / 255, 4),
                         "blue": round(b / 255, 4)}}


def letter(index):
    return chr(ord("A") + index)


def base_request(sheet_id):
    return {"repeatCell": {
        "range": {"sheetId": sheet_id},
        "cell": {"userEnteredFormat": {
            "textFormat": {"fontFamily": FONT, "fontSize": FONT_SIZE},
            "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
        "fields": "userEnteredFormat.textFormat.fontFamily,userEnteredFormat.textFormat.fontSize,"
                  "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment"}}


def head_request(sheet_id, row, color, start=None, end=None):
    rng = {"sheetId": sheet_id, "startRowIndex": row, "endRowIndex": row + 1}
    if start is not None:
        rng.update(startColumnIndex=start, endColumnIndex=end)
    return {"repeatCell": {
        "range": rng,
        "cell": {"userEnteredFormat": {
            "backgroundColorStyle": rgb(color),
            "textFormat": {"fontFamily": FONT, "fontSize": FONT_SIZE, "bold": True,
                           "foregroundColorStyle": rgb(BLACK)},
            "wrapStrategy": "WRAP", "verticalAlignment": "MIDDLE"}},
        "fields": "userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat,"
                  "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment"}}


def width_request(sheet_id, index, pixels):
    return {"updateDimensionProperties": {
        "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": index, "endIndex": index + 1},
        "properties": {"pixelSize": pixels},
        "fields": "pixelSize"}}


def tab_requests(sheet_id, widths, banding, heads, frozen_cols=1):
    """Grundformat, Kopf in Spaltenbereichen mit eigener Farbe, Fixierung, Breiten, Zebra ab Zeile 2
    ohne Kopffarbe: die Farbe eines Zebras überdeckt die Füllung der Zelle, ein Kopf im Zebra stünde
    in einer Farbe statt in zweien (gemessen am 05.10.2026)."""
    reqs = [base_request(sheet_id)]
    reqs += [head_request(sheet_id, 0, color, start, end) for start, end, color in heads]
    reqs.append({"updateSheetProperties": {
        "properties": {"sheetId": sheet_id,
                       "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": frozen_cols}},
        "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}})
    reqs += [width_request(sheet_id, i, px) for i, px in enumerate(widths)]
    if banding:
        reqs.append({"addBanding": {"bandedRange": {
            "range": {"sheetId": sheet_id, "startRowIndex": 1, "startColumnIndex": 0,
                      "endColumnIndex": len(widths)},
            "rowProperties": {"firstBandColorStyle": rgb(WHITE),
                              "secondBandColorStyle": rgb(STRIPE)}}}})
    return reqs


def runs(flags):
    """Die zusammenhängenden Bereiche gleicher Werte als (Anfang, Ende, Wert)."""
    out = []
    for i, f in enumerate(flags):
        if out and out[-1][2] == f:
            out[-1] = (out[-1][0], i + 1, f)
        else:
            out.append((i, i + 1, f))
    return out


def protection(sheet_id, start, end, description):
    return {"addProtectedRange": {"protectedRange": {
        "range": {"sheetId": sheet_id, "startRowIndex": 1, "startColumnIndex": start,
                  "endColumnIndex": end},
        "description": description, "warningOnly": True}}}


def list_requests(sheet_id, sheet, tab, lang, banding, protect=True):
    """Ein Tab der Anforderungsliste: Kopf nach Eigentümer, Schutz auf den Spalten des Repos und der
    Formel, im Tab Anforderungen die Dropdowns (§247, §283)."""
    cols = sheet.TABS[tab][1]
    machine = [owner != sheet.HUMAN for _, _, _, owner in cols]
    heads = [(a, b, YELLOW if m else YELLOW_LIGHT) for a, b, m in runs(machine)]
    reqs = tab_requests(sheet_id, [WIDTHS[c[0]] for c in cols], banding, heads)
    if protect:
        reqs += [protection(sheet_id, a, b, REPO_PROTECTION[lang]) for a, b, m in runs(machine) if m]
    if tab == "requirements":
        keys = [c[0] for c in cols]
        for key, field in DROPDOWNS:
            values = [v[sheet.LANGUAGES.index(lang)] for v in sheet.VALUES[field].values()]
            reqs.append(dropdown(sheet_id, keys.index(key), values))
    return reqs


def column_range(sheet_id, index):
    """Eine Spalte ab Zeile 2 bis zum Ende des Tabs, ohne Zeilenende."""
    return {"sheetId": sheet_id, "startRowIndex": 1, "startColumnIndex": index, "endColumnIndex": index + 1}


def dropdown(sheet_id, index, values):
    return {"setDataValidation": {
        "range": column_range(sheet_id, index),
        "rule": {"condition": {"type": "ONE_OF_LIST",
                               "values": [{"userEnteredValue": v} for v in values]},
                 "showCustomUi": True, "strict": True}}}


def rule(sheet_id, start, end, formula, fmt):
    return {"addConditionalFormatRule": {"index": 0, "rule": {
        "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "startColumnIndex": start, "endColumnIndex": end}],
        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": formula}]},
                        "format": fmt}}}}


def e2e_requests(sheet_id, e2e, keys, lang, banding, protect=True):
    """Der Tab `Testfälle` in der Sprache `lang` (§256, §337)."""
    order = [c[0] for c in e2e.COLUMNS]
    col = order.index
    reqs = tab_requests(sheet_id, [E2E_WIDTHS[k] for k in order], banding,
                        [(0, E2E_WRITTEN, YELLOW), (E2E_WRITTEN, len(order), YELLOW_LIGHT)],
                        frozen_cols=E2E_FROZEN_COLS)
    date = col("tested_on")
    # Das Datum als Text (§337): ein Datumswert zeigte den Monat im Gebietsschema des Sheets.
    reqs.append({"repeatCell": {
        "range": column_range(sheet_id, date),
        "cell": {"userEnteredFormat": {"numberFormat": {"type": "TEXT"}}},
        "fields": "userEnteredFormat.numberFormat"}})
    reqs += [dropdown(sheet_id, col("shop"), e2e.shop_values(keys, lang)),
             dropdown(sheet_id, col("status"), e2e.status(lang)),
             dropdown(sheet_id, col("round"), e2e.ROUNDS),
             dropdown(sheet_id, col("severity"), e2e.severity(lang))]
    status, severity = letter(col("status")), letter(col("severity"))
    failed, blocker = e2e.status_value("failed", lang), e2e.severity_value("blocker", lang)
    # Jede Regel geht an Stelle 0, die zuletzt ausgegebene steht also vorn und gewinnt: die
    # Statuszelle vor den Zeilenregeln, sonst färbte die Zeile auch sie. Die Formel einer Regel
    # deutet das Sheet in seinem Gebietsschema: `=AND(…,…)` lehnt ein Sheet in de_DE als
    # `Invalid ConditionValue.userEnteredValue` ab (gemessen am 05.10.2026). Darum ohne Funktion und
    # ohne Trenner, als Produkt zweier Vergleiche.
    reqs.append(rule(sheet_id, 0, len(order), f'=(${status}2="{failed}")*(${severity}2="{blocker}")',
                     {"backgroundColorStyle": rgb(ROW_RED)}))
    reqs.append(rule(sheet_id, 0, len(order), f'=${status}2="{e2e.status_value("not_applicable", lang)}"',
                     {"textFormat": {"foregroundColorStyle": rgb(ROW_GREY_TEXT)}}))
    for key, color in STATUS_COLORS.items():
        reqs.append(rule(sheet_id, col("status"), col("status") + 1,
                         f'=${status}2="{e2e.status_value(key, lang)}"', {"backgroundColorStyle": rgb(color)}))
    if protect:
        reqs.append(protection(sheet_id, 0, E2E_WRITTEN, e2e.text("protection", lang)))
    return reqs


def overview(e2e, keys, sep=",", lang="de"):
    """Die Zeilen des Tabs `Übersicht` als Werte für update_values, dazu die Zeilen (ab 0) der
    Köpfe und der Prozentwerte. Formeln zählen über offene Bereiche von `Testfälle`. `sep` trennt
    die Argumente: update_values deutet eine Formel im Gebietsschema des Sheets, und in de_DE wird
    jede Formel mit Komma `#ERROR!` („Formula parse error.“), mit Semikolon gezählt (gemessen am
    05.10.2026). Die Funktionsnamen bleiben englisch. Beschriftungen, Statuswerte und der Tab kommen
    aus der Tabelle in check-e2e.py, in der Sprache `lang` (§337)."""
    order = [c[0] for c in e2e.COLUMNS]
    statuses = e2e.status(lang)
    S = dict(zip([v[0] for v in e2e.STATUS_VALUES], statuses))

    def rng(key):
        c = letter(order.index(key))
        return f"'{e2e.tab('testcases', lang)}'!{c}2:{c}"

    def count(status, shop=None):
        cond = f'{rng("testcase")},"<>"' + (f',{rng("shop")},"{shop}"' if shop else "")
        if status == S["open"]:  # leer zählt als Offen
            return (f'COUNTIFS({cond},{rng("status")},"")'
                    f'+COUNTIFS({cond},{rng("status")},"{status}")')
        return f'COUNTIFS({cond},{rng("status")},"{status}")'

    def T(key):
        return e2e.text(key, lang)

    width = 1 + len(statuses)
    rows = [[T("metric"), T("value")], [T("total"), f'=COUNTIF({rng("testcase")},"<>")']]
    at = {}
    for status in statuses:
        at[status] = len(rows) + 1
        rows.append([status, "=" + count(status)])
    total, open_, passed, na = 2, at[S["open"]], at[S["passed"]], at[S["not_applicable"]]
    percent = [len(rows), len(rows) + 1]
    rows.append([T("progress"), f"=IF(B{total}=0,0,(B{total}-B{open_})/B{total})"])
    rows.append([T("pass_rate"), f"=IF(B{total}-B{na}=0,0,B{passed}/(B{total}-B{na}))"])
    rows.append([T("open_blockers"),
                 f'=COUNTIFS({rng("testcase")},"<>",{rng("status")},"{S["failed"]}",'
                 f'{rng("severity")},"{e2e.severity_value("blocker", lang)}")'])
    rows.append([])
    heads = [0, len(rows)]
    rows.append([e2e.column("shop", lang)] + statuses)
    for shop in e2e.shop_values(keys, lang):
        rows.append([shop] + ["=" + count(status, shop) for status in statuses])
    rows.append([])
    heads.append(len(rows))
    rows.append([e2e.column("round", lang), T("round_count")])
    for r in e2e.ROUNDS:
        rows.append([r, f'=COUNTIFS({rng("testcase")},"<>",{rng("round")},"{r}")'])
    # Beschriftungen mit Hochkomma: update_values deutet wie getippt, "1" würde eine Zahl.
    # Gebaut wird mit Komma, getrennt nach Gebietsschema; keine Beschriftung in einer Formel trägt eines.
    values = [[c.replace(",", sep) if c.startswith("=") else (f"'{c}" if c else c) for c in r]
              + [""] * (width - len(r)) for r in rows]
    return values, heads, percent


def overview_requests(sheet_id, e2e, keys, lang):
    values, heads, percent = overview(e2e, keys, lang=lang)
    width = len(values[0])
    reqs = [base_request(sheet_id)]
    for row in heads:
        reqs.append(head_request(sheet_id, row, YELLOW, 0, 2 if row in (heads[0], heads[-1]) else width))
    reqs += [width_request(sheet_id, i, px) for i, px in enumerate(OVERVIEW_WIDTHS[:width])]
    for row in percent:
        reqs.append({"repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": row, "endRowIndex": row + 1,
                      "startColumnIndex": 1, "endColumnIndex": 2},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0%"}}},
            "fields": "userEnteredFormat.numberFormat"}})
    return reqs


def epic_hours(sheet, lang, sep):
    """Die Formel in Zeile 2 von `Aufwand (h)` im Tab Epics: je Epic-ID die Summe der Stunden aus
    Solutioning über die IDs, deren Epic in Anforderungen sie nennt. MAP rechnet jede Zeile, FILTER
    liefert die IDs, SUMIF ihre Stunden; ein Epic ohne Anforderung ergibt 0."""
    def col(tab, key):
        keys = [c[0] for c in sheet.TABS[tab][1]]
        c = letter(keys.index(key))
        return f"'{sheet.tab_name(tab, lang)}'!{c}2:{c}"
    hours = letter([c[0] for c in sheet.TABS["epics"][1]].index("hours"))
    formula = (f'=MAP({col("epics", "id")},LAMBDA(e,IF(e="","",IFERROR(SUMPRODUCT(SUMIF('
               f'{col("solutioning", "id")},FILTER({col("requirements", "id")},'
               f'{col("requirements", "epic")}=e),{col("solutioning", "hours")})),0))))')
    return {"range": f"'{sheet.tab_name('epics', lang)}'!{hours}2", "values": [[formula.replace(",", sep)]]}


def parse_args(argv, tabs, e2e_tabs_of):
    o = {"sheets": {}, "no_banding": set(), "no_protect": set(), "keys": None,
         "values_only": False, "epic_hours": False, "separator": None, "language": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--overview-values", "--epic-hours"):
            o["values_only" if a == "--overview-values" else "epic_hours"] = True
            i += 1
            continue
        if a not in ("--sheet", "--no-banding", "--no-protect", "--shops", "--separator", "--language"):
            usage_error(f"unbekannte Option {a}")
        if i + 1 >= len(argv):
            usage_error(f"{a} braucht einen Wert")
        v = argv[i + 1]
        i += 2
        if a in ("--no-banding", "--no-protect"):
            if v not in tabs:
                usage_error(f"{a} braucht einen Tab ({', '.join(tabs)})")
            o[a[2:].replace("-", "_")].add(v)
        elif a == "--shops":
            keys = [k.strip() for k in v.split(",") if k.strip()]
            if not keys or len(set(keys)) != len(keys) or {"alle", "all"} & set(keys):
                usage_error("--shops nennt jeden Key aus shops einmal, durch Komma getrennt, ohne „alle“ oder „all“")
            o["keys"] = keys
        elif a == "--separator":
            if v not in (",", ";"):
                usage_error("--separator ist , oder ;")
            o["separator"] = v
        elif a == "--language":
            if v not in ("de", "en"):
                usage_error("--language ist de oder en")
            o["language"] = v
        else:
            tab, sep, sid = v.partition("=")
            if not sep or tab not in tabs or not sid.isdigit():
                usage_error(f"--sheet braucht <Tab>=<sheetId>, Tab aus {', '.join(tabs)}")
            if tab in o["sheets"]:
                usage_error(f"--sheet {tab} steht zweimal")
            o["sheets"][tab] = int(sid)
    sheets = o["sheets"]
    if o["values_only"] and o["epic_hours"]:
        usage_error("--overview-values und --epic-hours sind zwei Aufrufe")
    if o["values_only"]:
        if sheets or o["no_banding"] or o["no_protect"] or o["keys"] is None \
                or o["separator"] is None or o["language"] is None:
            usage_error("--overview-values steht allein mit --shops, --separator und --language")
        return o
    if o["epic_hours"]:
        if sheets or o["no_banding"] or o["no_protect"] or o["keys"] is not None \
                or o["separator"] is None or o["language"] is None:
            usage_error("--epic-hours steht allein mit --language und --separator")
        return o
    if o["separator"] is not None:
        usage_error("--separator gilt nur mit --overview-values oder --epic-hours")
    if not sheets:
        usage_error("sheet-format.py --sheet <Tab>=<sheetId>... [--no-banding <Tab>]... [--no-protect <Tab>]...")
    for opt in ("no_banding", "no_protect"):
        stray = o[opt] - set(sheets)
        if stray:
            usage_error(f"--{opt.replace('_', '-')} {', '.join(sorted(stray))} ohne --sheet")
    e2e_tabs = any(t in e2e_tabs_of for t in sheets)
    if e2e_tabs and o["keys"] is None:
        usage_error("--sheet Testfälle und --sheet Übersicht (Test cases, Overview) brauchen --shops")
    if o["keys"] is not None and not e2e_tabs:
        usage_error("--shops gilt nur mit --sheet Testfälle oder Übersicht (Test cases, Overview)")
    return o


def list_language(sheet, names, given):
    """Die eine Sprache der genannten Tabs der Anforderungsliste; Exit 2 bei zwei Sprachen."""
    langs = set(sheet.LANGUAGES)
    for name in names:
        langs &= set(sheet.tab_of(name)[1])
    if given:
        langs &= {given}
    if not langs:
        usage_error(f"die Tabs {', '.join(names)} stehen nicht in einer Sprache"
                    + (f" ({given})" if given else ""))
    return given or ("de" if "de" in langs else langs.pop())


def e2e_tab_names(e2e):
    """{Name im Sheet: (Schlüssel, Sprache)} der Tabs des E2E-Sheets."""
    return {name: (key, lang) for key, names in e2e.TABS.items() for lang, name in zip(e2e.LANGUAGES, names)}


def main(argv):
    sheet, e2e = load_contracts()
    list_tabs = {n: key for key, (names, _) in sheet.TABS.items() for n in names}
    e2e_tabs = e2e_tab_names(e2e)
    o = parse_args(argv, list(list_tabs) + list(e2e_tabs), e2e_tabs)
    findings = check_widths(sheet, e2e)
    if findings:
        for check, head, sentence in findings:
            print(f"{check} „{head}“ {sentence}")
        return 1
    sheets, keys = o["sheets"], o["keys"]
    if o["values_only"]:
        values, _, _ = overview(e2e, keys, o["separator"], o["language"])
        print(json.dumps({"range": f"'{e2e.tab('overview', o['language'])}'!A1:"
                                   f"{letter(len(values[0]) - 1)}{len(values)}",
                          "values": values}, ensure_ascii=False))
        return 0
    if o["epic_hours"]:
        print(json.dumps(epic_hours(sheet, o["language"], o["separator"]), ensure_ascii=False))
        return 0
    requests = []
    named = [t for t in sheets if t in list_tabs]
    if named:
        lang = list_language(sheet, named, o["language"])
        for key in sheet.TABS:
            name = sheet.tab_name(key, lang)
            if name in sheets:
                requests += list_requests(sheets[name], sheet, key, lang, name not in o["no_banding"],
                                          name not in o["no_protect"])
    named_e2e = [t for t in sheets if t in e2e_tabs]
    if not named and not named_e2e and o["language"]:
        usage_error("--language gilt nur mit Tabs der Anforderungsliste, des E2E-Sheets oder --epic-hours")
    if named_e2e:
        langs = {e2e_tabs[t][1] for t in named_e2e}
        if len(langs) > 1 or (o["language"] and o["language"] not in langs):
            usage_error(f"die Tabs {', '.join(named_e2e)} stehen nicht in einer Sprache"
                        + (f" ({o['language']})" if o["language"] else ""))
        e2e_lang = langs.pop()
        for key in ("testcases", "overview"):
            name = e2e.tab(key, e2e_lang)
            if name not in sheets:
                continue
            if key == "testcases":
                requests += e2e_requests(sheets[name], e2e, keys, e2e_lang, name not in o["no_banding"],
                                         name not in o["no_protect"])
            else:
                requests += overview_requests(sheets[name], e2e, keys, e2e_lang)
    print(json.dumps(requests, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
