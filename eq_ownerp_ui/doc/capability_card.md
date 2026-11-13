---
type: "Capability Card"
title: "eq_ownerp_ui — Agent Capability Card"
description:
  "Recolors the Odoo backend (navbar, links, buttons, list rows, apps icon) to match a
  corporate identity via live CSS variable overrides, with saveable color templates and
  a home-menu background image."
tags: [capability-card, eq_ownerp_ui]
generated: {by: "process:cli-capability-card", at: "2026-09-02T00:00:00Z"}
status: stable
module: eq_ownerp_ui
module_version: 19.0.1.4.16
license: LGPL-3
odoo_version: "19"
---

<!--
  Agent Capability Card — generated and maintained via the cli-capability-card skill (Odoo mode).
  Audience: LLM/agent consuming this module's surface as context. English only. NOT a help page:
  this file must NEVER be registered in doc/index.json (the eq_helper viewer ignores it by design).
  Regenerate the tables with scripts/introspect_odoo_module.py after any model/view/security change.
-->

# eq_ownerp_ui — Agent Capability Card

> Recolors the Odoo backend (navbar, links, buttons, list rows, apps icon) to match a
> corporate identity via live CSS variable overrides, with saveable color templates, a
> per-user dark mode, and a home-menu background image.

- **Module:** `eq_ownerp_ui` · **Version:** 19.0.1.4.16 · **License:** LGPL-3
- **Depends:** base_setup, mail, web · **Odoo:** 19 · **Card updated:** 2026-08-08

## Capabilities at a glance

- Pick colors (navbar background/font/hover, links, buttons, list-row backgrounds,
  apps-icon color) in a wizard; apply them instantly to the whole backend by overriding
  Odoo/Bootstrap/Enterprise CSS variables (scoped to `.o_web_client` so website/webshop
  pages are unaffected).
- Save a color set as a reusable, named `eq.colors` template; load it back into the
  wizard to re-apply or tweak it (`eq_set_colors()`).
- Apply a saved template in one step via `api_apply_template(template_id)` — designed
  for XML-RPC/external scripts.
- Reset the whole palette to Equitania's shipped defaults (`reset_default()`).
- Push the primary button colours into Odoo's e-mail template colours
  (`res.config.settings.action_eq_apply_theme_colors_to_email()`), so automated mails
  match the backend instead of keeping Odoo's aubergine default.
- Render the two e-mail colour fields (`res.company.email_primary_color` /
  `email_secondary_color`, owned by `mail`) with this module's `eq_color` widget so they
  match the theme's own colour fields.
- Set a custom Home Menu background image per company.
- Offer a per-user dark mode: a "Dark Mode" switch in the user menu writes the standard
  `color_scheme` cookie and stores the choice in `res.users.settings.eq_color_scheme`.
  The whole feature stands down when `web_enterprise` or OCA `web_dark_mode` is
  installed — detected on both sides through the same signal, the presence of
  `color_scheme` / `dark_mode` on `res.users.settings` (`has_foreign_provider()` on the
  server, `hasForeignColorSchemeProvider()` in the browser). The user menu then shows no
  second entry and `color_scheme()` hands the foreign answer through untouched.
- Hold a second, complete color set for dark mode. A light `eq.colors` template links
  its dark counterpart through `eq_dark_variant_id`; templates without one get colors
  derived from their light set (`_derive_dark_colors()`), so dark mode is never
  unusable.
- Colors persist as `ir.config_parameter` values (dark ones prefixed `eq_dark_`) and are
  rendered into a generated `<style>` block attached to `web.layout`
  (`scss_create_or_update_attachment()`). Both color sets are emitted side by side,
  wrapped in `t-if="color_scheme == 'dark'"` — the same render value `web.layout` uses
  to pick the asset bundle, so stylesheet and bundle cannot drift apart. Odoo swaps the
  bundle server-side and leaves no DOM marker, so a CSS selector cannot distinguish the
  two. On website/portal/kiosk pages, which render through `web.layout` as well, the
  name is absent from the render values and QWeb resolves it to `None`, so those get the
  light branch. Includes automatic detection of `web_responsive`/`web_enterprise` for
  compatible overrides and a computed hover shade for links (darker in light mode,
  brighter in dark).

## Data model reference

| Model                 | Kind                  | Purpose                                                              |
| --------------------- | --------------------- | -------------------------------------------------------------------- |
| `eq.colors`           | model                 | Saved, named color template                                          |
| `res.company`         | model (extension)     | Home Menu background image                                           |
| `eq.template.colors`  | transient             | The color-picker wizard (also the live "current" color state)        |
| `res.config.settings` | transient (extension) | Carries the e-mail colour fields and the "Apply Theme Colors" action |
| `res.users.settings`  | model (extension)     | Per-user `eq_color_scheme` (`system` / `light` / `dark`)             |
| `ir.http`             | abstract (extension)  | Resolves the colour scheme per request (`color_scheme()`)            |

### Fields — `eq.colors` (identical color fields also exist on `eq.template.colors`)

| Field                          | Type | Label                            | Notes         |
| ------------------------------ | ---- | -------------------------------- | ------------- |
| `name`                         | Char | Name                             | template name |
| `eq_basic_text_color`          | Char | Basic Text Color                 | —             |
| `eq_basic_secondary_color`     | Char | Basic Secondary Color            | —             |
| `eq_link_color`                | Char | Link Color                       | —             |
| `eq_apps_color`                | Char | App-Icon Color                   | —             |
| `eq_navi_background`           | Char | Navigation Background            | —             |
| `eq_navi_fontcolor`            | Char | Navigation Fontcolor             | —             |
| `eq_navi_hover`                | Char | Navigation Hover Background      | —             |
| `eq_navi_hover_fontcolor`      | Char | Navigation Hover Font            | —             |
| `eq_btn_primary_background`    | Char | Primary Button Backgroundcolor   | —             |
| `eq_btn_primary_fontcolor`     | Char | Primary Button Fontcolor         | —             |
| `eq_btn_secondary_background`  | Char | Secondary Button Backgroundcolor | —             |
| `eq_btn_secondary_fontcolor`   | Char | Secondary Button Fontcolor       | —             |
| `eq_list_primary_background`   | Char | Primary Backgroundcolor          | —             |
| `eq_list_secondary_background` | Char | Secondary Backgroundcolor        | —             |
| `eq_list_hoover_background`    | Char | Hover Backgroundcolor            | —             |

### Public methods — `eq.colors`

| Method     | Decorators | Purpose                                                                                                                                                                               |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unlink()` | —          | Before deleting, if this template is the currently-active one (`ir.config_parameter["eq_color_template_id"]`), clears that parameter so the app doesn't reference a deleted template. |

### Fields — `eq.template.colors` (additional, beyond the color fields above)

| Field                      | Type     | Label                 | Notes           |
| -------------------------- | -------- | --------------------- | --------------- |
| `name`                     | Char     | Name                  | —               |
| `eq_color_template_id`     | Many2one | Color Template        | → `eq.colors`   |
| `eq_company_id`            | Many2one | Company               | → `res.company` |
| `eq_background_image_name` | Char     | Background Image Name | —               |
| `eq_background_image`      | Binary   | Background Image      | —               |

### Fields — `res.company`

| Field                      | Type   | Label                             | Notes |
| -------------------------- | ------ | --------------------------------- | ----- |
| `eq_background_image`      | Binary | ownERP Home Menu Background Image | —     |
| `eq_background_image_name` | Char   | Background Image Name             | —     |

### Public methods — `eq.template.colors`

| Method                               | Decorators   | Purpose                                                                                                                                                                                                                                              |
| ------------------------------------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `eq_set_colors()`                    | api.onchange | When `eq_color_template_id` is picked, copies all its color fields into the wizard's own fields (preview before applying).                                                                                                                           |
| `execute()`                          | —            | Persists every color field as an `ir.config_parameter` and regenerates the SCSS attachment — this is the "Apply" action.                                                                                                                             |
| `reset_default()`                    | —            | Resets every color (config_parameter + wizard field) to Equitania's shipped default palette.                                                                                                                                                         |
| `default_get(fields)`                | —            | Pre-fills the wizard from current `ir.config_parameter` values, falling back to the shipped defaults for any unset one.                                                                                                                              |
| `scss_create_or_update_attachment()` | —            | Renders the SCSS_TEMPLATE with current colors (incl. a computed darker link-hover shade) and creates/updates the `ir.attachment` inherited into `web.layout`; detects installed `web_responsive`/`web_enterprise` for compatible variable overrides. |
| `api_apply_template(template_id)`    | —            | `call_kw`-friendly one-step apply: loads an `eq.colors` template by id and calls the equivalent of `eq_set_colors()` + `execute()` in one go. Returns `False` if the id doesn't exist.                                                               |

## HTTP routes

None — this module ships no controllers; color changes are delivered via a regenerated
CSS/SCSS asset, not an endpoint.

## UI surface

| Menu            | Parent                               | Action                    |
| --------------- | ------------------------------------ | ------------------------- |
| Template Colors | base.menu_administration             | —                         |
| Colors          | eq_ownerp_ui.eq_template_colors_menu | eq_template_colors_action |
| Templates       | eq_ownerp_ui.eq_template_colors_menu | eq_colors_action          |

Navigation: **Settings → Technical → Template Colors** (under General Settings'
administration menu).

| Action          | Kind       | Target model         | Views     |
| --------------- | ---------- | -------------------- | --------- |
| Template Colors | act_window | `eq.template.colors` | form      |
| Template Colors | act_window | `eq.colors`          | list,form |

### Public methods — `res.config.settings`

| Method                                    | Purpose                                                                                                                                                                                                                          |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `action_eq_apply_theme_colors_to_email()` | Copy `eq_btn_primary_background` → `email_secondary_color` and `eq_btn_primary_fontcolor` → `email_primary_color` for the settings' company. Returns None on purpose so the client reloads the record and the new swatches show. |

Helper (module `odoo.addons.eq_ownerp_ui.models.eq_res_config_settings`, importable and
pure): `normalize_hex_color(value, fallback)` — returns an uppercase `#RRGGBB`, trimming
an alpha channel and falling back on anything malformed.

## Security & access

| Model                | Group           | R   | W   | C   | U   |
| -------------------- | --------------- | --- | --- | --- | --- |
| `eq.template.colors` | base.group_user | 1   | 1   | 1   | 1   |
| `eq.colors`          | base.group_user | 1   | 1   | 1   | 1   |

No dedicated restriction group — any internal user can reach the wizard (the menu itself
sits under an administration-level parent menu, which is the practical gate).

## Recipes

### Apply a saved color template in one call (e.g. from an external script)

```python
env["eq.template.colors"].create({}).api_apply_template(template_id)
```

### Save the current live colors as a new named template

```python
wizard = env["eq.template.colors"].create({})  # default_get pulls current config_parameter values
env["eq.colors"].create({
    "name": "ACME Corporate",
    **{f: wizard[f] for f in wizard._fields if f.startswith("eq_") and f not in ("eq_color_template_id", "eq_company_id")},
})
```

### Reset to Equitania defaults

```python
env["eq.template.colors"].create({}).reset_default()
```

## Guardrails & gotchas

- **Destructive:** deleting an `eq.colors` template that is currently active clears the
  active-template reference (but does NOT revert the live colors — those stay as last
  applied via `execute()`).
- **Prerequisites:** none — works out of the box; `web_responsive`/`web_enterprise` are
  auto-detected, not required.
- **Constraints:** colors are plain `Char` fields (hex strings), not validated as real
  color values — an invalid value will silently produce broken CSS rather than raising
  an error.
- **Odoo's e-mail colour naming is inverted:** `email_primary_color` is the button
  _text_, `email_secondary_color` its _background_. Mapping them the obvious way
  produces white-on-white buttons.
- **The e-mail colours are never synced automatically** — only
  `action_eq_apply_theme_colors_to_email()` writes them, so a deliberately different
  mail colour survives a theme change. They are per-`res.company`, unlike the backend
  colours.
- **Other sharp edges:** `execute()` writes global `ir.config_parameter` values and
  regenerates a shared SCSS attachment — this affects **all users/companies** at once,
  it is not a per-user or per-company preference (except the Home Menu background image,
  which is per-`res.company`, and the light/dark choice, which is per-user).
- **Dark mode never gets its own DOM marker.** Odoo picks the dark asset bundle
  server-side in `web.layout`; nothing on `<body>` says "dark". Do not write CSS that
  tries to select the dark state, and do not read the `color_scheme` cookie either: it
  lags behind whenever another provider decides (Enterprise drops it on logout, OCA
  writes it only in `_post_dispatch`). Branch on the render value `color_scheme` at
  render time, which is what the generated stylesheet does.
- **Do not overrule another dark-mode provider, and do not infer it from the return
  value.** Both `web_enterprise` and OCA `web_dark_mode` answer `"light"` as a real
  decision — for a user who picked Light — and `"light"` is also what Community returns
  when nothing was decided at all. Detect them by their field instead
  (`has_foreign_provider()`) and hand `super()`'s answer through unchanged.
  `resolve_color_scheme()`'s "anything but light wins" rule remains only as a fallback
  for providers we do not know.
- **After changing the stylesheet template, re-run
  `scss_create_or_update_attachment()`** — the rendered CSS lives in the
  `eq_ownerp_ui.eq_colors` view and is not rebuilt on module update by itself. A
  migration script does this per version; a running server also caches the compiled QWeb
  template, so it needs a restart to serve the new arch.
- **Dark colours degrade, they do not vanish:** if no dark palette is configured,
  `_derive_dark_colors()` brightens the accents and swaps in dark surfaces. A light
  colour has no meaningful dark equivalent to scale towards, so surfaces are replaced
  rather than shifted.
- **Scope on plain Community:** without `web_enterprise` or OCA `web_dark_mode`, dark
  mode covers what CSS custom properties can reach. Odoo's own surface colours
  (`$o-view-background-color` and friends) are SCSS, compiled into the bundle and
  unreachable at runtime, so the generated stylesheet names the affected selectors
  explicitly. That selector list is empirical — it was built by measuring WCAG contrast
  in a running backend, so **extend it the same way rather than by reasoning about which
  rules should apply**.
- **Derived dark colours are contrast-driven, not offset-driven.** `_ensure_contrast()`
  shifts a colour until it clears 4.5:1 against the _lightest_ surface it can land on
  (page background, list stripe, hover), and `_readable_on()` then picks each text
  colour for the background it sits on. A fixed lightness offset silently produced
  white-on-pale-green buttons at 1.65:1. When adding a colour pair, run it through both
  helpers.
- **`web_responsive` renamed its apps-menu container** from `.dropdown-menu-custom` to
  `.app-menu-container`; `_background_image_css()` targets both. A selector that matches
  neither leaves the overlay in web_responsive's own pale gradient, which is invisible
  in light mode and a full-screen light panel in dark mode.
- **How another module joins dark mode:** style it through
  `var(--o-view-background-color, #fff)` and `var(--gray-100 … --gray-900, …)` with
  light fallbacks. The dark branch defines all of them, so such a module follows along
  with no changes here and no entry in the selector list. Hard-coded colours and SCSS
  constants cannot be reached at runtime and would each need naming — `eq_knowledge`
  demonstrates both halves: its surfaces are variable-driven and switch over, while its
  own `$o-eq-knowledge-primary` constant does not.

## Related docs

- Help page (human, DE/EN): `overview` (doc/index.json).
- `README.md` — bilingual module overview.
