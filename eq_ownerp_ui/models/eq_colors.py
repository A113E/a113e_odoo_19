# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class EqColors(models.Model):
    _name = "eq.colors"
    _description = "Color Template"

    name = fields.Char(string="Name")
    # Dark mode
    eq_is_dark = fields.Boolean(
        string="Dark Palette",
        help="Marks this record as the dark counterpart of another template. "
        "Dark palettes are not offered for selection on their own.",
    )
    eq_dark_variant_id = fields.Many2one(
        "eq.colors",
        string="Dark Variant",
        domain="[('eq_is_dark', '=', True), ('id', '!=', id)]",
        help="Palette applied when the user switches the backend to dark mode. "
        "Without one the light colours stay in place and stop the dark mode from working.",
    )
    eq_view_background = fields.Char(
        string="View Background",
        help="Background of views, sheets and dialogs. Only evaluated for dark palettes; "
        "in light mode Odoo's own white background is kept.",
    )
    # Basic Colors
    eq_basic_text_color = fields.Char(string="Basic Text Color")
    eq_basic_secondary_color = fields.Char(string="Basic Secondary Color")
    eq_link_color = fields.Char(string="Link Color")
    # Navigation
    eq_apps_color = fields.Char(string="App-Icon Color")
    eq_navi_background = fields.Char(string="Navigation Background")
    eq_navi_fontcolor = fields.Char(string="Navigation Fontcolor")
    eq_navi_hover = fields.Char(string="Navigation Hover Background")
    eq_navi_hover_fontcolor = fields.Char(string="Navigation Hover Font")
    # Buttons
    eq_btn_primary_background = fields.Char(string="Primary Button Backgroundcolor")
    eq_btn_primary_fontcolor = fields.Char(string="Primary Button Fontcolor")
    eq_btn_secondary_background = fields.Char(string="Secondary Button Backgroundcolor")
    eq_btn_secondary_fontcolor = fields.Char(string="Secondary Button Fontcolor")
    # List View
    eq_list_primary_background = fields.Char(string="Primary Backgroundcolor")
    eq_list_secondary_background = fields.Char(string="Secondary Backgroundcolor")
    eq_list_hoover_background = fields.Char(string="Hover Backgroundcolor")

    def unlink(self):
        for eq_colors in self:
            if (
                self.env["ir.config_parameter"].get_param("eq_color_template_id")
                and int(self.env["ir.config_parameter"].get_param("eq_color_template_id"))
                == self.id
            ):
                self.env["ir.config_parameter"].set_param("eq_color_template_id", False)
        return super(EqColors, self).unlink()
