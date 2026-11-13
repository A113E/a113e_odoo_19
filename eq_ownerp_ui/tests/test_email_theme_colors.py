# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.tests.common import TransactionCase

from odoo.addons.eq_ownerp_ui.models.eq_res_config_settings import normalize_hex_color


class TestNormalizeHexColor(TransactionCase):
    """Whatever is stored, an e-mail template gets a plain #RRGGBB colour."""

    def test_plain_value_is_uppercased(self):
        self.assertEqual(normalize_hex_color("#1e7a46", "#000000"), "#1E7A46")

    def test_missing_hash_is_added(self):
        self.assertEqual(normalize_hex_color("1E7A46", "#000000"), "#1E7A46")

    def test_alpha_channel_is_dropped(self):
        """Eight-digit colours reach mail clients that ignore the alpha channel."""
        self.assertEqual(normalize_hex_color("#0055FF80", "#000000"), "#0055FF")

    def test_empty_and_malformed_fall_back(self):
        for value in ("", None, "   ", "not-a-color", "#12345"):
            self.assertEqual(normalize_hex_color(value, "#374D8B"), "#374D8B")


class TestApplyThemeColorsToEmail(TransactionCase):
    """The settings action copies the theme's button colours into the e-mails."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.icp = cls.env["ir.config_parameter"].sudo()
        cls.company = cls.env.company

    def _apply(self):
        self.env["res.config.settings"].create({}).action_eq_apply_theme_colors_to_email()
        self.company.invalidate_recordset()

    def test_configured_theme_colors_are_applied(self):
        """Odoo's naming is inverted: primary is the text, secondary the background."""
        self.icp.set_param("eq_btn_primary_background", "#1E7A46")
        self.icp.set_param("eq_btn_primary_fontcolor", "#FFFDF5")

        self._apply()

        self.assertEqual(self.company.email_secondary_color, "#1E7A46")
        self.assertEqual(self.company.email_primary_color, "#FFFDF5")

    def test_unconfigured_theme_falls_back_to_defaults(self):
        """Never write an empty colour into a mail template."""
        self.icp.set_param("eq_btn_primary_background", "")
        self.icp.set_param("eq_btn_primary_fontcolor", "not-a-color")

        self._apply()

        self.assertEqual(self.company.email_secondary_color, "#374D8B")
        self.assertEqual(self.company.email_primary_color, "#FFFFFF")

    def test_action_returns_nothing_so_the_form_reloads(self):
        """A returned action would stop the client from refreshing the swatches."""
        settings = self.env["res.config.settings"].create({})

        self.assertIsNone(settings.action_eq_apply_theme_colors_to_email())


class TestEmailColorFieldsUseThemeWidget(TransactionCase):
    """The e-mail colour fields must look like every other colour field here."""

    def test_settings_view_uses_the_eq_color_widget(self):
        arch = self.env["res.config.settings"].get_view(view_type="form")["arch"]
        tree = etree.fromstring(arch.encode())

        for name in ("email_primary_color", "email_secondary_color"):
            fields = tree.xpath(f"//field[@name='{name}']")
            self.assertTrue(fields, f"{name} missing from the settings view")
            for field in fields:
                self.assertEqual(
                    field.get("widget"), "eq_color", f"{name} does not use the theme widget"
                )

    def test_settings_view_offers_the_apply_button(self):
        arch = self.env["res.config.settings"].get_view(view_type="form")["arch"]
        tree = etree.fromstring(arch.encode())

        self.assertTrue(tree.xpath("//button[@name='action_eq_apply_theme_colors_to_email']"))
