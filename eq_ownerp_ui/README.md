# Backend UI - Configurable Backend Theme

# Backend UI - Konfigurierbares Backend-Theme

![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)
![Odoo Version](https://img.shields.io/badge/Odoo-19.0+-purple.svg)

## FREE & OPEN SOURCE - LGPL-3 LICENSE

---

## English

### Overview

The **Backend UI** module provides an easy-to-configure backend theme for Odoo with
custom color selection. Personalize your Odoo backend appearance with your brand colors
using a modern OWL 3 color picker widget.

Works with both **Odoo Community Edition** and **Odoo Enterprise Edition**.

### Key Features

- **Custom Color Selection** - Choose your own colors for the backend interface
- **Dark Mode** - Switch in the user menu, with a separate colour set per template
- **OWL 3 Color Widget** - Modern color picker with hex code support
- **Template System** - Save and apply color templates
- **Live Preview** - See changes immediately without page refresh
- **Brand Integration** - Match Odoo to your corporate identity

### Dark Mode

The user menu carries a **Dark Mode** switch. The choice is stored on the user, so it
follows them to another browser or machine.

Every colour template holds a second colour set for dark mode, editable in the **Dark
Mode** tab under _Settings > Template Colors > Colors_. Templates without a dark set of
their own get derived colours automatically, so dark mode is never unusable.

The module writes the standard `color_scheme` cookie — the same mechanism Odoo
Enterprise and OCA `web_dark_mode` use. **If either of those is installed, this module's
dark mode stands down completely** and leaves them in control: the user menu never shows
two dark-mode entries, and the server hands their decision through untouched. The
colours configured here still apply and follow whichever scheme they picked.

> **On plain Community without either module**, dark mode covers every surface reachable
> through colour variables. A few Odoo components carry light colours compiled into
> their stylesheets that cannot be overridden at runtime. Installing OCA `web_dark_mode`
> (AGPL-3) adds their complete dark stylesheets on top and closes those gaps.

### Included Color Templates

Ten templates ship with the module, among them four **IT-Guy Terminal** variants (green,
amber, cyan, white) matching the `theme_itguy` website theme. In dark mode they use the
theme's phosphor colours unchanged; in light mode the same hues are darkened, because
the neon values reach only about 1.4:1 contrast on white.

### Technical Specifications

- **Architecture**: OWL 3 components with custom field widgets
- **Frontend**: Modern JavaScript ES6 modules with reactive state
- **Assets**: Custom CSS and XML templates for color widget
- **Compatibility**: Works with Odoo Community & Enterprise Edition 19.0+
- **Languages**: English, German

### Installation

1. Install module via Apps menu in Odoo
2. Go to **Settings > Template Colors > Colors**
3. Choose your preferred colors
4. Apply the color template to see changes

### Configuration

#### Color Templates

1. Go to **Settings > Template Colors > Templates**
2. Create a new template or edit the default
3. Use the color picker to select your brand colors
4. Save and apply the template

#### Available Color Options

- Primary color
- Secondary color
- Background colors
- Text colors
- Accent colors

### Use Cases

- **Corporate Branding**: Match Odoo to your company's visual identity
- **Department Differentiation**: Use different color schemes for different departments
- **User Experience**: Create a more personalized working environment
- **Multi-Company Setup**: Different colors for different company instances

---

## Deutsch

### Überblick

Das Modul **Backend UI** liefert ein einfach konfigurierbares Backend-Theme für Odoo mit
frei wählbarer Farbgebung. Über ein modernes OWL-3-Farbwidget passen Sie das
Odoo-Backend an Ihre Markenfarben an.

Funktioniert mit **Odoo Community Edition** und **Odoo Enterprise Edition**.

### Hauptfunktionen

- **Eigene Farbauswahl** - Wählen Sie Ihre eigenen Farben für die Backend-Oberfläche
- **Dark Mode** - Schalter im Benutzermenü, mit eigenem Farbsatz je Vorlage
- **OWL-3-Farbwidget** - Moderner Farbwähler mit Hex-Code-Eingabe
- **Vorlagen-System** - Farbvorlagen speichern und anwenden
- **Live-Vorschau** - Änderungen sind sofort sichtbar, ohne die Seite neu zu laden
- **Marken-Integration** - Odoo an Ihre Unternehmensidentität anpassen

### Dark Mode

Im Benutzermenü liegt ein Schalter **Dark Mode**. Die Wahl wird am Benutzer gespeichert
und gilt daher auch in einem anderen Browser oder auf einem anderen Rechner.

Jede Farbvorlage hält einen zweiten Farbsatz für den Dark Mode bereit, einzustellen im
Reiter **Dark Mode** unter _Einstellungen > Template Colors > Colors_. Vorlagen ohne
eigenen Dark-Satz bekommen automatisch abgeleitete Farben, der Dark Mode ist also nie
unbrauchbar.

Das Modul setzt dafür das übliche Cookie `color_scheme` — dieselbe Grundlage, die Odoo
Enterprise und OCA `web_dark_mode` verwenden. **Ist eines dieser Module installiert,
tritt der eigene Dark Mode vollständig zurück** und überlässt ihm die Steuerung: Im
Benutzermenü erscheint kein zweiter Eintrag, und der Server reicht dessen Entscheidung
unverändert durch. Die hier eingestellten Farben gelten trotzdem und folgen dem dort
gewählten Schema.

> **In reiner Community ohne eines dieser Module** deckt der Dark Mode alle Flächen ab,
> die über Farbvariablen erreichbar sind. Einzelne Odoo-Komponenten tragen fest
> einkompilierte helle Farben, die sich zur Laufzeit nicht überschreiben lassen. OCA
> `web_dark_mode` (AGPL-3) ergänzt deren vollständige Dark-Stylesheets und schließt
> diese Lücken.

### Mitgelieferte Farbvorlagen

Zehn Vorlagen liegen dem Modul bei, darunter vier Varianten **IT-Guy Terminal** (Grün,
Amber, Cyan, Weiß), abgestimmt auf das Website-Theme `theme_itguy`. Im Dark Mode tragen
sie die Phosphorfarben des Themes unverändert; im hellen Backend werden dieselben Töne
abgedunkelt, weil die Neonwerte auf Weiß nur etwa 1,4:1 Kontrast erreichen.

### Technische Spezifikationen

- **Architektur**: OWL 3 Komponenten mit benutzerdefinierten Feld-Widgets
- **Frontend**: Moderne JavaScript ES6 Module mit reaktivem Zustand
- **Assets**: Eigenes CSS und XML-Templates für das Farbwidget
- **Kompatibilität**: Funktioniert mit Odoo Community & Enterprise Edition 19.0+
- **Sprachen**: Englisch, Deutsch

### Installation

1. Modul über das Apps-Menü in Odoo installieren
2. Gehen Sie zu **Einstellungen > Template Colors > Colors**
3. Wählen Sie Ihre bevorzugten Farben
4. Wenden Sie die Farbvorlage an, um die Änderungen zu sehen

### Konfiguration

#### Farbvorlagen

1. Gehen Sie zu **Einstellungen > Template Colors > Templates**
2. Erstellen Sie eine neue Vorlage oder bearbeiten Sie die Standardvorlage
3. Wählen Sie Ihre Markenfarben über den Farbwähler aus
4. Speichern und wenden Sie die Vorlage an

#### Verfügbare Farboptionen

- Primärfarbe
- Sekundärfarbe
- Hintergrundfarben
- Textfarben
- Akzentfarben

### Anwendungsfälle

- **Corporate Branding**: Odoo an die visuelle Identität Ihres Unternehmens anpassen
- **Abteilungsdifferenzierung**: Verschiedene Farbschemata für verschiedene Abteilungen
- **Benutzererfahrung**: Eine persönlichere Arbeitsumgebung schaffen
- **Multi-Company-Setup**: Verschiedene Farben für verschiedene Unternehmensinstanzen

---

## Technical Information / Technische Informationen

- **Module Name**: eq_ownerp_ui
- **Version**: 19.0.1.4.16
- **Author**: Equitania Software GmbH
- **License**: LGPL-3 (GNU Lesser General Public License v3.0)
- **Website**: https://www.ownerp.com
- **Dependencies**: base_setup, mail, web

## OWL 3 Component Architecture

This module demonstrates modern OWL 3 patterns:

- Custom field widget (`eq_color`)
- Component-based architecture
- Reactive state management with `useState()`
- Registry integration for field types

## Professional Services / Professionelle Dienstleistungen

Equitania Software GmbH offers:

- Custom theme development
- Corporate identity integration
- UI/UX consulting for Odoo

Contact: info@equitania.de
