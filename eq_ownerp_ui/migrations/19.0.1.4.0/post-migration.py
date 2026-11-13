# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-apply the active template so the sharpened light colours take effect.

    Updating the module refreshes the ``eq.colors`` records, but the colours the
    backend actually renders live in ``ir.config_parameter`` and are only
    rewritten when a template is applied. Without this the corrected values
    would sit in the templates while the old ones stayed on screen.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        icp = env["ir.config_parameter"].sudo()
        template_id = icp.get_param("eq_color_template_id")
        if template_id:
            env["eq.template.colors"].api_apply_template(int(template_id))
            _logger.info(
                "eq_ownerp_ui: re-applied color template %s with the sharpened colors", template_id
            )
        else:
            # No template selected: hand-mixed colours stay untouched, but the
            # stylesheet still needs rebuilding.
            env["eq.template.colors"].create({}).scss_create_or_update_attachment()
            _logger.info("eq_ownerp_ui: stylesheet re-generated")
    except Exception as e:
        _logger.warning("eq_ownerp_ui: could not refresh the colors: %s", e)
