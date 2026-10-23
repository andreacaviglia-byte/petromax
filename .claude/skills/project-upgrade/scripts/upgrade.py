#!/usr/bin/env python3
"""Führt ein Projekt-Repo vom Stand einer Template-Version auf den einer neueren (§237).

Aufruf:
    upgrade.py latest <url>                               die höchste Version unter den Tags vX.Y.Z, ohne v
    upgrade.py plan <projekt> <alt> <neu> <arbeit>        vergleicht je Datei alt, neu und Projekt
    upgrade.py apply <projekt> <arbeit> [--delete <pfad>]... [--skip <pfad>]...
                                                          überträgt den Plan ins Projekt
    upgrade.py settled <projekt> <arbeit> <pfad>          eine ausgelassene Datei ist geschrieben

<alt> und <neu> sind Klone des Templates bei den Tags der beiden Versionen; <arbeit> ist ein Ordner
außerhalb des Projekts. plan schreibt <arbeit>/plan.json und je Datei, die sich im Projekt ändert,
die vorgeschlagene Fassung nach <arbeit>/files/<pfad>. Verglichen werden die Dateien, die git in alt
oder neu führt. Eine Datei, die in keinem von beiden liegt (Datalayer, eigene Skills), fasst das
Script nie an.

Fälle je Datei, die Folge nach §237:
    replace    Projekt gleich alt: die neue Fassung kommt
    keep       nur das Projekt weicht ab: die Fassung des Leads bleibt
    merge      beide weichen ab, an verschiedenen Stellen: git merge-file ergibt die neue Fassung
               mit der Änderung des Leads darin
    conflict   beide weichen ab, an derselben Stelle, oder eine neue Datei trifft auf eine andere am
               selben Pfad: die Fassung trägt Konfliktmarken, das Modell schlägt eine vor
    add        neu im Template: sie kommt dazu
    remove     im Template entfernt, im Projekt gleich alt: sie geht
    ask        im Template entfernt, im Projekt geändert: sie bleibt, bis apply sie mit --delete nennt
    deleted    im Projekt gelöscht: sie bleibt gelöscht
    projection eine Projektion (way-of-working.md, §286): apply schreibt sie nie; der Lauf projiziert
               sie danach aus dem neuen Standard und way-of-working/ neu
    unchanged  im Projekt steht schon die neue Fassung
.claude/template-version, CHANGELOG.md und der Standard der Arbeitsweise
.claude/way-of-working-standard.md pflegt der Lead nicht: sie sind immer replace. Die Abweichungen
des Projekts in way-of-working/ liegen nicht im Template und bleiben unberührt (§286).

Ausgelassene Dateien: apply schreibt eine Datei aus dem Plan nicht, die --skip nennt, etwa
.claude/settings.json, die der Lauf nach einem eigenen Ja selbst schreibt. Ihre Basis, die Fassung
des Templates, von der das Projekt noch ausgeht, kommt nach .claude/upgrade-pending.json. Das
nächste plan vergleicht die Datei gegen diese Basis statt gegen den alten Klon; sonst sähe der alte
Stand wie eine Änderung des Leads aus (keep). Nach apply trägt die Datei genau die Dateien, die
dieses apply ausließ. settled prüft, dass die Datei im Projekt der Fassung im Arbeitsordner gleicht,
und nimmt ihren Eintrag heraus. Ohne Eintrag gibt es die Datei nicht.

Prüfungen: template_version, workdir, git, plan, markers, delete, skip, settled, pending, tags. Ausgabe je Befund eine Zeile
"<prüfung>: <detail>". plan druckt je Datei außer unchanged eine Zeile "<fall> <pfad>", mit
"markers", wenn die Fassung Konfliktmarken trägt.

Exit 0: geschrieben (plan: ohne Datei, die der Lead entscheidet). Exit 1: ein Befund; plan schreibt
dann keinen Plan, apply nichts ins Projekt. Exit 2: falscher Aufruf. Exit 3 (nur plan): der Plan ist
geschrieben und trägt conflict oder ask.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ALWAYS_NEW = {".claude/template-version", "CHANGELOG.md", ".claude/way-of-working-standard.md"}
PROJECTION = {"way-of-working.md"}
WRITE = {"replace", "add", "merge", "conflict"}
DECIDE = {"conflict", "ask"}
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
TAG = re.compile(r"refs/tags/v(\d+\.\d+\.\d+)$")
MARKER = re.compile(rb"^(<<<<<<<|>>>>>>>)( |$)", re.M)
PENDING = ".claude/upgrade-pending.json"


class Befund(Exception):
    pass


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if r.returncode != 0:
        raise Befund(f"git: git {' '.join(args)} scheitert: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout


def version_von(wurzel, wer):
    datei = wurzel / ".claude" / "template-version"
    text = datei.read_text(encoding="utf-8").strip() if datei.is_file() else ""
    if not VERSION.match(text):
        raise Befund(f"template_version: {wer} trägt keine Version in .claude/template-version "
                     f"({text or 'fehlt'}); das Repo stammt nicht aus dem Template (§232)")
    return text


def schluessel(version):
    return tuple(int(t) for t in VERSION.match(version).groups())


def lies(pfad):
    return pfad.read_bytes() if pfad.is_file() and not pfad.is_symlink() else None


def markers(inhalt):
    return bool(inhalt is not None and MARKER.search(inhalt))


def ausgelassene(projekt):
    """Die ausgelassenen Dateien: {pfad: {"from": version, "base": text}} aus PENDING."""
    datei = projekt / PENDING
    if not datei.is_file():
        return {}
    try:
        daten = json.loads(datei.read_text(encoding="utf-8"))["files"]
        assert all(isinstance(e["from"], str) and isinstance(e["base"], str) for e in daten.values())
    except (ValueError, KeyError, TypeError, AssertionError, AttributeError):
        raise Befund(f"pending: {PENDING} ist kein Verzeichnis ausgelassener Dateien; "
                     f"erwartet {{\"files\": {{pfad: {{\"from\": …, \"base\": …}}}}}}")
    return daten


def schreib_ausgelassene(projekt, daten):
    datei = projekt / PENDING
    if daten:
        datei.write_text(json.dumps({"files": daten}, ensure_ascii=False, indent=1, sort_keys=True)
                         + "\n", encoding="utf-8")
    else:
        datei.unlink(missing_ok=True)


def latest(url):
    versionen = set()
    for zeile in git("ls-remote", "--tags", url).decode("utf-8").splitlines():
        m = TAG.search(zeile.split("\t")[-1])
        if m:
            versionen.add(m.group(1))
    if not versionen:
        raise Befund(f"tags: {url} trägt kein Tag der Form vX.Y.Z")
    print(max(versionen, key=schluessel))
    return 0


def zusammen(projekt, alt, neu):
    """git merge-file über drei Fassungen; liefert (Ergebnis, Zahl der Konflikte)."""
    with tempfile.TemporaryDirectory() as tmp:
        dateien = []
        for name, inhalt in (("projekt", projekt), ("alt", alt or b""), ("neu", neu)):
            p = Path(tmp) / name
            p.write_bytes(inhalt)
            dateien.append(str(p))
        r = subprocess.run(["git", "merge-file", "-p", "-L", "projekt", "-L", "alt", "-L", "neu",
                            *dateien], capture_output=True)
    if r.returncode < 0 or r.returncode > 127:
        raise Befund(f"git: git merge-file scheitert: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout, r.returncode


def fall(pfad, a, n, p):
    """Ordnet eine Datei einem Fall aus §237 zu; liefert (Fall, vorgeschlagene Fassung oder None)."""
    if pfad in PROJECTION:
        return ("unchanged", None) if n is None and p is None else ("projection", None)
    if pfad in ALWAYS_NEW and n is not None:
        return ("unchanged", None) if p == n else ("replace", n)
    if n is None:
        if p is None:
            return "unchanged", None
        return ("remove", None) if p == a else ("ask", None)
    if p is None:
        return ("add", n) if a is None else ("deleted", None)
    if p == n:
        return "unchanged", None
    if a is not None and p == a:
        return "replace", n
    if a is not None and a == n:
        return "keep", None
    ergebnis, konflikte = zusammen(p, a, n)
    if konflikte:
        return "conflict", ergebnis
    return ("keep", None) if ergebnis == p else ("merge", ergebnis)


def plan(projekt, alt, neu, arbeit):
    eigene = version_von(projekt, "das Projekt")
    von, nach = version_von(alt, "der alte Klon"), version_von(neu, "der neue Klon")
    if eigene != von:
        raise Befund(f"template_version: das Projekt steht auf {eigene}, der alte Klon auf {von}")
    if schluessel(nach) <= schluessel(von):
        raise Befund(f"template_version: {nach} ist nicht neuer als {von}")
    if arbeit == projekt or projekt in arbeit.parents:
        raise Befund("workdir: der Arbeitsordner liegt im Projekt; Arbeitsdateien liegen außerhalb (§233)")
    if (arbeit / "plan.json").exists() or (arbeit / "files").exists():
        raise Befund(f"workdir: {arbeit} trägt schon einen Plan; jeder Plan bekommt einen frischen Ordner")
    return rechne(projekt, alt, neu, arbeit, von, nach)


def rechne(projekt, alt, neu, arbeit, von, nach):
    """Der Plan ohne die Prüfungen der Versionen; auch für dev/probe-sync.py im Dev-Repo."""
    ausgelassen = ausgelassene(projekt)
    pfade = set()
    for klon in (alt, neu):
        pfade |= {t for t in git("ls-files", "-z", cwd=klon).decode("utf-8").split("\0") if t}
    eintraege = []
    for pfad in sorted(pfade):
        a, n, p = lies(alt / pfad), lies(neu / pfad), lies(projekt / pfad)
        basis = von
        if pfad in ausgelassen:
            a, basis = ausgelassen[pfad]["base"].encode("utf-8"), ausgelassen[pfad]["from"]
        name, fassung = fall(pfad, a, n, p)
        eintraege.append({"path": pfad, "case": name, "markers": markers(fassung), "base": basis,
                          "_text": fassung, "_base": a})
    arbeit.mkdir(parents=True, exist_ok=True)
    for e in eintraege:
        basis = e.pop("_base")
        if e["case"] in WRITE and basis is not None:
            ziel = arbeit / "base" / e["path"]
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_bytes(basis)
        fassung = e.pop("_text")
        if fassung is not None:
            ziel = arbeit / "files" / e["path"]
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_bytes(fassung)
            shutil.copymode(neu / e["path"], ziel)
    (arbeit / "plan.json").write_text(json.dumps({"from": von, "to": nach, "files": eintraege},
                                                 ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    offen = 0
    for e in eintraege:
        if e["case"] != "unchanged":
            print(f"{e['case']:9} {e['path']}" + ("  markers" if e["markers"] else "")
                  + (f"  basis {e['base']}" if e["base"] != von else ""))
        offen += e["case"] in DECIDE
    print(f"{von} auf {nach}: {len(eintraege)} Datei(en), "
          f"{sum(e['case'] == 'unchanged' for e in eintraege)} unverändert, {offen} zu entscheiden")
    return 3 if offen else 0


def apply(projekt, arbeit, loeschen, auslassen=()):
    datei = arbeit / "plan.json"
    if not datei.is_file():
        raise Befund(f"plan: {datei} fehlt; zuerst upgrade.py plan")
    daten = json.loads(datei.read_text(encoding="utf-8"))
    eigene = version_von(projekt, "das Projekt")
    if eigene != daten["from"]:
        raise Befund(f"plan: der Plan führt von {daten['from']}, das Projekt steht auf {eigene}")
    faelle = {e["path"]: e["case"] for e in daten["files"]}
    befunde = []
    for pfad in loeschen:
        if faelle.get(pfad) != "ask":
            befunde.append(f"delete: {pfad} ist im Plan nicht ask ({faelle.get(pfad, 'fehlt')}); "
                           f"gelöscht wird nur, was der Lead nach dem Plan entscheidet")
    basen = {e["path"]: e.get("base", daten["from"]) for e in daten["files"]}
    for pfad in auslassen:
        if faelle.get(pfad) not in WRITE:
            befunde.append(f"skip: {pfad} schreibt der Plan nicht ({faelle.get(pfad, 'fehlt')}); "
                           f"auslassen lässt sich nur, was apply schreiben würde")
        else:
            try:
                (arbeit / "base" / pfad).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                befunde.append(f"skip: {pfad} hat keine Basis als Text im Arbeitsordner; "
                               f"auslassen lässt sich nur eine Textdatei, die es im alten Stand gab")
    ausgelassene(projekt)
    schreiben = [p for p, c in faelle.items() if c in WRITE and p not in auslassen]
    for pfad in schreiben:
        quelle = arbeit / "files" / pfad
        if not quelle.is_file():
            befunde.append(f"plan: {quelle} fehlt")
        elif markers(quelle.read_bytes()):
            befunde.append(f"markers: {pfad} trägt noch Konfliktmarken; erst eine Fassung ohne sie")
    if befunde:
        raise Befund("\n".join(befunde))
    for pfad in schreiben:
        ziel = projekt / pfad
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(arbeit / "files" / pfad, ziel)
        shutil.copymode(arbeit / "files" / pfad, ziel)
    weg = [p for p, c in faelle.items() if c == "remove"] + list(loeschen)
    for pfad in weg:
        ziel = projekt / pfad
        ziel.unlink(missing_ok=True)
        ordner = ziel.parent
        while ordner != projekt and ordner.is_dir() and not any(ordner.iterdir()):
            ordner.rmdir()
            ordner = ordner.parent
    schreib_ausgelassene(projekt, {pfad: {"from": basen[pfad],
                                   "base": (arbeit / "base" / pfad).read_text(encoding="utf-8")}
                            for pfad in auslassen})
    (projekt / ".claude" / "template-version").write_text(daten["to"] + "\n", encoding="utf-8")
    print(f"{daten['from']} auf {daten['to']}: {len(schreiben)} geschrieben, {len(weg)} gelöscht, "
          f"{sum(c == 'ask' for c in faelle.values()) - len(loeschen)} nach Frage behalten"
          + (f", {len(auslassen)} ausgelassen" if auslassen else ""))
    for pfad in auslassen:
        print(f"ausgelassen {pfad}  basis {basen[pfad]}")
    return 0


def settled(projekt, arbeit, pfad):
    ausgelassen = ausgelassene(projekt)
    if pfad not in ausgelassen:
        raise Befund(f"settled: {pfad} steht nicht in {PENDING}")
    fassung = lies(arbeit / "files" / pfad)
    if fassung is None or lies(projekt / pfad) != fassung:
        raise Befund(f"settled: {pfad} im Projekt gleicht nicht der Fassung im Arbeitsordner; "
                     f"der Eintrag bleibt")
    del ausgelassen[pfad]
    schreib_ausgelassene(projekt, ausgelassen)
    print(f"settled {pfad}")
    return 0


def main(argv):
    args = argv[1:]
    try:
        if len(args) == 2 and args[0] == "latest":
            return latest(args[1])
        if len(args) == 5 and args[0] == "plan":
            projekt, alt, neu, arbeit = (Path(a).resolve() for a in args[1:])
            return plan(projekt, alt, neu, arbeit)
        if len(args) >= 3 and args[0] == "apply" and len(args) % 2 == 1 \
                and all(a in ("--delete", "--skip") for a in args[3::2]):
            paare = list(zip(args[3::2], args[4::2]))
            return apply(Path(args[1]).resolve(), Path(args[2]).resolve(),
                         [p for f, p in paare if f == "--delete"],
                         [p for f, p in paare if f == "--skip"])
        if len(args) == 4 and args[0] == "settled":
            return settled(Path(args[1]).resolve(), Path(args[2]).resolve(), args[3])
    except Befund as b:
        print(b)
        return 1
    print(__doc__.split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
