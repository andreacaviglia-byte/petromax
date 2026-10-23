# Einen Vorschlag zur Arbeitsweise anlegen

**`way-of-working.md` wird nie von Hand geschrieben** (§286): Sie ist die Projektion aus dem Standard
`.claude/way-of-working-standard.md` und den Abweichungen in `way-of-working/`. Eine Änderung der
Arbeitsweise ist deshalb immer eine neue Datei in `way-of-working/`, die nur der `project_owner` mit
`project-setup` schreibt (§299); alle anderen schlagen sie vor. Die Formen beider Dateien stehen im
Datalayer-Vertrag, Abschnitte `way-of-working/JJJJ-MM-TT-<slug>.md` und `todo/JJJJ-MM-TT-<slug>.md`.

## Was gefragt wird

Bevor du den Vorschlag vorlegst, klärst du mit der Person, je eine Frage:

- **Abschnitt:** welche Überschrift 2 des Standards die Änderung betrifft. `section` nennt sie
  **wörtlich**; einen Abschnitt, den der Standard nicht hat, lehnt die Projektion mit `wow_section` ab.
- **Was anders ist**, in Sätzen, die so in `way-of-working.md` stehen können.
- **Der Grund**, ein Satz.

**Würde die Änderung eine Prüfung eines Skripts verletzen** (etwa eine Pflichtspalte weglassen, ein
Feld anders füllen, als ein Vertrag es verlangt), ist sie keine Abweichung, sondern ein abgeleiteter
Skill (§225): du sagst das und nennst `skill-create`. **Betrifft sie nur die Arbeit eines Workstreams**,
gilt dasselbe, mit dem Solution Owner in `verantwortlich:`.

## Ein anderer schlägt vor

`wow-guard.py --owner .` endete mit Exit 2. Du sagst der Person, dass nur der `project_owner` die
Arbeitsweise ändert, und legst ihr den Vorschlag als Aufgabe an ihn vor, in der Form des
Datalayer-Vertrags `${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt
`todo/JJJJ-MM-TT-<slug>.md`, „Ein Vorschlag zur Arbeitsweise“, mit seinem Pfad. Nach ihrem Ja schreibst du die Datei, liest sie zurück und gehst
zum Ende des Laufs. Lieferte `--whoami` keinen Namen, fragst du nach ihm und schreibst ihn so, wie er
genannt ist; geprüft wird er dann nicht.

Über den Vorschlag entscheidet der `project_owner` mit `project-setup` (§299): er nimmt ihn an, ändert
ihn oder lehnt ihn ab.
