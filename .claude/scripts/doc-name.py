#!/usr/bin/env python3
"""Bildet den Namen eines Hauptdokuments aus project.yml: ‹Art› ‹title› – ‹Kunde› (§263, §337).

Aufruf:
    doc-name.py <repo> <art>        art: estimate | proposal | requirements | e2e

Ausgabe auf stdout genau eine Zeile, der Name. Die Art steht in der Sprache aus `language` (§337);
ohne `language` gilt `de`. Das Schätzdokument ist intern und heißt in jeder Sprache deutsch:

    Art           de                     en                     Dokument
    estimate      Aufwandsschätzung      Aufwandsschätzung      das Schätzdokument
    proposal      Solution Proposal      Solution Proposal      das Solution Proposal
    requirements  Anforderungsliste      Requirements list      das Sheet der Anforderungsliste
    e2e           E2E-Tests              E2E tests              das E2E-Sheet

‹title› ist title aus project.yml, wie er dort steht; ein „/“ wird „-“. ‹Kunde› ist customer ohne
die Rechtsform am Ende, sonst unverändert: Groß- und Kleinschreibung und Umlaute bleiben,
überzählige Leerzeichen und ein übrig bleibendes Komma oder „&“ am Ende fallen weg. Zwischen beiden
steht ein Halbgeviertstrich mit Leerzeichen davor und danach. Kein Datum, keine Uhrzeit: jede
Fassung trägt denselben Namen, die Lesezeit steht im Dokument.

Exit 0: der Name. Exit 1: project.yml fehlt oder ist nicht lesbar, oder customer oder title ist
leer, oder von customer bleibt ohne Rechtsform nichts, oder language ist weder de noch en; je Befund
eine Zeile "<prüfung>: <detail>" (project_yml, customer, title, language). Exit 2: falscher Aufruf. Gelesen wird mit dem Leser aus
check-project.py.
"""
import importlib.util
import re
import sys
from pathlib import Path

# Je Art ihr Name in de und en (§337); die deutschen bleiben in 1.x, wie sie sind.
KINDS = {
    "estimate": {"de": "Aufwandsschätzung", "en": "Aufwandsschätzung"},
    "proposal": {"de": "Solution Proposal", "en": "Solution Proposal"},
    "requirements": {"de": "Anforderungsliste", "en": "Requirements list"},
    "e2e": {"de": "E2E-Tests", "en": "E2E tests"},
}

# Längere Formen zuerst, damit "GmbH & Co. KG" nicht als "KG" endet.
LEGAL_FORMS = [
    r"GmbH\s*&\s*Co\.\s*KG", r"UG\s*\(haftungsbeschränkt\)", r"GmbH", r"AG", r"KG", r"OHG", r"UG",
    r"SE", r"e\.\s?K\.", r"Ltd\.", r"Inc\.", r"LLC", r"B\.V\.", r"BV",
]
LEGAL_FORM = re.compile(r"[\s,]+(?:" + "|".join(LEGAL_FORMS) + r")\s*$")


def short_customer(customer):
    """Der Kunde ohne Rechtsform am Ende (§263); leer, wenn nichts übrig bleibt."""
    text = re.sub(r"\s+", " ", customer).strip()
    text = LEGAL_FORM.sub("", text)
    return re.sub(r"[\s,&]+$", "", text)


def doc_name(kind, title, customer, language="de"):
    return f"{KINDS[kind][language]} {title.strip().replace('/', '-')} – {short_customer(customer)}"


def read_project(repo):
    spec = importlib.util.spec_from_file_location(
        "check_project", Path(__file__).with_name("check-project.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    path = repo / "project.yml"
    if not path.is_file():
        raise mod.Fehler("project.yml fehlt; zuerst project-setup")
    return mod.lies(path.read_text(encoding="utf-8"))


def main(argv):
    if len(argv) != 3 or argv[2] not in KINDS:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    repo, kind = Path(argv[1]), argv[2]
    try:
        data = read_project(repo)
    except Exception as e:  # Fehler aus check-project.py oder eine unlesbare Datei
        print(f"project_yml: {e}")
        return 1
    findings = []
    customer, title = data.get("customer", ""), data.get("title", "")
    if not isinstance(customer, str) or not customer.strip():
        findings.append("customer: leer; den Kunden trägt project-setup ein")
    elif not short_customer(customer):
        findings.append(f"customer: von '{customer}' bleibt ohne Rechtsform kein Name")
    if not isinstance(title, str) or not title.strip():
        findings.append("title: leer; den Titel des Vorhabens trägt project-setup ein")
    language = str(data.get("language") or "de").strip()
    if language not in ("de", "en"):
        findings.append(f"language: '{language}' ist weder de noch en (§202)")
    for f in findings:
        print(f)
    if findings:
        return 1
    print(doc_name(kind, title, customer, language))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
