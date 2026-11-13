# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EQResCompany(models.Model):
    _inherit = "res.company"

    eq_background_image = fields.Binary(string="ownERP Home Menu Background Image", attachment=True)
    eq_background_image_name = fields.Char(string="Background Image Name")
