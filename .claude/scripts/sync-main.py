#!/usr/bin/env python3
"""Zieht den Stand von `main` vor einem Lauf, an einer Stelle für alle Skills.

Eine Cloud-Sitzung startet auf einem abgelösten HEAD gleich `origin/main`, und der
lokale `main` steht auf dem Stand, mit dem der Klon angelegt wurde. Ein bloßes
`git pull --ff-only` scheitert dort mit "You are not currently on a branch".
Deshalb unterscheidet das Script vier Lagen:

- auf `main`: `git fetch origin main`, dann `git merge --ff-only origin/main`
  (dasselbe wie `git pull --ff-only`, ohne auf ein Upstream angewiesen zu sein).
- abgelöst und HEAD gleich `origin/main`: ohne Rückfrage `git switch main`,
  dann vorspulen. Nichts geht verloren: HEAD trägt keinen eigenen Commit.
- abgelöst auf einem anderen Commit: Ausgang 3, `Abgelöst`. Der Lauf hält an.
- auf einem anderen Branch ohne eigenen Commit und ohne Änderung an getrackten Dateien:
  ohne Rückfrage `git switch main`, dann vorspulen. So startet eine Cloud-Sitzung heute, auf
  einem eigenen Branch `claude/…` gleich `origin/main`; wie beim abgelösten HEAD geht nichts
  verloren.
- auf einem anderen Branch mit eigenem Commit, der auf dem Remote liegt, und ohne Änderung an
  getrackten Dateien: ohne Rückfrage `git switch main`, dann vorspulen (§396). Der Commit bleibt
  auf seinem Branch, lokal und auf dem Remote; die Zeile nennt Branch und Commit.
- auf einem anderen Branch mit einem Commit, den der Remote nicht hat, oder mit Änderungen:
  Ausgang 2, `Branch`. Der Wechsel ließe Arbeit liegen, die nur in dieser Sitzung steht; der Lauf
  nennt den Branch und fragt, bevor er wechselt.

Scheitert ein git-Befehl, steht seine Meldung wörtlich in der Ausgabe, Ausgang 1
(`Git`). Ausgang 0 heißt: das Repo steht auf `main` gleich `origin/main`.

Bringt das Ziehen eine andere `.claude/template-version` (§338), hat jemand das Template
upgegradet, während diese Sitzung Skills und Regeln des alten Stands im Kontext trägt. Das
Script zieht trotzdem bis zum Ende, merkt sich keinen Startcommit und endet mit Ausgang 4,
`Template`: „Das Template wurde auf <neu> aktualisiert (vorher <alt>); starte eine neue Sitzung.“

Ohne `--ids` (am Start des Laufs) merkt sich das Script danach den Commit, auf dem der Lauf
beginnt, als Ref `refs/strix/run-start` unter `.git/` und nennt ihn in der Zeile
`Startcommit <sha>`. Die Projektion rechnet mit ihm als `--base` (§319): committet der Lauf vor der
Projektion, etwa weil der Stop-Hook der Cloud-Sitzung es verlangt, erscheinen seine Werte als
`ÄNDERN`, nicht als `ABWEICHUNG`. Mit `--ids` bleibt die Ref, wie sie ist.

Mit `--ids` (vor der Projektion, §309) prüft das Script auf `main` nach dem Fetch und
vor dem Vorspulen die neuen Kennungen des Laufs gegen `origin/main`: Anforderungen, offene
Fragen, ADRs und Aufgaben in `todo/`, deren Datei es seit dem gemeinsamen Stand mit
`origin/main` nur hier gibt. Trägt `origin/main` dieselbe Kennung aus einem anderen
Lauf, bekommt die Datei dieses Laufs die nächste freie Nummer (eine Aufgabe in
`todo/` die Endung `-2`, `-3` …), und jeder Verweis in den Dateien des Laufs (neu
oder geändert gegen HEAD) wird umgeschrieben. Je Umnummerierung eine Zeile
`Kennung GAP-015 → GAP-021 (…)`. Danach spult das Script vor wie ohne Option; eine
gleichnamige Datei hielte das Vorspulen sonst an.

Aufruf: sync-main.py [<repo>] [--ids]
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Der Commit, auf dem der Lauf begann: Basis der Projektion (§319).
START_REF = "refs/strix/run-start"

# Ändert das Ziehen sie, hält der Lauf an (§338).
VERSION_FILE = ".claude/template-version"

# Ordner und Muster des Dateinamens je Art, deren Kennung ein Lauf selbst vergibt (§309).
NEW_IDS = {
    "requirements": re.compile(r"^(REQ)-(\d{3})\.md$"),
    "gaps": re.compile(r"^(GAP)-(\d{3})\.md$"),
    "decisions": re.compile(r"^(ADR)-(\d{3})-[a-z0-9-]+\.md$"),
    "todo": re.compile(r"^(\d{4}-\d{2}-\d{2}-[a-z0-9-]+)\.md$"),
}


def git(repo, *args):
    lauf = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return lauf.returncode, (lauf.stdout + lauf.stderr).strip()


def scheitert(befehl, meldung):
    print(f"Git — `git {befehl}` scheitert:\n{meldung}")
    return 1


def names(repo, rev, folder):
    """Die Dateinamen eines Ordners im Stand <rev>, ohne Unterordner."""
    _, out = git(repo, "ls-tree", "--name-only", rev, f"{folder}/")
    return {Path(p).name for p in out.split("\n") if p}


def key(folder, name):
    """Die Kennung einer Datei: REQ-001, GAP-015, ADR-002, bei todo der Name ohne Endung."""
    m = NEW_IDS[folder].match(name)
    if not m:
        return None
    return m.group(1) if folder == "todo" else f"{m.group(1)}-{m.group(2)}"


def renumber(repo, ziel):
    """Zählt die neuen Kennungen dieses Laufs weiter, die origin/main schon trägt (§309)."""
    _, basis = git(repo, "merge-base", "HEAD", ziel)
    work = Path(repo)
    mapping, moves = {}, []
    for folder in NEW_IDS:
        here = {f.name for f in (work / folder).glob("*.md")} if (work / folder).is_dir() else set()
        before = {key(folder, n) for n in names(repo, basis, folder)}
        theirs = {key(folder, n) for n in names(repo, ziel, folder)}
        taken = ({key(folder, n) for n in here} | theirs) - {None}
        for name in sorted(here):
            k = key(folder, name)
            if k is None or k in before or k not in theirs:
                continue
            if folder == "todo":
                n = 2
                while f"{k}-{n}" in taken:
                    n += 1
                new_key, new_name = f"{k}-{n}", f"{k}-{n}.md"
            else:
                prefix = k.split("-")[0]
                n = max(int(t.split("-")[1]) for t in taken if t and t.startswith(prefix)) + 1
                new_key = f"{prefix}-{n:03d}"
                new_name = name.replace(k, new_key, 1)
            taken.add(new_key)
            mapping[k] = new_key
            moves.append((folder, name, new_name))
    if not mapping:
        return 0, []
    for folder, old, new in moves:
        src, dst = f"{folder}/{old}", f"{folder}/{new}"
        if git(repo, "ls-files", "--error-unmatch", src)[0] == 0:
            code, meldung = git(repo, "mv", src, dst)
            if code:
                return scheitert(f"mv {src} {dst}", meldung), []
        else:
            os.rename(work / src, work / dst)
    # Die Dateien des Laufs: geändert gegen HEAD, vorgemerkt oder nicht, und neue.
    _, changed = git(repo, "diff", "--name-only", "-z", "HEAD")
    _, others = git(repo, "ls-files", "-z", "--others", "--exclude-standard")
    files = sorted({f for f in (changed + "\0" + others).split("\0") if f})
    # Eine Nummer endet vor der nächsten Ziffer (ADR-002-slug.md trifft), ein todo-Name vor dem nächsten Wortteil.
    pattern = re.compile("|".join(
        rf"(?<![\w-])({re.escape(k)})" + (r"(?!\d)" if re.match(r"^[A-Z]+-\d{3}$", k) else r"(?![\w-])")
        for k in sorted(mapping, key=len, reverse=True)))
    touched = {}
    for f in files:
        path = work / f
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        found = {m.group(m.lastindex) for m in pattern.finditer(text)}
        if found:
            path.write_text(pattern.sub(lambda m: mapping[m.group(m.lastindex)], text), encoding="utf-8")
            for old in found:
                touched.setdefault(old, []).append(f)
    lines = []
    for folder, old, new in moves:
        k = key(folder, old)
        where = touched.get(k, [])
        lines.append(f"Kennung {k} → {mapping[k]} ({folder}/{old} → {folder}/{new}; "
                     f"Verweise in {len(where)} Datei{'en' if len(where) != 1 else ''}"
                     + (f": {', '.join(sorted(where))}" if where else "") + ")")
    return 0, lines


def version(repo, rev="HEAD"):
    """Die Template-Version im Stand <rev>; "keine", wenn die Datei fehlt (§338)."""
    code, out = git(repo, "show", f"{rev}:{VERSION_FILE}")
    return out.strip() if code == 0 and out.strip() else "keine"


def frisch(repo):
    """Wahr, wenn HEAD keinen Commit trägt, den origin/main nicht hat, und keine getrackte Datei ändert."""
    code, _ = git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/main")
    if code:
        return False
    code, aenderungen = git(repo, "status", "--porcelain", "--untracked-files=no")
    return code == 0 and not aenderungen


def gesichert(repo, branch):
    """Wahr, wenn HEAD auf origin/<branch> liegt und keine getrackte Datei ändert (§396)."""
    code, _ = git(repo, "fetch", "origin", branch)
    if code:
        return False
    code, _ = git(repo, "merge-base", "--is-ancestor", "HEAD", f"origin/{branch}")
    if code:
        return False
    code, aenderungen = git(repo, "status", "--porcelain", "--untracked-files=no")
    return code == 0 and not aenderungen


def ids_pruefen(repo):
    """Nennt jede Umnummerierung; 1, wenn ein git-Befehl scheitert."""
    code, umnummeriert = renumber(repo, "origin/main")
    for zeile in umnummeriert:
        print(zeile)
    return code


def main():
    args = [a for a in sys.argv[1:] if a != "--ids"]
    ids = "--ids" in sys.argv[1:]
    repo = args[0] if args else "."
    code, meldung = git(repo, "fetch", "origin", "main")
    if code:
        return scheitert("fetch origin main", meldung)
    _, ziel = git(repo, "rev-parse", "origin/main")
    vorher = version(repo)
    code, branch = git(repo, "symbolic-ref", "-q", "--short", "HEAD")
    if code:
        _, kopf = git(repo, "rev-parse", "HEAD")
        if kopf != ziel:
            print(f"Abgelöst — HEAD steht abgelöst auf {kopf[:7]}, nicht auf "
                  f"origin/main ({ziel[:7]}); der Lauf hält an")
            return 3
        code, meldung = git(repo, "switch", "main")
        if code:
            return scheitert("switch main", meldung)
        print(f"HEAD stand abgelöst auf origin/main ({ziel[:7]}); gewechselt auf main")
    elif branch != "main":
        if frisch(repo):
            zeile = f"Branch '{branch}' trug keinen eigenen Commit; gewechselt auf main"
        elif gesichert(repo, branch):
            _, kopf = git(repo, "rev-parse", "HEAD")
            zeile = (f"Branch '{branch}' trägt eigene Commits, zuletzt {kopf[:7]}; sie bleiben "
                     f"dort und auf origin/{branch}; gewechselt auf main")
        else:
            print(f"Branch — das Repo steht auf '{branch}', nicht auf main, mit einem Commit, "
                  f"den der Remote nicht hat, oder mit Änderungen; der Lauf fragt, bevor er wechselt")
            return 2
        code, meldung = git(repo, "switch", "main")
        if code:
            return scheitert("switch main", meldung)
        print(zeile)
    elif ids and ids_pruefen(repo):
        return 1
    code, meldung = git(repo, "merge", "--ff-only", "origin/main")
    if code:
        return scheitert("merge --ff-only origin/main", meldung)
    nachher = version(repo)
    if nachher != vorher:
        print(f"Template — Das Template wurde auf {nachher} aktualisiert (vorher {vorher}); "
              f"starte eine neue Sitzung.")
        return 4
    print(f"main steht auf origin/main ({ziel[:7]})")
    if not ids:
        _, start = git(repo, "rev-parse", "HEAD")
        code, meldung = git(repo, "update-ref", START_REF, start)
        if code:
            return scheitert(f"update-ref {START_REF} {start}", meldung)
        print(f"Startcommit {start[:7]} ({START_REF})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
