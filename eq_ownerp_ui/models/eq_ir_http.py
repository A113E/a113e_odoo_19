# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
"""Decide whether a request is rendered light or dark.

Odoo 19 already carries the whole dark-mode plumbing in Community: the asset
bundle ``web.assets_web_dark`` exists and ``web.layout`` switches on the render
value ``color_scheme``. What Community does not ship is anything that ever
returns something other than ``"light"`` from ``ir.http.color_scheme()`` — that
part lives in Odoo Enterprise (``web_enterprise``) and in OCA's
``web_dark_mode``.

Both of those write the same cookie, ``color_scheme``, which is what makes it
possible to fit in here instead of competing: whenever one of them is installed
this module steps aside completely and hands their answer straight through.

Stepping aside has to be an explicit check, not a matter of what ``super()``
returned. Both foreign modules answer ``"light"`` as a deliberate decision — for
an Enterprise user who picked "Light" in the preferences, for an OCA user whose
``dark_mode`` is off — and ``"light"`` is also what Community returns when
nothing has been decided at all. The two are indistinguishable from the return
value alone, so reading it as "nobody decided" would overrule a choice the user
actually made.
"""

from odoo import models
from odoo.http import request

VALID_SCHEMES = ("light", "dark")

# What Community's ir.http.color_scheme() returns when nothing has been decided.
UNDECIDED = "light"

# The fields Odoo Enterprise (``color_scheme``) and OCA ``web_dark_mode``
# (``dark_mode``) add to res.users.settings. Their presence is what marks a
# foreign provider as installed — deliberately the same signal the switch in the
# user menu uses (see hasForeignColorSchemeProvider in eq_dark_mode.js), so the
# server and the browser can never disagree about who is in charge.
FOREIGN_PROVIDER_FIELDS = ("color_scheme", "dark_mode")


def resolve_color_scheme(inherited_scheme, cookie_scheme, user_scheme):
    """Pick the colour scheme from the three possible sources.

    Kept free of ``request`` and of the ORM so the precedence rules can be
    tested on their own — going through ``color_scheme()`` would run into
    whichever other dark-mode module happens to sit in the inheritance chain.

    Args:
        inherited_scheme: What ``super().color_scheme()`` returned. Anything
            other than ``"light"`` means another module already decided.
        cookie_scheme: Value of the ``color_scheme`` cookie, if any.
        user_scheme: Scheme stored on the user, if any.

    Returns:
        ``"light"`` or ``"dark"``.
    """
    if inherited_scheme != UNDECIDED:
        # Some provider made the call — do not overrule it. Enterprise and OCA
        # are caught earlier by has_foreign_provider(); this covers anything
        # else that answers something other than the Community default.
        return inherited_scheme
    if cookie_scheme in VALID_SCHEMES:
        return cookie_scheme
    if user_scheme in VALID_SCHEMES:
        return user_scheme
    return inherited_scheme


def has_foreign_provider(settings_field_names):
    """True when res.users.settings carries a foreign provider's field.

    Kept free of the ORM so the rule can be tested on any database, installed
    Enterprise or not.

    Args:
        settings_field_names: Field names present on ``res.users.settings``.
    """
    return any(name in settings_field_names for name in FOREIGN_PROVIDER_FIELDS)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def color_scheme(self):
        """Return ``"light"`` or ``"dark"`` for the current request."""
        inherited = super().color_scheme()
        if self._eq_foreign_provider_installed():
            # Enterprise or OCA owns the dark mode on this database.
            return inherited
        return resolve_color_scheme(
            inherited,
            self._eq_cookie_color_scheme(),
            self._eq_user_color_scheme(),
        )

    def _eq_foreign_provider_installed(self):
        """True when another module already provides the backend dark mode."""
        return has_foreign_provider(self.env["res.users.settings"]._fields)

    def _eq_cookie_color_scheme(self):
        """Scheme carried by the cookie the switch in the user menu writes."""
        if not request:
            return None
        return request.httprequest.cookies.get("color_scheme")

    def _eq_user_color_scheme(self):
        """Scheme stored on the user, so a fresh browser starts out right."""
        if not request:
            return None
        user = request.env.user
        if not user or not user._is_internal():
            return None
        return user.sudo().res_users_settings_id.eq_color_scheme
