#!/usr/bin/env python3
"""Schreibt am Ende eines Laufs eine Zeile nach .claude/metrics/runs.md (§246).

Aufruf:
    run-metrics.py --skill <name> [--cost <usd>] [--ccr-session <id>] [--settle <id>=<usd> ...]
                   [--transcript <pfad>] [--out <datei>]
    run-metrics.py --settle <id>=<usd> [--settle ...] [--out <datei>]
    run-metrics.py --open [--ccr-session <id>] [--out <datei>]

Gelesen wird das Protokoll der Sitzung, das Claude Code auf der Maschine führt:
~/.claude/projects/<ordner>/<sitzung>.jsonl, dazu die Protokolle ihrer Subagents unter
<ordner>/<sitzung>/subagents/. Ohne --transcript nimmt das Script das jüngste Protokoll unter
~/.claude/projects/ (oder $CLAUDE_CONFIG_DIR/projects/); das ist die laufende Sitzung. Je Lauf eine
frische Sitzung (§244): die Sitzung ist der Lauf.

Gerechnet wird:
    Wandzeit   erster bis letzter Zeitstempel der Hauptsitzung
    aktiv      je Turn von der Eingabe des Leads bis zur letzten Zeile vor seiner nächsten Eingabe,
               ohne die Zeit, in der eine Rückfrage (AskUserQuestion) auf ihre Antwort wartet; das
               Warten auf den Lead zählt nicht, das Warten auf einen Subagent schon. Erkennt das
               Script keine Eingabe, steht „ungemessen“ statt 0:00
    Tokens     Eingabe, Cache lesen, Cache schreiben, Ausgabe; Hauptsitzung und Subagents, je
               message.id einmal
    Kosten     --cost (in der Cloud cost_usd aus get_session), sonst der letzte cost-state des
               Protokolls, wenn nach ihm keine Antwort mehr kam, sonst „ungemessen“
    Modell     das Modell der Antworten der Hauptsitzung

Aktiv und gewartet trennt allein die Eingabe. Gewartet ist die Zeit von der letzten Zeile eines
Turns bis zur nächsten Eingabe und die Zeit einer offenen Rückfrage; alles andere ist aktiv, auch
das Warten auf einen Subagent, dessen Benachrichtigung deshalb keinen Turn beginnt. Eine Eingabe ist
eine user-Zeile mit Text, kein Tool-Ergebnis, und eine von dreien:
    - vom Menschen (origin.kind human oder ohne origin), keine Meta-Zeile;
    - mit Text, der mit <cross-session-message beginnt, auch als Meta-Zeile: so kam die Nachricht
      einer steuernden Sitzung per send_message (gemessen am 04.10.2026);
    - mit origin.kind task-notification und Text, der nicht mit <task-notification beginnt: so kommt
      die Nachricht einer steuernden Sitzung in der Cloud (gemessen am 10.10.2026, promptSource
      system, ohne Hülle). Ohne diese Form hatten alle Läufe der Probe zu 0.5.0 „aktiv“ 0:00. Die
      Benachrichtigung eines Subagents trägt dieselbe Herkunft, beginnt aber mit <task-notification.

Die Kosten aus --cost sind eine Untergrenze: get_session kennt in der laufenden Sitzung die Kosten nur
bis zum vorigen Turn, im ersten Turn gar keine; ein Lauf in einem Turn ruft deshalb ohne --cost auf und
bekommt „ungemessen“. --ccr-session hält die ID der Cloud-Sitzung (session_…) in der Spalte Sitzung
fest. Ein späterer Lauf fragt mit --open, welche Sitzungen noch offen sind, holt je ID die Kosten mit
get_session(session_id), die nach dem Ende der Sitzung vollständig sind, und ersetzt mit --settle die
Untergrenze oder „ungemessen“ in der letzten Zeile dieser Sitzung durch den genauen Wert (§388). Einen
genauen Wert ändert --settle nicht.

Fehlt --out, schreibt das Script runs.md neben sich; fehlt die Datei, legt es sie mit Kopf an.

Prüfungen: transcript, table, settle. Ausgabe je Befund eine Zeile "<prüfung>: <detail>", sonst die
geschriebene Zeile, je beglichene Sitzung eine Zeile, bei --open je offene Sitzung ihre ID. Exit 0:
geschrieben. Exit 1: ein Befund, nichts geschrieben. Exit 2: falscher Aufruf. Nur Standardbibliothek.
"""
import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

COLUMNS = ["Datum", "Skill", "Sitzung", "Wandzeit", "aktiv", "Eingabe", "Cache lesen",
           "Cache schreiben", "Ausgabe", "Kosten", "Modell"]
HEADER = "| " + " | ".join(COLUMNS) + " |"
RULE = "|" + "---|" * len(COLUMNS)
INTRO = (
    "# Läufe\n\n"
    "Je Lauf eine Zeile, geschrieben von `run-metrics.py` am Ende des Laufs (§246). Was die Spalten "
    "bedeuten, steht in `readme.md` daneben; die Datei gehört nicht zum Vorhaben, kein Skill liest sie.\n\n"
)
USAGE = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens")
# Zeilen, die zu einem Turn gehören. queue-operation steht Bruchteile einer Sekunde vor der Eingabe
# des Leads und gehört schon zum Warten.
TURN_TYPES = {"user", "assistant", "system", "attachment"}
# Werkzeuge, deren Ergebnis die Antwort des Leads ist: von ihrem Aufruf bis zum Ergebnis wartet der
# Lauf auf ihn. Gemessen am 04.10.2026: eine Rückfrage hielt einen Turn sechs Stunden offen.
WAIT_TOOLS = {"AskUserQuestion"}
SKILL = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CCR_SESSION = re.compile(r"^session_[A-Za-z0-9]+$")
# So beginnt eine Eingabe, die eine andere Sitzung per send_message schickt.
CROSS_SESSION = "<cross-session-message"
# Herkunft und Hülle der Benachrichtigung eines Subagents; ohne Hülle ist es eine steuernde Sitzung.
NOTIFICATION, NOTIFICATION_TAG = "task-notification", "<task-notification"
LOWER_BOUND = "mind. "
UNMEASURED = "ungemessen"
SESSION_COL, COST_COL = COLUMNS.index("Sitzung"), COLUMNS.index("Kosten")
TIMESTAMP = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(?:\.(\d+))?(Z|[+-]\d\d:?\d\d)?$")


class Befund(Exception):
    pass


def zeit(text):
    """ISO-Zeitstempel als aware datetime; Python 3.9 liest 'Z' und Millisekunden nicht selbst."""
    m = TIMESTAMP.match(text or "")
    if not m:
        return None
    j, mo, t, h, mi, s, frac, tz = m.groups()
    us = int((frac or "0")[:6].ljust(6, "0"))
    if tz in (None, "Z"):
        zone = datetime.timezone.utc
    else:
        vz = -1 if tz[0] == "-" else 1
        hh, mm = int(tz[1:3]), int(tz[-2:])
        zone = datetime.timezone(vz * datetime.timedelta(hours=hh, minutes=mm))
    return datetime.datetime(int(j), int(mo), int(t), int(h), int(mi), int(s), us, tzinfo=zone)


def lies(pfad):
    """Die JSON-Zeilen einer Datei; eine kaputte Zeile (etwa die halb geschriebene letzte) fällt weg."""
    zeilen = []
    with open(pfad, encoding="utf-8", errors="replace") as f:
        for roh in f:
            try:
                d = json.loads(roh)
            except ValueError:
                continue
            if isinstance(d, dict):
                zeilen.append(d)
    return zeilen


def projekte():
    basis = os.environ.get("CLAUDE_CONFIG_DIR")
    return (Path(basis) if basis else Path.home() / ".claude") / "projects"


def finde_protokoll():
    wurzel = projekte()
    kandidaten = sorted(wurzel.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime) if wurzel.is_dir() else []
    if not kandidaten:
        raise Befund(f"transcript: kein Protokoll unter {wurzel.name}/; ohne Protokoll ist der Lauf "
                     f"nicht zu messen, --transcript nennt es")
    return kandidaten[-1]


def text_der_zeile(d):
    """Der Text einer user-Zeile, wenn sie einen trägt; Tool-Ergebnisse tragen keinen."""
    inhalt = (d.get("message") or {}).get("content")
    if isinstance(inhalt, str):
        return inhalt
    if isinstance(inhalt, list):
        texte = [b.get("text") for b in inhalt if isinstance(b, dict) and b.get("type") == "text"]
        if texte:
            return "".join(t for t in texte if isinstance(t, str))
    return None


def eingabe_des_leads(d):
    """Eine echte Eingabe: kein Tool-Ergebnis, keine Meta-Zeile, keine Benachrichtigung. Die Eingabe
    einer steuernden Sitzung zählt, auch als synthetische Zeile."""
    if d.get("type") != "user" or d.get("isCompactSummary"):
        return False
    text = text_der_zeile(d)
    if text is None:
        return False
    if text.lstrip().startswith(CROSS_SESSION):
        return True
    if d.get("isMeta") or d.get("isVisibleInTranscriptOnly"):
        return False
    herkunft = d.get("origin")
    art = herkunft.get("kind", "human") if isinstance(herkunft, dict) else "human"
    if art == NOTIFICATION:
        return not text.lstrip().startswith(NOTIFICATION_TAG)
    return art == "human"


def bloecke(d, art):
    inhalt = (d.get("message") or {}).get("content")
    return [b for b in inhalt if isinstance(b, dict) and b.get("type") == art] if isinstance(inhalt, list) else []


def laufzeiten(haupt):
    """(erster Zeitstempel, Wandzeit, aktive Laufzeit) der Hauptsitzung; aktiv ist None ohne Eingabe."""
    alle, turns, warten, offen = [], [], datetime.timedelta(), {}
    for d in haupt:
        if d.get("isSidechain"):
            continue
        t = zeit(d.get("timestamp"))
        if t is None:
            continue
        alle.append(t)
        if eingabe_des_leads(d):
            turns.append([t, t])
            offen = {}
            continue
        if not turns or d.get("type") not in TURN_TYPES:
            continue
        turns[-1][1] = t
        for b in bloecke(d, "tool_use"):
            if b.get("name") in WAIT_TOOLS and b.get("id"):
                offen[b["id"]] = t
        for b in bloecke(d, "tool_result"):
            seit = offen.pop(b.get("tool_use_id"), None)
            if seit is not None:
                warten += t - seit
    if not alle:
        raise Befund("transcript: das Protokoll trägt keine Zeile mit Zeitstempel")
    if not turns:
        return min(alle), max(alle) - min(alle), None
    aktiv = sum(((ende - start) for start, ende in turns), datetime.timedelta()) - warten
    return min(alle), max(alle) - min(alle), aktiv


def tokens(dateien):
    """Summe je Feld über alle Antworten, je message.id einmal."""
    gesehen, summe = set(), dict.fromkeys(USAGE, 0)
    for zeilen in dateien:
        for d in zeilen:
            if d.get("type") != "assistant":
                continue
            m = d.get("message") or {}
            mid = m.get("id")
            if not mid or mid in gesehen:
                continue
            gesehen.add(mid)
            usage = m.get("usage") or {}
            for k in USAGE:
                wert = usage.get(k)
                if isinstance(wert, int):
                    summe[k] += wert
    return summe


def kostenstand(haupt):
    """totalCostUSD des letzten cost-state, wenn danach keine Antwort mehr kam; sonst None."""
    stand = None
    for d in haupt:
        if d.get("type") == "cost-state":
            stand = d.get("totalCostUSD")
        elif d.get("type") == "assistant":
            stand = None
    return stand if isinstance(stand, (int, float)) else None


def modell(haupt):
    zaehler = {}
    for d in haupt:
        if d.get("type") == "assistant" and not d.get("isSidechain"):
            m = (d.get("message") or {}).get("model")
            if m and not m.startswith("<"):
                zaehler[m] = zaehler.get(m, 0) + 1
    return ", ".join(sorted(zaehler, key=lambda m: -zaehler[m])) or "unbekannt"


def zahl(n):
    return f"{n:,}".replace(",", ".")


def dauer(td):
    minuten = int(td.total_seconds() // 60)
    return f"{minuten // 60}:{minuten % 60:02d}"


def usd(betrag, quelle):
    return f"{betrag:.2f}".replace(".", ",") + f" USD ({quelle})"


def zeile(skill, protokoll, cost, ccr_session):
    haupt = lies(protokoll)
    if not haupt:
        raise Befund(f"transcript: {protokoll.name} ist leer oder trägt kein JSON")
    sitzung = next((d["sessionId"] for d in haupt if isinstance(d.get("sessionId"), str)), protokoll.stem)
    start, wand, aktiv = laufzeiten(haupt)
    sub = protokoll.parent / protokoll.stem / "subagents"
    nebenher = [lies(p) for p in sorted(sub.rglob("agent-*.jsonl"))] if sub.is_dir() else []
    t = tokens([haupt] + nebenher)
    if cost is not None:
        # get_session zählt den laufenden Turn nicht mit (gemessen am 04.10.2026: 0,56 statt 4,53 USD)
        kosten = "mind. " + usd(cost, "get_session, ohne letzten Turn")
    else:
        stand = kostenstand(haupt)
        kosten = usd(stand, "Kostenstand") if stand is not None else "ungemessen"
    zellen = [start.astimezone().strftime("%d.%m.%Y"), skill, ccr_session or sitzung[:8], dauer(wand),
              dauer(aktiv) if aktiv is not None else "ungemessen",
              zahl(t["input_tokens"]), zahl(t["cache_read_input_tokens"]),
              zahl(t["cache_creation_input_tokens"]), zahl(t["output_tokens"]), kosten, modell(haupt)]
    return "| " + " | ".join(z.replace("|", "/") for z in zellen) + " |"


def tabelle(out):
    """Die Zeilen von runs.md; None, wenn es die Datei nicht gibt."""
    if not out.is_file():
        return None
    zeilen = out.read_text(encoding="utf-8").splitlines()
    if HEADER not in zeilen:
        raise Befund(f"table: {out.name} trägt nicht den Kopf '{HEADER}'; eine Zeile anderer "
                     f"Spalten wird nicht angehängt")
    return zeilen


def zellen_von(z):
    """Die Zellen einer Datenzeile der Tabelle, sonst None."""
    if not z.startswith("| ") or not z.endswith(" |") or z in (HEADER, RULE):
        return None
    zellen = z[2:-2].split(" | ")
    return zellen if len(zellen) == len(COLUMNS) else None


def letzte_zeilen(zeilen):
    """Je ID einer Cloud-Sitzung der Index ihrer letzten Zeile, in der Folge der Tabelle."""
    letzte = {}
    for i, z in enumerate(zeilen):
        zellen = zellen_von(z)
        if zellen and CCR_SESSION.match(zellen[SESSION_COL]):
            letzte.pop(zellen[SESSION_COL], None)
            letzte[zellen[SESSION_COL]] = i
    return letzte


def ohne_genauen_wert(kosten):
    """Eine Untergrenze oder „ungemessen“: im ersten Turn liefert get_session keine Kosten (§388)."""
    return kosten.startswith(LOWER_BOUND) or kosten == UNMEASURED


def offen(zeilen, ausser=None):
    """Die IDs, deren letzte Zeile keinen genauen Wert der Kosten trägt."""
    return [sid for sid, i in letzte_zeilen(zeilen).items()
            if sid != ausser and ohne_genauen_wert(zellen_von(zeilen[i])[COST_COL])]


def begleiche(zeilen, settle):
    """Ersetzt je ID die Untergrenze oder „ungemessen“ in der letzten Zeile ihrer Sitzung durch den
    genauen Wert."""
    letzte = letzte_zeilen(zeilen or [])
    for sid, betrag in settle:
        if sid not in letzte:
            raise Befund(f"settle: {sid} steht in keiner Zeile von runs.md")
        i = letzte[sid]
        zellen = zellen_von(zeilen[i])
        if not ohne_genauen_wert(zellen[COST_COL]):
            raise Befund(f"settle: die Zeile von {sid} trägt weder Untergrenze noch ungemessen, sondern "
                         f"'{zellen[COST_COL]}'; ein genauer Wert wird nicht überschrieben")
        zellen[COST_COL] = usd(betrag, "get_session")
        zeilen[i] = "| " + " | ".join(zellen) + " |"
    return zeilen


def schreibe(out, zeilen, neu):
    if zeilen is None:
        out.parent.mkdir(parents=True, exist_ok=True)
        text = INTRO + HEADER + "\n" + RULE + "\n"
    else:
        text = "\n".join(zeilen) + "\n"
    if neu is not None:
        text += neu + "\n"
    out.write_text(text, encoding="utf-8")


def kosten_arg(text):
    try:
        wert = float(text.replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError(f"keine Zahl: {text}")
    if wert < 0 or wert != wert:
        raise argparse.ArgumentTypeError(f"kein Betrag: {text}")
    return wert


def ccr_arg(text):
    if not CCR_SESSION.match(text):
        raise argparse.ArgumentTypeError(f"keine ID einer Cloud-Sitzung (session_…): {text}")
    return text


def settle_arg(text):
    sid, gleich, betrag = text.partition("=")
    if not gleich:
        raise argparse.ArgumentTypeError(f"nicht <id>=<usd>: {text}")
    return ccr_arg(sid), kosten_arg(betrag)


def skill_arg(text):
    if not SKILL.match(text):
        raise argparse.ArgumentTypeError(f"kein Skill-Name: {text}")
    return text


def main(argv):
    p = argparse.ArgumentParser(prog="run-metrics.py", description=__doc__.split("\n")[0])
    p.add_argument("--skill", type=skill_arg)
    p.add_argument("--cost", type=kosten_arg)
    p.add_argument("--ccr-session", type=ccr_arg)
    p.add_argument("--settle", type=settle_arg, action="append", default=[])
    p.add_argument("--open", action="store_true")
    p.add_argument("--transcript", type=Path)
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "runs.md")
    a = p.parse_args(argv[1:])
    if a.open and (a.skill or a.cost is not None or a.settle or a.transcript):
        p.error("--open steht allein, höchstens mit --ccr-session und --out")
    if not a.open and not a.skill and not a.settle:
        p.error("es fehlt --skill, --settle oder --open")
    if not a.open and not a.skill and (a.cost is not None or a.ccr_session or a.transcript):
        p.error("--cost, --ccr-session und --transcript gehören zu --skill")
    try:
        zeilen = tabelle(a.out)
        if a.open:
            for sid in offen(zeilen or [], ausser=a.ccr_session):
                print(sid)
            return 0
        if a.settle:
            zeilen = begleiche(zeilen, a.settle)
        neu = None
        if a.skill:
            if a.transcript is not None and not a.transcript.is_file():
                raise Befund(f"transcript: {a.transcript.name} gibt es nicht")
            protokoll = a.transcript or finde_protokoll()
            neu = zeile(a.skill, protokoll, a.cost, a.ccr_session)
        schreibe(a.out, zeilen, neu)
    except Befund as b:
        print(b)
        return 1
    for sid, betrag in a.settle:
        print(f"{sid}: {usd(betrag, 'get_session')}")
    if neu is not None:
        print(neu)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
