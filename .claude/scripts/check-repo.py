#!/usr/bin/env python3
"""Prüft die Objekte des Projekt-Repos gegeneinander (§280), am Ende jedes schreibenden Laufs und vor
der Projektion: ein Fehler zeigt sich hier, bevor der Kunde ihn im Sheet oder im Proposal sieht.

Aufruf:
    check-repo.py <repo> [--check NAME]...

Prüfungen (ohne --check alle):
    object        eine Datei in requirements/, epics/, gaps/, todo/, decisions/, tests/ oder
                  way-of-working/ hat keinen lesbaren Kopf, ihr Name folgt nicht dem Vertrag, oder
                  ihr `id` ist nicht die Kennung im Dateinamen
    value         ein Feld mit Vokabular trägt einen Wert, den der Vertrag nicht kennt
                  (requirements-list-contract.md, „Die Anzeigewerte“; `classification` nach
                  datalayer-contract.md, „Die Klassifizierung“, §324; dazu `status` einer Frage
                  open|closed, einer Aufgabe open|done, `own_sections` eine Zahl, `size_estimate_approach` wie `size`, `standard` eine
                  Standard-Anforderung eines Add-ons nach §303): er würde nicht
                  projiziert (§295)
    epic          eine Anforderung nennt ein Epic, das es nicht gibt, oder, sobald es Epics gibt,
                  eine gültige Anforderung (open, confirmed) steht in keinem (§150)
    gap_target    eine offene Frage hat kein `to`, kein `concerns`, `concerns` ist keine Liste, oder
                  `concerns` nennt eine Kennung, die es nicht gibt (§279)
    task_done     eine Aufgabe in todo/ trägt `done_by` oder `done_at`, ist aber nicht `done`, oder
                  `done_at` ist kein Datum JJJJ-MM-TT (§359); `to` wird nicht geprüft (§360)
    gap_question  eine Frage in gaps/ hat keinen Fragetext: der Rumpf bis zur ersten Überschrift
                  ist leer, also bleiben `Frage` im Tab `Offene Punkte` und der Kurztext leer
    gap_jargon    der Text einer offenen Frage nennt eine Datei des Repos, einen Skill, das Repo oder
                  eine Wendung der Werkzeugsprache („laut Arbeitsweise“, „Annahme des Leads“); der
                  Text geht wörtlich zum Kunden (datalayer-contract.md, „gaps/“, §278)
    depends_on    `depends_on` einer Anforderung ist keine Liste oder nennt etwas anderes als die Kennung einer
                  Anforderung, eines Epics oder einer ADR, etwa eine offene Frage; wer an einer
                  Frage hängt, steht in ihrem `concerns`
    shops         `shops` einer Anforderung oder ADR ist keine Liste oder nennt einen Schlüssel, den
                  `shops` in project.yml nicht trägt (§307)
    architecture  eine Zeile einer Tabelle in architecture.md hat eine andere Zahl von Spalten als
                  ihre Kopfzeile (§216)
    page_type     eine gültige Anforderung im Scope (in_scope) in einem Epic der Domäne
                  `storefront`, also ein Seitentyp im Theme-Epic, hat keine Größe oder keine Annahme
                  zu den eigenen Sections (`own_sections`, §285)
    sections      ein Seitentyp führt unter `## Sections` mehr angepasste oder neue Sections, als
                  `own_sections` annimmt: eine Änderung des Scopes (§285)
    effort_estimate
                  `effort_estimate_model` einer Anforderung ist weder leer noch eine Stundenzahl
                  (Ziffern, höchstens ein Dezimalpunkt), oder sie ist gesetzt, obwohl project.yml das
                  Add-on `solutioning` nicht führt oder die Lösung nicht `decided` ist: Stunden schätzt
                  das Modell nur für eine ausgearbeitete Lösung in einem Vorhaben mit Solutioning (§357)
    wow          way-of-working.md ist nicht die Projektion aus dem Standard und way-of-working/:
                  eine Abweichung ohne Datei im Abweichungsprotokoll, oder eine Datei nennt einen
                  Abschnitt, den der Standard nicht hat, oder der Standard
                  .claude/way-of-working-standard.md fehlt (§286)
    app_evaluation
                  eine Anforderung mit `app` in `classification` ist nicht evaluiert (§320): ist sie
                  `decided`, nennt sie in `depends_on` keine ADR mit `## Evaluation`, oder die ADR
                  steht nicht auf `accepted`; ist sie `proposed` mit einer solchen ADR, steht die ADR
                  nicht auf `proposed`; die Tabelle hat nicht die Spalten Candidate, Criterion,
                  Result, Level, Source, Date, eine Zeile einen Wert außerhalb des Vokabulars, eine
                  Annahme als Beleg, oder weniger als zwei Kandidaten (ein Lösungsansatz ohne App zählt
                  mit); der erste Lösungsansatz unter `## Approach` steht nicht als Kandidat da oder
                  erfüllt ein Kriterium nicht; oder ein Kriterium dieses Lösungsansatzes ist
                  `unproven`, und doch ist die Anforderung nicht `blocked`, die ADR nicht `proposed`
                  oder keine offene Frage mit `blocking: yes` betrifft sie

Ausgabe: je Verstoß eine Zeile `<prüfung> <Datei oder Kennung> <Satz>`. Exit 0 ohne Verstoß, 1 mit
Verstoß, 2 bei falschem Aufruf. Nur Standardbibliothek, Python 3.9.
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import repo_objects  # noqa: E402  Die Objekte des Repos, eine Datei je Objekt (§280)

CHECKS = ("object", "value", "epic", "gap_target", "task_done", "gap_question", "gap_jargon", "depends_on", "shops",
          "page_type", "sections", "effort_estimate", "architecture", "wow", "app_evaluation")
VALID = ("open", "confirmed")
THEME_DOMAIN = "storefront"

# Je Art und Feld die Zeile der Anzeigewerte im Vertrag; leer ist erlaubt, wo der Vertrag es sagt.
VOCAB = {
    "requirements": {"status": ("status (Anforderung)", False), "priority": ("priority", False),
                     "scope": ("scope", True),
                     "design_needed": ("design_needed, interface_needed", False),
                     "interface_needed": ("design_needed, interface_needed", False),
                     "live": ("live", True), "size": ("size", True),
                     "size_estimate_approach": ("size", True),
                     "solution_status": ("solution_status", True)},
    "epics": {"domain": ("domain (Epic, §252)", False), "status": ("status (Epic)", False),
              "information": ("information (Epic)", False)},
    "gaps": {"kind": ("kind (Frage)", False), "blocking": ("blocking", False)},
}
STATUS = {"gaps": ("open", "closed"), "todo": ("open", "done")}
# Die Standard-Anforderung eines Add-ons (§303); fehlt das Feld, ist es leer.
STANDARDS = ("", "design-concept", "design-qa", "content-migration")
SECTION_LINE = re.compile(r"^\s*[-*] \S")
DEPENDS_ON = re.compile(r"^(REQ|EP|ADR)-\d{3}$")
ARCHITECTURE = "architecture.md"
# Die Evaluierung einer App in der ADR (§320): Spalten und Vokabular, englisch wie jeder Wert im Repo (§295).
EVALUATION = "Evaluation"
EVALUATION_HEAD = ["Candidate", "Criterion", "Result", "Level", "Source", "Date"]
RESULTS = ("met", "not_met", "unproven")
LEVELS = ("dev_store", "vendor", "help_center", "shopify_dev", "assumption")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Die Modellschätzung (§357): Stunden als Zahl mit Dezimalpunkt oder leer; fehlt das Feld, ist es leer.
HOURS = re.compile(r"^\d+(\.\d+)?$")
OPTION = re.compile(r"^### (.+?)\s*$", re.M)


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_objects(objects):
    out = []
    for kind, items in objects.items():
        for o in items:
            if "error" in o:
                out.append(("object", o["name"], o["error"]))
            elif kind not in ("todo", "way_of_working") and str(o["head"].get("id", "")) != o["key"]:
                out.append(("object", o["name"], f"id ist „{o['head'].get('id', '')}“, der Dateiname "
                                                 f"sagt {o['key']}"))
    return out


def check_values(objects, sheet):
    out = []
    for kind, fields in VOCAB.items():
        for o in objects[kind]:
            if "head" not in o:
                continue
            for field, (row, empty_ok) in fields.items():
                v = o["head"].get(field, "")
                if not isinstance(v, str) or (v == "" and not empty_ok and "" not in sheet.VALUES[row]) \
                        or (v != "" and v not in sheet.VALUES[row]):
                    out.append(("value", o["key"], f"{field}: „{v}“ kennt der Vertrag nicht"))
    for o in objects["requirements"]:
        if "head" not in o:
            continue
        cls = o["head"].get("classification", [])
        cls = [] if cls == "" else cls
        if not isinstance(cls, list) or len(cls) > 2 or any(c not in sheet.VALUES["classification"] for c in cls):
            out.append(("value", o["key"], f"classification: „{cls}“ ist keine Liste von höchstens zwei "
                                           f"Werten des Vertrags"))
        standard = o["head"].get("standard", "")
        if standard not in STANDARDS:
            out.append(("value", o["key"], f"standard: „{standard}“, erlaubt {' | '.join(STANDARDS[1:])} oder leer"))
        own = str(o["head"].get("own_sections", ""))
        if own and not own.isdigit():
            out.append(("value", o["key"], f"own_sections: „{own}“ ist keine Zahl"))
    for o in objects["epics"]:
        order = str(o.get("head", {}).get("solve_order", ""))
        if order and not order.isdigit():
            out.append(("value", o["key"], f"solve_order: „{order}“ ist keine Zahl (§318)"))
    for kind, allowed in STATUS.items():
        for o in objects[kind]:
            if "head" in o and o["head"].get("status") not in allowed:
                out.append(("value", o.get("key", o["name"]),
                            f"status: „{o['head'].get('status')}“, erlaubt {' | '.join(allowed)}"))
    return out


def check_epics(objects):
    out = []
    epics = {e["key"] for e in objects["epics"] if "head" in e}
    for r in objects["requirements"]:
        if "head" not in r:
            continue
        epic = str(r["head"].get("epic", ""))
        if epic and epic not in epics:
            out.append(("epic", r["key"], f"nennt {epic}, das es in epics/ nicht gibt"))
        elif not epic and epics and r["head"].get("status") in VALID:
            out.append(("epic", r["key"], "steht in keinem Epic, obwohl der Schnitt da ist"))
    return out


def check_gaps(objects):
    out = []
    known = {o["key"] for kind in ("requirements", "epics") for o in objects[kind] if "head" in o}
    for g in objects["gaps"]:
        if "head" not in g or g["head"].get("status") != "open":
            continue
        h = g["head"]
        concerns = h.get("concerns") or []
        if isinstance(concerns, str):
            out.append(("gap_target", g["key"], f"concerns: „{concerns}“ ist keine Liste in eckigen Klammern; "
                                                "die Projektion liest es Zeichen für Zeichen"))
            concerns = [concerns]
        if not str(h.get("to", "")).strip():
            out.append(("gap_target", g["key"], "hat kein `to`: an wen die Frage geht"))
        if not concerns:
            out.append(("gap_target", g["key"], "hat kein `concerns`: was sie betrifft"))
        for c in concerns:
            if c not in known:
                out.append(("gap_target", g["key"], f"concerns nennt {c}, das es nicht gibt"))
    return out


def check_task_done(objects):
    """§359: wer abhakt, schreibt `done_by` und `done_at`; beide gibt es nur an einer erledigten Aufgabe."""
    out = []
    for o in objects["todo"]:
        head = o.get("head")
        if not head:
            continue
        done = head.get("status") == "done"
        for field in ("done_by", "done_at"):
            if str(head.get(field, "") or "") and not done:
                out.append(("task_done", o["name"], f"{field} steht an einer Aufgabe, die nicht done ist (§359)"))
        at = str(head.get("done_at", "") or "")
        if at and not ISO_DATE.match(at):
            out.append(("task_done", o["name"], f"done_at: „{at}“ ist kein Datum JJJJ-MM-TT (§359)"))
    return out


def check_gap_questions(objects):
    out = []
    for g in objects["gaps"]:
        if "head" in g and not repo_objects.sections(g["body"])[""]:
            out.append(("gap_question", g["key"], "hat keinen Fragetext: der Rumpf bis zur ersten Überschrift "
                                                  "ist die Frage, ihr erster Satz der Kurztext im Sheet"))
    return out


# Werkzeugsprache, die in keinem Text für den Kunden stehen darf: Dateien des Repos, Skills, das Repo
# selbst und die Wendungen, die der Datalayer-Vertrag für offene Fragen ausschließt (§278).
JARGON = re.compile(
    r"(?<![\w/.-])(?:architecture|customer|way-of-working|readme|project)\.(?:md|yml)\b"
    r"|\b(?:material-intake|requirements-(?:update|review)|epic-structure|solution-(?:approach|solve-order|design|"
    r"critical-path|review|estimate|proposal|epic-page)|ticket-factory|e2e-testing-sheet|"
    r"project-(?:setup|status|upgrade)|skill-create|grill-me)\b"
    r"|\b(?:laut Arbeitsweise|Annahme des Leads|according to the way of working|lead's assumption)\b"
    r"|\b[Rr]epo(?:sitory)?\b", re.I)


def check_gap_jargon(objects):
    out = []
    for g in objects["gaps"]:
        if "head" not in g or g["head"].get("status") == "closed":
            continue
        hit = JARGON.search(repo_objects.sections(g["body"])[""])
        if hit:
            out.append(("gap_jargon", g["key"], f"„{hit.group(0)}“ im Fragetext: der Text geht wörtlich zum Kunden; "
                                                "was der Lead weiß, steht als Material in notes/, die Frage ohne "
                                                "Datei, Skill und Werkzeugsprache"))
    return out


def check_depends_on(objects):
    out = []
    for r in objects["requirements"]:
        if "head" not in r:
            continue
        deps = r["head"].get("depends_on") or []
        if isinstance(deps, str):
            out.append(("depends_on", r["key"], f"depends_on: „{deps}“ ist keine Liste in eckigen Klammern; "
                                                "die Projektion liest es Zeichen für Zeichen"))
            deps = [deps]
        for d in deps:
            if not DEPENDS_ON.match(str(d)):
                hint = "; wer an einer Frage hängt, steht in ihrem `concerns`" if str(d).startswith("GAP-") else ""
                out.append(("depends_on", r["key"], f"nennt {d}, erlaubt sind Kennungen von Anforderungen, "
                                                    f"Epics und ADRs{hint}"))
    return out


def project_keys(repo):
    """Die `key` aus `shops` in project.yml; None, wenn die Datei fehlt oder nicht lesbar ist (das meldet
    check-project.py)."""
    try:
        return repo_objects.project_shop_keys(
            repo_objects.read_yaml((Path(repo) / "project.yml").read_text(encoding="utf-8")))
    except (OSError, repo_objects.ObjectError):
        return None


def check_shops(repo, objects):
    out, known = [], project_keys(repo)
    for kind in ("requirements", "decisions"):
        for o in objects[kind]:
            if "head" not in o:
                continue
            h = o["head"]
            value = h.get("shops", "")
            if value != "" and not isinstance(value, list):
                out.append(("shops", o["key"], f"shops: „{value}“ ist keine Liste in eckigen Klammern"))
                continue
            unknown = [k for k in repo_objects.shop_keys(value) if known is not None and k not in known]
            if unknown:
                out.append(("shops", o["key"], f"shops nennt {', '.join(unknown)}, project.yml trägt "
                                               f"{', '.join(known) or 'keinen Shop'}"))
    return out


def cells(line):
    """Die Zellen einer Zeile einer Markdown-Tabelle; `\\|` trennt keine Zelle."""
    inner = line.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") and not inner.endswith("\\|") else inner
    return re.split(r"(?<!\\)\|", inner)


def check_architecture(repo):
    path = Path(repo) / ARCHITECTURE
    if not path.is_file():
        return []
    out, header = [], None
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if not line.strip().startswith("|"):
            header = None
            continue
        if header is None:
            header = len(cells(line))
            continue
        width = len(cells(line))
        if width != header:
            out.append(("architecture", f"{ARCHITECTURE}:{n}", f"hat {width} Spalten, die Kopfzeile der "
                                                               f"Tabelle {header}"))
    return out


def page_types(objects):
    theme = {e["key"] for e in objects["epics"] if "head" in e and e["head"].get("domain") == THEME_DOMAIN}
    return [r for r in objects["requirements"] if "head" in r and str(r["head"].get("epic", "")) in theme
            and r["head"].get("status") in VALID]


def check_page_types(objects):
    out = []
    for r in page_types(objects):
        h = r["head"]
        if h.get("scope") != "in_scope":
            continue
        missing = [f for f in ("size", "own_sections") if not str(h.get(f, "")).strip()]
        if missing:
            out.append(("page_type", r["key"], f"Seitentyp im Scope ohne {' und '.join(missing)} (§285)"))
    return out


def check_sections(objects):
    out = []
    for r in page_types(objects):
        own = str(r["head"].get("own_sections", ""))
        listed = [l for l in repo_objects.sections(r["body"]).get("Sections", "").split("\n")
                  if SECTION_LINE.match(l)]
        if own.isdigit() and len(listed) > int(own):
            out.append(("sections", r["key"], f"{len(listed)} angepasste oder neue Sections, angenommen "
                                              f"{own}: eine Änderung des Scopes, offene Frage mit "
                                              f"blocking an Lead und Kunden (§285)"))
    return out


def evaluation_rows(adr):
    """Die Zeilen der Tabelle unter `## Evaluation` als dict je Spalte; None ohne den Abschnitt, eine
    Zeichenkette, wenn die Kopfzeile nicht dem Vertrag folgt."""
    text = repo_objects.sections(adr["body"]).get(EVALUATION)
    if text is None:
        return None
    lines = [l for l in text.split("\n") if l.strip().startswith("|")]
    if not lines or [c.strip() for c in cells(lines[0])] != EVALUATION_HEAD:
        return "die Kopfzeile ist nicht | " + " | ".join(EVALUATION_HEAD) + " |"
    rows = []
    for line in lines[1:]:
        values = [c.strip() for c in cells(line)]
        if all(set(v) <= set("-: ") for v in values):
            continue  # die Trennzeile
        rows.append(dict(zip(EVALUATION_HEAD, values + [""] * (len(EVALUATION_HEAD) - len(values)))))
    return rows


def solutioning(repo):
    """Ob project.yml das Add-on `solutioning` führt; None, wenn die Datei fehlt oder nicht lesbar ist."""
    try:
        add_ons = repo_objects.read_yaml((Path(repo) / "project.yml").read_text(encoding="utf-8")).get("add_ons")
    except (OSError, repo_objects.ObjectError):
        return None
    return "solutioning" in (add_ons if isinstance(add_ons, list) else [add_ons])


def check_effort_estimates(repo, objects):
    out, sold = [], solutioning(repo)
    for r in objects["requirements"]:
        if "head" not in r:
            continue
        v = r["head"].get("effort_estimate_model", "")
        if not isinstance(v, str) or (v and not HOURS.match(v)):
            out.append(("effort_estimate", r["key"], f"effort_estimate_model: „{v}“ ist weder leer noch eine "
                                                     f"Stundenzahl mit Dezimalpunkt (§357)"))
        elif v and sold is False:
            out.append(("effort_estimate", r["key"], "effort_estimate_model ist gesetzt, aber project.yml führt "
                                                     "das Add-on solutioning nicht (§357)"))
        elif v and r["head"].get("solution_status") != "decided":
            out.append(("effort_estimate", r["key"], f"effort_estimate_model ist gesetzt, aber die Lösung ist "
                                                     f"„{r['head'].get('solution_status', '')}“, nicht decided (§357)"))
    return out


def check_app_evaluation(objects):
    out = []
    adrs = {d["key"]: d for d in objects["decisions"] if "head" in d}
    blocking = set()
    for g in objects["gaps"]:
        if "head" in g and g["head"].get("status") == "open" and str(g["head"].get("blocking")) == "yes":
            concerns = g["head"].get("concerns") or []
            blocking.update([concerns] if isinstance(concerns, str) else concerns)
    for r in objects["requirements"]:
        if "head" not in r:
            continue
        h = r["head"]
        classes = h.get("classification") or []
        classes = [classes] if isinstance(classes, str) else classes
        state = h.get("solution_status")
        if "app" not in classes or state not in ("proposed", "decided", "blocked"):
            continue
        deps = h.get("depends_on") or []
        deps = [deps] if isinstance(deps, str) else deps
        evaluated = [(adrs[d], evaluation_rows(adrs[d])) for d in deps if d in adrs]
        evaluated = [(a, rows) for a, rows in evaluated if rows is not None]
        if not evaluated:
            if state == "decided":
                out.append(("app_evaluation", r["key"], "Public App ohne ADR mit `## Evaluation` in "
                                                        "`depends_on`: Kandidaten und Muss-Kriterien fehlen (§320)"))
            continue
        adr, rows = evaluated[0]
        where = f"{r['key']} {adr['key']}"
        adr_status = adr["head"].get("status")
        if state == "decided" and adr_status != "accepted":
            out.append(("app_evaluation", where, f"Anforderung decided, ADR {adr_status}: mit der Wahl steht "
                                                 f"sie auf accepted"))
        if state == "proposed" and adr_status != "proposed":
            out.append(("app_evaluation", where, f"Wahl offen, ADR {adr_status}: vor der Wahl steht sie auf "
                                                 f"proposed"))
        if isinstance(rows, str):
            out.append(("app_evaluation", where, rows))
            continue
        for row in rows:
            if row["Result"] not in RESULTS or row["Level"] not in LEVELS or not row["Source"] \
                    or not ISO_DATE.match(row["Date"]) or not row["Candidate"] or not row["Criterion"]:
                out.append(("app_evaluation", where, f"Zeile „{row['Candidate']} | {row['Criterion']}“: "
                                                     f"Result {'|'.join(RESULTS)}, Level {'|'.join(LEVELS)}, "
                                                     f"Source nicht leer, Date JJJJ-MM-TT"))
            elif row["Level"] == "assumption" and row["Result"] != "unproven":
                out.append(("app_evaluation", where, f"Zeile „{row['Candidate']} | {row['Criterion']}“: "
                                                     f"eine Annahme belegt nichts, Result ist unproven"))
        candidates = {row["Candidate"] for row in rows}
        if len(candidates) < 2:
            out.append(("app_evaluation", where, f"{len(candidates)} Kandidat(en), verlangt sind mindestens "
                                                 f"zwei mit Namen (§320)"))
        options = OPTION.findall(repo_objects.sections(r["body"]).get("Approach", ""))
        chosen = options[0] if options else ""
        if chosen not in candidates:
            out.append(("app_evaluation", where, f"der erste Lösungsansatz „{chosen}“ unter `## Approach` steht nicht "
                                                 f"als Kandidat in der Tabelle"))
            continue
        mine = [row for row in rows if row["Candidate"] == chosen]
        failed = [row["Criterion"] for row in mine if row["Result"] == "not_met"]
        if failed:
            out.append(("app_evaluation", where, f"„{chosen}“ erfüllt nicht: {'; '.join(failed)}; ein Lösungsansatz, "
                                                 f"der ein Muss-Kriterium nicht deckt, ist keiner"))
        open_ = [row["Criterion"] for row in mine if row["Result"] == "unproven"]
        if open_ and (state != "blocked" or adr_status != "proposed"
                      or r["key"] not in blocking):
            out.append(("app_evaluation", where, f"„{chosen}“ unbelegt: {'; '.join(open_)}; dann ist die "
                                                 f"Anforderung blocked, die ADR proposed, und eine offene Frage "
                                                 f"mit blocking: yes betrifft sie (§320)"))
    return out


def check_wow(repo, objects):
    if any("error" in o for o in objects["way_of_working"]):
        return []  # das meldet object
    readme = load("project-readme")
    if not (Path(repo) / readme.STANDARD).is_file():
        return [("wow", readme.STANDARD, "fehlt; ohne den Standard des Templates gibt es keine Projektion "
                                         "von way-of-working.md, project-upgrade bringt ihn (§286)")]
    try:
        text = readme.render_wow(repo, objects)
    except readme.Refused as e:
        return [("wow", "way-of-working/", str(e).split(" ", 1)[1])]
    path = Path(repo) / readme.WOW
    if not path.is_file() or path.read_text(encoding="utf-8") != text:
        return [("wow", readme.WOW, "ist nicht die Projektion aus dem Standard und way-of-working/; "
                                    "eine Abweichung gehört als Datei ins Abweichungsprotokoll (§286)")]
    return []


def main(argv):
    checks, repo, i = [], None, 0
    while i < len(argv):
        if argv[i] == "--check":
            if i + 1 >= len(argv) or argv[i + 1] not in CHECKS:
                print(f"Aufruf: --check braucht eine von {', '.join(CHECKS)}", file=sys.stderr)
                return 2
            checks.append(argv[i + 1])
            i += 2
        elif argv[i].startswith("-") or repo is not None:
            print("Aufruf: check-repo.py <repo> [--check NAME]...", file=sys.stderr)
            return 2
        else:
            repo = Path(argv[i])
            i += 1
    if repo is None or not repo.is_dir():
        print("Aufruf: check-repo.py <repo> [--check NAME]...", file=sys.stderr)
        return 2
    checks = checks or list(CHECKS)
    objects = repo_objects.load(repo)
    sheet = load("check-sheet")
    found = []
    runs = {"object": lambda: check_objects(objects), "value": lambda: check_values(objects, sheet),
            "epic": lambda: check_epics(objects), "gap_target": lambda: check_gaps(objects),
            "task_done": lambda: check_task_done(objects),
            "gap_question": lambda: check_gap_questions(objects),
            "gap_jargon": lambda: check_gap_jargon(objects),
            "depends_on": lambda: check_depends_on(objects),
            "shops": lambda: check_shops(repo, objects),
            "architecture": lambda: check_architecture(repo),
            "page_type": lambda: check_page_types(objects), "sections": lambda: check_sections(objects),
            "effort_estimate": lambda: check_effort_estimates(repo, objects),
            "wow": lambda: check_wow(repo, objects),
            "app_evaluation": lambda: check_app_evaluation(objects)}
    for c in CHECKS:
        if c in checks:
            found += runs[c]()
    for check, where, sentence in found:
        print(f"{check} {where} {sentence}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
