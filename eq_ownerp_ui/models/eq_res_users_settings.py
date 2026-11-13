# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
"""Per-user storage of the backend colour scheme.

The cookie ``color_scheme`` already decides which colours a request is served
with, but a cookie is bound to one browser. Storing the choice on the user makes
it survive a new device or a cleared browser.

The field is deliberately named ``eq_color_scheme`` rather than reusing
``color_scheme`` (Odoo Enterprise) or ``dark_mode`` (OCA ``web_dark_mode``):
those modules may be installed alongside this one, and sharing a field name with
a different type would break whichever module loads second.
"""

from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    # Every field on this model is handed to the web client as `user.settings`
    # (see _res_users_settings_format), so the switch in the user menu can read
    # it without an extra call.
    eq_color_scheme = fields.Selection(
        [
            ("system", "Follow System"),
            ("light", "Light"),
            ("dark", "Dark"),
        ],
        string="Backend Color Scheme",
        default="system",
        help="Color scheme of the Odoo backend. 'Follow System' uses the colour "
        "scheme configured in the operating system.",
    )
