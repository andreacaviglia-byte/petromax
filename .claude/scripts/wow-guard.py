#!/usr/bin/env python3
"""wow-guard: way-of-working/ ändert der project_owner; bei allen anderen fragt der Hook nach (§289,
§301). Hook für Claude Code, PreToolUse.

Greift bei
    Edit, Write   wenn tool_input.file_path unter <repo>/way-of-working/ liegt
    Bash          wenn der Befehl ein `git commit` ist, der eine Datei unter way-of-working/ enthält:
                  die gestagten Dateien (git diff --cached --name-only), bei -a/--all dazu die
                  geänderten getrackten, bei Pfaden nach `commit` dazu deren Änderungen
und vergleicht dann die Person der Sitzung mit `project_owner` aus project.yml. Beim project_owner
lässt er durch (er ändert mit `project-setup`, §299), ebenso bei einer Person mit Admin-Rechten am
Repo bei GitHub: sie hat die Rechte des project_owner (§390). Sonst, auch ohne project_owner, ohne lesbares
project.yml oder ohne Namen der Person, fragt er nach (§301): `permissionDecision: "ask"` mit dem
Hinweis, dass die Person nicht der Owner ist, und dem Weg über `project-status` als Vorschlag; der
Mensch entscheidet. Eine Sperre ist es nicht, die Regel gilt für Claude, nicht für GitHub: wer
außerhalb von Claude Code committet, wird hier nicht geprüft, Git zeigt jede Änderung.

Woher der GitHub-Name der Person kommt: allein aus `gh api user --jq .login`, also aus dem Konto,
dem das GitHub-Token der Sitzung gehört; GitHub selbst beantwortet die Frage. Bewusst nicht genutzt:
    git config user.name    ist kein GitHub-Name, sondern frei gesetzter Text
    git config github.user  setzt jeder, auch Claude selbst, mit einem Befehl: Vertrauen statt Prüfung,
                            und das gilt nur für die Skills, nicht für diesen Hook
    eine Umgebungsvariable  die Sitzung setzt keine mit dem GitHub-Namen
Ohne `gh`, ohne Anmeldung oder ohne Netz gibt es keinen Namen, und der Hook fragt nach. GitHub-Namen
unterscheiden Groß- und Kleinschreibung nicht; verglichen wird ohne sie.

Ob die Person Admin am Repo ist, sagt `gh api repos/<owner>/<repo> --jq .permissions.admin`, gefragt
nur, wenn sie nicht der project_owner ist; `<owner>/<repo>` kommt aus der URL von `origin`. Der Weg
über `collaborators/<Name>/permission` ist in der Cloud-Sitzung gesperrt, dieser nicht (gemessen am
21.10.2026). Liefert die Abfrage kein `true`, gilt die Person nicht als Admin. Ein leerer
project_owner bleibt leer, auch für einen Admin: dann ist es der erste Lauf von project-setup.

Das Repo ist $CLAUDE_PROJECT_DIR, sonst die Wurzel des Git-Repos im cwd des Hooks. Ein Commit in
einem anderen Repo (cd, git -C) greift nicht.

Drei Aufrufe für die Skills, mit derselben Quelle für den Namen wie der Hook:
    wow-guard.py --whoami          druckt den GitHub-Namen der Sitzung; Exit 1, wenn es keinen gibt.
                                   project-setup setzt damit project_owner.
    wow-guard.py --contact <repo>  druckt den project_owner und, wenn sein GitHub-Profil sie öffentlich
                                   führt, seine Mail-Adresse: `Name (Mail)` oder `Name`; Exit 1 ohne
                                   project_owner. project-upgrade nennt damit, an wen sich ein anderer
                                   wendet (§350). Die Mail liest `gh api users/<Name>`; gespeichert
                                   wird sie nirgends.
    wow-guard.py --owner <repo>    Exit 0 und `owner <Name>`, wenn die Person der project_owner oder
                                   Admin am Repo ist;
                                   sonst Exit 2 und der Verstoß auf stderr. project-setup fragt so,
                                   ob es die Einstellungen ändern darf (§299), project-status, ob es
                                   einen Vorschlag anlegt (§289), project-upgrade, ob es laufen
                                   darf; sonst endet es (§294, §350).

Schnittstelle (Claude Code Hooks): JSON auf stdin mit tool_name, tool_input, cwd. Exit 0 ohne Ausgabe
lässt durch; Exit 0 mit `hookSpecificOutput` (`hookEventName: PreToolUse`, `permissionDecision: ask`,
`permissionDecisionReason`) auf stdout fragt den Menschen. Ist die Eingabe nicht lesbar, endet der
Hook mit Exit 1: eine Meldung, keine Sperre, damit ein geändertes Format nicht jedes Werkzeug blockiert.

Nur Standardbibliothek, Python 3.9. project.yml liest der Leser `lies` aus check-project.py.
"""
import importlib.util
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

ORDNER = "way-of-working"
NAME = "wow-guard"
REGEL = (f"{ORDNER}/ ändert der project_owner aus project.yml, mit dem Skill `project-setup` (§299); "
         "wer es nicht ist, reicht die Änderung über den Skill `project-status` als Vorschlag ein oder "
         "ändert nur im Auftrag des Owners (§301).")
# Optionen von git commit, die einen Wert nehmen: ihr Wert ist kein Pfad.
MIT_WERT = {"-m", "-F", "-C", "-c", "-t", "--message", "--file", "--reuse-message", "--reedit-message",
            "--template", "--author", "--date", "--cleanup", "--fixup", "--squash", "--trailer",
            "--pathspec-from-file", "-S", "--gpg-sign"}
# Optionen von git selbst vor dem Unterbefehl, die einen Wert nehmen.
GIT_MIT_WERT = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}


def nachfragen(verstoss, owner):
    wer = f" ({owner})" if owner else ""
    grund = (f"{NAME}: Du bist nicht der Projekt-Owner{wer}. Bist du sicher, dass du das ändern willst? "
             f"Regel: {REGEL} Anlass: {verstoss}")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                             "permissionDecisionReason": grund}}, ensure_ascii=False))
    return 0


def git(ordner, *args):
    r = subprocess.run(["git", "-C", str(ordner), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def wurzel_von(ordner):
    out = git(ordner, "rev-parse", "--show-toplevel")
    return Path(out.strip()).resolve() if out else None


def projekt_wurzel(cwd):
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return wurzel_von(cwd) or Path(cwd).resolve()


def unter_ordner(pfad, repo):
    try:
        teile = Path(pfad).resolve().relative_to(repo).parts
    except ValueError:
        return False
    return len(teile) > 1 and teile[0] == ORDNER


def commits(befehl, cwd):
    """Je `git commit` im Befehl: (Ordner, Argumente nach commit). `cd <ordner>` davor wird mitgezählt."""
    ordner, funde = Path(cwd), []
    try:
        lexer = shlex.shlex(befehl.replace("\n", ";"), posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return [(ordner, [])] if "git" in befehl and "commit" in befehl else []
    segmente, aktuell = [], []
    for t in tokens:
        if t and set(t) <= set(";&|"):
            segmente.append(aktuell)
            aktuell = []
        else:
            aktuell.append(t)
    segmente.append(aktuell)
    for seg in segmente:
        if len(seg) >= 2 and seg[0] == "cd":
            ordner = (ordner / os.path.expanduser(seg[1])).resolve()
            continue
        if "git" not in seg:
            continue
        i = seg.index("git") + 1
        ziel = ordner
        while i < len(seg) and seg[i].startswith("-"):
            if seg[i] in GIT_MIT_WERT and i + 1 < len(seg):
                if seg[i] == "-C":
                    ziel = (ziel / os.path.expanduser(seg[i + 1])).resolve()
                i += 2
            else:
                i += 1
        if i < len(seg) and seg[i] == "commit":
            funde.append((ziel, seg[i + 1:]))
    return funde


def dateien_im_commit(repo, args):
    alle, pfade, i = False, [], 0
    while i < len(args):
        a = args[i]
        if a == "--":
            pfade.extend(args[i + 1:])
            break
        if a in ("-a", "--all"):
            alle = True
        elif a.startswith("-") and not a.startswith("--") and len(a) > 2:
            # gebündelte Kurzoptionen wie -am "Text": -a darin zählt, ein m am Ende nimmt den Wert
            alle = alle or "a" in a[1:]
            if a[-1] in "mFCct":
                i += 1
        elif a in MIT_WERT:
            i += 1
        elif not a.startswith("-"):
            pfade.append(a)
        i += 1
    namen = set((git(repo, "diff", "--cached", "--name-only") or "").split("\n"))
    if alle:
        namen |= set((git(repo, "diff", "--name-only") or "").split("\n"))
    if pfade:
        namen |= set((git(repo, "diff", "--name-only", "HEAD", "--", *pfade) or "").split("\n"))
    return sorted(n for n in namen if n.startswith(ORDNER + "/"))


def lies_projekt(repo):
    spec = importlib.util.spec_from_file_location(
        "check_project", Path(__file__).with_name("check-project.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.lies((repo / "project.yml").read_text(encoding="utf-8"))


def github_name():
    try:
        r = subprocess.run(["gh", "api", "user", "--jq", ".login"],
                           capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    name = r.stdout.strip()
    return name if r.returncode == 0 and name else None


def main():
    try:
        daten = json.load(sys.stdin)
        werkzeug = daten.get("tool_name", "")
        eingabe = daten.get("tool_input") or {}
        cwd = daten.get("cwd") or os.getcwd()
    except (ValueError, AttributeError) as e:
        print(f"{NAME}: Hook-Eingabe nicht lesbar, nicht geprüft: {e}", file=sys.stderr)
        return 1

    repo = projekt_wurzel(cwd)
    if werkzeug in ("Edit", "Write"):
        pfad = eingabe.get("file_path") or ""
        if not pfad or not unter_ordner(Path(cwd) / pfad, repo):
            return 0
        vorgang = f"{werkzeug} auf {(Path(cwd) / pfad).resolve().relative_to(repo)}"
    elif werkzeug == "Bash":
        betroffen = []
        for ordner, args in commits(eingabe.get("command") or "", cwd):
            if wurzel_von(ordner) == repo:
                betroffen += dateien_im_commit(repo, args)
        if not betroffen:
            return 0
        vorgang = f"git commit mit {', '.join(betroffen)}"
    else:
        return 0

    verstoss, _ = pruefe_person(repo, vorgang)
    return nachfragen(verstoss, owner_von(repo)) if verstoss else 0


def owner_von(repo):
    try:
        return str(lies_projekt(repo).get("project_owner") or "").strip()
    except Exception:
        return ""


def pruefe_person(repo, vorgang):
    """(Verstoß oder None, GitHub-Name oder None): ist die Person der Sitzung der project_owner?"""
    try:
        owner = str(lies_projekt(repo).get("project_owner") or "").strip()
    except Exception as e:  # fehlende Datei, Fehler des Lesers: ohne Owner keine Änderung
        return f"{vorgang}; project.yml nicht lesbar ({e}), der project_owner ist unbekannt.", None
    if not owner:
        return (f"{vorgang}; project_owner in project.yml ist leer. "
                "Ohne das Feld ändert niemand way-of-working/; project-setup trägt es ein."), None
    person = github_name()
    if not person:
        return (f"{vorgang}; der GitHub-Name der Sitzung ist unbekannt "
                "(`gh api user` lieferte keinen Login: gh fehlt, ist nicht angemeldet oder ohne Netz)."), None
    if person.casefold() != owner.casefold() and not repo_admin(repo):
        return f"{vorgang} durch {person}; project_owner ist {owner}.", person
    return None, person


def repo_admin(repo):
    """Hat die Person der Sitzung Admin-Rechte am Repo bei GitHub? Dann gilt sie als project_owner (§390)."""
    url = (git(repo, "remote", "get-url", "origin") or "").strip()
    teile = url.replace(":", "/").rstrip("/").split("/")
    if len(teile) < 2 or not teile[-1]:
        return False
    name = teile[-1][:-4] if teile[-1].endswith(".git") else teile[-1]
    try:
        r = subprocess.run(["gh", "api", f"repos/{teile[-2]}/{name}", "--jq", ".permissions.admin"],
                           capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0 and r.stdout.strip() == "true"


def kontakt(owner):
    """`Name (Mail)`, wenn das GitHub-Profil des Owners eine Mail öffentlich führt, sonst `Name`."""
    try:
        r = subprocess.run(["gh", "api", f"users/{owner}", "--jq", ".email"],
                           capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return owner
    mail = r.stdout.strip()
    return f"{owner} ({mail})" if r.returncode == 0 and mail and mail != "null" else owner


def cli(args):
    if args == ["--whoami"]:
        person = github_name()
        if not person:
            print(f"{NAME}: der GitHub-Name der Sitzung ist unbekannt (`gh api user` lieferte keinen Login)",
                  file=sys.stderr)
            return 1
        print(person)
        return 0
    if len(args) == 2 and args[0] == "--owner":
        repo = wurzel_von(args[1]) or Path(args[1]).resolve()
        verstoss, person = pruefe_person(repo, "Lauf, der nur dem project_owner zusteht")
        if verstoss:
            print(f"{NAME}: nicht der project_owner. Verstoß: {verstoss}", file=sys.stderr)
            return 2
        print(f"owner {person}")
        return 0
    if len(args) == 2 and args[0] == "--contact":
        owner = owner_von(wurzel_von(args[1]) or Path(args[1]).resolve())
        if not owner:
            print(f"{NAME}: project_owner in project.yml ist leer; project-setup trägt ihn ein", file=sys.stderr)
            return 1
        print(kontakt(owner))
        return 0
    print("Aufruf: wow-guard.py (Hook, JSON auf stdin) | --whoami | --owner <repo> | --contact <repo>",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]) if len(sys.argv) > 1 else main())
