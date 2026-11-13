# Module eq_ownerp_ui

## 14.10.2026

### Version 19.0.1.4.16

#### [FIX]

**DE:** Sonderzeichen auf der Store-Seite repariert. Mit 19.0.1.4.15 waren alle Entities
in UTF-8-Zeichen umgewandelt worden; der Store hat daraufhin sämtliche Umlaute, Akzente,
Gedankenstriche und Häkchen doppelt kodiert („FranÃ§ais“). Als Entity geschriebene
Zeichen kamen dagegen in beiden veröffentlichten Ständen richtig an. Die Seite besteht
jetzt ausschließlich aus ASCII-Zeichen, jedes Sonderzeichen steht als Entity (`&auml;`,
`&mdash;`, `&#10003;`). Im Releases-Bereich der Store-Seite trägt der aktuelle Eintrag
jetzt 19.0.1.4.16.

**EN:** Special characters on the store page repaired. Version 19.0.1.4.15 had turned
all entities into UTF-8 characters, and the store then double-encoded every umlaut,
accent, dash and check mark ("FranÃ§ais"). Characters written as entities had come
through correctly in both published states. The page now consists of ASCII characters
only, with every special character written as an entity (`&auml;`, `&mdash;`,
`&#10003;`). The latest entry in the store page's Releases section now reads
19.0.1.4.16.

### Version 19.0.1.4.15

#### [FIX]

**DE:** Store-Seite an den Filter von apps.odoo.com angepasst. Der Store lässt nur die
CSS-Eigenschaften durch, die auch Odoos eigener HTML-Filter erlaubt, und verwarf deshalb
Hintergründe, Schatten, linke Randlinien und das gesamte Flexbox-Layout: die Info-Chips
brachen mehrzeilig um, die dunkle Spalte des Hilfe-Blocks war weiß und lief aus der
Karte. Zudem kodierte der Store Umlaute, Gedankenstriche und Pfeile doppelt, wo sie im
selben Textstück wie eine HTML-Entity standen. Die Seite nutzt jetzt nur erlaubte
Eigenschaften (`background-color`, Tabelle statt Flexbox, Einzelangaben für den linken
Rand) und durchgehend UTF-8-Zeichen statt Entities; die drei Cross-Selling-Kacheln
stehen wieder in einer Reihe. Die Darstellung im Odoo-Apps-Menü ist unverändert. Der
Releases-Bereich der Store-Seite endete bei 19.0.1.4.2 und führt jetzt die Stände bis
19.0.1.4.15.

**EN:** Store page adapted to the apps.odoo.com filter. The store keeps only the CSS
properties Odoo's own HTML sanitizer allows, and therefore dropped backgrounds, shadows,
left border lines and the whole flexbox layout: the info chips wrapped onto several
lines, and the dark column of the help block turned white and ran out of its card. The
store also double-encoded umlauts, dashes and arrows wherever they shared a text run
with an HTML entity. The page now uses only permitted properties (`background-color`, a
table instead of flexbox, longhand left-border properties) and plain UTF-8 characters
instead of entities; the three cross-selling tiles sit in one row again. The rendering
in Odoo's Apps menu is unchanged. The Releases section of the store page stopped at
19.0.1.4.2 and now lists the versions up to 19.0.1.4.15.

## 04.09.2026

### Version 19.0.1.4.14

#### [CHG]

**DE:** Store-Seite neu abgestimmt: ruhige, neutrale Info-Chips statt zweifarbiger
Pills, weiße Kopfzeile mit feiner Trennlinie, Blau als einziger Akzent statt Aubergine,
Banner-Grafik neu erzeugt und als animierte Store-Kopfgrafik ergänzt: das erste
Manifest-Bild ist jetzt ein GIF, das nach der Wortmarke drei Aufnahmen der echten
Oberfläche einblendet (Farbvorlage, Vorlagen-Formular, Dark Mode), englisch beschriftet.
Neuer Chip „Odoo.sh“ neben Community und Enterprise; die FAQ nennt Odoo.sh ausdrücklich
und erklärt, dass Odoo Online keine Store-Apps zulässt.

**EN:** Store page re-tuned: quiet neutral info chips instead of two-tone pills, white
header with a thin rule, blue as the single accent instead of aubergine, banner graphic
regenerated and extended into an animated Store cover: the first manifest image is now a
GIF that follows the wordmark with three captures of the real UI (colour template,
template form, dark mode), captioned in English. New "Odoo.sh" chip next to Community
and Enterprise; the FAQ names Odoo.sh explicitly and explains that Odoo Online does not
accept store apps.

## 03.09.2026

### Version 19.0.1.4.13

#### [FIX]

**DE:** Die Regel, die Links in der Link-Farbe einfärbt, traf mit `!important` auch die
Einträge der Menü-Dropdowns in der Navigationsleiste, das Apps- bzw. Home-Menü samt
Suche und das mobile Burger-Menü. Folgen: Menüeinträge ließen sich nur noch über die
Link-Farbe steuern, der markierte Eintrag verlor seine eigene Farbe, und bei der grünen
Vorlage standen die Suchtreffer grün auf grünem Grund. Diese Bereiche behalten jetzt
Odoos eigene Farben. Ein Migrationsskript erzeugt das Stylesheet beim Update neu.

**EN:** The rule painting links in the link colour also hit, with `!important`, the
entries of the navbar dropdowns, the apps or home menu with its search results and the
mobile burger menu. Consequences: menu entries could only be steered through the link
colour, the marked entry lost its own colour, and with the green template the search
results stood green on green. Those areas now keep Odoo's own colours. A migration
script regenerates the stylesheet on update.

## 02.09.2026

### Version 19.0.1.4.12

#### [CHG]

**DE:** Die Modulbeschreibung nennt jetzt den häufigsten Einsatzfall, der bisher fehlte:
Wer für einen Kunden mehrere Systeme betreibt — eines für den täglichen Betrieb, eines
zum Üben und eines für Vorabversionen —, gibt jedem System eine eigene Farbe. Beim
Anmelden ist damit sofort sichtbar, wo gearbeitet wird, und eine geübte Änderung landet
nicht versehentlich im Produktivsystem. Ebenfalls ergänzt: Wird die Community-Edition
eingesetzt, lässt sich zusammen mit dem Zusatzmodul web_responsive der Odoo Community
Association ein Erscheinungsbild herstellen, das dem der Enterprise-Edition sehr
nahekommt. Die Versionsangabe der Beschreibung hing vier Stände zurück und ist
nachgezogen. Am Verhalten des Moduls ändert sich nichts.

**EN:** The module description now names its most common use case, which was missing so
far: anyone running several systems for a customer — one for daily work, one for
practising and one for previews — gives each system its own colour. Logging in then
shows immediately which system you are in, and a rehearsed change does not slip into
production by accident. Also added: when the Community edition is in use, the
web_responsive add-on from the Odoo Community Association produces a look that comes
close to the Enterprise edition. The description's version stamp lagged four releases
behind and has been brought up to date. Module behaviour is unchanged.

## 31.08.2026

### Version 19.0.1.4.11

#### [FIX]

**DE:** Das Hintergrundbild-Feld auf `res.company` heißt jetzt „ownERP Home Menu
Background Image“. Bisher trug es exakt dasselbe Label wie das gleichnamige Feld aus
Odoo Enterprise (`web_studio.background_image`). Sind beide Module installiert,
protokollierte Odoo bei jedem Registry-Aufbau eine Warnung, und in Feldauswahllisten —
Export, Filter, Odoo Studio — erschienen zwei nicht unterscheidbare Einträge „Home Menu
Background Image“. Das Feld selbst, seine Daten und die Oberfläche des Farb-Assistenten
bleiben unverändert.

**EN:** The background image field on `res.company` is now labelled "ownERP Home Menu
Background Image". It previously carried exactly the same label as the identically named
field from Odoo Enterprise (`web_studio.background_image`). With both modules installed
Odoo logged a warning on every registry build, and field pickers — export, filters, Odoo
Studio — offered two indistinguishable "Home Menu Background Image" entries. The field
itself, its data and the colour wizard's UI are unchanged.

## 25.08.2026

### Version 19.0.1.4.10

#### [CHG]

**DE:** Die Store-Seite trägt jetzt den Block „Die Hilfe zu diesem Modul ist
auffindbar“. Er zeigt in jeder Sprache, welche Hilfeseiten das Modul mitbringt und dass
ein KI-Assistent dieselben Inhalte über die Modulkarte lesen kann. Die genannten
Seitentitel und Textausschnitte stammen aus den tatsächlich mitgelieferten Hilfeseiten.

**EN:** The store listing now carries the "The help for this module is findable" block.
In every language it shows which help pages the module ships and that an AI assistant
reads the same content through the module card. The page titles and text excerpts shown
are taken from the help pages actually shipped.

## 25.08.2026

### Version 19.0.1.4.9

#### [FIX]

**DE:** Zusammenspiel mit fremden Dark-Mode-Modulen (Odoo Enterprise `web_enterprise`,
OCA `web_dark_mode`) bereinigt. Zwei Ursachen:

1. Der eingespritzte Farb-Stylesheet richtete sich nach dem Cookie `color_scheme`, Odoo
   wählt sein Dark-Paket aber nach `ir.http.color_scheme()`. Beide liefen auseinander,
   sobald ein Fremdmodul entschied — Enterprise löscht das Cookie beim Abmelden, OCA
   schreibt es erst nach dem Ausliefern der Seite. Nach jeder Anmeldung erschien deshalb
   kurz die dunkle Odoo-Oberfläche mit der hellen Firmenpalette darüber. Der Stylesheet
   folgt jetzt demselben Wert wie das Asset-Paket.
2. Ein „hell“ vom Fremdmodul wurde als „noch nicht entschieden“ gelesen und übersteuert.
   Damit gewann die hier gespeicherte Vorliebe gegen die bewusste Wahl „Hell“ in den
   Enterprise-Voreinstellungen beziehungsweise gegen ein abgeschaltetes `dark_mode` in
   OCA. Erkannt wird ein Fremdmodul jetzt an seinem Feld auf `res.users.settings` —
   dasselbe Signal, an dem der Schalter im Benutzermenü schon immer zurücktrat. Ist
   eines installiert, hält sich dieses Modul beim Dark Mode vollständig heraus; die
   Firmenfarben folgen dann dessen Entscheidung.

Zusätzlich bleibt der dunkle Seitenhintergrund jetzt auf das Backend beschränkt.
`web.layout` trägt auch Website-, Portal- und Kiosk-Seiten; eine nicht eingegrenzte
`body`-Regel färbte diese für jeden internen Benutzer mit dunklem Backend mit ein.

**EN:** Fixed the interplay with foreign dark-mode modules (Odoo Enterprise
`web_enterprise`, OCA `web_dark_mode`). Two causes:

1. The injected colour stylesheet branched on the `color_scheme` cookie while Odoo picks
   its dark bundle from `ir.http.color_scheme()`. The two drifted apart as soon as a
   foreign module decided — Enterprise drops the cookie on logout, OCA writes it only
   after the page has been rendered — so every login briefly showed the dark Odoo shell
   with the light corporate palette on top. The stylesheet now follows the same value as
   the asset bundle.
2. A `"light"` from a foreign module was read as "nothing decided yet" and overruled, so
   the preference stored here beat a deliberate "Light" choice in the Enterprise
   preferences or a disabled `dark_mode` in OCA. A foreign provider is now detected by
   its field on `res.users.settings` — the same signal the switch in the user menu has
   always used. With one installed, this module stays out of dark mode entirely and the
   corporate colours follow its decision.

The dark page backdrop is now confined to the backend as well. `web.layout` also carries
website, portal and kiosk pages, and an unqualified `body` rule tinted those for every
internal user running a dark backend.

## 22.08.2026

### Version 19.0.1.4.8

#### [CHG]

**DE:** Capability Card: Frontmatter auf OKF v0.2 umgestellt (generated/status statt
timestamp).

**EN:** Capability card: frontmatter migrated to OKF v0.2 (generated/status replace
timestamp).

## 12.08.2026

### Version 19.0.1.4.7

#### [CHG]

**DE:** Das Modul steht ab dieser Fassung unter der LGPL-3 statt unter der AGPL-3. Die
AGPL verlangt die Offenlegung des Quelltextes auch dann, wenn die Software nur über das
Netz genutzt und nicht weitergegeben wird - eine Bedingung, die auf ein Odoo-Modul im
Kundenbetrieb nicht passt. Die LGPL-3 lässt die Einbindung in eigene, auch geschlossene
Erweiterungen zu und verlangt die Offenlegung nur für Änderungen am Modul selbst. Für
bereits ausgelieferte Fassungen gilt die AGPL-3 unverändert weiter.

**EN:** From this release the module is licensed under LGPL-3 instead of AGPL-3. The
AGPL requires source disclosure even when the software is merely used over a network
rather than distributed - a condition that does not fit an Odoo module running at a
customer site. LGPL-3 permits use from proprietary extensions and requires disclosure
only for changes to the module itself. Versions already shipped remain under AGPL-3.

## 11.08.2026

### Version 19.0.1.4.6

#### [ADD]

**DE:** Die Store-Seite verweist jetzt auf das übrige Sortiment: auf das DACH-Paket, auf
Odoo2Fast.Report und auf den ownERP-Chatbot. Welche Ziele beworben werden, steht im
Manifest (`ownerp_cross_selling`) und nicht mehr nur in der erzeugten Seite.

**EN:** The Store page now points to the rest of the range: the DACH package,
Odoo2Fast.Report and the ownERP chatbot. What gets advertised is recorded in the
manifest (`ownerp_cross_selling`) rather than only in the generated page.

### Version 19.0.1.4.5

#### [FIX]

**DE:** Die Farbfelder für den Hover-Hintergrund waren mit „Hoover Backgroundcolor“
beschriftet — ein Tippfehler, der in der Farbverwaltung und im Dark Mode sichtbar war.
Die Beschriftung lautet jetzt „Hover Backgroundcolor“. Die technischen Feldnamen bleiben
unverändert, bestehende Farbvorlagen sind davon nicht betroffen. Spanische und
französische Übersetzungen für die Farbfelder sind ergänzt.

**EN:** The colour fields for the hover background were labelled “Hoover
Backgroundcolor” — a typo visible in the colour management and in dark mode. The label
now reads “Hover Backgroundcolor”. The technical field names are unchanged, so existing
colour templates are unaffected. Spanish and French translations for the colour fields
have been added.

## 08.08.2026

### Version 19.0.1.4.4

#### [CHG]

**DE:** Agent Capability Card auf den Stand des Moduls gebracht (Versionsstempel).

**EN:** Agent capability card brought up to the module's state (version stamp).

## 08.08.2026

### Version 19.0.1.4.3

#### [CHG]

**DE:** README überarbeitet: Werbefloskeln durch konkrete Aussagen ersetzt.

**EN:** README reworked: marketing filler replaced by concrete statements.

## 08.08.2026

### Version 19.0.1.4.2

#### [CHG]

**DE:** App-Store-Beschreibung neu erstellt: viersprachig (EN/DE/FR/ES) mit
Sprachumschalter, Marken-Banner und je Sprache eigenem Eyecatcher.

**EN:** App Store listing rebuilt: four languages (EN/DE/FR/ES) with a language
switcher, a brand banner and a per-language eyecatcher.

**DE:** Paketzugehörigkeit im Manifest hinterlegt und als Info-Pill sichtbar.

**EN:** Package membership recorded in the manifest and shown as an info pill.

**DE:** Funktionsumfang.md aus Anwendersicht ergänzt bzw. aktualisiert.

**EN:** Funktionsumfang.md added or refreshed from the user's perspective.

## 06.08.2026

### Version 19.0.1.4.1

#### [CHG]

**DE:** Die beiden Farbvorlagen-Ansichten tragen jetzt sprechende Backend-URLs:
`/odoo/ownerp-colors` (Vorlagen) und `/odoo/ownerp-template-colors` (Farbeinstellungen)
statt `/odoo/action-<Nummer>`. Die Nummer ist ein Datenbankschlüssel und auf jeder
Instanz eine andere — ein weitergegebener Link darauf zeigte anderswo ins Leere oder auf
einen fremden Bereich. Bestehende Links in Nummernform funktionieren weiterhin.

**EN:** The two colour-template views now have readable backend URLs:
`/odoo/ownerp-colors` (templates) and `/odoo/ownerp-template-colors` (colour settings)
instead of `/odoo/action-<id>`. That id is a database key and differs on every instance,
so a shared link pointed nowhere — or somewhere else entirely — on another system.
Existing numeric links keep resolving.

## 05.08.2026

### Version 19.0.1.4.0

#### [CHG]

**DE:** Fünf der zehn mitgelieferten Farbvorlagen unterschritten im hellen Backend den
Lesbarkeitswert von 4,5:1 (WCAG AA) — am deutlichsten „Warm Amber“ mit 3,68:1 in der
Navigationsleiste und 3,62:1 auf der primären Schaltfläche. Betroffen waren elf Werte in
„Default Blue“, „Default Red“, „Default Green“, „Tech Teal“ und „Warm Amber“. Sie wurden
so weit abgedunkelt, wie zum Erreichen von 4,5:1 nötig war; der Farbton bleibt
unverändert, die Vorlagen sehen also weiterhin so aus wie bisher, nur eine Spur satter.
Beim Update wird die aktive Vorlage automatisch neu angewendet.

| Vorlage       | Wert                           | vorher    | nachher   |
| ------------- | ------------------------------ | --------- | --------- |
| Default Blue  | Schrift sekundäre Schaltfläche | `#747474` | `#5D5D5D` |
| Default Red   | primäre Schaltfläche           | `#d94a28` | `#D24526` |
| Default Red   | Schrift sekundäre Schaltfläche | `#90440e` | `#8E430E` |
| Default Red   | Sekundärfarbe                  | `#858585` | `#767676` |
| Default Green | primäre Schaltfläche           | `#509114` | `#4A8514` |
| Default Green | Linkfarbe                      | `#08a427` | `#088A1D` |
| Tech Teal     | primäre Schaltfläche           | `#148F77` | `#14856D` |
| Tech Teal     | Linkfarbe                      | `#138D75` | `#13856D` |
| Warm Amber    | Navigation                     | `#B9770E` | `#A5690E` |
| Warm Amber    | primäre Schaltfläche           | `#CA6F1E` | `#B0621E` |
| Warm Amber    | Linkfarbe                      | `#B9770E` | `#A5690E` |

**EN:** Five of the ten shipped colour templates fell below the 4.5:1 readability
threshold (WCAG AA) in the light backend — most visibly "Warm Amber" at 3.68:1 on the
navbar and 3.62:1 on the primary button. Eleven values across "Default Blue", "Default
Red", "Default Green", "Tech Teal" and "Warm Amber" were affected. They have been
darkened by exactly as much as reaching 4.5:1 required; the hue is unchanged, so the
templates still look the way they did, just a shade richer. The active template is
re-applied automatically on update.

Ein Test prüft ab sofort jede mitgelieferte Vorlage auf Navigationsleiste,
Schaltflächen, Text, Sekundärtext und Links, damit eine neue Vorlage diesen Stand nicht
wieder unterschreitet.

A test now checks every shipped template across navbar, buttons, text, muted text and
links, so a new template cannot drop back below this.

**DE:** Die App-Store-Seite wurde auf diesen Stand gebracht (alle vier Sprachen):
Dunkelmodus als eigener Funktionsblock, 14 statt 10 Themen, die Angabe zur
Barrierefreiheit gilt jetzt für alle Vorlagen statt für sechs. Die Kurzbeschreibung im
Manifest nennt den Dunkelmodus.

**EN:** The App Store page was brought up to this state (all four languages): dark mode
as its own feature block, 14 themes instead of 10, and the accessibility statement now
covers every template rather than six. The manifest summary mentions dark mode.

### Version 19.0.1.3.2

#### [ADD]

**DE:** Der Dunkelmodus stellt jetzt die Flächenvariablen bereit, die andere Module
lesen: `--o-view-background-color`, `--o-webclient-background-color` und die Graustufen
`--gray-100` bis `--gray-900`. Module, die sauber über CSS-Variablen mit hellem Fallback
gestaltet sind — etwa `var(--o-view-background-color, #fff)` — folgen dem Dunkelmodus
damit von selbst, ohne dass dieses Modul ihre Klassennamen kennen muss. `eq_knowledge`
ist so gebaut und war deshalb bislang durchgehend weiß.

**EN:** Dark mode now provides the surface variables other modules read:
`--o-view-background-color`, `--o-webclient-background-color` and the grey scale
`--gray-100` through `--gray-900`. Modules styled properly through CSS variables with a
light fallback — `var(--o-view-background-color, #fff)`, for instance — follow dark mode
on their own, without this module needing to know their class names. `eq_knowledge` is
built that way and stayed entirely white until now.

#### [FIX]

**DE:** Der Kopfbereich von Formularen (`.o_form_statusbar`) blieb im Dunkelmodus hell —
sichtbar unter anderem im Farbwizard selbst, wo die Schaltflächen „Anwenden“ und „Alle
Farben zurücksetzen“ auf hellem Balken standen.

**EN:** The form header bar (`.o_form_statusbar`) stayed light in dark mode — visible in
the colour wizard itself, where the "Apply" and "Reset All Colors" buttons sat on a
light strip.

### Version 19.0.1.3.1

#### [FIX]

**DE:** Im Dunkelmodus waren mehrere Bereiche unlesbar. Betroffen waren Dropdown-Menüs,
die Einstellungsseite mit ihrer Seitenleiste, das App-Menü von `web_responsive`, die
Discuss-Oberfläche, Beschriftungen von Smart-Buttons sowie Hinweisboxen. Ursache: Odoo
kompiliert an diesen Stellen helle Flächen und die dunkle Schriftfarbe `#212529` fest in
seine Stylesheets; über Farbvariablen sind sie zur Laufzeit nicht erreichbar. Diese
Stellen werden jetzt einzeln gesetzt. Statusfarben (Erfolg, Warnung, Fehler) werden im
Dunkelmodus aufgehellt, weil Odoos Werte für weißen Hintergrund gemischt sind.

**EN:** Several areas were illegible in dark mode: dropdown menus, the settings page and
its sidebar, the `web_responsive` apps menu, the Discuss interface, smart-button labels
and alert boxes. The cause: Odoo compiles light surfaces and the dark text colour
`#212529` into its stylesheets at those points, out of reach of colour variables at
runtime. They are now set individually. Status colours (success, warning, danger) are
brightened in dark mode, because Odoo's values are mixed for a white background.

**DE:** Farbvorlagen ohne eigene Dunkel-Palette erzeugten teils unlesbare Kombinationen
— etwa weiße Schrift auf hellgrünem Button (1,65:1) bei „Default Green“. Die Ableitung
verschob die Helligkeit um einen festen Betrag und ließ die Schriftfarben unverändert.
Sie verschiebt Farben jetzt so weit, bis ein Kontrast von 4,5:1 gegen die hellste Fläche
erreicht ist, und wählt jede Schriftfarbe passend zu ihrem Untergrund. Beim Update wird
die aktive Vorlage automatisch neu berechnet.

**EN:** Colour templates without a dark palette of their own produced unreadable
combinations — white text on a pale green button (1.65:1) for "Default Green", among
others. The derivation shifted lightness by a fixed amount and left the text colours
untouched. It now shifts colours until they reach 4.5:1 against the lightest surface,
and picks each text colour to suit the background it sits on. The active template is
recalculated automatically on update.

**DE:** Das App-Menü von `web_responsive` behielt seinen eigenen hellen Farbverlauf,
statt die eingestellten Navigationsfarben zu übernehmen — im Dunkelmodus eine
bildschirmfüllende helle Fläche. Ursache: Die Regel adressierte nur die Klasse
`.dropdown-menu-custom`, während neuere Fassungen von `web_responsive` den Container
`.app-menu-container` nennen. Beide werden nun angesprochen. Das betraf auch den hellen
Modus, dort nur weniger auffällig.

**EN:** The `web_responsive` apps menu kept its own pale gradient instead of picking up
the configured navigation colours — a full-screen light panel in dark mode. The cause:
the rule addressed only the `.dropdown-menu-custom` class, while newer builds of
`web_responsive` name the container `.app-menu-container`. Both are now targeted. This
affected light mode as well, just less visibly.

**Geprüft / Verified:** Alle 14 Farbvorlagen wurden im Dunkelmodus über Listen-,
Einstellungs- und Discuss-Ansicht mit einer WCAG-Kontrastmessung durchlaufen — ohne
Befund.

### Version 19.0.1.3.0

#### [ADD]

**DE:** Dark Mode für das Backend. Im Benutzermenü liegt jetzt ein Schalter „Dark Mode“;
die Wahl wird am Benutzer gespeichert und gilt daher auch auf einem anderen Rechner.
Jede Farbvorlage hat dafür einen zweiten Farbsatz, der ausschließlich im Dark Mode
greift — einzustellen im Reiter „Dark Mode“ unter „Einstellungen > Template Colors >
Colors“. Vorlagen ohne eigenen Dark-Satz bekommen automatisch abgeleitete Farben, der
Dark Mode landet also nie auf einem unlesbaren Bildschirm.

Technisch setzt das Modul auf das Cookie `color_scheme`, dieselbe Grundlage, die Odoo
Enterprise und OCA `web_dark_mode` verwenden. Ist eines dieser Module installiert, tritt
der eigene Schalter zurück und überlässt ihm die Steuerung — im Benutzermenü erscheint
also nie ein zweiter Eintrag. Ohne beide funktioniert der Dark Mode trotzdem, auch in
reiner Community.

**Einschränkung:** In reiner Community ohne eines dieser Module deckt der Dark Mode die
Flächen ab, die über Farbvariablen erreichbar sind. Einzelne Odoo-Komponenten tragen
fest einkompilierte helle Farben, die sich zur Laufzeit nicht ändern lassen. Mit
`web_enterprise` oder OCA `web_dark_mode` greifen zusätzlich deren vollständige
Dark-Stylesheets, und beide vertragen sich mit den hier eingestellten Farben.

**EN:** Dark mode for the backend. The user menu now carries a "Dark Mode" switch; the
choice is stored on the user and therefore carries over to another machine. Every colour
template gained a second colour set that only applies in dark mode, editable in the
"Dark Mode" tab under "Settings > Template Colors > Colors". Templates without a dark
set of their own get derived colours automatically, so dark mode never lands on an
unreadable screen.

Under the hood this builds on the `color_scheme` cookie, the same basis Odoo Enterprise
and OCA `web_dark_mode` use. With either of those installed the module's own switch
stands down and leaves them in control, so the user menu never shows a second entry.
Without them dark mode still works, on plain Community too.

**Limitation:** On plain Community without either module, dark mode covers the surfaces
reachable through colour variables. A few Odoo components carry light colours compiled
into their stylesheets that cannot be changed at runtime. With `web_enterprise` or OCA
`web_dark_mode` their complete dark stylesheets apply on top, and both get along with
the colours configured here.

**DE:** Vier Farbvorlagen „IT-Guy Terminal“ (Grün, Amber, Cyan, Weiß), abgestimmt auf
das Website-Theme `theme_itguy`. Im Dark Mode tragen sie die Phosphorfarben des Themes
unverändert (Grün `#00FF00` auf Schwarz); im hellen Backend werden dieselben Töne
abgedunkelt, weil die Neonwerte auf weißem Grund nur etwa 1,4:1 Kontrast erreichen und
dort nicht lesbar wären.

**EN:** Four "IT-Guy Terminal" colour templates (green, amber, cyan, white), matching
the `theme_itguy` website theme. In dark mode they carry the theme's phosphor colours
unchanged (green `#00FF00` on black); in the light backend the same hues are darkened,
because the neon values reach only about 1.4:1 contrast on white and would be illegible
there.

#### [FIX]

**DE:** Die Theme-Farben machten jeden Dark Mode unbrauchbar: Textfarbe und weiße
Listenhintergründe wurden unabhängig vom Farbschema erzwungen, sodass mit Enterprise
oder OCA `web_dark_mode` dunkle Schrift auf dunklem Grund stand. Die Farben werden jetzt
pro Schema getrennt gesetzt.

**EN:** The theme colours broke every dark mode: the text colour and white list
backgrounds were forced regardless of the colour scheme, so with Enterprise or OCA
`web_dark_mode` dark text ended up on a dark background. The colours are now applied per
scheme.

## 03.08.2026

### Version 19.0.1.2.1

#### [CHG]

**DE:** README: deutscher Teil mit korrekten Umlauten neu geschrieben, EQ-Präfix
entfernt, Menüpfad auf den tatsächlichen Pfad „Einstellungen > Template Colors“
korrigiert, Odoo-Version auf 19.0+ korrigiert.

**EN:** README: rewrote the German part with proper umlauts, removed the EQ prefix,
corrected the menu path to the actual "Settings > Template Colors" and set the Odoo
version to 19.0+.

## 30.07.2026

### Version 19.0.1.2.0

#### [CHG]

**DE:** Die beiden Farbfelder unter „E-Mail-Vorlagen“ in den Einstellungen sehen jetzt
aus wie alle anderen Farbfelder des Themes. Sie stammen aus Odoo und wurden als nackter
Farbkreis mit danebengequetschter Beschriftung dargestellt; jetzt nutzen sie dasselbe
Widget wie die Theme-Farben (Farbfeld plus Hex-Eingabe) mit der Beschriftung über dem
Feld. Wortlaut und gespeicherte Werte bleiben unverändert.

**EN:** The two colour fields under "Email Templates" in the settings now look like
every other colour field of the theme. They come from Odoo and were rendered as a bare
colour circle with a label squeezed in beside it; they now use the same widget as the
theme colours (swatch plus hex input) with the label above the field. Wording and stored
values are unchanged.

#### [ADD]

**DE:** Neue Schaltfläche „Farben aus Theme übernehmen“ neben den E-Mail-Farben: Sie
schreibt Hintergrund- und Schriftfarbe der primären Schaltfläche aus der eingestellten
Farbvorlage in die E-Mail-Farben, damit automatische E-Mails dieselbe Hausfarbe tragen
wie das Backend. Bisher blieben dort Odoos Standardwerte (`#875A7B` Aubergine auf Weiß)
stehen, egal welche Farben eingestellt waren. Die Übernahme passiert nur auf Knopfdruck
— eine bewusst abweichende E-Mail-Farbe wird nie ungefragt überschrieben. Fehlende oder
unbrauchbare Werte fallen auf die Theme-Standardfarben zurück, achtstellige Hex-Werte
werden auf sechs Stellen gekürzt, weil E-Mail-Programme den Alphakanal nicht zuverlässig
unterstützen.

**EN:** New "Apply Theme Colors" button next to the e-mail colours: it copies the
primary button's background and font colour from the configured colour template into the
e-mail colours, so automated e-mails carry the same corporate colour as the backend.
Until now Odoo's defaults stayed there (`#875A7B` aubergine on white) no matter which
colours were configured. The copy only happens on demand — a deliberately different
e-mail colour is never overwritten unasked. Missing or unusable values fall back to the
theme defaults, and eight-digit hex values are trimmed to six because mail clients do
not reliably support the alpha channel.

**DE:** Erste Testabdeckung für das Modul (15 Tests): Farbnormalisierung,
Übernahme-Aktion samt Rückfallwerten und die Darstellung der E-Mail-Felder in der
Einstellungsansicht.

**EN:** First test coverage for the module (15 tests): colour normalization, the apply
action including its fallbacks, and the rendering of the e-mail fields in the settings
view.

#### [FIX]

**DE:** `mail` als Abhängigkeit ergänzt — die E-Mail-Farbfelder stammen aus diesem Modul
und werden hier angepasst.

**EN:** Added `mail` as a dependency — the e-mail colour fields come from that module
and are adjusted here.

## 26.07.2026

### Version 19.0.1.1.7

#### [CHG]

**DE:** Technische Bezeichner (Ansichts-, Regel- und Vorlagennamen): „EQ“-Token
entfernt.

**EN:** Technical record names (views, rules, templates): removed the "EQ" token.

## 17.07.2026

### Version 19.0.1.1.6

#### [CHG]

**DE:** Capability Card: OKF-v0.1-Frontmatter (maschinenlesbare Metadaten für
KI-Agenten) ergänzt.

**EN:** Capability card: added OKF v0.1 frontmatter (machine-readable metadata for AI
agents).

## 08.07.2026

### Version 19.0.1.1.5

#### [ADD]

**DE:** In-App-Hilfe (`doc/overview`, DE/EN) und Agent Capability Card
(`doc/capability_card.md`) ergänzt.

**EN:** Added in-app help (`doc/overview`, DE/EN) and an agent capability card
(`doc/capability_card.md`).

## 21.06.2026

### Version 19.0.1.1.4

#### ADD

- App Store listing page `static/description/index.html`: multilingual (EN/DE/FR/ES)
  sales page with brand banner, OCA-style info pills, tabbed
  Overview/Features/FAQ/Releases, localised eye-catchers and a colour-theming FAQ
- ownERP-branded product graphics (icon, language-neutral banner, per-language
  eye-catchers `_de`/`_en`/`_fr`/`_es`); language-switcher flags
- `Funktionsumfang.md` (user-facing German value description)

#### CHG

- Manifest `summary` made benefit-led; fixed `images` (pointed to a non-existent
  `images/` folder, now the brand banner + icon)

## 18.03.2026

### Version 19.0.1.1.3

#### FIX

- Scoped all CSS selectors in "EQ Custom Colors" template under `.o_web_client` to
  prevent backend theme styles from leaking into website/webshop pages.
- Added post-migration script to auto-regenerate CSS template on module upgrade (no
  manual re-apply needed).

## 15.03.2026

### Version 19.0.1.1.1

#### FIX

- Fixed navbar color selectors for Odoo 19 Enterprise: `.o_menu_brand`,
  `.o_menu_toggle`, `mark`, `.o_switch_company_menu`, `.o_user_menu` were not targeted
  by CSS due to changed DOM structure (no longer direct children of `.o_main_navbar`)
- Added missing Odoo 19 Enterprise CSS variable overrides: `--o-enterprise-color`,
  `--o-brand-primary`, `--o-brand-odoo`, `--o-action-color`,
  `--o-enterprise-action-color`, `--bs-primary`, `--bs-link-color`,
  `--bs-link-hover-color`
- Fixed `.btn-primary` and `.btn-secondary` base rules missing `!important`, causing
  Enterprise CSS to override theme colors (login button text was same color as
  background)
- All navbar text elements now correctly inherit the configured font color

## 02.02.2026

### Version 19.0.1.1.0

#### Added

- Added 6 new WCAG AA compliant color themes:
  - Corporate Purple (Software, Creative Agencies, Consulting, Education)
  - Tech Teal (IT, SaaS, Healthtech, Fintech, Startups)
  - Warm Amber (E-Commerce, Gastronomy, Events, Logistics)
  - Navy Executive (Banks, Insurance, Legal, Government)
  - Earth Sienna (Agriculture, Wood, Organic, Real Estate)
  - Modern Magenta (Marketing, Fashion, Gaming, Social Media)

## 31.12.2025

### Version 19.0.1.0.2

#### Fixed

- Fixed typo in hex color code for "Default Blue" template (missing 'f')

### Version 19.0.1.0.1

#### Fixed

- Fixed `target='inline'` to `target='current'` in action window (V19 compatibility)

### Version 19.0.1.0.0

#### Migration

- Migrated from Odoo 18.0 to Odoo 19.0
- Updated version format to 19.0.x.x.x
- Applied V19 compatibility patterns

#### 30.12.2025

#### Version 18.0.1.0.3

##### ADD

- Added `api_apply_template` method for external API control.

##### FIX

- Fixed XML parsing error in CSS template.
- Fixed Smart Button value color and Radio Button active state color.
- Fixed color picker.

#### 27.12.2025

#### Version 18.0.1.0.0

##### CHG

- Migration to Odoo 18.
- Updated JavaScript widget from OWL2 to OWL3.
- Changed view type from tree to list.
- Removed deprecated manifest keys (qweb, demo, css).

#### 08.05.2024

#### Version 1.0.11

##### ADD

- Default colors.

#### 07.05.2024

#### Version 1.0.10

##### ADD

- Added colors for the list view.

#### 10.02.2024

#### Version 1.0.8

##### FIX

- black, isort, flake8

#### 02.02.2024

#### Version 1.0.8

##### FIX

- black, isort

#### 17.07.2023

#### Version 1.0.7

##### FIX

- Removed bootstrap-colorpicker.css.map as the map file has no function in Odoo.

#### 07.07.2023

#### Version 1.0.6

##### ADD/FIX

- If a template is deleted when it is selected in the setting, it will be removed.
- The colors are shown in the form view.
- For a temporary fix, I made the save and discard buttons appear.

#### 29.06.2023

#### Version 1.0.5

##### ADD/CHG

- Improved existing 2 colors (red/blue)
- Added 2 new colors (green/grey)

#### 12.05.2023

#### Version 1.0.4

##### ADD

- Added documentation.

#### 12.05.2023

#### Version 1.0.3

##### ADD

- Add logic when there is no background Image.
- Corrected css styles.
- Added templates.

#### 11.05.2023

#### Version 1.0.2

##### ADD

- Added background image option.

#### 09.05.2023

#### Version 1.0.1

##### ADD

- Added Change color function.
- Added color widget.

#### 09.05.2023

#### Version 1.0.0

##### ADD

- Option to change the colors.(not done)
