# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-render the stylesheet and re-derive the dark colours.

    19.0.1.3.1 fixes both halves of the dark mode: the stylesheet gained rules
    for surfaces Odoo compiles light (dropdowns, settings, Discuss), and the
    derivation now measures contrast instead of shifting lightness by a fixed
    amount. Databases already on 19.0.1.3.0 hold colours produced by the old
    derivation, so re-applying the active template is what actually repairs them.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        icp = env["ir.config_parameter"].sudo()
        template_id = icp.get_param("eq_color_template_id")
        if template_id:
            # Re-applying recomputes the dark set through the corrected maths.
            env["eq.template.colors"].api_apply_template(int(template_id))
            _logger.info(
                "eq_ownerp_ui: re-applied color template %s with corrected dark colors", template_id
            )
        else:
            env["eq.template.colors"].create({}).scss_create_or_update_attachment()
            _logger.info("eq_ownerp_ui: stylesheet re-generated")
    except Exception as e:
        _logger.warning("eq_ownerp_ui: could not refresh the dark mode colors: %s", e)
