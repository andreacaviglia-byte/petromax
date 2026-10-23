#!/usr/bin/env python3
"""Prüft die Anforderungsliste auf dem, was der Lauf schon gelesen hat, und trägt ihre Tabs,
Spalten und Anzeigewerte, wie sie in .claude/docs/requirements-list-contract.md stehen (§247, §295).

Aufruf:
    check-sheet.py <anforderungen> [--epics <epics>] [--check NAME]... [--page EP-001 <ids-datei>]...
                   [--header <Tab> <datei>]... [--language de|en] [--project <project.yml>]

<anforderungen> ist der CSV-Export des Tabs `Anforderungen` (`Requirements`) mit Kopfzeile (Spalte
`ID`) oder eine TSV, deren erste Spalte die ID trägt, Kopfzeile erlaubt. <epics> ist eine CSV oder
TSV des Tabs `Epics` mit Kopfzeile und den Spalten `Epic-ID` und `Anforderungen` (`en`: `Epic ID`,
`Requirements`); die IDs einer Zelle sind durch Komma, Semikolon oder Leerraum getrennt. <ids-datei>
trägt die IDs, die der Lauf auf der Seite des Epics gelesen hat, getrennt durch Leerraum oder Komma;
eine ID, die zweimal auf der Seite steht, steht zweimal in der Datei. --header nennt einen Tab mit
seinem Namen im Sheet, in `de` oder `en`, und eine CSV oder TSV, deren erste Zeile die gelesene
Kopfzeile dieses Tabs ist. --language legt die Sprache fest, sonst gilt jede, deren Tab so heißt.

Prüfungen:
    duplicate_id    eine ID steht in mehr als einer Zeile des Tabs Anforderungen
    unassigned      eine Anforderung steht in keiner Zelle Anforderungen des Tabs Epics
    multiple_epics  eine ID steht mehr als einmal in der Spalte Anforderungen, in einem Epic oder in
                    zweien
    unknown_id      die Spalte Anforderungen nennt eine ID, die im Tab Anforderungen fehlt
    once_on_page    eine Anforderung des Epics fehlt auf seiner Seite oder steht mehrfach dort,
                    oder die Seite nennt eine ID, die laut Sheet nicht zu diesem Epic gehört
    header          die Kopfzeile eines Tabs weicht vom Vertrag ab (je --header; ohne --header die
                    Kopfzeile von <anforderungen>)
    cut             der Schnitt nach §252: domain (die Domäne eines Epics steht nicht in der festen
                    Liste), epic_size (ein Epic trägt mehr als 12 Anforderungen, und die
                    Kurzbeschreibung trägt kein „Größe bestätigt“), add_on (ein Add-on aus --project,
                    das ein Epic schaltet, hat kein Epic seiner Domäne); braucht --epics mit den Spalten
                    Domäne und Kurzbeschreibung

Ohne --check laufen duplicate_id, mit --epics dazu unassigned, multiple_epics und unknown_id, und
once_on_page je --page; header und cut laufen nur mit --check. `--check header` mit --header braucht
<anforderungen> nicht. Vor dem Schnitt sind die Epics leer (§150); ein Lauf vor dem Schnitt ruft
deshalb `--check duplicate_id` ohne --epics.

Ausgabe: je Verstoß eine Zeile `<prüfung> <ID> <Satz>`. Exit 0 ohne Verstoß, 1 mit Verstoß,
2 bei falschem Aufruf oder fehlender Spalte. Nur Standardbibliothek, Python 3.9.
"""
import csv
import io
import re
import sys
from collections import Counter, defaultdict

CHECKS = ("duplicate_id", "unassigned", "multiple_epics", "unknown_id", "once_on_page", "header", "cut")
NEEDS_EPICS = ("unassigned", "multiple_epics", "unknown_id", "once_on_page", "cut")
LANGUAGES = ("de", "en")

# Die Eigentümer einer Spalte (§283): das Repo schreibt sie, ein Mensch schreibt sie, oder sie trägt
# eine Formel, die kein Lauf schreibt.
REPO, HUMAN, FORMULA = "repo", "human", "formula"

# Die Tabs der Anforderungsliste, wörtlich wie in .claude/docs/requirements-list-contract.md;
# dev/tests/check-sheet.py hält beide zusammen. Je Tab sein Name in de und en und je Spalte ihr
# Schlüssel, ihre Kopfzeile in de und en und ihr Eigentümer.
TABS = {
    "requirements": (("Anforderungen", "Requirements"), [
        ("id", "ID", "ID", REPO),
        ("title", "Anforderung", "Requirement", REPO),
        ("description", "Beschreibung", "Description", REPO),
        ("epic", "Epic", "Epic", REPO),
        ("cluster", "Cluster", "Cluster", HUMAN),
        ("owner_customer", "Owner Kunde", "Customer owner", HUMAN),
        ("owner_strix", "Owner Strix", "Strix owner", HUMAN),
        ("status", "Status", "Status", REPO),
        ("priority", "Priorität", "Priority", REPO),
        ("scope", "Scope", "Scope", REPO),
        ("design_needed", "Design nötig?", "Design needed?", REPO),
        ("interface_needed", "Interface nötig?", "Interface needed?", REPO),
        ("open_questions", "Offene Fragen", "Open questions", REPO),
        ("comment", "Kommentar", "Comment", HUMAN),
        ("source", "Quelle", "Source", REPO),
        ("live", "Heute live?", "Live today?", REPO),
        ("current_state", "Hinweis (IST)", "Current state", REPO),
        ("shops", "Shops", "Shops", REPO),
    ]),
    "solutioning": (("Solutioning", "Solutioning"), [
        ("id", "ID", "ID", REPO),
        ("title", "Anforderung", "Requirement", REPO),
        ("classification", "Klassifizierung", "Classification", REPO),
        ("size", "Aufwand", "Size", REPO),
        ("hours", "Aufwand (h)", "Effort (h)", HUMAN),
        ("option_1", "Lösungsoption 1", "Solution option 1", REPO),
        ("option_2", "Lösungsoption 2", "Solution option 2", REPO),
        ("option_3", "Lösungsoption 3", "Solution option 3", REPO),
        ("recommendation", "Empfehlung", "Recommendation", REPO),
        ("open_questions", "Offene Fragen / Entscheidungsbedarf", "Open questions / decisions", REPO),
        ("depends_on", "Abhängigkeiten", "Dependencies", REPO),
        ("solution_status", "Solutioning-Status", "Solutioning status", REPO),
    ]),
    "epics": (("Epics", "Epics"), [
        ("id", "Epic-ID", "Epic ID", REPO),
        ("domain", "Domäne", "Domain", REPO),
        ("title", "Epic", "Epic", REPO),
        ("summary", "Kurzbeschreibung", "Summary", REPO),
        ("requirements", "Anforderungen", "Requirements", REPO),
        ("status", "Status", "Status", REPO),
        ("information", "Informationsstand", "Information", REPO),
        ("clarification", "Klärungsbedarf", "Clarification", REPO),
        ("owner_strix", "Owner Strix", "Strix owner", HUMAN),
        ("owner_customer", "Owner Kunde", "Customer owner", HUMAN),
        ("hours", "Aufwand (h)", "Effort (h)", FORMULA),
        ("reviewed_by", "Geprüft von", "Reviewed by", HUMAN),
        ("reviewed_on", "Geprüft am", "Reviewed on", HUMAN),
        ("draft", "Entwurf", "Draft", REPO),
        ("epic_page", "Epic Page", "Epic page", REPO),
        ("board_key", "Board-Schlüssel", "Board key", REPO),
    ]),
    "open_items": (("Offene Punkte", "Open items"), [
        ("id", "GAP-ID", "GAP ID", REPO),
        ("kind", "Art", "Kind", REPO),
        ("question", "Frage", "Question", REPO),
        ("to", "An", "To", REPO),
        ("concerns", "Betrifft", "Concerns", REPO),
        ("blocking", "Blockiert", "Blocking", REPO),
        ("responsible", "Verantwortlich", "Responsible", HUMAN),
        ("due", "Bis", "Due", HUMAN),
    ]),
}

# Die Anzeigewerte, wörtlich wie im Vertrag, Abschnitt „Die Anzeigewerte“ (§295): je Feld mit
# Vokabular der Wert im Repo und seine Anzeige in de und en. Ein leerer Wert bleibt leer, außer wo er
# hier steht.
VALUES = {
    "status (Anforderung)": {"open": ("Offen", "Open"), "confirmed": ("Bestätigt", "Confirmed"),
                             "rejected": ("Verworfen", "Rejected"), "duplicate": ("Duplikat", "Duplicate")},
    "priority": {"must-have": ("Must-have", "Must-have"), "nice-to-have": ("Nice-to-have", "Nice-to-have")},
    "scope": {"in_scope": ("In Scope", "In scope"), "out_of_scope": ("Out of Scope", "Out of scope")},
    "live": {"yes": ("Ja", "Yes"), "no": ("Nein", "No"), "partial": ("Teilweise", "Partial"),
             "verify": ("Verifizieren", "Verify")},
    "design_needed, interface_needed": {"yes": ("ja", "yes"), "no": ("nein", "no"), "open": ("offen", "open")},
    "size": {"S": ("S", "S"), "M": ("M", "M"), "L": ("L", "L"), "XL": ("XL", "XL")},
    "solution_status": {"": ("Entwurf", "Draft"), "proposed": ("Entwurf", "Draft"),
                        "decided": ("Entschieden", "Decided"), "blocked": ("Blocker", "Blocked")},
    "kind (Frage)": {"discovery": ("Discovery", "Discovery"), "solutioning": ("Solutioning", "Solutioning"),
                     "decision": ("Entscheidung", "Decision")},
    "blocking": {"yes": ("Ja", "Yes"), "no": ("Nein", "No")},
    "information (Epic)": {"thin": ("Dünn", "Thin"), "partial": ("Teilweise", "Partial"),
                           "solid": ("Tragfähig", "Solid")},
    "status (Epic)": {"open": ("Offen", "Open"), "in_progress": ("In Bearbeitung", "In progress"),
                      "in_review": ("Zur Abnahme", "In review"),
                      "internal_review": ("Interne Abnahme", "Internal review"),
                      "merged": ("Zusammengeführt", "Merged"), "dissolved": ("Aufgelöst", "Dissolved")},
    "domain (Epic, §252)": {
        "basic_setup": ("Basissetup", "Basic setup"), "design": ("Design", "Design"),
        "storefront": ("Storefront", "Storefront"), "product_data": ("Produktdaten", "Product data"),
        "search_navigation": ("Suche & Navigation", "Search & navigation"),
        "cart_checkout": ("Warenkorb & Checkout", "Cart & checkout"),
        "customer_account": ("Kundenkonto", "Customer account"), "b2b": ("B2B", "B2B"),
        "subscription_loyalty": ("Abo & Kundenbindung", "Subscriptions & loyalty"),
        "markets_shipping": ("Märkte & Versand", "Markets & shipping"),
        "legal_consent": ("Recht & Consent", "Legal & consent"),
        "marketing_crm": ("Marketing & CRM", "Marketing & CRM"),
        "apps_features": ("Apps & Features", "Apps & features"), "interfaces": ("Schnittstellen", "Interfaces"),
        "data_migration": ("Datenmigration", "Data migration"),
        "content_migration": ("Content-Migration", "Content migration")},
}
# Die acht Klassifizierungen (§324), wörtlich wie im Datalayer-Vertrag, Abschnitt „Die Klassifizierung“,
# ihrem einzigen Besitzer: je Wert die Anzeige in de und en. dev/tests/check-sheet.py hält beide gleich.
VALUES["classification"] = {
    "shop": ("Shopify-nativ", "Shopify native"), "theme_native": ("Theme-nativ", "Theme native"),
    "app": ("Public App", "Public app"), "theme": ("Theme-Anpassung", "Theme customization"),
    "custom_app": ("Custom App", "Custom app"),
    "integration_connector": ("Standard-Konnektor", "Standard connector"),
    "integration_middleware": ("Middleware", "Middleware"),
    "integration_custom": ("Custom Schnittstelle", "Custom integration")}
DOMAIN = "domain (Epic, §252)"
EPIC_STATUS = "status (Epic)"


def tab_name(tab, language):
    return TABS[tab][0][LANGUAGES.index(language)]


def columns(tab, language):
    """Die Kopfzeile eines Tabs in einer Sprache."""
    i = LANGUAGES.index(language) + 1
    return [c[i] for c in TABS[tab][1]]


def column(tab, key, language):
    """Die Kopfzeile einer Spalte, gefunden über ihren Schlüssel."""
    i = LANGUAGES.index(language) + 1
    return next(c[i] for c in TABS[tab][1] if c[0] == key)


def display(field, value, language):
    """Der Anzeigewert eines Werts aus dem Repo; None, wenn der Vertrag ihn nicht kennt."""
    pair = VALUES[field].get(value)
    return pair[LANGUAGES.index(language)] if pair else None


# HEADERS[language][Tab-Name] ist die Kopfzeile, die ein Lauf in dieser Sprache liest.
HEADERS = {lang: {tab_name(t, lang): columns(t, lang) for t in TABS} for lang in LANGUAGES}

# Die Domänen des Schnitts in der Anzeige eines deutschen Projekts; check-solution-doc.py liest sie.
DOMAINS = tuple(v[0] for v in VALUES[DOMAIN].values())
# Je Add-on in project.yml, das ein Epic schaltet, die Domäne dieses Epics (§303).
ADD_ON_DOMAIN = {"design": "design"}
EPIC_LIMIT = 12
SIZE_OK = {"de": "Größe bestätigt", "en": "Size confirmed"}
EPIC = re.compile(r"^EP-\d{3}$")
SEP = re.compile(r"[\s,;]+")


def usage_error(sentence):
    print(f"Aufruf: {sentence}", file=sys.stderr)
    sys.exit(2)


def tab_of(name):
    """Der Schlüssel eines Tabs und die Sprachen, in denen er so heißt."""
    for key, (names, _) in TABS.items():
        langs = [lang for lang, n in zip(LANGUAGES, names) if n == name]
        if langs:
            return key, langs
    return None, []


def parse_args(argv):
    sheet, epics, checks, pages, headers, project, language = None, None, [], [], [], None, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--check":
            if i + 1 >= len(argv) or argv[i + 1] not in CHECKS:
                usage_error(f"--check braucht eine von {', '.join(CHECKS)}")
            checks.append(argv[i + 1]); i += 2
        elif a == "--epics":
            if i + 1 >= len(argv):
                usage_error("--epics braucht eine Datei")
            epics = argv[i + 1]; i += 2
        elif a == "--page":
            if i + 2 >= len(argv) or not EPIC.match(argv[i + 1]):
                usage_error("--page braucht eine Epic-ID (EP-001) und eine Datei mit IDs")
            pages.append((argv[i + 1], argv[i + 2])); i += 3
        elif a == "--header":
            names = [n for t in TABS.values() for n in t[0]]
            if i + 2 >= len(argv) or argv[i + 1] not in names:
                usage_error(f"--header braucht einen Tab ({', '.join(dict.fromkeys(names))}) und eine Datei")
            headers.append((argv[i + 1], argv[i + 2])); i += 3
        elif a == "--language":
            if i + 1 >= len(argv) or argv[i + 1] not in LANGUAGES:
                usage_error(f"--language braucht eine von {', '.join(LANGUAGES)}")
            language = argv[i + 1]; i += 2
        elif a == "--project":
            if i + 1 >= len(argv):
                usage_error("--project braucht den Pfad zu project.yml")
            project = argv[i + 1]; i += 2
        elif a.startswith("-"):
            usage_error(f"unbekannte Option {a}")
        elif sheet is None:
            sheet = a; i += 1
        else:
            usage_error("genau eine Datei des Tabs Anforderungen")
    if sheet is None and not (headers and checks == ["header"]):
        usage_error("check-sheet.py <anforderungen> [--epics <epics>] [--check NAME]... [--page EP-001 <ids-datei>]...")
    if not checks:
        checks = ["duplicate_id"]
        if epics:
            checks += ["unassigned", "multiple_epics", "unknown_id"]
        if pages:
            checks.append("once_on_page")
    missing = [c for c in checks if c in NEEDS_EPICS and not epics]
    if missing:
        usage_error(f"{', '.join(missing)} braucht --epics")
    if "once_on_page" in checks and not pages:
        usage_error("once_on_page braucht mindestens ein --page")
    if language:
        stray = [t for t, _ in headers if language not in tab_of(t)[1]]
        if stray:
            usage_error(f"--header {', '.join(stray)} heißt in {language} anders")
    return sheet, epics, checks, pages, headers, project, language


def read_table(path):
    """Liefert (Trenner, Zeilen). Erkennt TSV an einem Tab in der ersten Zeile."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    first = text.split("\n", 1)[0]
    delimiter = "\t" if "\t" in first else ","
    # Eine Zelle kann Zeilenumbrüche tragen; der Leser bekommt deshalb den Text, nicht seine Zeilen.
    rows = [r for r in csv.reader(io.StringIO(text), delimiter=delimiter) if any(c.strip() for c in r)]
    return delimiter, rows


def read_requirements(path):
    delimiter, rows = read_table(path)
    if not rows:
        return []
    head = [c.strip() for c in rows[0]]
    if delimiter == "\t" and head[0] != "ID":
        return [r[0] for r in rows]
    if "ID" not in head:
        usage_error(f"{path}: Spalte ID fehlt in der Kopfzeile")
    col = head.index("ID")
    return [(r + [""] * len(head))[col] for r in rows[1:]]


def locate(path, head, tab, keys):
    """Die Sprache der Kopfzeile und je Schlüssel die Stelle seiner Spalte; Exit 2, wenn eine fehlt."""
    for lang in LANGUAGES:
        names = [column(tab, k, lang) for k in keys]
        if all(n in head for n in names):
            return lang, [head.index(n) for n in names]
    wanted = " bzw. ".join(", ".join(column(tab, k, lang) for k in keys) for lang in LANGUAGES)
    usage_error(f"{path}: es fehlt eine der Spalten {wanted}")


def read_epics(path):
    """Liefert je Epic-Zeile (Epic-ID, [IDs])."""
    _, rows = read_table(path)
    head = [c.strip() for c in rows[0]] if rows else []
    _, (e, r) = locate(path, head, "epics", ("id", "requirements"))
    out = []
    for z in rows[1:]:
        z = z + [""] * len(head)
        if z[e].strip():
            out.append((z[e].strip(), [t for t in SEP.split(z[r]) if t]))
    return out


def add_ons(path):
    """Die Add-ons aus project.yml (§303)."""
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "check_project", Path(__file__).with_name("check-project.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        daten = mod.lies(Path(path).read_text(encoding="utf-8"))
    except (OSError, mod.Fehler) as e:
        usage_error(f"{path}: {e}")
    found = daten.get("add_ons") or []
    return list(found) if isinstance(found, list) else []


def check_cut(path, project):
    _, rows = read_table(path)
    head = [c.strip() for c in rows[0]] if rows else []
    lang, (e, d, r, k) = locate(path, head, "epics", ("id", "domain", "requirements", "summary"))
    shown = {v[LANGUAGES.index(lang)]: key for key, v in VALUES[DOMAIN].items()}
    out, domains = [], set()
    for z in rows[1:]:
        z = z + [""] * len(head)
        epic = z[e].strip()
        if not epic:
            continue
        domain = z[d].strip()
        domains.add(shown.get(domain))
        if domain not in shown:
            out.append(("cut", epic, f"domain: Domäne '{domain}' steht nicht in der Liste des Vertrags."))
        n = len([t for t in SEP.split(z[r]) if t])
        if n > EPIC_LIMIT and SIZE_OK[lang] not in z[k]:
            out.append(("cut", epic, f"epic_size: trägt {n} Anforderungen, mehr als {EPIC_LIMIT}; teilen "
                                     f"oder „{SIZE_OK[lang]}“ in {column('epics', 'summary', lang)}."))
    if project:
        for add_on in add_ons(project):
            if add_on in ADD_ON_DOMAIN and ADD_ON_DOMAIN[add_on] not in domains:
                want = display(DOMAIN, ADD_ON_DOMAIN[add_on], lang)
                out.append(("cut", add_on, f"add_on: verkauft, aber kein Epic mit Domäne '{want}'."))
    return out


def check_header(name, path, language):
    tab, langs = tab_of(name) if name else ("requirements", list(LANGUAGES))
    name = name or "/".join(dict.fromkeys(TABS["requirements"][0]))
    if language:
        langs = [language]
    _, rows = read_table(path)
    got = [c.strip() for c in rows[0]] if rows else []
    while got and not got[-1]:
        got.pop()
    if any(got == columns(tab, lang) for lang in langs):
        return []
    want = columns(tab, langs[0])
    extra = [c for c in got if c not in want]
    missing = [c for c in want if c not in got]
    detail = "; ".join(x for x in (f"fremd: {', '.join(extra)}" if extra else "",
                                    f"fehlt: {', '.join(missing)}" if missing else "") if x)
    return [("header", name, f"Kopfzeile weicht vom Vertrag ({'/'.join(langs)}) ab "
                             f"({detail or 'andere Reihenfolge'}).")]


def run_checks(ids, epics, checks, pages):
    ids = [i.strip() for i in ids if i.strip()]
    violations = []
    if "duplicate_id" in checks:
        for req_id, n in sorted(Counter(ids).items()):
            if n > 1:
                violations.append(("duplicate_id", req_id, f"steht in {n} Zeilen des Tabs Anforderungen."))
    if epics is None:
        return violations
    in_epics = defaultdict(list)
    for epic, members in epics:
        for req_id in members:
            in_epics[req_id].append(epic)
    known = set(ids)
    if "unassigned" in checks:
        for req_id in sorted(known):
            if req_id not in in_epics:
                violations.append(("unassigned", req_id, "steht in keinem Epic."))
    if "multiple_epics" in checks:
        for req_id, where in sorted(in_epics.items()):
            if len(where) > 1:
                violations.append(("multiple_epics", req_id, f"steht {len(where)}-mal in der Spalte Anforderungen ({', '.join(where)})."))
    if "unknown_id" in checks:
        for req_id, where in sorted(in_epics.items()):
            if req_id not in known:
                violations.append(("unknown_id", req_id, f"steht in Anforderungen von {', '.join(where)}, aber nicht im Tab Anforderungen."))
    if "once_on_page" in checks:
        for epic, path in pages:
            with open(path, encoding="utf-8") as f:
                seen = Counter(t for t in SEP.split(f.read()) if t)
            members = sorted({i for i, w in in_epics.items() if epic in w and i in known})
            for req_id in members:
                n = seen.get(req_id, 0)
                if n == 0:
                    violations.append(("once_on_page", req_id, f"gehört zu {epic}, fehlt aber auf dessen Seite."))
                elif n > 1:
                    violations.append(("once_on_page", req_id, f"steht {n}-mal auf der Seite von {epic}."))
            for req_id in sorted(seen):
                if req_id not in known:
                    violations.append(("once_on_page", req_id, f"steht auf der Seite von {epic}, aber nicht im Sheet."))
                elif epic not in in_epics.get(req_id, []):
                    target = ", ".join(in_epics.get(req_id, [])) or "kein Epic"
                    violations.append(("once_on_page", req_id, f"steht auf der Seite von {epic}, gehört laut Sheet zu {target}."))
    return violations


def main(argv):
    sheet, epics_path, checks, pages, headers, project, language = parse_args(argv)
    epics = read_epics(epics_path) if epics_path else None
    violations = []
    if "header" in checks:
        for name, path in headers or [(None, sheet)]:
            violations += check_header(name, path, language)
    if "cut" in checks:
        violations += check_cut(epics_path, project)
    if sheet is not None:
        violations += run_checks(read_requirements(sheet), epics, checks, pages)
    for check, req_id, sentence in violations:
        print(f"{check} {req_id} {sentence}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
