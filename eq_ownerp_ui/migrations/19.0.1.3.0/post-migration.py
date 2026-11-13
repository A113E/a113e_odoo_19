# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Re-generate the stylesheet so it carries the new dark branch.

    Before this version the injected view held a single ``<style>`` block. The
    dark colours only exist once it has been rendered again, so without this the
    dark mode would switch to a stylesheet that is still entirely light — and
    users would have to open the colour settings and press Apply to find out.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        wizard = env["eq.template.colors"].create({})
        wizard.scss_create_or_update_attachment()
        _logger.info("eq_ownerp_ui: stylesheet re-generated with light and dark color sets")
    except Exception as e:
        _logger.warning("eq_ownerp_ui: could not auto-regenerate the stylesheet: %s", e)
