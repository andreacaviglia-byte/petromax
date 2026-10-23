#!/usr/bin/env python3
"""Prüft, ob das Projekt-Repo aus dem Template stammt und ob project.yml dem Vertrag folgt (§229, §232).

Aufruf:
    check-project.py <repo>                     prüft .claude/template-version und project.yml
    check-project.py <repo> --needs a,b.c       dazu: welche der genannten Felder leer sind
    check-project.py <repo> --template-only     nur .claude/template-version (vor dem ersten project.yml)

Prüfungen: template_version, project_yml, schema, key, language, project_type, shops, audience, add_ons,
team, board, confluence, baselines, empty. `team` prüft nur die Form (§360): eine Liste, jede Person
mit `name`; `role`, `github` und `workstream` sind Freitext. Ausgabe je Befund eine Zeile "<prüfung>: <detail>". `baselines` prüft
baselines.yml, wenn es die Datei gibt (§269): je Rechtsraum genau path, sha und read_on.

Eine Warnung, kein Befund: `skill_header` nennt jeden Skill unter .claude/skills/, der nicht aus dem
Template stammt und eine der drei Kopfzeilen nicht trägt: abgeleitet von, gilt für, verantwortlich
(§225, §271). Standard ist ein Skill, den die CLAUDE.md in der Wurzel unter "## Die Skills" in
Backticks nennt; das ist die Liste des Templates, und dev/tests/check-project.py hält sie gleich den
Skills des Templates. Eine Warnung ändert den Exit nicht; sie steht nach den Befunden.

Exit 0: alles da, auch mit Warnung. Exit 1: ein Verstoß, der Lauf hält an. Exit 3: kein Verstoß,
aber ein Feld aus --needs ist leer; der Skill, der es braucht, fragt danach (§229). Exit 2: falscher
Aufruf.

Das Schema steht in .claude/docs/datalayer-contract.md, Abschnitte project.yml und baselines.yml;
dev/tests/check-project.py hält beide gleich. Gelesen wird ohne Fremdbibliothek, weil der Rechner eines Leads kein PyYAML haben
muss; verstanden wird genau die Form des Vertrags: Schlüssel und Werte, eine Ebene Unterschlüssel,
die Listen shops und team mit Einträgen, Listen in eckigen Klammern, Kommentare mit #.
"""
import re
import sys
from pathlib import Path

TOP = {"customer", "key", "title", "language", "project_folder", "project_owner", "project_type",
       "add_ons", "shops", "team", "requirements_sheet", "e2e_sheet", "figma", "confluence", "board"}
SUB = {"confluence": {"cloud_id", "space", "parent_page"}, "board": {"tool", "project"}}
SHOP = {"key", "domain", "plan", "markets", "jurisdiction", "audience"}
AUDIENCE = ("b2c", "b2b", "both")
PROJECT_TYPES = ("project", "expert_service")
ADD_ONS = ("solutioning", "design", "content_migration", "e2e_testing")
KEY = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
SKILL_NAME = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
# Die drei Kopfzeilen eines eigenen Skills (§225), je am Zeilenanfang, gern als Listenpunkt oder fett.
KOPFZEILEN = ("abgeleitet von", "gilt für", "verantwortlich")
BASELINE = ("path", "sha", "read_on")
SHA = re.compile(r"^[0-9a-f]{7,64}$")
DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Fehler(Exception):
    pass


def skalar(text):
    """Ein Wert: ohne Kommentar, ohne Anführungszeichen; [a, b] wird eine Liste."""
    text = text.strip()
    if text.startswith(("'", '"')):
        quote = text[0]
        ende = text.find(quote, 1)
        if ende < 0:
            raise Fehler(f"Anführungszeichen nicht geschlossen: {text}")
        return text[1:ende]
    text = re.sub(r"\s+#.*$", "", text).strip()
    if text.startswith("#"):
        return ""
    if text.startswith("["):
        if not text.endswith("]"):
            raise Fehler(f"Liste nicht geschlossen: {text}")
        return [skalar(t) for t in text[1:-1].split(",") if t.strip()]
    return text


def lies(text):
    """Liest die Form des Vertrags in ein dict. Was nicht in diese Form passt, ist ein Fehler."""
    zeilen = []
    for nr, roh in enumerate(text.split("\n"), 1):
        if not roh.strip() or roh.lstrip().startswith("#"):
            continue
        if "\t" in roh[: len(roh) - len(roh.lstrip())]:
            raise Fehler(f"Zeile {nr}: Tabulator in der Einrückung")
        zeilen.append((nr, len(roh) - len(roh.lstrip()), roh.strip()))
    daten, i = {}, 0
    while i < len(zeilen):
        nr, tiefe, inhalt = zeilen[i]
        if tiefe != 0:
            raise Fehler(f"Zeile {nr}: eingerückt ohne Oberschlüssel")
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", inhalt)
        if not m:
            raise Fehler(f"Zeile {nr}: kein 'schlüssel: wert'")
        name, rest = m.group(1), m.group(2)
        i += 1
        kinder = []
        while i < len(zeilen) and zeilen[i][1] > 0:
            kinder.append(zeilen[i])
            i += 1
        if kinder and skalar(rest) not in ("", []):
            raise Fehler(f"Zeile {nr}: '{name}' hat einen Wert und eingerückte Zeilen")
        if not kinder:
            daten[name] = skalar(rest)
        elif kinder[0][2].startswith("- "):
            daten[name] = liste(kinder)
        else:
            daten[name] = abbildung(kinder)
    return daten


def abbildung(kinder):
    out = {}
    tiefe = kinder[0][1]
    for nr, t, inhalt in kinder:
        if t != tiefe:
            raise Fehler(f"Zeile {nr}: Einrückung passt nicht")
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", inhalt)
        if not m:
            raise Fehler(f"Zeile {nr}: kein 'schlüssel: wert'")
        out[m.group(1)] = skalar(m.group(2))
    return out


def liste(kinder):
    eintraege, aktuell, tiefe = [], None, kinder[0][1]
    for nr, t, inhalt in kinder:
        if t == tiefe and inhalt.startswith("- "):
            aktuell = {}
            eintraege.append(aktuell)
            inhalt = inhalt[2:].strip()
        elif aktuell is None or t <= tiefe:
            raise Fehler(f"Zeile {nr}: Eintrag der Liste ohne '- '")
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", inhalt)
        if not m:
            raise Fehler(f"Zeile {nr}: kein 'schlüssel: wert' im Eintrag")
        aktuell[m.group(1)] = skalar(m.group(2))
    return eintraege


def leer(wert):
    return wert in ("", None, [], {})


def pruefe(daten):
    befunde = []
    for name in daten:
        if name not in TOP:
            befunde.append(f"schema: unbekanntes Feld '{name}'")
    for name, erlaubt in SUB.items():
        wert = daten.get(name, {})
        if wert == "":
            continue
        if not isinstance(wert, dict):
            befunde.append(f"schema: '{name}' ist keine Abbildung")
            continue
        for sub in wert:
            if sub not in erlaubt:
                befunde.append(f"schema: unbekanntes Feld '{name}.{sub}'")
    for name in TOP - {"shops", "team", "add_ons", "confluence", "board"}:
        if isinstance(daten.get(name, ""), (list, dict)):
            befunde.append(f"schema: '{name}' muss ein einzelner Wert sein")
    if not leer(daten.get("key")) and not KEY.match(str(daten["key"])):
        befunde.append(f"key: '{daten['key']}' ist nicht klein, a-z, 0-9, - und _")
    if daten.get("language", "") not in ("", "de", "en"):
        befunde.append(f"language: '{daten['language']}' ist weder de noch en (§202)")
    if daten.get("project_type", "") not in ("", *PROJECT_TYPES):
        befunde.append(f"project_type: '{daten['project_type']}' ist weder project noch expert_service (§303)")
    shops = daten.get("shops", [])
    if not leer(shops):
        if not isinstance(shops, list):
            befunde.append("shops: keine Liste von Einträgen")
        else:
            schluessel = []
            for n, shop in enumerate(shops, 1):
                for feld in shop:
                    if feld not in SHOP:
                        befunde.append(f"shops: Eintrag {n} hat das unbekannte Feld '{feld}'")
                if leer(shop.get("key")):
                    befunde.append(f"shops: Eintrag {n} hat keinen key")
                elif not KEY.match(str(shop["key"])):
                    befunde.append(f"shops: key '{shop['key']}' ist nicht klein, a-z, 0-9, - und _")
                schluessel.append(shop.get("key"))
                if not isinstance(shop.get("markets", []), list):
                    befunde.append(f"shops: Eintrag {n}, markets ist keine Liste")
                if not leer(shop.get("audience")) and shop["audience"] not in AUDIENCE:
                    befunde.append(f"audience: Eintrag {n} hat '{shop['audience']}', "
                                   f"erlaubt sind {', '.join(AUDIENCE)} (§249)")
            doppelt = sorted({k for k in schluessel if k and schluessel.count(k) > 1})
            if doppelt:
                befunde.append(f"shops: key doppelt: {', '.join(doppelt)}")
    team = daten.get("team", [])
    if not leer(team):
        if not isinstance(team, list):
            befunde.append("team: keine Liste von Einträgen (§360)")
        else:
            for n, person in enumerate(team, 1):
                if leer(person.get("name")):
                    befunde.append(f"team: Eintrag {n} hat keinen name (§360)")
    add_ons = daten.get("add_ons", [])
    if not leer(add_ons):
        if not isinstance(add_ons, list):
            befunde.append("add_ons: keine Liste in eckigen Klammern")
        else:
            for a in add_ons:
                if a not in ADD_ONS:
                    befunde.append(f"add_ons: '{a}' ist kein Add-on des Vertrags, erlaubt sind "
                                   f"{', '.join(ADD_ONS)} (§303)")
    board = daten.get("board", {}) or {}
    if isinstance(board, dict) and board.get("tool", "") not in ("", "jira", "asana"):
        befunde.append(f"board: tool '{board['tool']}' ist weder jira noch asana")
    conf = daten.get("confluence", {}) or {}
    if isinstance(conf, dict) and "." in str(conf.get("cloud_id", "")):
        befunde.append("confluence: cloud_id ist ein Hostname, keine UUID")
    return befunde


def pruefe_baselines(daten):
    """baselines.yml (§269): je Rechtsraum ein Eintrag mit genau path, sha und read_on."""
    befunde = []
    if not daten:
        return ["baselines: baselines.yml trägt keinen Rechtsraum"]
    for kennung, eintrag in daten.items():
        if not KEY.match(kennung):
            befunde.append(f"baselines: Rechtsraum '{kennung}' ist nicht klein, a-z, 0-9, - und _")
        if not isinstance(eintrag, dict):
            befunde.append(f"baselines: '{kennung}' trägt keine Felder path, sha, read_on")
            continue
        for feld in eintrag:
            if feld not in BASELINE:
                befunde.append(f"baselines: '{kennung}' hat das unbekannte Feld '{feld}'")
        for feld in BASELINE:
            if leer(eintrag.get(feld)):
                befunde.append(f"baselines: '{kennung}' ohne {feld}")
        pfad = eintrag.get("path", "")
        if not leer(pfad) and pfad != f"minimum-standard/{kennung}.md":
            befunde.append(f"baselines: '{kennung}' liest '{pfad}', erwartet "
                           f"minimum-standard/{kennung}.md")
        sha = eintrag.get("sha", "")
        if not leer(sha) and not SHA.match(str(sha)):
            befunde.append(f"baselines: '{kennung}' hat den sha '{sha}', erwartet hexadezimal, "
                           f"wie get_file_contents ihn nennt")
        datum = eintrag.get("read_on", "")
        if not leer(datum) and not DATUM.match(str(datum)):
            befunde.append(f"baselines: '{kennung}' hat read_on '{datum}', erwartet JJJJ-MM-TT")
    return befunde


def standard_skills(repo):
    """Die Skills des Templates: die Namen in Backticks unter "## Die Skills" der Wurzel-CLAUDE.md."""
    pfad = repo / "CLAUDE.md"
    if not pfad.is_file():
        return set()
    abschnitt = re.search(r"^## Die Skills\s*\n(.*?)(?=^## |\Z)", pfad.read_text(encoding="utf-8"),
                          re.S | re.M)
    return set(SKILL_NAME.findall(abschnitt.group(1))) if abschnitt else set()


def warnungen_skills(repo):
    """Je eigener Skill ohne alle drei Kopfzeilen eine Warnung skill_header (§225, §271)."""
    skills = sorted(p for p in (repo / ".claude" / "skills").glob("*/SKILL.md"))
    if not skills:
        return []
    standard = standard_skills(repo)
    if not standard:
        return ["skill_header: die CLAUDE.md in der Wurzel nennt unter „## Die Skills“ keinen "
                "Skill des Templates; ob ein Skill eigen ist, bleibt ungeprüft"]
    out = []
    for skill in skills:
        name = skill.parent.name
        if name in standard:
            continue
        text = skill.read_text(encoding="utf-8")
        fehlt = [k for k in KOPFZEILEN
                 if not re.search(rf"^\s*(?:[-*]\s+)?(?:\*\*)?{k}(?:\*\*)?\s*:(?:\*\*)?\s*\S",
                                  text, re.M | re.I)]
        if fehlt:
            out.append(f"skill_header: .claude/skills/{name} stammt nicht aus dem Template, und "
                       f"ihm fehlt {', '.join(repr(k) for k in fehlt)}; ein eigener Skill trägt "
                       f"die Kopfzeilen abgeleitet von, gilt für, verantwortlich (§225)")
    return out


def wert(daten, pfad):
    teil = daten
    for stueck in pfad.split("."):
        if not isinstance(teil, dict):
            return ""
        teil = teil.get(stueck, "")
    return teil


def main(argv):
    args = argv[1:]
    if not args or args[0].startswith("--"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    repo = Path(args[0])
    needs, nur_template = [], False
    rest = args[1:]
    while rest:
        if rest[0] == "--needs" and len(rest) > 1:
            needs = [n.strip() for n in rest[1].split(",") if n.strip()]
            rest = rest[2:]
        elif rest[0] == "--template-only":
            nur_template = True
            rest = rest[1:]
        else:
            print(f"unbekanntes Argument: {rest[0]}", file=sys.stderr)
            return 2
    for n in needs:
        kopf = n.split(".")[0]
        if kopf not in TOP or ("." in n and n.split(".", 1)[1] not in SUB.get(kopf, set())):
            print(f"--needs nennt '{n}', das der Vertrag nicht kennt", file=sys.stderr)
            return 2

    befunde = []
    version = repo / ".claude" / "template-version"
    if not version.is_file() or not version.read_text(encoding="utf-8").strip():
        befunde.append("template_version: .claude/template-version fehlt oder ist leer; "
                       "das Repo stammt nicht aus dem Template (§232)")
    warnungen = warnungen_skills(repo)
    if nur_template:
        for b in befunde + warnungen:
            print(b)
        return 1 if befunde else 0

    pfad = repo / "project.yml"
    if not pfad.is_file():
        befunde.append("project_yml: project.yml fehlt; zuerst project-setup")
        daten = None
    else:
        try:
            daten = lies(pfad.read_text(encoding="utf-8"))
        except Fehler as e:
            befunde.append(f"project_yml: {e}")
            daten = None
    if daten is not None:
        befunde += pruefe(daten)
        if leer(daten.get("project_folder")):
            befunde.append("project_folder: leer; ohne Projektordner hat kein Lauf einen Ort (§229)")
    baselines = repo / "baselines.yml"
    if baselines.is_file():
        try:
            befunde += pruefe_baselines(lies(baselines.read_text(encoding="utf-8")))
        except Fehler as e:
            befunde.append(f"baselines: {e}")
    for b in befunde + warnungen:
        print(b)
    if befunde:
        return 1
    leere = [n for n in needs if leer(wert(daten, n))]
    for n in leere:
        print(f"empty: {n}")
    return 3 if leere else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
