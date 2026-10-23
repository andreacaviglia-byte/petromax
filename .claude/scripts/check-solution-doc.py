#!/usr/bin/env python3
"""Rechnet Schätzdokument und Proposal eines Vorhabens aus dem Gelesenen und prüft die Eingaben (§212, §220, §355).

Aufruf:
  check-solution-doc.py positions <ordner>
  check-solution-doc.py estimate <ordner>
  check-solution-doc.py proposal <ordner>
  check-solution-doc.py layout
  check-solution-doc.py footer <estimate|proposal> <ordner> <footerId>
  check-solution-doc.py readback <estimate|proposal> <ordner> <rücklesung>
  check-solution-doc.py font <read_doc-antwort>

<ordner> ist der Temp-Ordner des Laufs mit den Dateien, die der Skill aus seinen Lesungen schreibt;
was er je Dokument trägt, steht unten (Proposal) und im Abschnitt „Schätzdokument“.

Ausgabe: das Dokument als HTML mit Inline-Stilen auf stdout, Exit 0; der Lauf legt daraus mit
`create_file` und `text/html` ein Google-Doc an (§248). Verletzt eine Eingabe den Vertrag, steht je
Befund eine Zeile `<prüfung> <detail>` da, Exit 1, und es entsteht kein Dokument. Eine Lücke im Stand
(keine Stunden, keine Seite, keine Größe) ist kein Befund: sie steht im Dokument.

Hinweise zum Lauf stehen in keinem der beiden Dokumente (§264): oben steht nur „Stand: ‹Datum der
Lesezeit›“, und kein fester Satz nennt einen Skill; eine Lücke sagt, was fehlt und was als Nächstes
zu tun ist, in Worten für Menschen. Der Stand, aus dem ein Dokument gerechnet ist, steht auf stderr
in der Zeile `STAND`; der Lauf nennt sie im Bericht und schreibt sie in den Rumpf seines Commits.

Die Stile stehen an einer Stelle (STYLE). Inline, weil ein `<style>`-Block beim Anlegen die Schrift
verliert (gemessen am 04.10.2026: Arial statt Poppins). Oben steht die Strix-Wortmarke als `<img>`
mit der PNG aus .claude/assets/ als data-URI; eine Bild-Adresse im Netz braucht es dafür nicht. Text
aus den Daten wird maskiert; `html_markup` lehnt ein Dokument ab, das ein Element, ein Attribut oder
einen Stil trägt, den das Script nicht selbst setzt, auch ein anderes Bild als die Wortmarke.

`layout` gibt die `requests` des ersten `update_doc` aus: A4, Ränder, eine leere Fußzeile; die
Antwort trägt die `footerId`. `footer` gibt die `requests` des zweiten aus: den Text der Fußzeile und
seinen Stil, mit der Länge in UTF-16 als `endIndex`. `readback` bringt das Dokument und die Rücklesung
von `read_file_content` (als Text oder als JSON-Antwort) auf eine gemeinsame Form und vergleicht sie
Zeile für Zeile; Exit 0 mit `GLEICH`, sonst `readback` mit der ersten abweichenden Zeile.

`font` gibt die `requests` des dritten `update_doc` aus: Poppins auf den ganzen Text des Body, aus dem
Ende des Body in der Antwort von `read_doc`, und danach die Fettung, wo sie vorher stand. Das HTML
trägt die Schrift an jedem Element, und doch kam das Schätzdokument vom 08.10.2026 (rund 130 KB HTML)
in Arial an, das Proposal desselben Stands in Poppins; Größe und Farbe kamen in beiden an. Der Import
verliert die Schrift also bei manchen Docs, und das Script setzt sie danach über die API. Auf stderr
steht `SCHRIFT`: wie viele Textläufe vorher nicht in Poppins waren und wie viele Abschnitte fett.

Die Stunden kommen aus `Aufwand (h)` je Anforderung im Tab Solutioning (§280 Regel 10); sie setzt
ein Mensch. Das Script schätzt keine Stunde und leitet keine aus einer Größe ab. Fehlen Stunden, heißt
die Gesamtzeile „unvollständig" (keine Stunde: „offen"). Stunden nennt nur das Schätzdokument; das
Proposal nennt keine (§355).

Das Schätzdokument gliedert den Aufwand in Positionen, in fester Folge (§355): Shop-Setup
(Lösungsansatz `shop`), Erweiterte Shop-Features (`app`), UX/UI (das Design-Epic, `theme_native`,
`theme`), Custom-Erweiterungen (`custom_app`), Schnittstellen (`integration_*`), Daten-Migration und
Content-Migration (die Epics dieser Domänen). Die Domänen `design`, `data_migration` und
`content_migration` gehen vor dem Lösungsansatz; trägt eine Anforderung zwei, zählt die erste, außer eine Schnittstelle (`integration_*`), die immer zu Schnittstellen zählt. Eine
Position ohne Anforderung entfällt. Eine gezählte Anforderung, die noch keinen Lösungsansatz
trägt (`classification` leer) und die über ihre Domäne zu keiner Position gehört, steht in der letzten Position
„Lösungsansatz offen“, mit ihren Stunden. `positions <ordner>` gibt je Position ihre Stunden und Anforderungen aus (`POSITION`), aus
denen der Lauf die Bullets in Kundensprache fasst; `bullets.json` trägt sie je Position, und `bullet`
lehnt eine Position ohne Bullet, einen Schlüssel ohne Position und einen Bullet mit Stunden,
„Aufschlag“, „Budget“, einer Kennung oder Werkzeugsprache ab. Darunter folgen „Summe Umsetzung“, je
Satz aus dem Aufruf seine Zeile mit Grund und Prozent auf die Summe der Umsetzung (§258), die
Zusatzpositionen und das Gesamt. Grund und Name tragen weder „Aufschlag“ noch „Budget“ noch ein
Prozentzeichen (`effort_row`).

Ein Budget kennt das Schätzdokument nicht (§355): den Abgleich mit dem verkauften Budget machen PM
oder Sponsor außerhalb der Strecke. Trägt `meta.json` ein Budget, lehnt `budget` ab, beim Proposal
ebenso.

Das Proposal rechnet aus dem Projekt-Repo (§280). Sein <ordner> trägt:

  meta.json          `repo` (der Pfad des Projekt-Repos), `commit` (sein Stand, `git rev-parse
                     --short HEAD`), `read_at` (die Lesezeit des Sheets); keine Angaben zum Aufwand
  epics.json         die Tabs Epics und Offene Punkte (`Open items`), je die Antwort von `get_values`
  offene-punkte.json über den ganzen Tab, wie für die Projektion gelesen; das Script nimmt daraus nur
                     die Spalten der Menschen (§280 Regel 5): `Geprüft von` und `Geprüft am` je Epic
                     (§277), `Bis` je Frage
  assumed.json       optional: je offene Kundenfrage, die ein Epic schon als Annahme führt, `epic` und
                     `quote` (§241)

Aus dem Repo liest es project.yml (customer, title, language, shops), requirements/, epics/, gaps/ und
decisions/. Ins Proposal kommen nur geprüfte Epics mit Zielen und Annahmen aus dem Rumpf ihrer Datei;
die übrigen stehen in der Tabelle Scope als „in Arbeit“. Bei einem Seitentyp im Theme-Epic steht unter den Annahmen die
Annahme zu den eigenen Sections (`own_sections`, §285). „Nicht im Scope“ nennt die Anforderungen mit
`status: rejected` oder `scope: out_of_scope`, mit ihrer Priorität, Must-have zuerst (§327), und dem
Satz `Entscheidung:` ihrer jüngsten gültigen ADR als Grund; „Vor Beauftragung zu klären“ die offenen Fragen in gaps/ an den Kunden (§279), mit
`Bis` aus dem Sheet. Auf stderr steht `STAND` mit Lesezeit, Stand des Repos, geprüften Epics und
Epics in Arbeit.

Das Proposal nennt keine Aufwände (§355): keine Stunden, keine Tabelle zum Aufwand, keine Zeilen für
Projektmanagement und Testing, kein Gesamt. Die Epics stehen gruppiert nach Domäne, in der Folge der
festen Liste in check-sheet.py (§252, §295). Trägt `meta.json` Angaben zum Aufwand (`surcharges`,
`extras`), lehnt `meta` ab, ein Budget `budget`; steht im Text für den Kunden eine Stundenangabe oder
„Aufschlag“, lehnt `effort` ab, „Budget“ `budget`, je mit der Datei, aus der der Text kam. Ein
gezähltes Epic ohne Domäne der Liste lehnt `domain` ab; die Domäne setzt `epic-structure`.

Wo das Proposal eine Stelle des Epics nennt (Goals, Assumptions, Status in Blueprint), nennt es sie
mit der Bezeichnung in seiner Sprache, aus der Tabelle in docs/draft-and-epic-page-contract.md über
page_labels.py (§255).

Das Proposal hat keinen Abschnitt „Offene Fragen" (§241). Eine offene Frage, deren Adressat mit `Kunde`
(`Customer`) beginnt, steht am Ende unter „Vor Beauftragung zu klären", blockierende zuerst; leer fehlt
der Abschnitt. Führt ein geprüftes Epic sie schon als Annahme, trägt assumed.json sie mit dem Epic und
dem Wortlaut der Annahme als Fundstelle (`quote`); dann steht sie nur als diese Annahme da. Die Zahl
der offenen Kundenfragen steht auf stderr als `KUNDENFRAGEN`. Der Grund einer Ausklammerung geht ohne
die ADR-Kennung an seinem Ende hinein. `internal_source` nennt die Datei im Repo, aus der der
gesperrte Text kam.
"""
import base64
import csv
import html
import importlib.util
import json
import re
import string
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_labels  # noqa: E402  Die Bezeichnungen von Seite und Entwurf, aus dem Vertrag (§255)


# --- Die Stile, an einer Stelle (§248) --------------------------------------------
FONT = "Poppins"           # nur der Name: eine Fallback-Liste trägt nicht (gemessen am 04.10.2026)
TEXT = "#030813"
YELLOW = "#FFDB32"         # Tabellenköpfe, Hervorhebung
RULE = "#DDDDD9"           # Rahmen der Zellen
LINK = "#3540F8"
FOOT = "#595959"           # Fußzeile, 8 pt
# Die Wortmarke: 110 × 35 px kommen im Doc als Bild mit 82,5 × 26,25 pt an, der Abstand unten am Absatz
# als spaceBelow 18 pt, der Schutzraum (gemessen am 04.10.2026).
WORDMARK = Path(__file__).resolve().parent.parent / "assets" / "strix-wordmark.png"
WORDMARK_SIZE = ("110", "35")
_F = f"font-family:'{FONT}';color:{TEXT}"
_CELL = f"{_F};font-size:9pt;border:1px solid {RULE};padding:4pt"
# Die Abstände (gemessen am 08.10.2026): margin-bottom kommt im Doc als spaceBelow in derselben Größe an,
# margin-top an einer Überschrift nach einem Absatz dagegen als spaceBelow dieses Absatzes. Der Abstand
# über der Überschrift ist darum padding-top bei margin-top:0; er kommt als spaceAbove an, und der Absatz
# davor behält spaceBelow 0. Das zählt direkt unter einer Tabelle: dort zeigt das Doc den spaceAbove
# eines Absatzes nur, solange sein spaceBelow 0 ist. margin an <table> fällt weg, den Abstand zur
# Tabelle trägt der Absatz davor oder danach; border-bottom unter einer Überschrift wird ein eigener
# Absatz mit einer grauen Linie.
STYLE = {
    "wordmark": "margin:0 0 18pt 0",
    # 600 wird im Doc fett, letter-spacing fällt weg (gemessen am 04.10.2026); also gleich 700, ohne Sperrung
    "eyebrow": f"{_F};font-size:9pt;font-weight:700",
    "h1": f"{_F};font-size:22pt;font-weight:700",
    "h2": f"{_F};font-size:14pt;font-weight:700;margin-top:0;padding-top:22pt;margin-bottom:10pt",
    "h3": f"{_F};font-size:11pt;font-weight:700;margin-top:0;padding-top:16pt;margin-bottom:6pt",
    "h4": f"{_F};font-size:10pt;font-weight:700;margin-top:0;padding-top:12pt;margin-bottom:4pt",
    "p": f"{_F};font-size:10pt",
    "p_before_table": f"{_F};font-size:10pt;margin-bottom:10pt",
    "p_after_table": f"{_F};font-size:10pt;margin-top:12pt",
    "li": f"{_F};font-size:10pt",
    "table": "border-collapse:collapse",
    "td": _CELL,
    "th": f"{_CELL};font-weight:700;background-color:{YELLOW}",
    "a": f"color:{LINK}",
    "mark": f"background-color:{YELLOW}",
}
PAGE = [  # das erste update_doc, so angenommen am 04.10.2026; die Antwort trägt die footerId
    {"updateDocumentStyle": {"documentStyle": {
        "pageSize": {"width": {"magnitude": 595.28, "unit": "PT"}, "height": {"magnitude": 841.89, "unit": "PT"}},
        "marginLeft": {"magnitude": 56.7, "unit": "PT"}, "marginRight": {"magnitude": 56.7, "unit": "PT"}},
        "fields": "pageSize,marginLeft,marginRight"}},
    {"createFooter": {"type": "DEFAULT"}},
]
FOOTER_SIZE = 8
# Die Spaltenbreiten in pt, je Tabelle des Scripts. Das Doc nimmt `width` an der Zelle als Verhältnis und
# setzt die Tabelle auf 468 pt, die Satzbreite von US Letter; nach A4 mit 56,7 pt Rand bleiben 481,9 pt
# (gemessen am 08.10.2026). Schmale Spalten für Kennungen und Zahlen, die Breite für den Text.
WIDTHS = {
    "meta": (130, 338), "scope": (52, 140, 96, 78, 102), "two": (288, 180),
    "out": (70, 52, 150, 196), "out_priority": (70, 52, 130, 76, 140), "domains": (130, 218, 120), "overview": (52, 140, 96, 60, 120),
    "section": (58, 150, 42, 56, 82, 80),
}
TABLE_WIDTHS = re.compile(r"^\x00widths ([\d,]+)$")

SIZES = ("S", "M", "L", "XL")
READ_AT = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d)Z$")
PAGE_LABELS = page_labels.labels()
QUESTIONS_HEAD = re.compile(r"^#{1,6}[ \t]*(Offene Fragen|Open questions)[ \t]*$", re.I | re.M)
INTERNAL = re.compile(r"docs\.google\.com|drive\.google\.com|sheets\.google\.com|\bADR-\d{3}\b"
                      r"|(?<![\w/.-])(?:inputs|notes|decisions|gaps|todo|scope)/")

# Was im Grund eines Satzes auf die Umsetzung oder im Namen einer Zusatzposition nicht stehen darf: beide
# sind der Name der Tätigkeit, der Satz steht im Feld daneben (§355).
EFFORT_WORDS = re.compile(r"aufschl[aä]g|surcharge|budget|%", re.I)
# Was der Kunde im Proposal nicht liest und ein Bullet der Schätzung nicht trägt (§355): eine
# Stundenangabe, „Aufschlag“, „Budget“. Am Wortanfang, damit „Versandaufschlag“ nicht anschlägt.
HOURS_TEXT = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:h|Std|Stunden|hours?)\b", re.I)
SURCHARGE_TEXT = re.compile(r"\b(?:aufschl[aä]g\w*|surcharges?)\b", re.I)
BUDGET_TEXT = re.compile(r"\bbudget\w*", re.I)
LABELS = {
    "de": {
        "internal": "Intern — nicht für den Kunden.",
        "stand": "Stand: {date}",
        "overview": "Übersicht", "epic": "Epic", "title": "Titel",
        "note": "Hinweis", "total": "Gesamt", "position": "Position",
        "h": "Stunden", "sum_epics": "Summe der Epics", "sum_impl": "Summe Umsetzung",
        "surcharge": "{r}, {p} %", "extra": "Zusatzposition {n}",
        "no_surcharge": "Projektmanagement und Testing: kein Satz angegeben, nicht eingerechnet.",
        "no_extra": "Zusatzpositionen: keine.",
        "req": "REQ", "size": "Größe",
        "open": "Offen", "gaps": "Lücken",
        "gap_noepic": "Anforderungen im Umfang, noch keinem Epic zugeordnet: {ids}; nächster Schritt: einem Epic zuordnen",
        "partial": "unvollständig, {n} Epic(s) ohne Stunden",
        "no_size_1": "1 Anforderung ohne Größe", "no_size_n": "{n} Anforderungen ohne Größe",
        "merged": "zusammengeführt, zählt nicht", "dissolved": "aufgelöst, zählt nicht",
        "out": "{n} Anforderung(en) außerhalb des Umfangs zählen nicht.",
        "shops": "Shops",
        "scope": "Scope", "epic_page": "Epic Page", "in_work": "in Arbeit",
        "sections_assumed": "{i} {t}: bis zu {n} eigene Sections",
        "draft_cell": "Entwurf, nicht freigegeben", "open_h": "offen",
        "goals": "$goals", "assumptions": "$assumptions", "status_head": "$status_head",
        "empty": "Noch nicht beschrieben.", "not_in_scope": "Nicht im Scope",
        "requirement": "Anforderung", "reason": "Grund", "before_order": "Vor Beauftragung zu klären",
        "priority": "Priorität",
        "blocking_mark": "Blockierend", "due_by": "bis {d}", "blockers": "Blocker", "blocked_by": "Blockiert durch", "internal_clarification": "in interner Klärung",
        "eyebrow_estimate": "AUFWANDSSCHÄTZUNG", "eyebrow_proposal": "SOLUTION PROPOSAL",
        "meta_version": "Version", "meta_date": "Datum", "meta_by": "Erstellt von", "meta_review": "Reviewed von",
        "foot_estimate": "Aufwandsschätzung", "foot_proposal": "Solution Proposal",
        "conf_estimate": "intern", "conf_proposal": "vertraulich",
        "domain": "Domäne", "epics": "Epics",
    },
    "en": {
        "internal": "Internal — not for the customer.",
        "stand": "As of: {date}",
        "overview": "Overview", "epic": "Epic", "title": "Title",
        "note": "Note", "total": "Total", "position": "Item",
        "h": "Hours", "sum_epics": "Sum of epics", "sum_impl": "Implementation subtotal",
        "surcharge": "{r}, {p} %", "extra": "Additional item {n}",
        "no_surcharge": "Project management and testing: no rate given, not included.",
        "no_extra": "Additional items: none.",
        "req": "REQ", "size": "Size",
        "open": "Open", "gaps": "Gaps",
        "gap_noepic": "Requirements in scope, not yet assigned to an epic: {ids}; next step: assign them to an epic",
        "partial": "incomplete, {n} epic(s) without hours",
        "no_size_1": "1 requirement without size", "no_size_n": "{n} requirements without size",
        "merged": "merged, not counted", "dissolved": "dissolved, not counted",
        "out": "{n} requirement(s) out of scope are not counted.",
        "shops": "Shops",
        "scope": "Scope", "epic_page": "Epic Page", "in_work": "in progress",
        "sections_assumed": "{i} {t}: up to {n} custom sections",
        "draft_cell": "draft, not approved", "open_h": "open",
        "goals": "$goals", "assumptions": "$assumptions", "status_head": "$status_head",
        "empty": "Not yet described.", "not_in_scope": "Out of scope",
        "requirement": "Requirement", "reason": "Reason", "before_order": "To be clarified before the order",
        "priority": "Priority",
        "blocking_mark": "Blocking", "due_by": "due {d}", "blockers": "Blockers", "blocked_by": "Blocked by", "internal_clarification": "under internal clarification",
        "eyebrow_estimate": "EFFORT ESTIMATE", "eyebrow_proposal": "SOLUTION PROPOSAL",
        "meta_version": "Version", "meta_date": "Date", "meta_by": "Created by", "meta_review": "Reviewed by",
        "foot_estimate": "Effort estimate", "foot_proposal": "Solution Proposal",
        "conf_estimate": "internal", "conf_proposal": "confidential",
        "domain": "Domain", "epics": "Epics",
    },
}


def _page_terms():
    """Setzt die Bezeichnungen der Seite in LABELS ein, je Sprache aus dem Vertrag von Entwurf und Epic Page (§255): das Dokument
    zitiert Abschnitte und Kopfzeilen so, wie sie im Epic seiner Sprache heißen."""
    for lang, labels in LABELS.items():
        P = PAGE_LABELS[lang]
        terms = {"goals": P["section_goals"], "assumptions": P["section_assumptions"],
                 "status_head": P["head_status"]}
        for key, text in labels.items():
            labels[key] = string.Template(text).safe_substitute(terms)


_page_terms()


class Refused(Exception):
    """Ein Befund gegen den Vertrag; die erste Zeile ist `<prüfung> <detail>`."""


# --- Lesen ----------------------------------------------------------------------

def value_ranges(node):
    if isinstance(node, dict):
        if isinstance(node.get("valueRanges"), list):
            return node["valueRanges"]
        for v in node.values():
            found = value_ranges(v)
            if found is not None:
                return found
    if isinstance(node, list):
        for v in node:
            found = value_ranges(v)
            if found is not None:
                return found
    return None


def rows_from_json(data):
    """Eine Liste von Zeilen, oder die Bereiche einer BATCH_GET-Antwort nebeneinandergelegt."""
    ranges = value_ranges(data) if isinstance(data, dict) else None
    if ranges is None:
        return [[str(c) for c in r] for r in data]
    blocks = [r.get("values", []) for r in ranges]
    width = [len(b[0]) if b else 0 for b in blocks]
    height = max((len(b) for b in blocks), default=0)
    rows = []
    for i in range(height):
        row = []
        for b, w in zip(blocks, width):
            part = [str(c) for c in (b[i] if i < len(b) else [])]
            row += part + [""] * (w - len(part))
        rows.append(row)
    return rows


def read_json(folder, name):
    path = folder / name
    if not path.is_file():
        raise Refused(f"input {name} fehlt")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        raise Refused(f"input {name} nicht lesbar: {e}")


def number(text):
    t = str(text).strip().replace(" ", "").replace(" ", "")
    if re.fullmatch(r"\d+(?:[.,]\d+)?", t):
        return float(t.replace(",", "."))
    return None


def fmt(x, lang):
    """Eine Zahl mit Tausendertrennung: 60.000 und 12,5 deutsch, 60,000 und 12.5 englisch."""
    if x is None:
        return ""
    s = f"{x:,.1f}".rstrip("0").rstrip(".") if x != int(x) else f"{int(x):,}"
    return s.translate(str.maketrans(",.", ".,")) if lang == "de" else s


def cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


ADR_TAIL = re.compile(r"[,;]?\s*ADR-\d{3}(?:\s*[,;]\s*ADR-\d{3})*\s*$")


ADR_DECISION = re.compile(r"^\s*(?:Entscheidung|Decision):\s*(.*\S)\s*$", re.M)
ADR_CONCERNS = re.compile(r"^\s*(?:Betrifft|Concerns):\s*(.*\S)\s*$", re.M)


def reason(adr_body):
    """Der Grund einer Ausklammerung: der Satz `Entscheidung:` ihrer ADR (docs/datalayer-contract.md, Die ADR),
    ohne eine ADR-Kennung am Ende; die Kennung verweist ins Repo, das der Kunde nicht liest."""
    m = ADR_DECISION.search(adr_body)
    return ADR_TAIL.sub("", m.group(1)).strip() if m else ""


CUSTOMER = re.compile(r"^\s*(?:kunde|customer)", re.I)


def to_customer(addressee):
    """Eine Frage geht ins Proposal nur, wenn sie an den Kunden gerichtet ist: der Adressat beginnt mit
    `Kunde`, auch „Kunde und Dienstleister“ oder „Kunde, Logistik“. Sie steht dann unter „Vor Beauftragung
    zu klären“ oder, wenn die Seite sie als Annahme führt, nur als diese Annahme (§241)."""
    return bool(CUSTOMER.match(addressee))


def norm(text):
    return " ".join(str(text).split())


def assumed_questions(assumed, shown, open_customer):
    """Die offenen Kundenfragen, die ein geprüftes Epic schon als Annahme führt (§241). Ob das so ist,
    entscheidet der Lauf; er trägt sie in assumed.json ein, je Frage ihre GAP-ID mit `epic` und `quote`
    (die Annahme, wörtlich aus Assumptions and delimitations dieses Epics). Geprüft wird, dass das Epic
    mit seinen Annahmen im Proposal steht, die Fundstelle dort steht und die Frage offen und an den
    Kunden ist. `shown` trägt je gezeigtem Epic seine Annahmen aus der Datei."""
    if not isinstance(assumed, dict):
        raise Refused("assumed assumed.json ist kein Objekt je GAP-ID")
    covered = set()
    for gid, a in assumed.items():
        if not isinstance(a, dict) or not norm(a.get("epic", "")):
            raise Refused(f"assumed {gid}: Eintrag {a!r} braucht epic und quote")
        eid, quote = norm(a["epic"]), norm(a.get("quote", ""))
        if gid not in open_customer:
            raise Refused(f"assumed {gid}: keine offene Kundenfrage dieser Kennung in gaps/")
        if eid not in shown:
            raise Refused(f"assumed {gid}: {eid} steht nicht mit seinen Annahmen im Proposal; "
                          f"seine Annahme deckt keine Frage")
        if not quote:
            raise Refused(f"assumed {gid}: ausgenommene Frage ohne Fundstelle; `quote` trägt die Annahme "
                          f"wörtlich aus Assumptions and delimitations von {eid}")
        if quote not in norm(shown[eid]):
            raise Refused(f"assumed {gid}: die Fundstelle „{quote}“ steht nicht unter Assumptions and "
                          f"delimitations von {eid}")
        covered.add(gid)
    return covered


MONTHS_EN = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
DATE_DE = re.compile(r"^\s*(\d{1,2})\.(\d{1,2})\.(\d{4})\s*$")
DATE_ISO = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})")


def date_text(y, m, d, lang):
    """Ein Datum in der Form der Sprache (§337): `de` 11.10.2026, `en` 11 Oct 2026; dieselbe Form wie
    `date_text` in repo_objects.py, dem Datalayer-Vertrag, Abschnitt „Die festen Wendungen“."""
    y, m, d = int(y), int(m), int(d)
    if not 1 <= m <= 12:
        return None
    return f"{d} {MONTHS_EN[m - 1]} {y}" if lang == "en" else f"{d:02d}.{m:02d}.{y}"


def due_text(value, lang):
    """`Bis` einer Frage, wie ein Mensch es im Sheet schreibt: ein Datum TT.MM.JJJJ oder JJJJ-MM-TT steht
    in der Form der Sprache, jeder andere Text, wie er steht."""
    m = DATE_DE.match(str(value))
    if m:
        return date_text(m[3], m[2], m[1], lang) or str(value).strip()
    m = DATE_ISO.match(str(value))
    if m:
        return date_text(m[1], m[2], m[3], lang) or str(value).strip()
    return str(value).strip()


def question_line(i, q, L, lang="de"):
    """Eine Zeile unter „Vor Beauftragung zu klären“: kurz, blockierende markiert; der Adressat, wie
    `to` ihn nennt, die Frist in der Form der Sprache."""
    mark = f"**{L['blocking_mark']}:** " if q["blocking"] else ""
    tail = ", ".join(x for x in (i, q["addressee"], L["due_by"].format(d=due_text(q["due"], lang))
                                 if q["due"] else "") if x)
    return f"- {mark}{q['question']} ({tail})"


def ids(text):
    return [i for i in re.split(r"[\s,;]+", str(text)) if i]


# --- Stand --------------------------------------------------------------------

def additions(meta):
    """Die Angaben aus dem Aufruf der Schätzung: Sätze auf die Umsetzung (§258) und Zusatzpositionen. Ein
    Budget nimmt die Schätzung nicht an (§355)."""
    out = {"surcharges": [], "extras": []}
    if "budget" in meta:
        raise Refused("budget meta.json trägt ein Budget; das Schätzdokument kennt kein Budget (§355), "
                      "nimm `budget` aus meta.json")
    for s in meta.get("surcharges") or []:
        p = number(s.get("percent", ""))
        if p is None or not str(s.get("reason", "")).strip():
            raise Refused(f"surcharge {s!r}: braucht Grund und Prozent als Zahl")
        out["surcharges"].append((effort_name(s["reason"], "Grund"), p))
    for x in meta.get("extras") or []:
        h = number(x.get("hours", ""))
        if h is None or not str(x.get("name", "")).strip():
            raise Refused(f"extra {x!r}: braucht Namen und Stunden als Zahl")
        out["extras"].append((effort_name(x["name"], "Name"), h))
    return out


def effort_name(text, what):
    """Grund oder Name einer Zeile der Schätzung (§355): der Name der Tätigkeit, ohne „Aufschlag“,
    Prozent und Budget; der Prozentsatz steht im Feld daneben."""
    name = norm(text)
    hit = EFFORT_WORDS.search(name)
    if hit:
        raise Refused(f"effort_row „{name}“: der {what} trägt „{hit.group(0)}“; er ist der Name der Tätigkeit, "
                      f"ohne Aufschlag, Prozent und Budget (§355), etwa „Projektmanagement“")
    return name


def stand_date(meta, L):
    """Die Zeile oben im Dokument: nur das Datum der Lesezeit (§264)."""
    return L["stand"].format(date=meta["read_at_date"])


def by_domain(epics, order):
    """Die gezählten Epics je Domäne, in der Folge der festen Liste (`order`, §252); eine Domäne ohne Epic
    entfällt."""
    counted = [e for e in epics if not e.get("merged")]
    return [(d, [e for e in counted if e["domain"] == d]) for d in order if any(e["domain"] == d for e in counted)]


def domain_name(sheet, domain, lang):
    """Der Anzeigename einer Domäne in der Sprache des Projekts, aus der festen Liste in check-sheet.py."""
    name = sheet.display(sheet.DOMAIN, domain, lang)
    if not name:
        raise Refused(f"domain „{domain}“ hat keinen Anzeigenamen in der festen Liste (§252); die Domäne setzt "
                      f"`epic-structure`")
    return name


def table(head, rows, widths=None):
    """Die Tabelle als Markdown; `widths` (ein Schlüssel von WIDTHS) geht als eigene Zeile davor, die
    nur das Script schreibt: ein Steuerzeichen kommt aus keiner Zelle des Sheets und keiner Seite."""
    out = [f"\x00widths {','.join(map(str, WIDTHS[widths]))}"] if widths else []
    out += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return out


# --- HTML -----------------------------------------------------------------------
# Das Dokument entsteht als Markdown wie bisher und wird hier in HTML mit Inline-Stilen gesetzt. Das
# Markdown ist die Form, in der Goals und Assumptions von der Seite kommen; die Umsetzung kennt genau,
# was Script und Seite schreiben: Überschriften, Absätze, Listen, Tabellen, fett, kursiv, Links.

def esc(text):
    """Text aus den Daten, maskiert. Die eine Stelle, an der Daten ins HTML gehen."""
    return html.escape(str(text), quote=True)


INLINE_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
TABLE_SPLIT = re.compile(r"(?<!\\)\|")
LIST_ITEM = re.compile(r"^(?:([-*+])|(\d+)[.)])\s+(.*)$")
HR = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")


def inline(text):
    t = esc(text)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = INLINE_LINK.sub(lambda m: f'<a href="{m.group(2)}" style="{STYLE["a"]}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<i>\1</i>", t)


def cells(line):
    inner = line.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") and not inner.endswith("\\|") else inner
    return [c.strip().replace("\\|", "|") for c in TABLE_SPLIT.split(inner)]


def cell_style(kind, widths, i):
    """Der Stil einer Zelle, mit ihrer Breite, wenn die Tabelle Breiten trägt und die Spalte eine hat."""
    if widths and i < len(widths):
        return f'{STYLE[kind]};width:{widths[i]}pt'
    return STYLE[kind]


def th(text, widths=None, i=0):
    return f'<td style="{cell_style("th", widths, i)}"><b>{text}</b></td>'


def html_table(rows, head=None, widths=None):
    out = [f'<table style="{STYLE["table"]}">']
    if head is not None:
        out.append("<tr>" + "".join(th(inline(c), widths, i) for i, c in enumerate(head)) + "</tr>")
    out += ["<tr>" + "".join(f'<td style="{cell_style("td", widths, i)}">{inline(c)}</td>' for i, c in enumerate(r))
            + "</tr>" for r in rows]
    return out + ["</table>"]


def meta_table(pairs):
    """Die Meta-Tabelle am Anfang des Proposals: links die Bezeichnung als Kopf, rechts der Wert."""
    w = WIDTHS["meta"]
    return ([f'<table style="{STYLE["table"]}">']
            + [f'<tr>{th(esc(k), w, 0)}<td style="{cell_style("td", w, 1)}">{esc(v)}</td></tr>' for k, v in pairs]
            + ["</table>"])


def md_to_html(text):
    """Je Zeile ein Block: eine Zeile des Scripts ist ein Absatz, auch ohne Leerzeile dazwischen."""
    out, lines, i, widths = [], str(text).split("\n"), 0, None
    while i < len(lines):
        if TABLE_WIDTHS.match(lines[i]):
            widths = [int(w) for w in TABLE_WIDTHS.match(lines[i]).group(1).split(",")]
            i += 1
            continue
        s = lines[i].strip()
        head = re.match(r"^(#{1,6})\s+(.*)$", s)
        item = LIST_ITEM.match(s)
        if not s or HR.match(s):
            pass
        elif head:
            tag = "h" + str(min(len(head.group(1)), 4))
            out.append(f'<{tag} style="{STYLE[tag]}">{inline(head.group(2).strip())}</{tag}>')
        elif s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(cells(lines[i]))
                i += 1
            i -= 1
            sep = len(block) > 1 and all(re.fullmatch(r":?-+:?", c) for c in block[1] if c) and any(block[1])
            out += html_table(block[2:], block[0], widths) if sep else html_table(block, None, widths)
            widths = None
        elif item:
            tag = "ul" if item.group(1) else "ol"
            items = [item.group(3)]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith(("|", "#")):
                nxt = LIST_ITEM.match(lines[i + 1].strip())
                if nxt:
                    items.append(nxt.group(3))
                else:
                    items[-1] += " " + lines[i + 1].strip()
                i += 1
            out.append(f"<{tag}>")
            out += [f'<li style="{STYLE["li"]}">{inline(t)}</li>' for t in items]
            out.append(f"</{tag}>")
        else:
            out.append(f'<p style="{STYLE["p"]}">{inline(s)}</p>')
        i += 1
    return out


def table_spacing(blocks):
    """Ein Absatz direkt vor oder nach einer Tabelle hält den Abstand zu ihr; die Tabelle selbst kann es nicht."""
    out, plain_p = list(blocks), f'<p style="{STYLE["p"]}">'
    for i, block in enumerate(out):
        if not block.startswith(plain_p):
            continue
        after = i > 0 and out[i - 1] == "</table>"
        before = i + 1 < len(out) and out[i + 1].startswith("<table")
        # zwischen zwei Tabellen zählt der Abstand nach oben: mit spaceBelow zeigte das Doc ihn nicht
        kind = "p_after_table" if after else "p_before_table" if before else ""
        if kind:
            out[i] = f'<p style="{STYLE[kind]}">' + block[len(plain_p):]
    return out


def html_page(blocks):
    return "\n".join(['<html><head><meta charset="utf-8"></head><body>'] + table_spacing(blocks)
                     + ["</body></html>"]) + "\n"


def para(text, style="p"):
    return f'<p style="{STYLE[style]}">{esc(text)}</p>'


_WORDMARK_SRC = []


def wordmark_src():
    """Die Wortmarke als data-URI, einmal gelesen."""
    if not _WORDMARK_SRC:
        if not WORDMARK.is_file():
            raise Refused(f"wordmark {WORDMARK.name} fehlt unter .claude/assets/; das Template bringt sie mit")
        _WORDMARK_SRC.append("data:image/png;base64," + base64.b64encode(WORDMARK.read_bytes()).decode("ascii"))
    return _WORDMARK_SRC[0]


def wordmark_attrs():
    w, h = WORDMARK_SIZE
    return {"src": wordmark_src(), "width": w, "height": h, "alt": "Strix"}


def head_blocks(eyebrow, title, customer_line):
    img = "".join(f' {k}="{v}"' for k, v in wordmark_attrs().items())
    return [f'<p style="{STYLE["wordmark"]}"><img{img}></p>', para(eyebrow, "eyebrow"),
            f'<h1 style="{STYLE["h1"]}">{esc(title)}</h1>', para(customer_line)]


ALLOWED = {"html": (), "head": (), "meta": ("charset",), "body": (), "p": ("style",), "h1": ("style",),
           "h2": ("style",), "h3": ("style",), "h4": ("style",), "table": ("style",), "tr": (),
           "td": ("style",), "b": (), "i": (), "a": ("href", "style"), "span": ("style",),
           "ul": (), "ol": (), "li": ("style",), "img": ("src", "width", "height", "alt")}


class Markup(HTMLParser):
    """Liest jedes Element des Dokuments mit seiner Zeile."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []

    def handle_starttag(self, tag, attrs):
        self.found.append((self.getpos()[0], tag, attrs))

    def handle_endtag(self, tag):
        self.found.append((self.getpos()[0], tag, None))


def check_markup(doc):
    """`html_markup`: nur Elemente, Attribute und Stile, die das Script selbst setzt. Was sonst
    dasteht, kam unmaskiert aus den Daten und würde im Doc als Formatierung oder gar nicht erscheinen."""
    m = Markup()
    m.feed(doc)
    m.close()
    styles = set(STYLE.values())
    mark, images = wordmark_attrs(), 0
    for line, tag, attrs in m.found:
        if tag not in ALLOWED:
            raise Refused(f"html_markup Zeile {line}: Element <{tag}> setzt das Script nicht; "
                          f"ein Text aus den Daten ist nicht maskiert")
        if tag == "img" and attrs is not None:
            images += 1
            if images > 1 or dict(attrs) != mark or len(attrs) != len(mark):
                raise Refused(f"html_markup Zeile {line}: ein Bild außer der Wortmarke setzt das Script nicht; "
                              f"ein Text aus den Daten ist nicht maskiert")
            continue
        for name, value in attrs or []:
            sized = re.fullmatch(r"(.*);width:\d+pt", value or "") if tag == "td" else None
            ok = name in ALLOWED[tag] and (
                (name == "style" and (value in styles or (sized and sized.group(1) in (STYLE["td"], STYLE["th"]))))
                or (name == "charset" and value == "utf-8")
                or (name == "href" and re.match(r"https?://", value or "")))
            if not ok:
                raise Refused(f"html_markup Zeile {line}: Attribut {name}=„{value}“ an <{tag}> setzt das "
                              f"Script nicht; ein Text aus den Daten ist nicht maskiert")


def check_customer_text(doc, places, jargon=None):
    """Was der Kunde nicht lesen soll: eine Überschrift „Offene Fragen“ (§241) und interne Quellen. `places`
    trägt je gelesene Stelle, die ins Proposal geht, ihre Datei im Repo und ihren Text."""
    for n, line in enumerate(doc.split("\n"), 1):
        h = re.match(r"^<h[1-6][^>]*>(.*)</h[1-6]>$", line)
        name = html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip() if h else ""
        if h and QUESTIONS_HEAD.match("# " + name):
            raise Refused(f"questions_section Zeile {n}: „{name}“; das Proposal hat keinen Abschnitt für "
                          f"offene Fragen (§241). Sie steht in {source_of(name, places)}")
    hit = INTERNAL.search(doc) or (jargon.search(doc) if jargon else None)
    if hit:
        line = doc[:hit.start()].count("\n") + 1
        raise Refused(f"internal_source Zeile {line}: „{hit.group(0)}“ ist eine interne Quelle; "
                      f"der Kunde liest das Proposal. Sie steht in {source_of(hit.group(0), places)}")


def footer_text(mode, meta):
    L = LABELS[meta["language"]]
    return f"Strix · {L['foot_' + mode]} · {meta['title']} · {L['conf_' + mode]}"


def utf16_len(text):
    return len(text.encode("utf-16-le")) // 2


def footer_requests(mode, meta, footer_id):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", footer_id or ""):
        raise Refused(f"footer_id „{footer_id}“: das ist keine footerId; sie steht in der Antwort des ersten "
                      f"update_doc unter createFooter")
    text = footer_text(mode, meta)
    rgb = {k: round(int(FOOT[i:i + 2], 16) / 255, 4) for k, i in (("red", 1), ("green", 3), ("blue", 5))}
    return [
        {"insertText": {"text": text, "endOfSegmentLocation": {"segmentId": footer_id}}},
        {"updateTextStyle": {"range": {"segmentId": footer_id, "startIndex": 0, "endIndex": utf16_len(text)},
                             "textStyle": {"weightedFontFamily": {"fontFamily": FONT},
                                           "fontSize": {"magnitude": FOOTER_SIZE, "unit": "PT"},
                                           "foregroundColor": {"color": {"rgbColor": rgb}}},
                             "fields": "weightedFontFamily,fontSize,foregroundColor"}},
    ]


def body_of(node):
    """Der Body aus der Antwort von `read_doc`: im ersten Tab, oder direkt, mit oder ohne Hülle `content`."""
    if isinstance(node, dict):
        if isinstance(node.get("tabs"), list) and node["tabs"]:
            return body_of(node["tabs"][0].get("documentTab", {}))
        if isinstance(node.get("body"), dict):
            return node["body"]
        for key in ("content", "document"):
            if isinstance(node.get(key), dict):
                return body_of(node[key])
    return None


def text_runs(content):
    """Die Textläufe des Body mit ihren Indizes und der Absatzvorlage, auch in Tabellenzellen."""
    for el in content:
        if "paragraph" in el:
            named = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
            yield from ((r, named) for r in el["paragraph"].get("elements", []) if "textRun" in r)
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for c in row.get("tableCells", []):
                    yield from text_runs(c.get("content", []))


def font_requests(path):
    """Poppins auf den ganzen Text des Body, von Index 1 bis vor das letzte Absatzende, danach die Fettung,
    wo sie vorher stand. Das Setzen der Schrift nimmt sie mit (gemessen am 08.10.2026): aus fett wurde
    nicht fett, und eine Überschrift, die ihr Fett aus der Vorlage erbte, bekam `bold: false`. Also wird
    fett wieder fett, und in einer Überschrift erbt ein Lauf ohne `bold` es wieder aus der Vorlage.
    Benachbarte Läufe derselben Art gehen in einen Request, auch über Zellgrenzen."""
    try:
        body = body_of(json.loads(Path(path).read_text(encoding="utf-8")))
        end = body["content"][-1]["endIndex"]
    except (OSError, ValueError, TypeError, KeyError, IndexError):
        raise Refused(f"read_doc {path}: keine Antwort von read_doc mit einem Body; die Datei trägt die Antwort "
                      f"auf `read_doc` mit `documentId` = ID aus Schritt 2, als JSON")
    runs = list(text_runs(body["content"]))
    other = sum(1 for r, _ in runs
                if r["textRun"].get("textStyle", {}).get("weightedFontFamily", {}).get("fontFamily") != FONT)
    spans = []  # [start, end, art]; art "bold" oder "inherit", ein Lauf ohne Fett beendet den Abschnitt
    last = None
    for r, named in runs:
        a, b = max(r["startIndex"], 1), min(r["endIndex"], end - 1)
        bold = r["textRun"].get("textStyle", {}).get("bold")
        kind = "bold" if bold else "inherit" if bold is None and named.startswith("HEADING_") else None
        if a < b and kind:
            if last == kind:
                spans[-1][1] = b
            else:
                spans.append([a, b, kind])
        last = kind
    requests = [{"updateTextStyle": {"range": {"startIndex": 1, "endIndex": end - 1},
                                     "textStyle": {"weightedFontFamily": {"fontFamily": FONT}},
                                     "fields": "weightedFontFamily"}}]
    requests += [{"updateTextStyle": {"range": {"startIndex": a, "endIndex": b},
                                      "textStyle": {"bold": True} if kind == "bold" else {}, "fields": "bold"}}
                 for a, b, kind in spans]
    return requests, f"SCHRIFT {other} von {len(runs)} Textläufen nicht in {FONT}, {len(spans)} Abschnitte fett"


# --- Rücklesung -----------------------------------------------------------------
# `read_file_content` gibt ein Doc als Markdown zurück (gemessen am 04.10.2026): Überschriften fett
# umschlossen, die Linie unter Überschrift 2 (bis 08.10.2026 gesetzt) als `-----`, jede Tabelle mit leerer Kopfzeile und der
# eigentlichen Kopfzeile als erster Datenzeile, Markdown-Zeichen in Zellen maskiert. Die Wortmarke
# gibt es nicht zurück, der Text beginnt mit dem Eyebrow (gemessen am 04.10.2026); ihr Absatz trägt
# keinen Text und fällt auf der Seite des Dokuments weg. Beide Seiten
# kommen auf dieselbe Form: eine Zeile je Absatz, Überschrift, Listenpunkt und Tabellenzeile, ohne
# Auszeichnung, Zellen mit „ | “ getrennt; verglichen wird ohne Leerraum.

UNESCAPE = re.compile(r"\\([!-/:-@\[-`{-~])")


def plain(text):
    t = UNESCAPE.sub(r"\1", text)
    t = re.sub(r"\[([^\]]*)\]\(([^)\s]*)\)", r"\1 <\2>", t)
    t = re.sub(r"[*_`]", "", t)
    return " ".join(t.split())


def common_lines(text):
    out = []
    for raw in str(text).replace("\r\n", "\n").split("\n"):
        s = raw.replace("\u00a0", " ").replace("\u200b", "").strip()
        if not s or HR.match(s):
            continue
        if s.startswith("|"):
            row = [plain(c) for c in cells(s)]
            if not any(row) or all(re.fullmatch(r":?-+:?", c) for c in row if c):
                continue
            out.append(" | ".join(row))
            continue
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", s)
        if plain(s):
            out.append(plain(s))
    return out


class Lines(HTMLParser):
    """Das erwartete Dokument als Text: je Block eine Zeile, Links als [Text](Adresse)."""
    BLOCK = {"p", "h1", "h2", "h3", "h4", "li"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.buf, self.row, self.links = [], None, None, []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK or tag == "td":
            self.buf = []
        elif tag == "tr":
            self.row = []
        elif tag == "a" and self.buf is not None:
            self.links.append((len(self.buf), dict(attrs).get("href", "")))
            self.buf.append("[")

    def handle_endtag(self, tag):
        if tag == "a" and self.links and self.buf is not None:
            self.buf.append(f"]({self.links.pop()[1]})")
        elif tag == "td" and self.row is not None:
            self.row.append("".join(self.buf or []).replace("|", "\\|"))
            self.buf = None
        elif tag == "tr" and self.row is not None:
            self.lines.append("| " + " | ".join(self.row) + " |")
            self.row = None
        elif tag in self.BLOCK and self.buf is not None:
            self.lines.append(("- " if tag == "li" else "") + "".join(self.buf))
            self.buf = None

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)


def expected_lines(doc):
    parser = Lines()
    parser.feed(doc)
    parser.close()
    return common_lines("\n".join(" ".join(z.split()) for z in parser.lines))


def readback_text(path):
    """Die Rücklesung, wie die Sitzung sie abgelegt hat: Text, oder die Antwort als JSON."""
    path = Path(path)
    if not path.is_file():
        raise Refused(f"input {path.name} fehlt")
    text = path.read_text(encoding="utf-8")
    if text.lstrip()[:1] in ("{", "[", '"'):
        try:
            strings = list(json_strings(json.loads(text)))
        except ValueError:
            strings = []
        if strings:
            return max(strings, key=len)
    if "\n" not in text.strip() and "\\n" in text:
        text = text.replace("\\n", "\n")
    return text


def json_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from json_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from json_strings(v)


def compare(doc, read, footer):
    """`readback`: dieselben Zeilen in derselben Folge; eine Zeile, die die Fußzeile trägt, zählt nicht."""
    key = lambda z: re.sub(r"\s+", "", z)
    want = expected_lines(doc)
    foot = key(plain(footer))
    got = [z for z in common_lines(read) if key(z) != foot]
    for n in range(max(len(want), len(got))):
        w = want[n] if n < len(want) else "(Ende)"
        g = got[n] if n < len(got) else "(Ende)"
        if key(w) != key(g):
            raise Refused(f"readback Zeile {n + 1}: erwartet „{w}“, gelesen „{g}“")
    return len(want)


# --- Schätzdokument -------------------------------------------------------------
#
# Das Schätzdokument liest nicht die Dateien des Proposals, sondern das Projekt-Repo (§280):
# requirements/, epics/, gaps/ und project.yml (Kunde, Titel, Sprache, `design`). Dazu im Temp-Ordner:
#
#   meta.json    repo (die Wurzel des Projekt-Repos), read_at (die Lesezeit der Stunden) und die
#                Angaben aus dem Aufruf: surcharges, extras; kein Budget (§355); die Datei liegt
#                im Temp-Ordner des Laufs, außerhalb des Repos (§233)
#   bullets.json je Position, die Schätzung trägt, eine Liste von Bullets in Kundensprache (§355)
#   hours.json   die schmale Spalte `Aufwand (h)` (`Effort (h)`) des Tabs Solutioning mit `ID`: die
#                Antworten von get_values in der Hülle {"valueRanges": [...]}, oder eine Liste von
#                Zeilen mit der Kopfzeile zuerst
#
# Stunden setzt ein Mensch je Anforderung (§280 Regel 5 und 10, §283); das Script schätzt keine und
# leitet keine aus einer Größe ab. Ein Epic trägt die Summe seiner Anforderungen, wie die Formel im
# Tab Epics. Gezählt wird eine Anforderung mit `status` open oder confirmed, `scope` nicht
# out_of_scope, in einem Epic, das nicht merged oder dissolved ist. Fehlen Stunden, heißt die
# Gesamtzeile „unvollständig", ohne jede Stunde „offen". Der Aufwand steht oben je Position, in deren
# Folge (§355); die Sätze auf die Umsetzung stehen dort mit Grund und Prozent (§258). Ein Seitentyp (Anforderung in einem Epic der
# Domäne storefront) zeigt neben Größe und Stunden die Annahme zu den eigenen Sections (§285).
# Mit dem Add-on `design` trägt ein Epic der Domäne design die Stunden des Designers, darin die UX/UI-QA,
# erkannt an `standard: design-qa` (§285, §303). Was fehlt, steht unter den Lücken. Die Zeile STAND auf stderr nennt Lesezeit und die
# gelesenen Stunden je Anforderung: mit dem Commit des Repos ist das Dokument nachzurechnen (§264).

VALID_STATUS = ("open", "confirmed")
THEME_DOMAIN, DESIGN_DOMAIN = "storefront", "design"
WIDTHS.update({"section_theme": (52, 124, 38, 58, 52, 70, 74)})

ESTIMATE_LABELS = {
    "de": {
        "own": "Eigene Sections", "own_cell": "bis {n}", "q": "{n} offene Frage(n)", "qb": "davon {n} blockierend",
        "hours_partial": "unvollständig, {n} Anforderung(en) ohne Stunden",
        "without": "nicht enthalten: {n} Anforderung(en) ohne Stunden",
        "partial_note": "Die Summe ist unvollständig: {n} von {m} Anforderungen im Umfang tragen keine Stunden in `{col}`.",
        "no_hours_1": "1 Anforderung ohne Stunden", "no_hours_n": "{n} Anforderungen ohne Stunden",
        "no_reqs": "keine Anforderung im Umfang",
        "gap_size": "keine Größe: {ids}", "gap_hours": "keine Stunden in `{col}`: {ids}",
        "gap_undecided": "Lösung noch nicht entschieden: {ids}",
        "gap_own": "Seitentyp ohne Annahme zu den eigenen Sections: {ids}",
        "gap_design": "Das Add-on Design ist verkauft, aber kein Epic trägt die Domäne Design; es fehlen die Stunden des "
                      "Designers, darin die UX/UI-QA; nächster Schritt: das Design-Epic schneiden",
        "gap_design_qa": "Das Add-on Design ist verkauft, aber im Design-Epic ist keine Anforderung als UX/UI-QA markiert; "
                         "es fehlt die UX/UI-QA vor dem Go-Live; nächster Schritt: sie aus dem Add-on anlegen",
        "out": "{n} Anforderung(en) außerhalb des Umfangs, verworfen oder Duplikat, zählen nicht.",
        "stand_none": "keine",
        "by_position": "Aufwand je Position",
    },
    "en": {
        "own": "Own sections", "own_cell": "up to {n}", "q": "{n} open question(s)", "qb": "{n} blocking",
        "hours_partial": "incomplete, {n} requirement(s) without hours",
        "without": "not included: {n} requirement(s) without hours",
        "partial_note": "The sum is incomplete: {n} of {m} requirements in scope carry no hours in `{col}`.",
        "no_hours_1": "1 requirement without hours", "no_hours_n": "{n} requirements without hours",
        "no_reqs": "no requirement in scope",
        "gap_size": "no size: {ids}", "gap_hours": "no hours in `{col}`: {ids}",
        "gap_undecided": "solution not yet decided: {ids}",
        "gap_own": "page type without an assumption on its own sections: {ids}",
        "gap_design": "The add-on Design is sold, but no epic carries the domain Design; the designer's hours are missing, "
                      "including the UX/UI QA; next step: cut the design epic",
        "gap_design_qa": "The add-on Design is sold, but no requirement in the design epic is marked as UX/UI QA; "
                         "the UX/UI QA before go-live is missing; next step: create it from the add-on",
        "out": "{n} requirement(s) out of scope, rejected or duplicate are not counted.",
        "stand_none": "none",
        "by_position": "Effort by item",
    },
}


# Die Positionen der Schätzung, in ihrer Folge (§355), mit dem Namen in der Sprache des Projekts. Die
# Domäne des Epics geht vor dem Lösungsansatz; sonst entscheidet der erste Wert von `classification`.
POSITIONS = {
    "shop_setup": ("Shop-Setup", "Shop setup"),
    "shop_features": ("Erweiterte Shop-Features", "Extended shop features"),
    "ux_ui": ("UX/UI", "UX/UI"),
    "custom_extensions": ("Custom-Erweiterungen", "Custom extensions"),
    "interfaces": ("Schnittstellen", "Interfaces"),
    "data_migration": ("Daten-Migration", "Data migration"),
    "content_migration": ("Content-Migration", "Content migration"),
    "approach_open": ("Lösungsansatz offen", "Approach open"),
}
POSITION_BY_DOMAIN = {"design": "ux_ui", "data_migration": "data_migration", "content_migration": "content_migration"}
POSITION_BY_CLASS = {"shop": "shop_setup", "app": "shop_features", "theme_native": "ux_ui", "theme": "ux_ui",
                     "custom_app": "custom_extensions", "integration_connector": "interfaces",
                     "integration_middleware": "interfaces", "integration_custom": "interfaces"}
# Was ein Bullet nicht trägt (§355): er steht in Kundensprache, ohne Kennung und ohne Werte des Repos.
BULLET_TOOL = re.compile(r"\b(?:REQ|EP|GAP|ADR)-\d{3}\b|\b(?:theme_native|custom_app|integration_\w+|"
                         r"data_migration|content_migration|solution_status|own_sections)\b")


def position_of(req, domain):
    """Die Position einer gezählten Anforderung: über die Domäne ihres Epics, sonst über den ersten
    Lösungsansatz; „Lösungsansatz offen“, solange keiner gesetzt ist."""
    if domain in POSITION_BY_DOMAIN:
        return POSITION_BY_DOMAIN[domain]
    cls = req.get("classification") or []
    cls = [str(c) for c in cls] if isinstance(cls, list) else []
    # Eine Schnittstelle zählt zu „Schnittstellen“, auch wenn ein anderer Lösungsansatz zuerst steht,
    # etwa ein Konnektor aus dem App Store `[app, integration_connector]` (Testlauf 14.10.2026).
    if any(c.startswith("integration_") for c in cls):
        return "interfaces"
    pos = POSITION_BY_CLASS.get(cls[0]) if cls else None
    return pos or "approach_open"


def check_bullets(bullets, present, jargon):
    """`bullet`: je Position mindestens ein Bullet, kein Schlüssel ohne Position, und kein Bullet mit
    Stunden, „Aufschlag“, „Budget“, einer Kennung oder Werkzeugsprache (§355)."""
    if not isinstance(bullets, dict):
        raise Refused("input bullets.json ist kein Objekt mit je Position einer Liste")
    for key in bullets:
        if key not in present:
            known = key in POSITIONS
            raise Refused(f"bullet {key}: " + ("die Position hat keine gezählte Anforderung und entfällt (§355)" if known
                                              else f"keine Position; es gibt {', '.join(POSITIONS)}"))
    for key in present:
        items = bullets.get(key)
        if not isinstance(items, list) or not [b for b in items if str(b).strip()]:
            raise Refused(f"bullet {key}: die Position trägt keinen Bullet; je Position so viele wie nötig, "
                          f"so wenige wie möglich (§355)")
        for b in items:
            text = norm(str(b))
            for pattern in (HOURS_TEXT, SURCHARGE_TEXT, BUDGET_TEXT, BULLET_TOOL, INTERNAL, jargon):
                hit = pattern.search(text)
                if hit:
                    raise Refused(f"bullet {key}: „{text}“ trägt „{hit.group(0)}“; ein Bullet steht in "
                                  f"Kundensprache, ohne Stunden, Aufschlag, Budget, Kennung und Werkzeugsprache (§355)")


def _sheet():
    """Kopfzeilen, Anzeigewerte und Domänen aus check-sheet.py, der einen Stelle für den Vertrag (§295)."""
    spec = importlib.util.spec_from_file_location("check_sheet", Path(__file__).resolve().parent / "check-sheet.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def estimate_load(folder):
    """meta (aus meta.json und project.yml), die Objekte des Repos, die Stunden je Anforderung, der Aufruf."""
    import repo_objects  # erst hier: Kopien des Scripts ohne das Modul rechnen weiter das Proposal
    folder = Path(folder)
    sheet = _sheet()
    meta = read_json(folder, "meta.json")
    if not isinstance(meta, dict):
        raise Refused("input meta.json ist kein Objekt")
    repo = Path(str(meta.get("repo", "")).strip() or "\0")
    if not str(meta.get("repo", "")).strip() or not (repo / "project.yml").is_file():
        raise Refused(f"meta 'repo' „{meta.get('repo', '')}“: dort liegt keine project.yml; "
                      f"repo ist die Wurzel des Projekt-Repos")
    try:
        project = repo_objects.read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
    except repo_objects.ObjectError as e:
        raise Refused(f"input project.yml nicht lesbar: {e}")
    for key in ("customer", "title", "language"):
        meta[key] = str(project.get(key, "") or "").strip()
        if not meta[key]:
            raise Refused(f"meta '{key}' fehlt in project.yml")
    add_ons = project.get("add_ons") or []
    meta["design"] = isinstance(add_ons, list) and "design" in add_ons
    meta["shop_keys"] = repo_objects.project_shop_keys(project)
    if meta["language"] not in LABELS:
        raise Refused(f"meta language '{meta['language']}' ist weder de noch en (§202)")
    m = READ_AT.match(str(meta.get("read_at", "")))
    if not m:
        raise Refused(f"meta read_at '{meta.get('read_at', '')}' hat nicht die Form JJJJ-MM-TTTHH:MMZ")
    meta["read_at_text"] = f"{m[3]}.{m[2]}.{m[1]} {m[4]}:{m[5]}"
    meta["read_at_date"] = date_text(m[1], m[2], m[3], meta["language"])

    objects = repo_objects.load(repo)
    for kind in ("requirements", "epics", "gaps"):
        for o in objects[kind]:
            if "error" in o:
                raise Refused(f"object {o['name']}: {o['error']}; die Datei berichtigt der Lauf, der sie schreibt")

    lang = meta["language"]
    id_col, h_col = (sheet.column("solutioning", k, lang) for k in ("id", "hours"))
    path = folder / "hours.json"
    if not path.is_file():
        raise Refused("input hours.json fehlt")
    try:
        rows = rows_from_json(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, AttributeError, TypeError) as e:
        raise Refused(f"input hours.json nicht lesbar: {e}")
    head = [h.strip() for h in rows[0]] if rows else []
    missing = [c for c in (id_col, h_col) if c not in head]
    if missing:
        raise Refused(f"header hours.json: es fehlt {', '.join(repr(c) for c in missing)}")
    hours = {}
    for r in rows[1:]:
        r = list(r) + [""] * (len(head) - len(r))
        i, raw = r[head.index(id_col)].strip(), r[head.index(h_col)].strip()
        if not i or not raw:
            continue
        if number(raw) is None:
            raise Refused(f"hours {i}: {h_col} „{raw}“ ist keine Zahl; die Stunden setzt ein Mensch im Sheet")
        hours[i] = raw
    return meta, objects, hours, additions(meta), sheet


def estimate_data(folder):
    """Das Gerechnete der Schätzung: Epics mit Zeilen und Lücken, die gezählten Anforderungen und je
    Position ihre Anforderungen in der Folge der Positionen (§355)."""
    meta, objects, hours, calls, sheet = estimate_load(folder)
    import repo_objects  # liegt nach estimate_load auf dem Pfad
    lang = meta["language"]
    L = {**LABELS[lang], **ESTIMATE_LABELS[lang]}
    col = sheet.column("solutioning", "hours", lang)
    reqs = {o["key"]: o["head"] for o in objects["requirements"]}
    gaps_open = [o["head"] for o in objects["gaps"] if o["head"].get("status") == "open"]
    for i, h in reqs.items():
        size = str(h.get("size", "")).strip()
        if size and size not in SIZES:
            raise Refused(f"size {i}: „{size}“ ist keine Größe S, M, L oder XL; Stunden stehen nur in "
                          f"`{col}` (§280 Regel 10)")

    def counted(h):
        return h.get("status") in VALID_STATUS and h.get("scope") != "out_of_scope"

    def h_of(i):
        return number(hours[i]) if i in hours else None

    def h_cell(ids_):
        vals = [h_of(i) for i in ids_ if h_of(i) is not None]
        head = fmt(sum(vals), lang) if vals else L["open_h"]
        n = len(ids_) - len(vals)
        return f"{head} ({L['hours_partial'].format(n=n)})" if n else head

    def title_of(i):
        r = reqs[i]
        return repo_objects.shops_title(str(r.get("title", "")), r.get("shops"), meta["shop_keys"], lang)

    epics, overview, sections, gaps = [], [], [], []
    by_position = {k: [] for k in POSITIONS}
    for o in objects["epics"]:
        h, eid = o["head"], o["key"]
        title = str(h.get("title", ""))
        if h.get("status") in ("merged", "dissolved"):
            overview.append([eid, title, "", "", L["dissolved" if h.get("status") == "dissolved" else "merged"]])
            continue
        domain = str(h.get("domain", "")).strip()
        if domain not in sheet.VALUES[sheet.DOMAIN]:
            what = f"Domäne „{domain}“ steht nicht in der festen Liste" if domain else "Domäne fehlt"
            raise Refused(f"domain {eid}: {what} (§252); die Domäne setzt `epic-structure`, "
                          f"ohne sie gehört das Epic zu keiner Position der Summe")
        mine = sorted(i for i, r in reqs.items() if str(r.get("epic", "")) == eid and counted(r))
        for i in mine:
            by_position[position_of(reqs[i], domain)].append(i)
        e = {"id": eid, "title": title, "domain": domain, "reqs": mine}
        epics.append(e)
        theme = domain == THEME_DOMAIN
        rows, g_size, g_hours, g_undecided, g_own = [], [], [], [], []
        for i in mine:
            r = reqs[i]
            size, own = str(r.get("size", "")).strip(), str(r.get("own_sections", "")).strip()
            status = str(r.get("solution_status", "")).strip()
            g_size += [] if size else [i]
            g_hours += [] if i in hours else [i]
            g_undecided += [] if status == "decided" else [i]
            g_own += [i] if theme and not own else []
            qs = [g for g in gaps_open if i in (g.get("concerns") or [])]
            flag = [L["q"].format(n=len(qs))] if qs else []
            nb = sum(1 for g in qs if g.get("blocking") == "yes")
            flag += [L["qb"].format(n=nb)] if nb else []
            row = [i, title_of(i), size or "—"]
            row += [L["own_cell"].format(n=own) if own else "—"] if theme else []
            row += [fmt(h_of(i), lang) or "—", sheet.display("solution_status", status, lang) or status or "—",
                    ", ".join(flag) or "—"]
            rows.append(row)
        notes = [] if mine else [L["no_reqs"]]
        if g_size:
            notes.append(L["no_size_1"] if len(g_size) == 1 else L["no_size_n"].format(n=len(g_size)))
        if g_hours:
            notes.append(L["no_hours_1"] if len(g_hours) == 1 else L["no_hours_n"].format(n=len(g_hours)))
        parts = [L[k].format(ids=", ".join(v), col=col) for k, v in
                 (("gap_size", g_size), ("gap_hours", g_hours), ("gap_undecided", g_undecided), ("gap_own", g_own)) if v]
        if parts:
            gaps.append(f"**{eid} {title}**: " + " · ".join(parts))
        with_h = [h_of(i) for i in mine if h_of(i) is not None]
        # Die Übersicht nennt nur Aufwand (h); was fehlt, steht im Hinweis (§265).
        overview.append([eid, title, domain_name(sheet, domain, lang), fmt(sum(with_h), lang) if with_h else "—",
                         "; ".join(notes) or "—"])
        head = [L["req"], L["title"], L["size"]] + ([L["own"]] if theme else []) + \
               [col, sheet.column("solutioning", "solution_status", lang), L["open"]]
        # Ein Epic ohne Anforderung im Umfang zeigt keine leere Tabelle (Testlauf 14.10.2026)
        sections += [f"## {eid} {title}", ""] + (table(head, rows, "section_theme" if theme else "section") if rows
                                                  else [L["no_reqs"]]) + [""]

    known = {e["id"] for e in epics}
    without_epic = sorted(i for i, r in reqs.items() if counted(r) and str(r.get("epic", "")) not in known)
    if without_epic:
        gaps.append(L["gap_noepic"].format(ids=", ".join(without_epic)))
    if meta["design"] and not any(e["domain"] == DESIGN_DOMAIN for e in epics):
        gaps.append(L["gap_design"])
    elif meta["design"] and not any(str(reqs[i].get("standard", "")).strip() == "design-qa"
                                            for e in epics if e["domain"] == DESIGN_DOMAIN for i in e["reqs"]):
        gaps.append(L["gap_design_qa"])
    present = [(k, POSITIONS[k][sheet.LANGUAGES.index(lang)], ids_) for k, ids_ in by_position.items() if ids_]
    return {"meta": meta, "calls": calls, "sheet": sheet, "L": L, "lang": lang, "col": col, "hours": hours,
            "epics": epics, "overview": overview, "sections": sections, "gaps": gaps, "positions": present,
            "counted_ids": [i for e in epics for i in e["reqs"]], "out_count": sum(1 for r in reqs.values() if not counted(r)),
            "h_of": h_of, "h_cell": h_cell, "title_of": title_of}


def positions(folder):
    """Je Position ihre Stunden und Anforderungen, aus denen der Lauf die Bullets fasst (§355)."""
    d = estimate_data(folder)
    lines = [f"POSITION {k} {name} | {d['h_cell'](ids_)} | " + "; ".join(f"{i} {d['title_of'](i)}" for i in ids_)
             for k, name, ids_ in d["positions"]]
    return "\n".join(lines) or "POSITION keine", [], d["meta"]


def estimate(folder):
    d = estimate_data(folder)
    meta, calls, L, lang, col, hours = d["meta"], d["calls"], d["L"], d["lang"], d["col"], d["hours"]
    h_of, h_cell, counted_ids = d["h_of"], d["h_cell"], d["counted_ids"]
    path = Path(folder) / "bullets.json"
    if not path.is_file():
        raise Refused("input bullets.json fehlt; `positions` nennt je Position die Anforderungen, aus denen der "
                      "Lauf die Bullets fasst")
    bullets = read_json(Path(folder), "bullets.json")
    check_bullets(bullets, [k for k, _, _ in d["positions"]], _module("check-repo").JARGON)

    head = head_blocks(L["eyebrow_estimate"], meta["title"], meta["customer"])
    head.append(f'<p style="{STYLE["p"]}"><span style="{STYLE["mark"]}"><b>{esc(L["internal"])}</b></span></p>')

    # Die Summe: fehlen Stunden, heißt die Gesamtzeile „unvollständig", ohne jede Stunde „offen"
    # (Kettentest 30.09.2026: „Gesamt 0").
    missing = [i for i in counted_ids if i not in hours]
    base = sum(h_of(i) for i in counted_ids if i in hours)
    none_set = bool(missing) and len(missing) == len(counted_ids)
    partial = f" ({L['hours_partial'].format(n=len(missing))})" if missing else ""
    # §355: je Position ihre Stunden, in der festen Folge; darunter die Summe der Umsetzung
    rows = [(name, h_cell(ids_)) for _, name, ids_ in d["positions"]]
    rows.append((L["sum_impl"], (L["open_h"] if none_set else fmt(base, lang)) + partial))
    total = base
    for r, p in calls["surcharges"]:
        amount = round(base * p / 100, 1)
        total += amount
        rows.append((L["surcharge"].format(r=r, p=fmt(p, lang)), L["open_h"] if none_set else fmt(amount, lang)))
    for n, h in calls["extras"]:
        total += h
        rows.append((L["extra"].format(n=n), fmt(h, lang)))
    rows.append((L["total"], (L["open_h"] if none_set else fmt(total, lang)) + partial))
    doc = [stand_date(meta, L), "", f"## {L['by_position']}", ""] + table([L["position"], L["h"]], rows, "two") + [""]
    if missing:
        doc.append(L["partial_note"].format(n=len(missing), m=len(counted_ids), col=col))
    if not calls["surcharges"]:
        doc.append(L["no_surcharge"])
    if not calls["extras"]:
        doc.append(L["no_extra"])
    doc += [""]
    for k, name, ids_ in d["positions"]:
        doc += [f"### {name}", "", f"{L['h']}: {h_cell(ids_)}", ""]
        doc += [f"- {norm(str(b))}" for b in bullets[k] if str(b).strip()] + [""]
    doc += [f"## {L['overview']}", ""]
    doc += table([L["epic"], L["title"], L["domain"], col, L["note"]], d["overview"], "overview")
    if d["out_count"]:
        doc += ["", L["out"].format(n=d["out_count"])]
    doc += [""]
    doc += d["sections"]
    if d["gaps"]:
        doc += [f"## {L['gaps']}", ""] + [f"- {g}" for g in d["gaps"]] + [""]
    out = html_page(head + md_to_html("\n".join(doc)))
    check_markup(out)
    # Die Zeile STAND geht in den Commit.
    read = "; ".join(f"{i} {hours[i]}" for i in counted_ids if i in hours) or L["stand_none"]
    return out, [f"STAND {meta['read_at_text']} UTC; {col}: {read}"], meta


# --- Proposal: aus dem Projekt-Repo (§280) ---------------------------------------

# Die Spalten der Menschen, die das Proposal braucht (§280 Regel 5): je Datei der Tab und die Schlüssel
# der Spalten in check-sheet.py; die übrigen Spalten des Tabs liest das Script nicht.
HUMAN = {"epics.json": ("epics", ("id", "reviewed_by", "reviewed_on")),
         "offene-punkte.json": ("open_items", ("id", "due"))}
COMMIT = re.compile(r"^[0-9a-f]{7,40}$")
_MODULES = {}


def _module(name):
    """Ein Script daneben als Modul, erst wenn das Proposal es braucht; es gibt jedes nur einmal."""
    if name not in _MODULES:
        path = Path(__file__).resolve().parent / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODULES[name] = mod
    return _MODULES[name]


def human_columns(folder, name, lang):
    """Je Kennung die Spalten der Menschen eines Tabs, gelesen wie scope-snapshot.py liest."""
    snap, sheet = _module("scope-snapshot"), _module("check-sheet")
    tab, keys = HUMAN[name]
    try:
        rows = snap.load_rows(Path(folder) / name)
    except snap.Refused as e:
        raise Refused(str(e))
    head = [h.strip() for h in rows[0]]
    want = [sheet.column(tab, k, lang) for k in keys]
    missing = [w for w in want if w not in head]
    if missing:
        raise Refused(f"header {name}: es fehlt {', '.join(repr(m) for m in missing)} "
                      f"(Tab {sheet.tab_name(tab, lang)}, Sprache {lang})")
    at = [head.index(w) for w in want]
    out = {}
    for r in rows[1:]:
        r = list(r) + [""] * len(head)
        if r[at[0]].strip():
            out[r[at[0]].strip()] = {k: r[i].strip() for k, i in zip(keys[1:], at[1:])}
    return out


def epic_parts(body, lang):
    """Status in Blueprint, Goals und Assumptions aus dem Rumpf einer Epic-Datei (docs/draft-and-epic-page-contract.md)."""
    P = PAGE_LABELS[lang]
    parts = _module("check-repo").repo_objects.sections(body)
    status = re.search(rf"^\|\s*{re.escape(P['head_status'])}\s*\|\s*(.*?)\s*\|\s*$", parts.get("", ""), re.M)
    return {"status": status.group(1) if status else "", "goals": parts.get(P["section_goals"], ""),
            "assumptions": parts.get(P["section_assumptions"], "")}


def gap_question(body):
    """Die Frage: der Rumpf bis zur ersten Überschrift, in einer Zeile."""
    return norm(re.split(r"^#", body, maxsplit=1, flags=re.M)[0])


def load_repo(folder):
    """Das Gelesene des Proposals: Repo und Spalten der Menschen. Angaben zum Aufwand nimmt es nicht an (§355)."""
    folder = Path(folder)
    meta = read_json(folder, "meta.json")
    if "budget" in meta:
        raise Refused("budget meta.json trägt ein Budget; das Proposal kennt kein Budget (§355), "
                      "nimm `budget` aus meta.json")
    effort = [k for k in ("surcharges", "extras") if k in meta]
    if effort:
        raise Refused(f"meta meta.json trägt {', '.join(effort)}; das Proposal nennt keine Aufwände (§355), "
                      f"nimm sie aus meta.json")
    for key in ("repo", "commit", "read_at"):
        if not str(meta.get(key, "")).strip():
            raise Refused(f"meta '{key}' fehlt")
    if not COMMIT.match(str(meta["commit"])):
        raise Refused(f"meta commit '{meta['commit']}' ist kein Stand aus `git rev-parse --short HEAD`")
    m = READ_AT.match(str(meta["read_at"]))
    if not m:
        raise Refused(f"meta read_at '{meta['read_at']}' hat nicht die Form JJJJ-MM-TTTHH:MMZ")
    meta["read_at_text"] = f"{m[3]}.{m[2]}.{m[1]} {m[4]}:{m[5]}"
    check_repo = _module("check-repo")
    objects_mod = check_repo.repo_objects
    repo = Path(meta["repo"])
    if not (repo / "project.yml").is_file():
        raise Refused(f"input project.yml fehlt in {repo}")
    try:
        project = objects_mod.read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
    except objects_mod.ObjectError as e:
        raise Refused(f"input project.yml nicht lesbar: {e}")
    for key in ("customer", "title", "language"):
        meta[key] = str(project.get(key, "") or "").strip()
        if not meta[key]:
            raise Refused(f"meta '{key}' fehlt in project.yml")
    if meta["language"] not in LABELS:
        raise Refused(f"meta language '{meta['language']}' ist weder de noch en (§202)")
    meta["read_at_date"] = date_text(*READ_AT.match(str(meta["read_at"])).groups()[:3], meta["language"])
    meta["shops"] = project.get("shops") or []
    objects = objects_mod.load(repo)
    broken = [o for kind in ("requirements", "epics", "gaps", "decisions") for o in objects[kind] if "error" in o]
    if broken:
        raise Refused(f"input {broken[0]['name']}: {broken[0]['error']}; check-repo.py nennt den Lauf, dem sie gehört")
    lang = meta["language"]
    human = {name: human_columns(folder, name, lang) for name in HUMAN}
    assumed = read_json(folder, "assumed.json") if (folder / "assumed.json").is_file() else {}
    return meta, objects, human, assumed, check_repo


def check_effort_text(doc, places):
    """`effort` und `budget`: der Kunde liest im Proposal keine Stundenangabe, kein „Aufschlag“ und kein
    „Budget“ (§355). Geprüft wird der Text des Dokuments, wie er zurückgelesen wird, ohne Wortmarke und Stile."""
    for n, line in enumerate(expected_lines(doc), 1):
        for check, pattern in (("effort", HOURS_TEXT), ("effort", SURCHARGE_TEXT), ("budget", BUDGET_TEXT)):
            hit = pattern.search(line)
            if hit:
                raise Refused(f"{check} Zeile {n}: „{hit.group(0)}“; das Proposal nennt keine Aufwände und kein "
                              f"Budget (§355). Es steht in {source_of(hit.group(0), places)}")


def proposal(folder):
    meta, objects, human, assumed, check_repo = load_repo(folder)
    lang = meta["language"]
    L = LABELS[lang]
    sheet = _module("check-sheet")
    domains = sheet.VALUES[sheet.DOMAIN]
    reqs = {o["key"]: o for o in objects["requirements"]}
    shop_keys = [str(s.get("key")) for s in meta["shops"] if isinstance(s, dict) and s.get("key")]

    def req_title(i):
        """Der Titel einer Anforderung mit dem Shop-Bezug hinten (§307)."""
        h = reqs[i]["head"]
        return check_repo.repo_objects.shops_title(str(h.get("title", "")), h.get("shops"), shop_keys, lang)

    counted_req = {i for i, o in reqs.items() if o["head"].get("status") in check_repo.VALID
                   and o["head"].get("scope") != "out_of_scope"}
    places = []  # (Stelle, Text) je gelesene Stelle, die ins Proposal geht; für internal_source

    epics = []
    for o in objects["epics"]:
        h, eid = o["head"], o["key"]
        e = {"id": eid, "title": str(h.get("title", "")), "merged": h.get("status") in ("merged", "dissolved"),
             "epic_page": str(h.get("epic_page", "")).strip(), "draft": str(h.get("draft", "")).strip(),
             "domain": str(h.get("domain", "")).strip()}
        domain = e["domain"]
        if domain not in domains and not e["merged"]:
            what = f"Domäne „{domain}“ steht nicht in der festen Liste" if domain else "Domäne fehlt"
            raise Refused(f"domain {eid}: {what} (§252); die Domäne setzt `epic-structure`, "
                          f"ohne sie gehört das Epic zu keiner Gruppe im Proposal")
        seen = human["epics.json"].get(eid, {})
        e["checked"] = bool(seen.get("reviewed_by")) and bool(seen.get("reviewed_on"))
        e["reqs"] = sorted(i for i in counted_req if reqs[i]["head"].get("epic") == eid)
        e.update(epic_parts(o["body"], lang))
        if e["checked"] and not e["merged"]:
            for key, label in (("goals", L["goals"]), ("assumptions", L["assumptions"]), ("status", L["status_head"])):
                places.append((f"epics/{eid}.md, {label}", e[key]))
        places.append((f"epics/{eid}.md, title", e["title"]))
        epics.append(e)
    epic_ids = {e["id"] for e in epics if not e["merged"]}
    shown = {e["id"]: e["assumptions"] for e in epics if e["checked"] and not e["merged"]}

    shops = ", ".join(shop_text(s) for s in meta["shops"] if isinstance(s, dict) and shop_text(s))
    head = head_blocks(L["eyebrow_proposal"], meta["title"],
                       f"{meta['customer']} · {L['shops']}: {shops}" if shops else meta["customer"])
    # Version und Erstellt/Reviewed von bestätigt kein Schritt des Laufs; sie trägt ein Mensch im Doc ein.
    head += meta_table([(L["meta_version"], "–"), (L["meta_date"], meta["read_at_date"]),
                        (L["meta_by"], "–"), (L["meta_review"], "–")])
    # Kein Aufwand im Proposal (§355); die Epics folgen den Domänen.
    doc = [stand_date(meta, L), ""]
    grouped = [(domain_name(sheet, d, lang), group) for d, group in by_domain(epics, domains)]
    scope = []
    for name, group in grouped:
        for e in group:
            if not e["checked"]:
                where, status = "—", L["in_work"]
            else:
                where = (f"[{L['epic_page']}]({e['epic_page']})" if e["epic_page"].startswith("http")
                         else L["draft_cell"] if e["draft"] else "—")
                status = e["status"] or "—"
            scope.append([e["id"], e["title"], name, where, status])
    doc += [f"## {L['scope']}", ""]
    doc += table([L["epic"], L["title"], L["domain"], L["epic_page"], L["status_head"]], scope, "scope") + [""]
    for name, group in grouped:
        checked = [e for e in group if e["checked"]]
        if checked:
            doc += [f"## {name}", ""]
        for e in checked:
            assumptions = e["assumptions"].strip()
            if e["domain"] == check_repo.THEME_DOMAIN:
                # Je Seitentyp die Annahme zu den eigenen Sections (§285); der Kunde bestätigt sie mit dem Scope.
                lines = [f"- {L['sections_assumed'].format(i=i, t=req_title(i), n=own)}"
                         for i in e["reqs"] for own in [str(reqs[i]["head"].get("own_sections", "")).strip()] if own]
                assumptions = "\n\n".join(x for x in (assumptions, "\n".join(lines)) if x)
            doc += [f"### {e['id']} {e['title']}", "",
                    f"#### {L['goals']}", "", e["goals"].strip() or L["empty"], "",
                    f"#### {L['assumptions']}", "", assumptions or L["empty"], ""]

    adrs = {}  # je Anforderung die jüngste gültige ADR, die sie unter Betrifft nennt
    for o in objects["decisions"]:
        if o["head"].get("status") != "accepted":
            continue
        m = ADR_CONCERNS.search(o["body"])
        for i in ids(m.group(1)) if m else []:
            adrs[i.strip(".,;")] = o
    gaps = [o for o in objects["gaps"] if o["head"].get("status") == "open"]
    out_rows, blockers, questions = [], [], []
    for i, o in reqs.items():
        h = o["head"]
        places.append((f"requirements/{i}.md, title", str(h.get("title", ""))))
        title = req_title(i)
        if h.get("status") == "rejected" or (h.get("status") in check_repo.VALID and h.get("scope") == "out_of_scope"):
            adr = adrs.get(i)
            why = reason(adr["body"]) if adr else ""
            if adr:
                places.append((f"{adr['name']}, Entscheidung", why))
            # §327: die Priorität steht dabei; was der Kunde braucht und doch nicht gebaut wird, zuerst
            prio = sheet.display("priority", h.get("priority"), lang) or "—"
            out_rows.append([i, h.get("epic") or "—", title, prio, why or "—"])
        elif i in counted_req and h.get("solution_status") == "blocked":
            # Blockiert durch: nur Fragen an den Kunden; eine Frage an Consultant oder Gewerk bleibt intern.
            by = [g for g in gaps if str(g["head"].get("blocking")) == "yes" and to_customer(str(g["head"].get("to", "")))
                  and i in (g["head"].get("concerns") or [])]
            # Ohne Frage an den Kunden steht die Anforderung trotzdem da, mit „in interner Klärung“ statt
            # eines Strichs, der sich wie „blockiert durch nichts“ liest (Testlauf 14.10.2026).
            blockers.append([i, h.get("epic") or "—", title,
                             "; ".join(gap_question(g["body"]) for g in by) or L["internal_clarification"]])
            places += [(f"gaps/{g['key']}.md", gap_question(g["body"])) for g in by]
    for g in gaps:
        gh = g["head"]
        concerns = [c for c in (gh.get("concerns") or []) if c in counted_req or c in epic_ids]
        if not concerns or not to_customer(str(gh.get("to", ""))):
            continue
        q = {"question": gap_question(g["body"]), "addressee": str(gh.get("to", "")).strip(),
             "due": human["offene-punkte.json"].get(g["key"], {}).get("due", ""),
             "blocking": str(gh.get("blocking")) == "yes"}
        places.append((f"gaps/{g['key']}.md", q["question"]))
        questions.append((g["key"], ", ".join(concerns), q))
    covered = assumed_questions(assumed, shown, {gid for gid, _, _ in questions})
    listed = sorted(((c, q) for gid, c, q in questions if gid not in covered), key=lambda t: not t[1]["blocking"])
    if out_rows:
        out_rows.sort(key=lambda r: r[3] != sheet.display("priority", "must-have", lang))
        doc += [f"## {L['not_in_scope']}", ""] + table([L["requirement"], L["epic"], L["title"], L["priority"],
                                                         L["reason"]], out_rows, "out_priority") + [""]
    if blockers:
        doc += [f"## {L['blockers']}", ""] + table([L["requirement"], L["epic"], L["title"], L["blocked_by"]], blockers, "out") + [""]
    if listed:
        doc += [f"## {L['before_order']}", ""] + [question_line(c, q, L, lang) for c, q in listed] + [""]
    out = html_page(head + md_to_html("\n".join(doc)))
    places += [("project.yml, customer", meta["customer"]), ("project.yml, title", meta["title"])]
    check_customer_text(out, places, check_repo.JARGON)
    check_effort_text(out, places)
    check_markup(out)
    live = [e for e in epics if not e["merged"]]
    notes = [f"STAND {meta['read_at_text']} UTC; Repo {meta['commit']}; "
             f"geprüft: {', '.join(e['id'] for e in live if e['checked']) or '—'}; "
             f"in Arbeit: {', '.join(e['id'] for e in live if not e['checked']) or '—'}"]
    without_epic = sorted(i for i in counted_req if not reqs[i]["head"].get("epic"))
    if without_epic:
        notes.append("OHNE-EPIC " + ", ".join(without_epic))
    n_block = sum(1 for _, _, q in questions if q["blocking"])
    notes.append(f"KUNDENFRAGEN {len(questions)} offen, davon {n_block} blockierend, {len(covered)} als Annahme")
    return out, notes, meta


def shop_text(shop):
    """`domain (DE, AT)`; ohne Domain nur die Märkte, ohne beides nichts."""
    domain = str(shop.get("domain", "")).strip()
    markets = ", ".join(str(m) for m in shop.get("markets", []) or [])
    if domain and markets:
        return f"{domain} ({markets})"
    return domain or markets


def source_of(token, places):
    """Die Datei im Repo, aus der ein gesperrter Text ins Proposal kam, damit der Lauf sie nennt."""
    return "; ".join(where for where, text in places if token in str(text)) or "keiner gelesenen Stelle"


def main(argv):
    docs = {"estimate": estimate, "proposal": proposal}
    shape = {"positions": 3, "estimate": 3, "proposal": 3, "layout": 2, "footer": 5, "readback": 5, "font": 3}
    if len(argv) < 2 or shape.get(argv[1]) != len(argv) or (len(argv) > 3 and argv[2] not in docs):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        if argv[1] == "layout":
            text = json.dumps(PAGE, ensure_ascii=False)
        elif argv[1] == "footer":
            _, _, meta = docs[argv[2]](argv[3])
            text = json.dumps(footer_requests(argv[2], meta, argv[4]), ensure_ascii=False)
        elif argv[1] == "font":
            requests, note = font_requests(argv[2])
            print(note, file=sys.stderr)
            text = json.dumps(requests, ensure_ascii=False)
        elif argv[1] == "readback":
            doc, _, meta = docs[argv[2]](argv[3])
            text = f"GLEICH {compare(doc, readback_text(argv[4]), footer_text(argv[2], meta))} Zeilen"
        else:
            text, notes, _ = {**docs, "positions": positions}[argv[1]](argv[2])
            for z in notes:
                print(z, file=sys.stderr)
    except Refused as e:
        print(str(e))
        return 1
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
