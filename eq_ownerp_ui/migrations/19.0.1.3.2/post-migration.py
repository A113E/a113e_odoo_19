# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-render the stylesheet so the new dark rules reach existing databases.

    19.0.1.3.2 adds the surface variables other modules read
    (``--o-view-background-color``, ``--gray-*``), the form status bar, and the
    corrected apps-menu selector. All of it lives in the generated stylesheet,
    which is only rebuilt when a template is applied.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        icp = env["ir.config_parameter"].sudo()
        template_id = icp.get_param("eq_color_template_id")
        if template_id:
            env["eq.template.colors"].api_apply_template(int(template_id))
        else:
            env["eq.template.colors"].create({}).scss_create_or_update_attachment()
        _logger.info("eq_ownerp_ui: stylesheet re-generated with the extended dark rules")
    except Exception as e:
        _logger.warning("eq_ownerp_ui: could not refresh the stylesheet: %s", e)
