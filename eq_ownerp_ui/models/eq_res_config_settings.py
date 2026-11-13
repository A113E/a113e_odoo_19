# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
"""Bring the e-mail template colours in line with the backend theme.

Odoo styles the buttons of automated e-mails from two fields on the company
(`email_primary_color` / `email_secondary_color`) that default to Odoo's own
aubergine and know nothing about the colours configured here. The action below
copies the configured primary button colours over, so a mail carries the same
corporate identity as the backend.
"""

import re

from odoo import models

# Falls back to the theme defaults from eq.template.colors.reset_default()
DEFAULT_BUTTON_BACKGROUND = "#374D8B"
DEFAULT_BUTTON_FONTCOLOR = "#FFFFFF"

HEX_COLOR_RE = re.compile(r"^#?([0-9A-Fa-f]{6})")


def normalize_hex_color(value, fallback):
    """Return a plain ``#RRGGBB`` colour.

    The colour picker stores six-digit hex, but a value typed by hand (or an
    eight-digit value carried over from the list colours) would end up in an
    e-mail template, where alpha channels are poorly supported.

    Args:
        value: Stored colour value, possibly empty or malformed.
        fallback: Colour to use when nothing usable can be read.

    Returns:
        An uppercase ``#RRGGBB`` string.
    """
    match = HEX_COLOR_RE.match((value or "").strip())
    return f"#{match.group(1).upper()}" if match else fallback


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def action_eq_apply_theme_colors_to_email(self):
        """Copy the theme's primary button colours into the e-mail colours.

        Applies to the company the settings are being edited for. Odoo's field
        names are inverted with respect to their labels: ``primary`` is the
        button *text*, ``secondary`` its background.

        Deliberately returns nothing: a button that returns an action stops the
        client from reloading the record, and the two colour fields would keep
        showing the previous values. Without a return value the form reloads and
        the new colours are visible straight away.
        """
        self.ensure_one()
        icp = self.env["ir.config_parameter"].sudo()
        background = normalize_hex_color(
            icp.get_param("eq_btn_primary_background"), DEFAULT_BUTTON_BACKGROUND
        )
        fontcolor = normalize_hex_color(
            icp.get_param("eq_btn_primary_fontcolor"), DEFAULT_BUTTON_FONTCOLOR
        )

        # "primary" is the button text, "secondary" its background — Odoo's naming
        self.email_primary_color = fontcolor
        self.email_secondary_color = background
