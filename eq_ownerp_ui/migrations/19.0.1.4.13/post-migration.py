# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-generate the stylesheet with the narrowed link rule.

    The rendered CSS lives in the ``eq_ownerp_ui.eq_colors`` view and is not
    rebuilt on module update by itself. Without this step the menu entries would
    keep the link colour until someone opened the colour settings and pressed
    Apply.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        env["eq.template.colors"].create({}).scss_create_or_update_attachment()
        _logger.info(
            "eq_ownerp_ui: stylesheet re-generated, link rule no longer paints menu entries"
        )
    except Exception as e:
        _logger.warning("eq_ownerp_ui: could not auto-regenerate the stylesheet: %s", e)
