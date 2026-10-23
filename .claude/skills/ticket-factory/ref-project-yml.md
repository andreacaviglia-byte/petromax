# Board, Kennung und Figma in `project.yml` eintragen

**Dieser Lauf trägt `board.tool`, `board.project`, `key` und `figma` ein, wenn sie leer sind** (§229),
und sonst kein Feld. Er ist ein Schritt von `SKILL.md`, Step 1. Frag je Sache einmal,
in dieser Folge; „noch offen" ist eine Antwort.

- **`board.*`:** „Der Link zum Board, Jira oder Asana?" Geprüft wird nach „Das Board eintragen" in
  [ref-jira.md](ref-jira.md) oder [ref-asana.md](ref-asana.md); eine gescheiterte Prüfung nennst du
  mit der Meldung und fragst neu.
- **`key`:** „Eine kurze Kennung des Vorhabens, klein, `a-z`, `0-9`, `-` und `_` (`relaunch`)?" Sie
  steht an jedem Epic-Ticket in der Zeile `Beauftragung:` (§233).
- **Ohne Board oder `key` hältst du an, bevor du etwas schreibst**: der Lauf kann kein Ticket anlegen.
- **`figma`:** Steht `design` in `add_ons` und ist `figma` leer: „Der Link zur Figma-Datei?" Ohne ihn
  fehlen der Link am Epic-Ticket des Theme-Epics und das Kriterium der Darstellung an den Seitentypen ([ref-ticket-templates.md](ref-ticket-templates.md)).
- **`project_type` und `add_ons` trägst du nicht ein** (§299, §303): ist `project_type` leer, fragst du
  einmal, ob das Vorhaben ein Projekt oder ein Expert Service ist und ob das Add-on `design` verkauft
  ist, nimmst die Antwort für diesen Lauf und nennst `project-setup` im Bericht.

**Jede Antwort außer „noch offen" schreibst du** nach dem Datalayer-Vertrag,
`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, Abschnitt `project.yml`: direkt davor lesen,
nur die Zeile des Feldes ändern, die ganze Datei schreiben, zurücklesen, dann ohne `--needs`

```
python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-project.py .
```

Ein Verstoß ist ein Halt. Committet wird am Ende des Laufs (`SKILL.md`, Step 10).
