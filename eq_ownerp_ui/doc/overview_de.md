# Backend-Farben anpassen

**eq_ownerp_ui** ermöglicht es, das Odoo-Backend — Navigationsleiste, Links, Buttons,
Listenzeilen und das App-Icon — an das Corporate Design des Unternehmens anzupassen,
ganz ohne Code.

## Wo zu finden

**Einstellungen → Technisch → Template Colors**, mit zwei Untermenüs:

- **Colors** — der Farbauswahl-Assistent; einen Wert ändern und auf „Anwenden“ klicken,
  um das gesamte Backend sofort zu aktualisieren.
- **Templates** — ein Farbset unter einem Namen speichern (z. B. „ACME Corporate“), um
  es später wiederzuverwenden oder weiterzugeben.

## Was sich anpassen lässt

- Hintergrund, Schriftfarbe und Hover-Zustand der Navigationsleiste
- Linkfarbe
- Primär- und Sekundärfarben der Buttons
- Hintergrundfarben der Listenansicht-Zeilen (inkl. Hover)
- Farbe des App-Menü-Icons
- Ein Hintergrundbild für das Home-Menü (pro Unternehmen)
- Ein zweiter, vollständiger Farbsatz für den Dark Mode

## Typischer Ablauf

1. **Colors** öffnen, Werte anpassen (oder ein gespeichertes **Template** wählen).
2. Auf **Anwenden** klicken — Änderungen gelten sofort für alle.
3. Optional das Ergebnis als neues **Template** für die Wiederverwendung speichern.
4. Mit **Auf Standard zurücksetzen** jederzeit zur Equitania-Standardpalette
   zurückkehren.

## Dark Mode

Über das **Benutzermenü** (oben rechts) lässt sich mit dem Schalter **Dark Mode**
zwischen hellem und dunklem Backend wechseln. Anders als die Farben selbst ist das eine
**persönliche Einstellung**: Sie gilt nur für den jeweiligen Benutzer, wird aber am
Benutzerkonto gespeichert und steht daher auch auf einem anderen Rechner zur Verfügung.

Welche Farben der Dark Mode verwendet, legen Sie im Reiter **Dark Mode** unter
**Colors** fest — ein vollständiger zweiter Satz, unabhängig von den hellen Farben.
Wählen Sie eine Farbvorlage aus, werden beide Sätze zugleich gefüllt. Bringt eine
Vorlage keine eigenen Dark-Farben mit, werden sie automatisch abgeleitet; der Dark Mode
ist also nie unlesbar.

Vier mitgelieferte Vorlagen **IT-Guy Terminal** (Grün, Amber, Cyan, Weiß) passen zum
Website-Theme `theme_itguy` und zeigen im Dark Mode dessen Terminal-Optik: Phosphorfarbe
auf schwarzem Grund. Im hellen Backend sind dieselben Töne abgedunkelt, weil die
Neonfarben auf Weiß nicht lesbar wären.

**Hinweis zum Funktionsumfang:** Ist Odoo Enterprise oder das Modul OCA `web_dark_mode`
installiert, übernimmt dessen Schalter die Steuerung — es erscheint dann nur ein
Dark-Mode-Eintrag im Benutzermenü, und die hier eingestellten Farben gelten weiterhin
und folgen dem dort gewählten Schema. Ohne diese Module funktioniert der Dark Mode
ebenfalls, einzelne Odoo-Bestandteile behalten dann aber ihre hellen Flächen.

## Farben der automatischen E-Mails

Odoo gestaltet die Schaltflächen in automatischen E-Mails über zwei eigene Farbwerte,
die nichts von den hier eingestellten Farben wissen — sie stehen ab Werk auf
Odoo-Aubergine. Sie finden sie unter **Einstellungen → Allgemeine Einstellungen →
Unternehmen → E-Mail-Vorlagen**.

Die Schaltfläche **Farben aus Theme übernehmen** schreibt dort Hintergrund- und
Schriftfarbe Ihrer primären Schaltfläche hinein, sodass E-Mails dieselbe Hausfarbe
tragen wie das Backend. Das geschieht nur auf Knopfdruck: Eine bewusst abweichende
E-Mail-Farbe bleibt erhalten, auch wenn Sie die Backend-Farben später ändern.

Anders als die Backend-Farben gelten diese beiden Werte **pro Unternehmen**.

## Wissenswertes

- Das Anwenden von Farben ändert diese für **alle Benutzer und Unternehmen**
  gleichzeitig. Persönlich ist allein die Wahl zwischen hell und dunkel; das
  Home-Menü-Hintergrundbild wird pro Unternehmen gesetzt.
- Farben sind einfache Textwerte (Hex-Codes) — ein ungültiger Wert löst keinen Fehler
  aus, wird aber falsch dargestellt.
