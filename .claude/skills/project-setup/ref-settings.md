# Die Einstellungen ändern, Sache des `project_owner`

**Jeder Lauf nach dem ersten ist für die Einstellungen** (§299): die Felder von `project.yml`, die
Arbeitsweise und den `project_owner` selbst. Er läuft für den Owner ohne Rückfrage, für jeden anderen
erst nach einem Ja (§301, unten „Die Prüfung“). Du fragst, was geändert werden soll, und arbeitest je Änderung
**zeigen, Ja, schreiben, zurücklesen** ab; mehrere Änderungen gehen in einen Commit.

| Der Owner will | Abschnitt |
|---|---|
| ein Feld von `project.yml` ändern oder ergänzen, etwa Board, Confluence-Bereich, Projektordner, das Team (`team`) | „Felder von `project.yml`“ |
| die Arbeitsweise ändern | „Eine Abweichung schreiben“ |
| offene Vorschläge zur Arbeitsweise sehen und entscheiden | „Über einen Vorschlag entscheiden“ |
| das Projekt an eine andere Person übergeben | „Den Owner übertragen“ |

## Die Prüfung: ist die Person der `project_owner`?

Ein Schritt, vor allem anderen in diesem Lauf (§299, §301):

1. Lies `project_owner` aus `project.yml`. **Fehlt `project.yml`, oder ist das Feld leer, ist es der
   erste Lauf**: er läuft durch und setzt den Owner auf die Person der Sitzung (SKILL.md, Step 5;
   liefert `--whoami` keinen Namen, fragst du nach dem GitHub-Namen). Die Prüfung endet hier.
2. Sonst fragst du dieselbe Stelle wie `project-upgrade`:

   ```
   python3 ${CLAUDE_SKILL_DIR}/../../scripts/wow-guard.py --owner .
   ```

3. **Exit 0:** die Person ist der Owner oder Projekt-Admin (Admin am Repo bei GitHub, §390); es geht
   ohne Rückfrage mit den Einstellungen unten weiter.
4. **Exit 2:** die Person ist nicht der Owner, oder ihr Name lässt sich nicht ermitteln. Du fragst
   **einmal**, als Rückfrage nach `CLAUDE.md`: „Du bist nicht der Projekt-Owner
   (‹project_owner›). Bist du sicher, dass du `project-setup` aufrufen willst?“ Auf **Ja** geht es mit
   allen Einstellungen unten weiter, auch dem Übertragen des Owners; der Bericht nennt, dass jemand
   anderes als der Owner geändert hat. Auf **Nein** endest du ohne zu schreiben und nennst
   `project-status` für einen Vorschlag. Ein Schreiben in `way-of-working/` fragt danach der Hook
   `wow-guard` noch einmal nach; das Ja dort gibt der Mensch.

## Felder von `project.yml`

Je Feld die Frage aus [ref-project-yml.md](ref-project-yml.md), „Die Fragen des ersten Laufs“ oder
„Die Fragen des Steckbriefs“, und dieselbe Prüfung: den Projektordner nach SKILL.md, Step 6, Board und
Confluence-Bereich nach [ref-project-yml.md](ref-project-yml.md), „Board und Space prüfen“. **`key` änderst du nicht** (§233): an ihm findet `ticket-factory` seine Epics auf dem Board
wieder. **`project_type` wechselt höchstens einmal**, nach dem Go-Live, von `project` zu
`expert_service` im selben Repo (§224, §303); einen anderen Wechsel nimmst du nicht vor und sagst
warum. Ein Feld, das ein anderer Skill führt (`requirements_sheet`, `e2e_sheet`), änderst du nur
auf ausdrücklichen Wunsch und sagst dazu, dass der Skill danach das genannte Dokument liest. Du zeigst
die Vorschau nach [ref-project-yml.md](ref-project-yml.md), „Die Vorschau“, schreibst nach dem Ja nach
derselben Ref und prüfst mit `check-project.py .`.

## Eine Abweichung schreiben

**`way-of-working.md` wird nie von Hand geschrieben** (§286): sie ist die Projektion aus dem Standard
`.claude/way-of-working-standard.md` und den Abweichungen in `way-of-working/`. Eine Änderung der
Arbeitsweise ist deshalb immer eine neue Datei in `way-of-working/`. Du klärst, je eine Frage:

- **Abschnitt:** welche Überschrift 2 des Standards die Änderung betrifft. `section` nennt sie
  **wörtlich**; einen Abschnitt, den der Standard nicht hat, lehnt die Projektion mit `wow_section` ab.
- **Was anders ist**, in Sätzen, die so in `way-of-working.md` stehen können.
- **Der Grund**, ein Satz.

**Würde die Änderung eine Prüfung eines Skripts verletzen** (etwa eine Pflichtspalte weglassen, ein
Feld anders füllen, als ein Vertrag es verlangt), ist sie keine Abweichung, sondern ein abgeleiteter
Skill (§225): du sagst das und nennst `skill-create`. **Betrifft sie nur die Arbeit eines Workstreams**,
gilt dasselbe, mit dem Solution Owner in `verantwortlich:`.

Dann zeigst du den vollständigen Text der Datei, in der Form des Datalayer-Vertrags:

```
---
date: 2026-10-12
section: Übergaben
reason: Der Kunde arbeitet nur über das Board; Übergaben stehen deshalb auch dort.
by: <GitHub-Name des project_owner>
proposed_by: ""
skill: ""
---

Eine Übergabe an eine andere Person steht zusätzlich als Kommentar am Epic-Ticket.
```

Pfad `way-of-working/<Datum>-<slug>.md`, das Datum von heute (`date +%F`), der Slug kurz, klein, mit
`-`. Lehnt der Hook `wow-guard` das Schreiben trotzdem ab, nennst du seine Meldung wörtlich und hältst
an.

## Über einen Vorschlag entscheiden

Offene Vorschläge sind die Dateien in `todo/` mit `status: open`, `to` = der `project_owner` und einem
Titel, der mit `Arbeitsweise:` beginnt; angelegt hat sie `project-status`. Du zeigst sie einzeln und
fragst je Vorschlag: annehmen, ändern oder ablehnen.

- **Annehmen** (auch geändert): eine Datei in `way-of-working/` wie oben, mit `by` = der Owner und
  `proposed_by` = wer vorschlug; in der Aufgabe `status: done`, `done_by` = der Owner, `done_at` = heute
  (`${CLAUDE_SKILL_DIR}/../../docs/ref-tasks.md`, 2, §359) und eine letzte Zeile
  `Übernommen in way-of-working/<Datei> am <Datum>.`
- **Ablehnen:** in der Aufgabe `status: done`, `done_by`, `done_at` und eine letzte Zeile `Abgelehnt von <Name> am
  <Datum>: <Grund>.` In `way-of-working/` entsteht nichts.

Aufgabe und Abweichung gehen in denselben Commit.

## Den Owner übertragen

Du fragst nach dem GitHub-Namen der neuen Person, wie sie ihn schreibt; er wird nicht geprüft. Vor
dem Ja sagst du: **ab dem Commit ist diese Person der Owner**; Einstellungen und `project-upgrade`
fragen danach jeden anderen zurück, auch die Person dieser Sitzung (§299, §301). Dann schreibst du nur
die Zeile `project_owner` in `project.yml`, liest zurück und prüfst mit `check-project.py .`. Die
übrigen Änderungen dieses Laufs schreibst du davor.

## Das Ende

Nach dem Schreiben endest du nach `${CLAUDE_SKILL_DIR}/../../docs/ref-projection.md`, Teile 1, 5 und
6: `check-repo.py`, `readme.md` und `way-of-working.md`, Commit und Push. Ins Sheet projiziert dieser
Lauf nichts; Teile 2 bis 4 entfallen. Die Nachricht beginnt mit `project-setup:`.
