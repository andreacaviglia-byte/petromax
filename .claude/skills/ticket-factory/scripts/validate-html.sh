#!/usr/bin/env bash
# Prüft einen Ticket-Body gegen die Auszeichnungs-Whitelist des Boards und
# escaped Freitext für den Einbau darin. Deterministisch, kein Urteil.
#
#   validate <html>   Whitelist + Tag-Balance. Exit 1 bei Verstoß.
#   escape   <text>   & < > maskieren, bevor Freitext in den Body geht.
#
# Eingabe als Argument oder über stdin.
#
# WARUM DAS EIN SKRIPT IST UND KEINE REGEL IM SKILL:
# Der Fehler fällt sonst erst beim Anlegen auf, mit der Meldung
# "XML is invalid" und ohne Angabe, welches Zeichen sie ausgelöst hat —
# auf einem kundensichtbaren Board, mitten in einem Lauf, der schon Tickets
# angelegt hat. Ein Skript prüft vorher und nennt die Stelle.
#
# GEMESSEN am 16.08.2026 gegen den Asana-Connector:
#   * '<br/>' wird abgelehnt, obwohl es gängiges HTML ist.
#   * '<h3>' und '<table>' werden angenommen, obwohl sie nicht auf der
#     Liste stehen. Die Liste wird also NICHT gleichmäßig durchgesetzt —
#     deshalb prüfen wir gegen sie und nicht gegen das Beobachtete.
#   * 'table', 'tr' und 'td' stehen NICHT auf der Liste, obwohl Asana sie
#     annimmt (25.09.2026): das Epic-Ticket trägt seine Anforderungen als
#     Block je Anforderung (§222), weil die Spalten einer Tabelle im Ticket
#     zu schmal stehen. Eine Tabelle im Body ist deshalb ein Fehler.
#   * HTML-Entities wie '&middot;' gehen durch. Ein nacktes '&' in
#     Freitext dagegen nicht: es ist in XML der Beginn einer Entity.
#
# Der Kommentar-Endpunkt trägt WENIGER als der Ticket-Body: ihm fehlen
# h1, h2, hr, img. Dieser Lauf schreibt keine Kommentare; kommt das dazu,
# braucht es eine zweite, engere Liste — nicht dieselbe.

set -euo pipefail

ERLAUBT="body strong em u s code ol ul li a blockquote pre h1 h2 hr img"
# Tags ohne schließendes Gegenstück. Sie aus der Balance-Zählung
# herauszunehmen ist der Unterschied zwischen einer Prüfung und einem
# Fehlalarm bei jedem Trennstrich.
OHNE_SCHLUSS="hr img"

pruefen() {
  local html="$1"
  [ -z "$html" ] && return 0

  local erlaubt_re fremd
  erlaubt_re=$(echo "$ERLAUBT" | tr ' ' '|')
  # Zwei sed-Ausdrücke statt '^</\?': das '\?' ist eine GNU-Erweiterung,
  # die macOS-sed nicht kennt — dort bliebe die Klammer stehen und JEDES
  # Tag galte als fremd. Gemessen beim Port.
  fremd=$(echo "$html" | grep -oE '</?[a-zA-Z][a-zA-Z0-9]*' \
            | sed -e 's|^</||' -e 's|^<||' | tr '[:upper:]' '[:lower:]' \
            | sort -u | grep -vE "^(${erlaubt_re})$" || true)
  if [ -n "$fremd" ]; then
    echo "validate-html: Auszeichnung nicht erlaubt:" >&2
    echo "$fremd" | sed 's/^/  /' >&2
    echo "  Erlaubt: ${ERLAUBT}" >&2
    return 1
  fi

  local ohne_re offen zu
  ohne_re=$(echo "$OHNE_SCHLUSS" | tr ' ' '|')
  offen=$(echo "$html" | grep -oE '<[a-zA-Z][a-zA-Z0-9]*' | sed 's|<||' \
            | tr '[:upper:]' '[:lower:]' | grep -vE "^(${ohne_re})$" \
            | sort || true)
  zu=$(echo "$html" | grep -oE '</[a-zA-Z][a-zA-Z0-9]*' | sed 's|</||' \
            | tr '[:upper:]' '[:lower:]' | sort || true)
  if [ "$offen" != "$zu" ]; then
    echo "validate-html: Tags nicht ausgeglichen." >&2
    echo "  offen: $(echo "$offen" | tr '\n' ' ')" >&2
    echo "  zu:    $(echo "$zu" | tr '\n' ' ')" >&2
    return 1
  fi
  return 0
}

# Reihenfolge zwingend: '&' zuerst, sonst wird das Ampersand in '&lt;'
# selbst noch einmal maskiert. sed und nicht die Bash-Ersetzung, weil dort
# das '&' im Ersatztext für den gefundenen Text steht — aus '<' würde
# '<lt;'.
maskieren() {
  printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}

eingabe() { if [ $# -ge 1 ]; then printf '%s' "$1"; else cat; fi; }

modus="${1:-}"
shift || true
case "$modus" in
  validate) pruefen "$(eingabe "$@")" ;;
  escape)   maskieren "$(eingabe "$@")" ;;
  *)
    echo "Aufruf: $0 validate [html]" >&2
    echo "        $0 escape   [text]" >&2
    exit 2 ;;
esac
