# Der Lösungsansatz, die Gewerke und der Schnitt einer Anforderung in Tickets

**`ticket-factory` schlägt nie einen Lösungsansatz vor** (§275): den groben Lösungsansatz je Anforderung schlägt
`solution-approach` vor, gewählt wird er in `solution-design` oder, im Expert Service, vom Lead. Dieser
Schritt liest den Lösungsansatz, ordnet jedes Kriterium einem Gewerk zu und schneidet daraus Story und
Subtasks (§281). Er ist ein Schritt von `SKILL.md`, kein eigener Skill. **Die Datei der Anforderung
trägt kein Gewerk und bekommt keines** (§280, Regel 2): es entsteht hier und steht nur am Ticket.

## Woher der Lösungsansatz kommt

**Aus `## Approach` der Datei der Anforderung, sonst nirgends** (§280). Der erste Lösungsansatz unter
`### <Name>` ist der gewählte oder empfohlene, `classification` seine Art, `## Details` die Angaben,
die er braucht. Eine Notiz von `solution-approach` in `notes/` ist keine Quelle des Lösungsansatzes.

| `solution_status` | Was gilt |
|---|---|
| `decided` | der Lösungsansatz dieser Tickets |
| `proposed` | ein Vorschlag aus `solution-approach`, ungeprüft (§275). Die Vorschau nennt ihn so, mit `Fit:`; erst das Ja des Leads zur Vorschau macht ihn zum Lösungsansatz dieser Tickets. Die Datei bleibt, wie sie ist |
| `blocked` | der Lösungsansatz hängt an einer offenen Frage mit `blocking: yes`: nach „Offen lassen“, mit der Kennung der Frage in der Vorschau |
| leer, kein `## Approach` | **kein Ticket für diese Anforderung** (§275): die Vorschau nennt sie mit „kein Lösungsansatz; der nächste Lauf ist `solution-approach`“, die übrigen laufen weiter. Ausgenommen ist eine Anforderung im Epic der Domäne `design` (unten, §297) |

Ein Lösungsansatz, den dieser Lauf selbst ableitet, sähe am Board aus wie ein geprüfter, und ein falscher Lösungsansatz
zeigte sich erst beim Bauen. **Wählt der Lead in der Vorschau einen anderen Lösungsansatz**, gilt die Wahl nur
für die Tickets dieses Laufs; die Datei schreibst du dafür nicht, und der Bericht nennt den Lauf, der
sie festhält: `solution-design`, im Expert Service `solution-approach`.

## Anforderungen im Design-Epic

**Eine Anforderung in einem Epic der Domäne `design` bekommt ihre Story auch ohne Lösungsansatz** (§297): sie
trägt die Arbeit des Designers (Sessions, Konzept, Figma, Abnahme, QS, UX/UI-QA, §285), und für die
gibt es keinen Lösungsansatz in `classification`. Die Story hat ein Gewerk, `UX/UI`, Stufe `story`, und trägt
ihre Abnahme-Kriterien aus `## Acceptance criteria`. Den `Lösungsansatz` und die `Angaben für UX/UI`
füllt der Lauf aus `## Description` und, wo es ihn gibt, `## Approach` nach der Art aus der
Gewerk-Tabelle in [ref-ticket-templates.md](ref-ticket-templates.md); was die Datei nicht trägt, steht
als `- offen`. Für jede andere Anforderung gilt §275 weiter: ohne Lösungsansatz kein Ticket.

## Offen lassen

**Ist der Lösungsansatz nicht entscheidbar**, weil `classification` leer ist, `## Approach` mehrere Lösungsansätze
ohne Wahl trägt oder `solution_status` `blocked` ist, **legt der Lauf die Lösungsansätze der Datei dem Lead
vor** (§220); eigene fügt er nicht hinzu. Lässt der Lead ihn offen, steht im `Lösungsansatz` der
Story „Entscheidung offen, entscheidet ‹Gewerk›; Alternative ‹…›; geprüft und verworfen ‹…›" in der
Sprache des Projekts. Das Ticket entsteht trotzdem (§214).

## Das Gewerk je Kriterium

**Jedes Kriterium aus `## Acceptance criteria` bekommt ein Gewerk** (§281): das des Teils des Lösungsansatzes,
der es erfüllt. Trägt `classification` zwei Arten, sagt `## Details`, welcher Teil welches Kriterium
trägt. Die Zuordnung ist in jeder Art der Beauftragung gleich; der Lead bestätigt sie in der
Vorschau.

**Das Gewerk je Klassifizierung steht im Datalayer-Vertrag**, Abschnitt „Die Klassifizierung“
(`${CLAUDE_SKILL_DIR}/../../docs/datalayer-contract.md`, §324): `Konfig` für `shop`, `theme_native`,
`app`; `DEV` für `theme`, `custom_app`; `Schnittstelle` für die drei `integration_*`. **Bei einer
Migration folgt es der Domäne des Epics**: im Epic `data_migration` `Schnittstelle`, gleich über
welchen Lösungsansatz, im Epic `content_migration` `Konfig`. Dazu, nur am Ticket:

| Fall | Gewerk |
|---|---|
| die Anforderung steht im Epic der Domäne `design`: die Arbeit des Designers, auch ohne Lösungsansatz (§285, §297) | `UX/UI` |
| im Expert Service das Design zu einem Feature, mit dem Add-on `design` und `design_needed: yes` (§285, §303) | `UX/UI` |

Ein Feed ist keine Schnittstelle, sondern `Konfig`. Tracking ist kein Gewerk: seine Kriterien gehen an
`Konfig` oder `DEV`. **Ohne das Add-on `design` in `add_ons` gibt es keine UX/UI-Arbeit** (§303);
`design_needed: open` fragt der Lauf den Lead.

**Ein Kriterium ohne Gewerk ist eine offene Frage zum Lösungsansatz** (§281): kein Teil des Lösungsansatzes erfüllt es.
Die Vorschau nennt es als Befund mit dem nächsten Lauf, `solution-design`, im Expert Service
`solution-approach`. Die Story entsteht trotzdem und trägt das Kriterium, weil an ihr abgenommen
wird; einem Subtask ordnet der Lauf es nur zu, wenn der Lead in der Vorschau ein Gewerk nennt.

## Story oder Story mit Subtasks

| Fall | Story | Subtasks |
|---|---|---|
| **ein Gewerk** | Komponente bzw. `Kategorie` des Gewerks, `Angaben für ‹Gewerk›`, Stufe `story` | keine |
| **mehrere Gewerke** | keine Komponente, keine Angaben, der übergreifende `Lösungsansatz`, Stufe `story --split` | je Arbeitseinheit eines Gewerks einer, Stufe `subtask` |
| **Seitentyp** (eine Anforderung in einem Epic der Domäne `storefront`, wie `check-repo.py` sie als `page_type` zählt) | immer Stufe `story --split`, ohne Komponente: ihre Arbeitseinheiten sind die Sections | erst nach der Übergabe des Designs, je Section einer (unten) |

**Die Arbeitseinheit eines Gewerks** ist sein Teil des Lösungsansatzes: ein Subtask je Gewerk, außer `## Details`
nennt für ein Gewerk getrennte Arbeit, etwa „App installieren“ und „App einrichten“. Ein Subtask trägt
einen eigenen Titel, der die Aufgabe nennt, nie das Gewerk; als User Story die der Story,
zugeschnitten auf das, was er liefert (`../../docs/user-story-contract.md`); als `Kriterien der Umsetzung` die Kriterien seines Gewerks, mit
`## Details` technischer gefasst; und die Angaben seines Gewerks. Kein Subtask für Testing oder
Dokumentation (§281).

**Kommt bei einer Anforderung ein Gewerk dazu**, baut die Vorschau die Story um (§281): Komponente
weg, Body nach `story --split`, je Gewerk ein Subtask. Das ist eine Änderung an einem bestehenden
Ticket und läuft nach `SKILL.md`, Step 5 und 9.

## Seitentypen und Sections

**Mit der Freigabe entsteht die Story je Seitentyp mit ihren Abnahme-Kriterien, ohne
Section-Subtasks** (§285); die erste Story im Theme-Epic ist „Design-System und globale Sections“
(ohne das Add-on `design` „Theme-Einstellungen und globale Sections“; bei `en` „Design system and
global sections“ bzw. „Theme settings and global sections“), wie `requirements-update` und
`epic-structure` sie anlegen.

**Section-Subtasks entstehen nach der Übergabe des Designs**: aus jedem Listenpunkt unter
`## Sections` ein Subtask, Titel `REQ-012-n ‹Name der Section›`, Gewerk `DEV`, unter `Links` die
`Design-Referenz` mit dem Frame aus dem Listenpunkt. Bei einem gekauften Theme nennt der Lead in der
Vorschau, welche Section im Editor eingestellt wird; deren Subtask trägt `Konfig`.

**Meldet `check-repo.py` für die Anforderung `sections`**, sind mehr Sections übergeben als angenommen,
eine Änderung des Scopes (§285): für diese Anforderung entsteht kein Section-Subtask, und die Vorschau
nennt die offene Frage in `gaps/`, die sie klärt, oder dass sie fehlt. Der nächste Lauf ist
`requirements-update`.

## Die Reihenfolge der Subtasks

**Die Subtasks einer Story stehen in Arbeitsreihenfolge, ausgedrückt durch ihre Nummer** (§285), etwa
`REQ-012-1 App installieren` (Konfig), `REQ-012-2 Screendesign` (UX/UI), `REQ-012-3 Anpassung` (DEV).
Der Lauf leitet sie aus dem Lösungsansatz ab: was die anderen voraussetzen, zuerst, also Einstellung oder
Installation, dann Design, dann Bau, dann Anbindung oder Übernahme, wo `## Details` nichts anderes
sagt; Sections in der Folge der Liste unter `## Sections`. Der Lead bestätigt die Reihenfolge in der
Vorschau. **Keine Verknüpfung „blocks“** (§209).

Ein Subtask, der schon auf dem Board steht, behält seine Nummer; ein neuer zählt vom höchsten
`REQ-012-n` der Anforderung weiter, auch wenn die Arbeitsreihenfolge ihn weiter vorn sähe. Die
Vorschau nennt das.
