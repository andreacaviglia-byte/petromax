#!/usr/bin/env python3
"""Prüft einen fertigen Ticket-Body gegen die Blockfolge der Vorlage.

Aufruf: check-ticket-body.py [--language de|en] [--title <Titel>] [--repo <Projekt-Repo>]
                             <stufe> [--split] <datei|->
        stufe: epic | story | story --split | subtask

Die Stufen nach dem Ticketschnitt (§281): die Story einer Anforderung mit einem
Gewerk ('story'), die Story mit mehreren Gewerken ('story --split') und je
Arbeitseinheit eines Gewerks ein Subtask ('subtask'). '--title' prüft den
Titel des Tickets mit; an 'subtask' ist er Pflicht, weil der Subtask einen
eigenen Titel trägt. '--language' ist die Sprache aus `language` in project.yml
(Standard 'de'): Überschriften und feste Zeilen stehen in ihr (§295); eine
Überschrift der anderen Sprache meldet 'language'. '--repo' ist das Projekt-Repo:
mit ihm prüft der Lauf am Titel einer Story auch den Shop-Bezug hinten aus
`shops` der Anforderung und `shops` in project.yml (§307).

Der Anlass ist gemessen und war ein eigener Fehler: ein Lauf hat die
Ticket-Texte ERFUNDEN, weil er 'ref-ticket-templates.md' erst ab der Mitte
gelesen hat. Das Ticket kam ohne 'Kunde', 'Link zum Shop', 'User Story' und
'Akzeptanzkriterien', das Theme-Ticket mit frei erfundenen Überschriften
anstelle des 'Lösungsansatz'-Blocks. Beide Texte sahen
vollständig aus, und keine Prüfung sah hin — der Kanal nimmt jeden Body.

Deshalb prüft nicht die Prosa, sondern dieser Lauf. Er läuft vor
'validate-html.sh': erst die Blockfolge, dann die Auszeichnung.

Er nimmt Markdown ('## Kunde') und die HTML-Form des Kanals ('<h2>Kunde</h2>')
gleichermaßen — dieselbe Blockfolge, zwei Schreibweisen auf demselben Weg.

Geprüft wird der Body, der gesendet wird. Die Vorlagen in
'ref-ticket-templates.md' tragen Platzhalter in '<…>' und kommen deshalb nicht
durch; ein gesendeter Body trägt keinen.
"""

import re
import sys
from pathlib import Path

# Die Blockfolge: erst, was gewollt ist, dann der gewählte Lösungsansatz, zuletzt die
# Identität (§209). 'Angaben für ‹Gewerk›' trägt den Namen des Gewerks und wird
# am Anfang erkannt; 'Links' kommt nur an einer Theme-Story mit Ziel.
ANGABEN = "Angaben für"
STORY = ["Kunde", "Link zum Shop", "User Story", "Regeln", "Akzeptanzkriterien",
         "Nicht enthalten", "Lösungsansatz", ANGABEN, "Links", "Kontext"]
# Das Epic-Ticket ist die Abnahmefläche des Kunden (§220 W8).
EPIC = ["Ziel", "Kontext", "Anforderungen", "Lösungsansatz", "Links"]

# Die Story mit mehreren Gewerken trägt die Kriterien der Abnahme und den
# übergreifenden Lösungsansatz; die Angaben stehen an den Subtasks (§281).
STORY_SPLIT = [b for b in STORY if b != ANGABEN]
# Der Subtask: User Story, seine Kriterien der Umsetzung, seine Angaben; der
# Schlüssel steht wie an der Story zuletzt im 'Kontext' (§281). Kunde, Shop,
# Abgrenzung und Lösungsansatz trägt die Story, unter der er hängt.
KRITERIEN_UMSETZUNG = "Kriterien der Umsetzung"
SUBTASK = ["User Story", KRITERIEN_UMSETZUNG, ANGABEN, "Links", "Kontext"]

EBENEN = {"epic": EPIC, "story": STORY, "story-split": STORY_SPLIT,
          "subtask": SUBTASK}
# Die Stufe, wie der Aufruf sie nennt.
STUFE = {"epic": "epic", "story": "story", "story-split": "story --split",
         "subtask": "subtask"}
# Die Ebenen unter dem Epic: Schlüssel zuletzt, Design-Referenz, Gewerk, Titel.
UNTER_EPIC = ("story", "story-split", "subtask")

# Blöcke, die da sein DÜRFEN und nicht müssen. 'Links' fällt weg, wenn
# keine seiner Zeilen ein Ziel hat: 'Produkt: —' ist keine Angabe, sondern
# Rauschen an der Stelle, an der ein Mensch nach einem Sprung sucht. 'Regeln'
# steht nur, wenn etwas gilt, das kein Kriterium ausdrücken kann. 'Angaben für
# ‹Gewerk›' gehört seit §281 zur Form der Story mit einem Gewerk und des
# Subtasks: im Body steht das Gewerk nur dort, der Titel nennt es nie.
OPTIONAL = {"Links", "Regeln"}

# Die vier Gewerke (§209, §220 W6), mit den Namen aus Glossar und Board:
# 'Schnittstelle', nicht 'Integration' (Probe 0.5, 10.10.2026: der Text sagte
# 'Integration', die Kategorie des Boards 'Schnittstelle'). Heißt ein Gewerk
# auf einem Board anders, bildet der Board-Vertrag es ab; im Text steht immer
# dieser Name, damit jede Story auf jedem Kanal gleich aussieht.
GEWERKE = ("DEV", "Konfig", "Schnittstelle", "UX/UI")

# Die Form der Schlüssel (§281): die Story trägt die Kennung der Anforderung,
# der Subtask sie mit laufender Nummer, das Epic seine Epic-ID. Ein Schlüssel
# in der Form der anderen Ebene träfe im Abgleich das falsche Ticket oder
# keines und ließe es ein zweites Mal entstehen.
STORY_KEY = re.compile(r"^REQ-\d{3,}$")
SUBTASK_KEY = re.compile(r"^REQ-\d{3,}-\d+$")
SCHLUESSEL = {"story": STORY_KEY, "story-split": STORY_KEY,
              "subtask": SUBTASK_KEY, "epic": re.compile(r"^EP-\d{3,}$")}
FORM = {"story": "REQ-012", "story-split": "REQ-012", "subtask": "REQ-012-1",
        "epic": "EP-003"}

# Der Titel (§281): Story 'REQ-012 ‹Titel der Anforderung›', Subtask
# 'REQ-012-1 ‹eigene Aufgabe›'. Das Gewerk steht nie im Namen; erkannt wird es
# in den Formen, in denen es angehängt oder vorangestellt wird. Vorangestellt
# heißt: mit Trenner dahinter ('DEV: …', 'UX/UI | …', 'Konfig – …'), ein
# Bindestrich nur mit Leerzeichen davor ('DEV - …'). Ohne Leerzeichen ist er
# ein Wort: der Standardtitel 'UX/UI-QA vor dem Go-Live' (ref-baseline-rows.md)
# fiel in der Probe 0.5 (10.10.2026) als Gewerk durch. Hinter dem Shop-Bezug
# angehängt ('… (B2C) Konfig') kam es in der zweiten Proberunde (10.10.2026) durch.
TITEL = re.compile(r"^(REQ-\d{3,}(?:-\d+)?)\s+(\S.*)$")
GEWERK_IM_TITEL = re.compile(
    r"(?:^|[·|:(\[]\s*|\s[-–]\s*|\)\s*)(?:DEV|Konfig|Schnittstelle|UX/UI)\s*[)\]]?\s*$"
    r"|^(?:DEV|Konfig|Schnittstelle|UX/UI)(?:\s*[:·|–]|\s+-)")

# Das Epic-Ticket trägt je Anforderung nur ID und Titel (§281): je Zeile
# 'REQ-012 ‹Titel›'. Eine User Story oder ein Kriterium darunter ist der Inhalt
# der Story und stünde am Epic ein zweites Mal.
ANFORDERUNG = re.compile(r"^REQ-\d{3,}\s+\S")

# Das Vorhaben des Epics (ref-ticket-templates.md, „Das Epic-Ticket"): der
# `key` aus project.yml. Ein Board kann mehrere Vorhaben tragen, und die
# Epic-ID zählt je Sheet; ohne Sheet ist die Zeile das Einzige, woran ein
# späterer Lauf sein Epic wiederfindet. Gemessen im Kettentest (30.09.2026):
# ein Epic ohne Sheet trug keinen Schlüssel, und auf dem geteilten Board stand
# ein fremdes EP-001.
BEAUFTRAGUNG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")

# Die Design-Referenz hat zwei Formen (ref-ticket-templates.md): der Verweis
# auf das UX/UI-Ticket oder die Adresse des Frames. Das UX/UI-Ticket ist seit
# §281 eine Story ('REQ-012') oder ein Subtask ('REQ-012-2').
REFERENZ = re.compile(r"^aus\s+(REQ-\d{3,}(?:-\d+)?|<[^>]+>)$|^https?://\S+$")

# Eine Größe gehört ins Größenfeld des Boards, nie in den Text (Board-Vertrag §1).
GROESSE = re.compile(r"\b(Größe|Aufwand|T-Shirt)\s*:?\s*(XS|S|M|L|XL)\b")

# Aufwand und Preis des Projekts (§141): die Wörter der Kalkulation, ein
# Aufwand mit Zahl, Personentage. Ein Betrag allein ist kein Treffer.
KALKULATION = re.compile(
    r"Schätzung|Kalkulation|Tagessatz|Stundensatz|Personentag\w*|Festpreis"
    r"|\bAufwand\w*\s*(?:von\s+|:\s*)?(?:ca\.\s*|rund\s+)?\d"
    r"|\b\d+(?:[.,]\d+)?\s*PT\b", re.I)


# Ein Platzhalter, der im gesendeten Body stehen bleibt, sieht im Ticket wie
# eine Angabe aus: '<Adresse der Req Page>' im 'Kontext' lief durch diesen
# Prüfer, solange er Platzhalter nur in 'Design-Referenz' suchte. Gesucht wird in jedem Block, nach '‹…›' und nach '<…>', das kein Tag
# ist. Die Tags der HTML-Form fallen vorher heraus, ein maskierter Platzhalter
# ('&lt;Adresse&gt;') wird erst danach entmaskiert und dann gefunden.
HTML_TAG = re.compile(r"</?(?:body|strong|em|u|s|b|i|code|ol|ul|li|a|blockquote|pre"
                      r"|h[1-6]|hr|img|p|br|span|div|table|thead|tbody|tr|td|th)"
                      r"\b[^<>]*>", re.I)
PLATZHALTER = re.compile(r"‹[^›\n]*›|<(?!\s)[^<>\n]+(?<!\s)>")
# Die Ersatzmarken des Datalayer-Vertrags stehen an der Stelle entfernter
# Daten und dürfen in einem Body stehen; sie sind kein offener Platzhalter. Sie
# stehen in der Sprache des Projekts (§337), wörtlich wie in „Die festen
# Wendungen“; dev/tests/check-ticket-body.py hält beide gleich.
ERSATZMARKEN = ("‹Zugangsdatum entfernt›", "‹Gesundheitsdaten entfernt›",
                "‹Endkundendaten entfernt›", "‹credential removed›",
                "‹health data removed›", "‹end-customer data removed›")


def entmaskieren(s):
    """Im Body des Kanals ist '&' maskiert: 'Verhalten &amp; Regeln'."""
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def zeilenwert(teil, marke):
    """Der Wert hinter 'Marke:' in einem Teil des Bodys, ohne Tags.

    Ein Anker wird zu seiner Adresse: in der HTML-Form des Kanals steht die
    Referenz auf einen Frame als '<a href="…">…</a>'.
    """
    rest = teil.split(marke, 1)[1]
    anker = re.search(r'<a\s[^>]*href="([^"]+)"', rest)
    if anker:
        return entmaskieren(anker.group(1)).strip()
    rest = re.sub(r"</?(li|ul|ol|p|body|h[12])>", "", rest)
    return entmaskieren(rest).strip()

H2 = re.compile(r"^\s*##\s+(.+?)\s*$|<h2>\s*(.*?)\s*</h2>", re.M | re.I)
TABELLE = re.compile(r"^\s*\|.*\|\s*$|<table[\s>]", re.M | re.I)
TIEFER = re.compile(r"^\s*#{3,}\s|<h[3-6][\s>]", re.M | re.I)

# Die Herkunft einer Wahl steht in der Lösung, nicht im Ticket. Zwei
# Formen davon sind am Text erkennbar: ein Datum und die Wörter, mit denen
# eine Hausregel eingeleitet wird. Geprüft wird nur im 'Lösungsansatz' -- im
# 'Kontext' steht ein Abrufdatum mit Recht, und in 'Regeln' eine Frist.
HERKUNFT_DATUM = re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b|\b\d{4}-\d{2}-\d{2}\b"
                            r"|\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}\b")
HERKUNFT_WORTE = (r"seit dem\b", r"\bVorgabe für\b", r"\bStandard für\b",
                  r"\bhier greift\b", r"\bunser Standard\b")
HERKUNFT_WORTE_EN = (r"\bsince\s+\d", r"\bstandard for\b", r"\bapplies here\b",
                     r"\bour standard\b")

# Die Sprache des Projekts (§295): Überschriften und feste Zeilen stehen im Ticket in der Sprache
# aus `language` in project.yml; übersetzt wird nur in der Vorlage. Diese Tabelle ist das Vokabular
# aus ref-ticket-templates.md, Zeile für Zeile; dev/tests/check-ticket-body.py hält beide gleich.
# Geprüft wird in der deutschen Form: ein englischer Body wird vorher übersetzt. 'Schlüssel:',
# 'Beauftragung:' und die Namen der Gewerke stehen in jeder Sprache gleich, an ihnen findet der
# Abgleich das Ticket wieder.
VOKABULAR_EN = {
    "Kunde": "Customer", "Link zum Shop": "Shop link", "User Story": "User story",
    "Regeln": "Rules", "Akzeptanzkriterien": "Acceptance criteria",
    "Nicht enthalten": "Not included", "Lösungsansatz": "Approach",
    "Angaben für": "Details for", "Links": "Links", "Kontext": "Context",
    "Kriterien der Umsetzung": "Implementation criteria", "Ziel": "Goal",
    "Anforderungen": "Requirements",
    "Design-Referenz:": "Design reference:", "aus": "from",
    "Betroffene Ansicht:": "Affected view:", "Epic Page:": "Epic page:",
    "Design:": "Design:", "Kunde:": "Customer:", "Projekt": "project", "offen": "open",
    "Darstellung gemäß Figma (siehe Link)": "Display as in Figma (see link)",
    "Entscheidung offen, entscheidet": "Decision open, decided by",
    "Alternative": "alternative", "geprüft und verworfen": "checked and discarded",
    "Shopify-nativ": "Shopify native", "Theme-nativ": "Theme native", "Public App": "Public app",
    "Theme-Anpassung": "Theme customization", "Custom App": "Custom app",
    "Standard-Konnektor": "Standard connector", "Middleware": "Middleware",
    "Custom Schnittstelle": "Custom integration",
    "Design (Figma)": "Design (Figma)", "Analyse": "Analysis",
}
SPRACHEN = ("de", "en")

# Der Block 'Lösungsansatz' (§312): je Klassifizierung ein Punkt mit ihrer Anzeige aus dem
# Datalayer-Vertrag (§324), bei einer App und einer Schnittstelle mit dem Namen dessen, was den
# Lösungsansatz trägt; im Design-Epic die Art der Arbeit (§297); ohne Quelle 'offen', ohne entschiedenen Lösungsansatz
# 'Entscheidung offen, entscheidet …'. In der Probe 0.5 (10.10.2026) stand die Klassifizierung als
# Präfix im Fließtext, der Name der App nur in den Angaben.
KLASSIFIZIERUNG = ("Shopify-nativ", "Theme-nativ", "Public App", "Theme-Anpassung", "Custom App",
                   "Standard-Konnektor", "Middleware", "Custom Schnittstelle", "Design (Figma)", "Analyse")
# Die vier Klassifizierungen, hinter denen ein Name steht: 'Public App: ‹Name›', 'Middleware: ‹Name› an …'.
MIT_NAMEN = ("Public App", "Standard-Konnektor", "Middleware", "Custom Schnittstelle")
OHNE_WEG = ("offen", "Entscheidung offen, entscheidet")
# Die Kurzbeschreibung trägt keine Kennungen (§312): im selben Absatz stand in der Probe eine
# geschlossene offene Frage.
KENNUNG = re.compile(r"\b(?:GAP|ADR|REQ|EP)-\d{3,}")
UEBERSCHRIFTEN = set(STORY + EPIC + SUBTASK)
EN_ZU_DE = {VOKABULAR_EN[d]: d for d in UEBERSCHRIFTEN}

# Größe und Kalkulation in einem englischen Body (§209): dieselben Sperren in den Wörtern der Sprache.
GROESSE_EN = re.compile(r"\b(Size|Effort|T-shirt)\s*:?\s*(XS|S|M|L|XL)\b")
KALKULATION_EN = re.compile(
    r"\bEstimation\b|\bDay rate\b|\bHourly rate\b|\bPerson-days?\b|\bFixed price\b"
    r"|\bEffort\w*\s*(?:of\s+|:\s*)?(?:approx\.\s*|about\s+)?\d"
    r"|\b\d+(?:[.,]\d+)?\s*PD\b", re.I)


def ueberschrift_der_sprache(name, sprache):
    """Die deutsche Form einer Überschrift, oder None, wenn sie der anderen Sprache gehört."""
    if sprache == "en":
        if name.startswith("Details for "):
            return ANGABEN + name[len("Details for"):]
        if name.startswith(ANGABEN + " ") or (name in UEBERSCHRIFTEN and name not in EN_ZU_DE):
            return None
        return EN_ZU_DE.get(name, name)
    if name.startswith("Details for ") or (name in EN_ZU_DE and name not in UEBERSCHRIFTEN):
        return None
    return name


def uebersetzen(text, sprache):
    """Den Body in die deutsche Form, an der geprüft wird; dazu je fremde Überschrift ihr Name.

    Eine Überschrift der anderen Sprache ist kein Stil, sondern ein Body, der nicht aus der Vorlage
    dieser Sprache stammt: im Ticket stünden zwei Sprachen nebeneinander (§295).
    """
    fremd = []

    def ersetzen(m):
        roh = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
        deutsch = ueberschrift_der_sprache(entmaskieren(roh), sprache)
        if deutsch is None:
            fremd.append(entmaskieren(roh))
            return m.group(0)
        return m.group(0).replace(roh, deutsch, 1)

    text = H2.sub(ersetzen, text)
    if sprache == "en":
        text = text.replace("Design reference:", "Design-Referenz:")
        text = re.sub(r"(Design-Referenz:\s*)from\s+", r"\1aus ", text)
    return text, fremd


def ueberschriften(text):
    """Die Blöcke in ihrer Reihenfolge — Markdown oder HTML des Kanals."""
    # Im Body des Kanals ist '&' maskiert: 'Verhalten &amp; Regeln'.
    def entmaskieren(s):
        return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return [block_name(entmaskieren((a or b).strip())) for a, b in H2.findall(text)]


def block_name(name):
    """'Angaben für DEV' ist der Block 'Angaben für'."""
    return ANGABEN if name.startswith(ANGABEN + " ") else name


def zusammenlaufend(text):
    """Blöcke, deren mehrere Zeilen im Ticket in einer landen.

    Gemessen am angelegten Ticket (27.08.2026): der Body erreicht den Kanal als
    EINE Zeile, und einen Umbruch erzeugen dort nur ein Listenpunkt und eine
    Überschrift. Drei schlichte Zeilen im 'Kontext' stehen im Ticket als
    '…REQ-001.md</a>Lösung:'; ein '<br/>' lehnt der Kanal ab. Der Block
    sieht in der Markdown-Quelle richtig aus — deshalb prüft das hier und
    nicht das Auge.
    """
    gefunden = []
    for block, rumpf in bloecke(text):
        zeilen = [z.strip() for z in rumpf.splitlines() if z.strip()]
        if len(zeilen) < 2:
            continue
        schlicht = [z for z in zeilen
                    if not z.startswith(("- ", "* ", "+ ", "#", "|"))
                    and not re.match(r"^\d+\.\s|^<(li|ul|ol|h[12]|p)[\s>]", z, re.I)]
        if schlicht:
            gefunden.append(("Umbruch", f"der Block '{block}' trägt mehrere "
                                        f"Zeilen, aber {len(schlicht)} davon "
                                        f"ist/sind kein Listenpunkt — im "
                                        f"Ticket laufen sie in eine Zeile "
                                        f"zusammen: {schlicht[0][:40]!r}"))
    return gefunden


def platzhalter(text):
    """Je Block die Platzhalter, die im Body stehen geblieben sind."""
    treffer = list(H2.finditer(text))
    grenzen = [0] + [m.start() for m in treffer] + [len(text)]
    namen = [""] + [(m.group(1) or m.group(2) or "").strip() for m in treffer]
    gefunden = []
    # Je Abschnitt mit seiner Überschrift: auch 'Angaben für <Gewerk>' ist ein Platzhalter.
    for block, von, bis in zip(namen, grenzen, grenzen[1:]):
        rest = entmaskieren(HTML_TAG.sub(" ", text[von:bis]))
        for marke in ERSATZMARKEN:
            rest = rest.replace(marke, " ")
        for treffer in PLATZHALTER.finditer(rest):
            gefunden.append((block, treffer.group(0)))
    return gefunden


def bloecke(text):
    """Je Block sein Rumpf, in der Reihenfolge des Bodys."""
    treffer = list(H2.finditer(text))
    for i, m in enumerate(treffer):
        name = (m.group(1) or m.group(2) or "").strip()
        ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(text)
        yield name, text[m.end():ende]


def shop_bezug(repo, kennung):
    """Der Shop-Bezug hinten am Titel der Story nach §307 (' (B2C)' oder ""), oder ein Text, warum er
    nicht zu bestimmen ist. Gerechnet wie in repo_objects.py, damit Prüfer und Lauf dasselbe sagen."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    import repo_objects
    repo = Path(repo)
    try:
        projekt = repo_objects.read_yaml((repo / "project.yml").read_text(encoding="utf-8"))
        kopf, _ = repo_objects.read_object(repo / "requirements" / f"{kennung}.md")
    except (OSError, repo_objects.ObjectError) as e:
        return None, f"{e}"
    return repo_objects.shops_label(kopf.get("shops"), repo_objects.project_shop_keys(projekt),
                                    projekt.get("language", "de")), None


def pruefe_titel(ebene, titel, text, repo=None):
    """Der Titel des Tickets: Schlüssel, eigener Text, kein Gewerk (§281); mit dem Repo der
    Shop-Bezug hinten an der Story (§307)."""
    aufgabe = "eigene Aufgabe" if ebene == "subtask" else "Titel der Anforderung"
    if not titel or not titel.strip():
        return [("title", "die Stufe 'subtask' verlangt '--title' — der "
                          "Subtask trägt einen eigenen Titel "
                          "'REQ-012-1 ‹eigene Aufgabe›'")]
    titel = titel.strip()
    treffer = TITEL.match(titel)
    if not treffer:
        return [("title", f"{titel!r} hat nicht die Form '{FORM[ebene]} "
                          f"‹{aufgabe}›' — der Abgleich findet das Ticket über "
                          f"die Kennung am Anfang des Titels")]
    gefunden = []
    kennung, rest = treffer.groups()
    if not SCHLUESSEL[ebene].match(kennung):
        gefunden.append(("title", f"der Titel beginnt mit {kennung!r}, die "
                                  f"Stufe '{STUFE[ebene]}' verlangt die Form "
                                  f"{FORM[ebene]}"))
    schluessel = [t for t in re.split(r"</li>|</h[12]>|</p>|\n", text)
                  if "Schlüssel:" in t]
    if schluessel:
        wert = zeilenwert(schluessel[0], "Schlüssel:")
        if "<" not in wert and wert != kennung:
            gefunden.append(("title", f"der Titel trägt {kennung!r}, die Zeile "
                                      f"'Schlüssel:' {wert!r} — dann ist nicht "
                                      f"entschieden, welches Ticket es ist"))
    if GEWERK_IM_TITEL.search(rest):
        gefunden.append(("title", f"{titel!r} nennt das Gewerk — es steht nie "
                                  f"im Namen, sondern in der Komponente und im "
                                  f"Block 'Angaben für ‹Gewerk›' (§281)"))
    # Der Shop-Bezug steht hinten am Titel der Story (§307). In der zweiten Proberunde (10.10.2026)
    # fehlte er an Stories, deren Anforderung `shops` trug, in einem Projekt mit zwei Shops.
    if repo is not None and ebene != "subtask" and SCHLUESSEL[ebene].match(kennung):
        bezug, warum = shop_bezug(repo, kennung)
        if warum:
            gefunden.append(("shops", f"der Shop-Bezug zu {kennung!r} ist nicht zu bestimmen: {warum}"))
        elif bezug and not titel.endswith(bezug):
            gefunden.append(("shops", f"{titel!r} endet nicht auf {bezug.strip()!r} — der Shop-Bezug "
                                      f"steht hinten am Titel, aus `shops` der Anforderung; die Zeile "
                                      f"gibt repo_objects.py (§307)"))
    return gefunden


def punkte(rumpf):
    """Die Listenpunkte eines Blocks, ohne Tags, in Markdown wie in der HTML-Form des Kanals."""
    if re.search(r"<li[\s>]", rumpf, re.I):
        roh = re.findall(r"<li[^>]*>(.*?)</li>", rumpf, re.I | re.S)
    else:
        roh = [z.strip()[2:] for z in rumpf.splitlines() if z.strip().startswith(("- ", "* ", "+ "))]
    return [entmaskieren(HTML_TAG.sub("", p)).strip() for p in roh]


def pruefe_loesungsansatz(text, sprache):
    """Der Block 'Lösungsansatz' (§312): zuerst die Klassifizierung, keine Kennungen."""
    namen = KLASSIFIZIERUNG + OHNE_WEG
    if sprache == "en":
        namen = tuple(VOKABULAR_EN[n] for n in namen)
    mit_namen = tuple(VOKABULAR_EN[n] for n in MIT_NAMEN) if sprache == "en" else MIT_NAMEN
    gefunden = []
    for block, rumpf in bloecke(text):
        if block != "Lösungsansatz":
            continue
        liste = punkte(rumpf)
        erster = liste[0] if liste else ""
        if not erster.startswith(namen):
            gefunden.append(("approach_class", f"der erste Punkt im 'Lösungsansatz' ist "
                                               f"{erster[:40]!r}, keine Klassifizierung — je "
                                               f"Klassifizierung ein Punkt mit ihrer Anzeige aus "
                                               f"dem Datalayer-Vertrag (§312, §324)"))
        # Kein Ticket verlinkt den Entwurf, auch nicht unter 'Epic Page:' (§312). In der zweiten
        # Proberunde (10.10.2026) stand dort die Adresse des Google-Docs. Gesucht wird in der Zeile
        # mit ihren Tags: in der HTML-Form steht die Adresse im href.
        for zeile in re.split(r"</li>|\n", rumpf):
            if re.search(r"Epic [Pp]age:", zeile) and "docs.google.com" in zeile:
                gefunden.append(("epic_page", "die Zeile 'Epic Page:' zeigt auf den Entwurf "
                                              "(docs.google.com) — sie verlinkt die Epic Page in "
                                              "Confluence; fehlt die, läuft erst solution-epic-page "
                                              "(§312, §313)"))
        for p in liste:
            name = next((n for n in mit_namen if p == n or p.startswith(n + ":") or p.startswith(n + " ")),
                        None)
            if name and not re.match(re.escape(name) + r":\s*\S", p):
                gefunden.append(("approach_class", f"{p[:40]!r} nennt keinen Namen — bei {name!r} steht "
                                                   f"der Name in der Zeile: '- {name}: ‹Name›' "
                                                   f"(§312, §324)"))
        for p in liste:
            if p.startswith(("Epic Page:", "Epic page:")):
                continue
            kennung = KENNUNG.search(p)
            if kennung:
                gefunden.append(("approach_id", f"{kennung.group(0)!r} steht im 'Lösungsansatz' — "
                                                f"die Kurzbeschreibung trägt keine Kennungen und "
                                                f"keine Zuteilung an Gewerke (§312)"))
    return gefunden


# Die User Story (§323): eine Ableitung aus Ist, Soll, FC und UC nach .claude/docs/user-story-contract.md,
# an Story und Subtask nie leer, nie 'offen', und in der Form der Sprache des Projekts.
USER_STORY_FORM = {"de": re.compile(r"^Als\s+\S.*?\s+möchte ich\s+\S", re.S),
                   "en": re.compile(r"^As\s+\S.*?\bI want\s+\S", re.S)}
USER_STORY_MUSTER = {"de": "Als ‹Rolle› möchte ich ‹Ziel›, damit ‹Nutzen›.",
                     "en": "As ‹role›, I want ‹goal› so that ‹benefit›."}


def pruefe_user_story(text, sprache):
    """Der Block 'User Story' an Story und Subtask: ein Satz in der Form des Vertrags (§323)."""
    gefunden = []
    for block, rumpf in bloecke(text):
        if block != "User Story":
            continue
        satz = entmaskieren(HTML_TAG.sub(" ", rumpf))
        satz = re.sub(r"^\s*[-*+]\s+", "", satz.strip())
        satz = re.sub(r"\s+", " ", satz).strip()
        if not satz:
            gefunden.append(("user_story", "der Block 'User Story' ist leer — die User Story wird aus "
                                           "Ist, Soll, FC und UC abgeleitet oder aus der Epic-Datei "
                                           "abgeschrieben (§323)"))
        elif re.fullmatch(r"(?i)(offen|open)[.!]?", satz):
            gefunden.append(("user_story", f"der Block 'User Story' trägt {satz!r} — eine User Story ist "
                                           f"nie offen, sie wird abgeleitet (§323)"))
        elif not USER_STORY_FORM[sprache].match(satz):
            gefunden.append(("user_story", f"{satz[:50]!r} hat nicht die Form "
                                           f"'{USER_STORY_MUSTER[sprache]}' (§323, "
                                           f"user-story-contract.md)"))
    return gefunden


def pruefe(ebene, text, titel=None, sprache="de", repo=None):
    erwartet = EBENEN[ebene]
    verstoesse = []

    def melde(regel, detail):
        verstoesse.append(f"{regel} — {detail}")

    text, fremd = uebersetzen(text, sprache)
    for name in fremd:
        melde("language", f"die Überschrift {name!r} gehört nicht zur Sprache {sprache!r} — "
                          f"Überschriften stehen in der Sprache aus `language`, übersetzt nur in "
                          f"der Vorlage (§295, ref-ticket-templates.md)")
    gefunden = ueberschriften(text)

    fehlend = [b for b in erwartet
               if b not in gefunden and b not in OPTIONAL]
    if fehlend:
        melde("Blockfolge", f"es fehlen: {', '.join(fehlend)}. Die Vorlage "
                            f"der Ebene '{STUFE[ebene]}' führt sie "
                            f"(ref-ticket-templates.md)")
    fremd = [b for b in gefunden if b not in erwartet]
    if ebene == "story-split" and ANGABEN in fremd:
        melde("Blockfolge", "'Angaben für' an einer Story mit mehreren "
                            "Gewerken — die Angaben stehen je Gewerk an "
                            "seinem Subtask, die Story trägt den "
                            "übergreifenden 'Lösungsansatz' (§281)")
        fremd = [b for b in fremd if b != ANGABEN]
    if fremd:
        melde("Blockfolge", f"nicht vorgesehen auf dieser Ebene: "
                            f"{', '.join(fremd)}. Ein Block, den die Vorlage "
                            f"nicht führt, kommt nicht ins Ticket — auch "
                            f"nicht als bessere Idee")
    # Die Reihenfolge ist Vertrag, nicht Geschmack: derselbe Block steht auf
    # beiden Ebenen an derselben Stelle.
    ordnung = [b for b in gefunden if b in erwartet]
    if ordnung and ordnung != [b for b in erwartet if b in ordnung]:
        melde("Reihenfolge", f"die Blöcke stehen in anderer Ordnung als die "
                             f"Vorlage: {' → '.join(ordnung)}")

    if TABELLE.search(text):
        melde("Auszeichnung", "eine Tabelle — im Ticket stehen ihre Spalten zu "
                              "schmal, und die Kriterien einer Zelle laufen "
                              "in eine Zeile; die Anforderungen stehen als "
                              "Block je Anforderung (§222)")

    if TIEFER.search(text):
        melde("Auszeichnung", "eine Überschrift tiefer als Ebene 2 — der "
                              "Kanal-Vertrag führt nur Überschrift 1 und 2; "
                              "die sechs Punkte bleiben Listenpunkte")

    # Die Identität. Daran hängt, ob ein zweiter Lauf dieses Ticket
    # wiedererkennt — ohne sie legt er es ein zweites Mal an.
    # Der Body des Kanals ist EINE Zeile (ref-asana.md) — nach Zeilen zu
    # trennen fände dort alles auf einmal und jeder Link irgendwo im Text
    # gälte als Link um den Schlüssel. Getrennt wird deshalb am Element.
    teile = re.split(r"</li>|</h[12]>|</p>|\n", text)
    schluessel = [t for t in teile if "Schlüssel:" in t]
    # Im Expert Service trägt das Epic keine Epic-ID und damit keine Schlüssel-Zeile (§220).
    if not schluessel and ebene == "epic":
        pass
    elif not schluessel:
        melde("Identität", "die Zeile 'Schlüssel: <schluessel>' fehlt im "
                            "Block 'Kontext' — ohne sie ist das Ticket für "
                            "den Abgleich nicht identifiziert und wird beim "
                            "nächsten Lauf ein zweites Mal angelegt")
    else:
        if len(schluessel) > 1:
            melde("Identität", "mehr als eine Schlüssel-Zeile — dann ist "
                                "nicht entschieden, welche gilt")
        if "](" in schluessel[0] or "<a " in schluessel[0].lower():
            melde("Identität", "der Schlüssel steht in einem Linktext — im "
                                "Plaintext des Kanals wird der Linktext durch "
                                "die URL ersetzt und der Schlüssel ist für "
                                "den Abgleich unsichtbar")
        wert = zeilenwert(schluessel[0], "Schlüssel:")
        if "<" not in wert and not SCHLUESSEL[ebene].match(wert):
            melde("Identität", f"der Schlüssel {wert!r} hat nicht die Form "
                                f"{FORM[ebene]} (§281) — der Abgleich vergleicht "
                                f"exakt und fände das Ticket nicht wieder")
        if ebene in UNTER_EPIC and gefunden and gefunden[-1] != "Kontext":
            melde("Identität", "'Kontext' ist nicht der letzte Block — der "
                                "Schlüssel steht zuletzt, weil darüber "
                                "Menschen Links ergänzen")

    # Die Beauftragung steht an jedem Ticket, nicht nur am Epic (§221): die
    # Kennung zählt je Repo, und auf einem Board mit einem zweiten Vorhaben
    # stehen dieselben EP-… und REQ-… mehrmals (Probe 0.5, 10.10.2026). Eigen
    # ist ein Ticket erst, wenn Schlüssel und Beauftragung passen.
    beauftragung = [t for t in teile if "Beauftragung:" in t]
    if not beauftragung:
        melde("Beauftragung", "die Zeile 'Beauftragung: <key>' fehlt im Block "
                              "'Kontext' — ohne sie zählt kein Lauf das Ticket "
                              "als eigenes"
                              + (", und im Expert Service findet ihn keiner wieder"
                                 if ebene == "epic" else
                                 "; der Schlüssel allein kollidiert auf einem Board "
                                 "mit einem zweiten Vorhaben"))
    else:
        if len(beauftragung) > 1:
            melde("Beauftragung", "mehr als eine Zeile 'Beauftragung:' — dann "
                                  "ist nicht entschieden, wem das Ticket gehört")
        if "](" in beauftragung[0] or "<a " in beauftragung[0].lower():
            melde("Beauftragung", "die Beauftragung steht in einem Linktext — "
                                  "im Plaintext des Kanals wäre sie unsichtbar")
        wert = zeilenwert(beauftragung[0], "Beauftragung:")
        if "<" not in wert and not BEAUFTRAGUNG.match(wert):
            melde("Beauftragung", f"{wert!r} ist kein key eines Vorhabens "
                                  f"aus project.yml (etwa 'relaunch') — der "
                                  f"Abgleich vergleicht exakt")

    if ebene in UNTER_EPIC:
        # Die Design-Referenz wird NICHT verlangt: es gibt Projekte ohne
        # Entwurf, und dort gibt es keine. Geprüft wird
        # allein, dass keine leere Hülle dasteht -- eine Zeile mit "TODO" oder
        # einem Strich behauptet eine Referenz, die niemand hat.
        referenz = [t for t in re.split(r"</li>|\n", text)
                    if "Design-Referenz:" in t]
        wert = zeilenwert(referenz[0], "Design-Referenz:") if referenz else ""
        if referenz and (not wert or wert in ("—", "-", "TODO")):
            melde("Design-Referenz", "'Design-Referenz:' steht da und ist "
                                     "leer — gibt es keine, fällt die Zeile "
                                     "weg statt einen Platzhalter zu tragen")
        elif referenz and not REFERENZ.match(wert):
            melde("Design-Referenz", f"{wert!r} ist keine der zwei Formen — "
                                     f"'aus <Schlüssel des UX/UI-Subtasks>' oder "
                                     f"die Adresse des Frames")

        # Das Gewerk im Block 'Angaben für ‹Gewerk›' ist eines der vier.
        for a, b in H2.findall(text):
            name = entmaskieren((a or b).strip())
            if name.startswith(ANGABEN + " "):
                gewerk = name[len(ANGABEN) + 1:].strip()
                if gewerk not in GEWERKE and "<" not in gewerk:
                    melde("Gewerk", f"'{name}' nennt kein Gewerk "
                                    f"({', '.join(GEWERKE)}); wie es auf dem "
                                    f"Board heißt, bildet der Board-Vertrag ab")

    if ebene == "epic":
        for block, rumpf in bloecke(text):
            if entmaskieren(block) != "Anforderungen":
                continue
            for zeile in re.split(r"</li>|<li>|\n", rumpf):
                zeile = entmaskieren(HTML_TAG.sub(" ", zeile)).strip()
                zeile = re.sub(r"^[-*+]\s+", "", zeile).strip("* ")
                if zeile and not ANFORDERUNG.match(zeile):
                    melde("requirement_line", f"{zeile[:50]!r} steht unter "
                          f"'Anforderungen' — das Epic-Ticket trägt je "
                          f"Anforderung nur ID und Titel ('REQ-012 Titel'); "
                          f"User Story und Kriterien stehen an der Story (§281)")

    if ebene in UNTER_EPIC and (titel is not None or ebene == "subtask"):
        for regel, detail in pruefe_titel(ebene, titel, text, repo):
            melde(regel, detail)

    for regel, detail in zusammenlaufend(text):
        melde(regel, detail)

    for block, wert in platzhalter(text):
        wo = f"im Block '{entmaskieren(block)}'" if block else "vor dem ersten Block"
        melde("Platzhalter", f"{wert!r} steht {wo} — ein Platzhalter der Vorlage "
                             f"wird vor dem Senden ersetzt; fehlt der Wert, steht "
                             f"'offen' oder die Zeile entfällt")

    # Der 'Lösungsansatz' nennt das Gewählte, nicht seine Herkunft. Geprüft
    # wird der Teil davon, der eine Form hat: ein Datum und die Wörter, mit
    # denen eine Hausregel eingeleitet wird. Gemessen am angelegten Ticket
    # UX-004 (28.08.2026): dort stand 'das seit dem 21.08.2026 die Vorgabe für
    # neue Projekte ist' -- ein Datum unserer Ablauforganisation, an dem
    # niemand etwas umsetzt. Warum die Alternative fiel, ist nicht prüfbar und
    # bleibt eine Regel der Vorlage.
    for block, rumpf in bloecke(text):
        if block != "Lösungsansatz":
            continue
        if HERKUNFT_DATUM.search(rumpf):
            melde("Herkunft", "im 'Lösungsansatz' steht ein Datum — seit wann "
                              "etwas bei uns gilt, ist unsere Ablauforganisation "
                              "und macht das Ticket nicht ausführbarer; der "
                              "Grund steht in der Lösung des Epics und in der ADR")
        for wort in HERKUNFT_WORTE + (HERKUNFT_WORTE_EN if sprache == "en" else ()):
            treffer = re.search(wort, rumpf, re.I)
            if treffer:
                melde("Herkunft", f"im 'Lösungsansatz' steht "
                                  f"{treffer.group(0)!r} — der Block sagt, was "
                                  f"gebaut wird und womit, nicht warum unsere "
                                  f"Regel hier greift")

    for regel, detail in pruefe_loesungsansatz(text, sprache):
        melde(regel, detail)

    if ebene in UNTER_EPIC:
        for regel, detail in pruefe_user_story(text, sprache):
            melde(regel, detail)

    # Stunden und Preise stehen in keiner Datei und in keinem Ticket (§141).
    # Gesucht wird nach dem, was nur aus einer Schätzung stammen kann — nicht
    # nach 'Stunden': eine Frist ist eine Regel und darf im Body stehen. Auch
    # nicht nach einem Betrag an sich: ein Versandtarif oder eine Freigrenze
    # des Shops ist eine Angabe für Konfig (gemessen am 30.09.2026, dort fiel
    # '4,90 €' als Kalkulation durch). Gesperrt ist der Aufwand und sein Preis.
    kalkulation = list(KALKULATION.finditer(text))
    if sprache == "en":
        kalkulation += list(KALKULATION_EN.finditer(text))
    for treffer in kalkulation:
        melde("Kalkulation", f"{treffer.group(0)!r} steht im Body — Aufwand "
                             f"und Preis des Projekts gehören nie auf ein "
                             f"Board, das der Kunde sieht, auch keine Größe "
                             f"(§166)")

    groesse = GROESSE.search(text) or (GROESSE_EN.search(text) if sprache == "en" else None)
    if groesse:
        melde("Kalkulation", f"{groesse.group(0)!r} steht im Body — eine Größe "
                             f"steht nur im Größenfeld des Boards, wo es eines "
                             f"gibt, nie im Text")

    return verstoesse


def main():
    args, titel, sprache, repo = sys.argv[1:], None, "de", None
    if "--language" in args:
        i = args.index("--language")
        sprache = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
        if sprache not in SPRACHEN:
            print(f"Aufruf: --language ist {' oder '.join(SPRACHEN)}, wie `language` in "
                  f"project.yml", file=sys.stderr)
            return 2
    if "--title" in args:
        i = args.index("--title")
        titel = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if "--repo" in args:
        i = args.index("--repo")
        repo = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
        if not Path(repo).is_dir():
            print("Aufruf: --repo ist das Projekt-Repo mit project.yml", file=sys.stderr)
            return 2
    split = "--split" in args
    if split:
        args.remove("--split")
    if len(args) != 2 or args[0] not in ("epic", "story", "subtask") \
            or (split and args[0] != "story") \
            or (titel is not None and args[0] == "epic"):
        print("Aufruf: check-ticket-body.py [--language de|en] [--title <Titel>] [--repo <Projekt-Repo>] "
              "<epic|story|story --split|subtask> <datei|->", file=sys.stderr)
        return 2
    ebene = "story-split" if split else args[0]
    quelle = args[1]
    text = sys.stdin.read() if quelle == "-" else \
        Path(quelle).read_text(encoding="utf-8")

    verstoesse = pruefe(ebene, text, titel, sprache, repo)
    for zeile in verstoesse:
        print(zeile)
    if verstoesse:
        print(f"\n{len(verstoesse)} Verstoß/Verstöße — der Body geht so "
              f"nicht aufs Board")
        return 1
    print(f"Blockfolge der Ebene '{STUFE[ebene]}' eingehalten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
