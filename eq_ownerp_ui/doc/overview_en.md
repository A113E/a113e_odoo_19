# Customizing Backend Colors

**eq_ownerp_ui** lets you recolor the Odoo backend — navigation bar, links, buttons,
list rows and the apps icon — to match your company's corporate identity, without
touching any code.

## Where to find it

**Settings → Technical → Template Colors**, under two sub-menus:

- **Colors** — the color-picker wizard; change any color and click "Apply" to update the
  whole backend immediately.
- **Templates** — save a color set under a name (e.g. "ACME Corporate") to reuse or
  share it later.

## What you can customize

- Navigation bar background, font color, and hover state
- Link color
- Primary and secondary button colors
- List view row background colors (including hover)
- The Apps menu icon color
- A background image for the Home Menu (per company)
- A second, complete color set for dark mode

## Typical workflow

1. Open **Colors**, adjust the values (or pick a saved **Template**).
2. Click **Apply** — changes take effect for everyone immediately.
3. Optionally save the result as a new **Template** for future reuse.
4. Use **Reset to default** at any time to go back to the standard Equitania palette.

## Dark mode

The **user menu** (top right) carries a **Dark Mode** switch to move between a light and
a dark backend. Unlike the colors themselves this is a **personal setting**: it applies
only to that user, but it is stored on their account and therefore follows them to
another machine.

Which colors dark mode uses is set in the **Dark Mode** tab under **Colors** — a
complete second set, independent of the light one. Picking a color template fills both
sets at once. Templates that carry no dark colors of their own get them derived
automatically, so dark mode is never illegible.

Four bundled **IT-Guy Terminal** templates (green, amber, cyan, white) match the
`theme_itguy` website theme and show its terminal look in dark mode: phosphor on black.
In the light backend the same hues are darkened, because the neon colors would be
unreadable on white.

**A note on scope:** with Odoo Enterprise or the OCA `web_dark_mode` module installed,
their switch takes over — only one dark-mode entry appears in the user menu, and the
colors set here still apply and follow whichever scheme that switch picked. Without
those modules dark mode works too, but a few Odoo components keep their light surfaces.

## Colors of automated e-mails

Odoo styles the buttons of automated e-mails from two colour values of its own that know
nothing about the colours configured here — out of the box they are Odoo aubergine. You
find them under **Settings → General Settings → Companies → Email Templates**.

The **Apply Theme Colors** button writes the background and font colour of your primary
button into them, so e-mails carry the same corporate colour as the backend. This only
happens on demand: a deliberately different e-mail colour is kept, even when you change
the backend colours later.

Unlike the backend colours, these two values apply **per company**.

## Things to know

- Applying colors changes them for **all users and companies** at once. The only
  personal choice is light versus dark; the Home Menu background image is set per
  company.
- Colors are plain text values (hex codes) — an invalid value won't raise an error, it
  will just render incorrectly.
