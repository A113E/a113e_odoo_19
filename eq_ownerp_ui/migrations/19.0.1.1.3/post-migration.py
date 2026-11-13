# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-generate EQ Custom Colors CSS with .o_web_client scoping.

    This ensures the CSS template is updated automatically during module
    upgrade without requiring the user to manually re-apply colors.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        wizard = env["eq.template.colors"].create({})
        wizard.scss_create_or_update_attachment()
        _logger.info("eq_ownerp_ui: CSS template re-generated with .o_web_client scoping")
    except Exception as e:
        _logger.warning("eq_ownerp_ui: Could not auto-regenerate CSS template: %s", e)
