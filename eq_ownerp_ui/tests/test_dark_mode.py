# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
"""Dark mode: scheme resolution and the two rendered colour sets."""

import pathlib
from unittest.mock import patch

from lxml import etree

from odoo.tests.common import TransactionCase

from odoo.addons.eq_ownerp_ui.models.eq_ir_http import (
    FOREIGN_PROVIDER_FIELDS,
    has_foreign_provider,
    resolve_color_scheme,
)
from odoo.addons.eq_ownerp_ui.models.eq_template_colors import (
    COLOR_FIELDS,
    DEFAULT_DARK,
    VIEW_BACKGROUND_FIELD,
    _dark_name,
)


class TestColorSchemeResolution(TransactionCase):
    """Precedence between another module, the cookie and the user's choice.

    Tested through the pure function rather than through color_scheme(): with
    web_enterprise or OCA web_dark_mode installed, super() runs their code,
    which expects a real bound request and would fail here for reasons that have
    nothing to do with these rules.
    """

    def test_dark_cookie_selects_dark(self):
        self.assertEqual(resolve_color_scheme("light", "dark", None), "dark")

    def test_light_cookie_selects_light(self):
        self.assertEqual(resolve_color_scheme("light", "light", "dark"), "light")

    def test_no_cookie_and_no_preference_stays_light(self):
        self.assertEqual(resolve_color_scheme("light", None, "system"), "light")

    def test_stored_preference_applies_without_cookie(self):
        """A fresh browser still starts in the scheme the user picked."""
        self.assertEqual(resolve_color_scheme("light", None, "dark"), "dark")

    def test_garbage_cookie_is_ignored(self):
        self.assertEqual(resolve_color_scheme("light", "neon", None), "light")

    def test_other_provider_wins(self):
        """Enterprise or OCA already decided — do not overrule them."""
        self.assertEqual(resolve_color_scheme("dark", "light", "light"), "dark")


class TestForeignProviderDetection(TransactionCase):
    """When Enterprise or OCA is installed, this module has to step aside.

    Reading super()'s return value is not enough: both of them answer "light"
    as a real decision, which is also what Community answers when nothing has
    been decided. Only the presence of their field tells the two apart.
    """

    def test_enterprise_field_marks_a_foreign_provider(self):
        self.assertTrue(has_foreign_provider({"color_scheme", "push_to_talk_key"}))

    def test_oca_field_marks_a_foreign_provider(self):
        self.assertTrue(has_foreign_provider({"dark_mode", "dark_mode_device_dependent"}))

    def test_plain_community_has_no_foreign_provider(self):
        self.assertFalse(has_foreign_provider({"push_to_talk_key", "channel_notifications"}))

    def test_our_own_field_is_not_mistaken_for_a_foreign_one(self):
        """eq_color_scheme is deliberately named apart from both of theirs."""
        self.assertFalse(has_foreign_provider({"eq_color_scheme"}))

    def test_the_installed_database_is_judged_by_the_same_rule(self):
        installed = self.env["ir.http"]._eq_foreign_provider_installed()
        self.assertEqual(installed, has_foreign_provider(self.env["res.users.settings"]._fields))

    def test_the_browser_checks_for_the_very_same_fields(self):
        """Server and web client must never disagree about who is in charge.

        The switch in the user menu stands down on the same signal; if the two
        lists drift apart, one side hides the switch while the other keeps
        overruling the provider that owns it.
        """
        source = (pathlib.Path(__file__).parent.parent / "static/src/js/eq_dark_mode.js").read_text(
            encoding="utf-8"
        )
        body = source.split("hasForeignColorSchemeProvider", 1)[1]
        for name in FOREIGN_PROVIDER_FIELDS:
            self.assertIn(f"settings.{name}", body, f"{name} is not checked in eq_dark_mode.js")


class TestColorSchemeSources(TransactionCase):
    """Where the cookie value and the stored preference are read from."""

    def setUp(self):
        super().setUp()
        self.ir_http = self.env["ir.http"]
        # res_users_settings_id is computed from res_users_settings_ids and stays
        # empty until a record exists, so writing to it without this would be a
        # silent no-op.
        self.settings = self.env["res.users.settings"]._find_or_create_for_user(self.env.user)

    def _fake_request(self, cookies=None):
        return type(
            "FakeRequest",
            (),
            {
                "httprequest": type("FakeHttpRequest", (), {"cookies": cookies or {}})(),
                "env": self.env,
            },
        )()

    def test_cookie_is_read_from_the_request(self):
        with patch(
            "odoo.addons.eq_ownerp_ui.models.eq_ir_http.request",
            self._fake_request({"color_scheme": "dark"}),
        ):
            self.assertEqual(self.ir_http._eq_cookie_color_scheme(), "dark")

    def test_user_preference_is_read_from_the_settings(self):
        self.settings.eq_color_scheme = "dark"
        with patch("odoo.addons.eq_ownerp_ui.models.eq_ir_http.request", self._fake_request()):
            self.assertEqual(self.ir_http._eq_user_color_scheme(), "dark")

    def test_sources_are_empty_outside_a_request(self):
        """Rendering happens outside HTTP too — cron, tests, the shell."""
        with patch("odoo.addons.eq_ownerp_ui.models.eq_ir_http.request", None):
            self.assertIsNone(self.ir_http._eq_cookie_color_scheme())
            self.assertIsNone(self.ir_http._eq_user_color_scheme())


class TestRenderedStylesheet(TransactionCase):
    """Both colour sets end up in the view injected into web.layout."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["eq.template.colors"].create({})
        cls.view = cls.env.ref("eq_ownerp_ui.eq_colors")

    def _arch(self):
        self.wizard.scss_create_or_update_attachment()
        self.view.invalidate_recordset()
        return self.view.arch

    def test_both_branches_are_rendered(self):
        arch = self._arch()
        tree = etree.fromstring(arch.encode())

        styles = tree.xpath("//style")
        self.assertEqual(len(styles), 2, "expected one stylesheet per colour scheme")
        self.assertTrue(tree.xpath("//t[@t-if]"), "dark branch has no condition")
        self.assertTrue(tree.xpath("//t[@t-else]"), "light branch has no condition")

    def test_dark_branch_switches_on_the_rendered_scheme(self):
        """The stylesheet must follow the same value that picked the asset bundle.

        web.layout chooses web.assets_web_dark on the render value
        `color_scheme`. Branching on anything else — the cookie, most of all —
        lets the two drift apart: Enterprise drops the cookie on logout and OCA
        web_dark_mode writes it only in _post_dispatch, so a cookie-driven
        branch paints the light palette onto the dark bundle for one render
        after every login.
        """
        tree = etree.fromstring(self._arch().encode())

        condition = tree.xpath("//t[@t-if]")[0].get("t-if")
        self.assertEqual(condition, "color_scheme == 'dark'")
        self.assertNotIn("cookie", condition)

    def test_dark_backdrop_stays_inside_the_backend(self):
        """web.layout also renders website, portal and kiosk pages.

        An unqualified `body` rule would paint those dark for every internal
        user whose backend is dark.
        """
        tree = etree.fromstring(self._arch().encode())
        dark_css = tree.xpath("//t[@t-if]//style")[0].text

        for line in dark_css.splitlines():
            selector = line.strip().rstrip("{ ,").strip()
            if selector == "body":
                self.fail("dark stylesheet carries an unqualified body rule")
        self.assertIn("body.o_web_client", dark_css)

    def test_dark_branch_carries_surface_colors(self):
        """Without surface rules the backend would stay white in dark mode."""
        tree = etree.fromstring(self._arch().encode())
        dark_css = tree.xpath("//t[@t-if]//style")[0].text
        light_css = tree.xpath("//t[@t-else]//style")[0].text

        self.assertIn("--bs-body-bg", dark_css)
        self.assertIn("color-scheme: dark", dark_css)
        self.assertNotIn("--bs-body-bg", light_css)

    def test_configured_dark_colors_reach_the_stylesheet(self):
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param(_dark_name("eq_navi_background"), "#00FF00")
        icp.set_param(_dark_name(VIEW_BACKGROUND_FIELD), "#000000")

        tree = etree.fromstring(self._arch().encode())
        dark_css = tree.xpath("//t[@t-if]//style")[0].text
        light_css = tree.xpath("//t[@t-else]//style")[0].text

        self.assertIn("#00FF00", dark_css)
        self.assertNotIn("#00FF00", light_css)

    def test_dark_branch_exports_the_variables_other_modules_read(self):
        """Modules that theme themselves properly read these and follow along.

        A module written as `var(--o-view-background-color, #fff)` stays white in
        dark mode unless somebody defines the variable. Exporting them is what
        lets such a module (eq_knowledge, for one) switch over without this
        stylesheet having to know any of its class names — so treat these names
        as a contract, not an implementation detail.
        """
        tree = etree.fromstring(self._arch().encode())
        dark_css = tree.xpath("//t[@t-if]//style")[0].text

        for variable in ("--o-view-background-color", "--gray-100", "--gray-300", "--gray-900"):
            self.assertIn(variable, dark_css, f"{variable} missing — themed modules stay light")

    def test_light_branch_is_unaffected_by_dark_settings(self):
        """Dark mode must not change how the light backend looks."""
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("eq_navi_background", "#123456")
        icp.set_param(_dark_name("eq_navi_background"), "#654321")

        tree = etree.fromstring(self._arch().encode())
        light_css = tree.xpath("//t[@t-else]//style")[0].text

        self.assertIn("#123456", light_css)
        self.assertNotIn("#654321", light_css)


class TestDerivedDarkColorsAreReadable(TransactionCase):
    """Derived dark colours must be legible, not merely different.

    Shifting a colour by a fixed amount is not enough: brightening a button
    without revisiting its label produced white text on pale green (1.65:1), and
    an accent that only cleared the page background fell short on the lighter
    surfaces stacked above it.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["eq.template.colors"].create({})

    def _derived_for(self, template):
        return self.wizard._derive_dark_colors({name: template[name] for name in COLOR_FIELDS})

    def test_every_shipped_template_derives_readable_colors(self):
        """Runs over all templates, so a new one cannot quietly break this."""
        templates = self.env["eq.colors"].search([("eq_is_dark", "=", False)])
        self.assertTrue(templates, "no color templates found")

        for template in templates:
            derived = self._derived_for(template)
            surfaces = [
                derived[VIEW_BACKGROUND_FIELD],
                derived["eq_list_secondary_background"],
                derived["eq_list_hoover_background"],
            ]
            lightest = max(surfaces, key=lambda c: self.wizard._relative_luminance(c) or 0)

            with self.subTest(template=template.name):
                button = self.wizard._contrast_ratio(
                    derived["eq_btn_primary_fontcolor"], derived["eq_btn_primary_background"]
                )
                self.assertGreaterEqual(
                    button, 4.5, f"{template.name}: button label unreadable ({button:.2f}:1)"
                )

                link = self.wizard._contrast_ratio(derived["eq_link_color"], lightest)
                self.assertGreaterEqual(
                    link, 4.5, f"{template.name}: links unreadable ({link:.2f}:1)"
                )

                navbar = self.wizard._contrast_ratio(
                    derived["eq_navi_fontcolor"], derived["eq_navi_background"]
                )
                self.assertGreaterEqual(
                    navbar, 4.5, f"{template.name}: navbar unreadable ({navbar:.2f}:1)"
                )

    def test_contrast_ratio_matches_wcag(self):
        """Anchor the maths against the two values WCAG fixes exactly."""
        self.assertAlmostEqual(self.wizard._contrast_ratio("#FFFFFF", "#000000"), 21.0, places=1)
        self.assertAlmostEqual(self.wizard._contrast_ratio("#FFFFFF", "#FFFFFF"), 1.0, places=1)

    def test_ensure_contrast_lifts_a_failing_color(self):
        dark_green = "#0A7A20"
        self.assertLess(self.wizard._contrast_ratio(dark_green, "#000000"), 4.5)
        lifted = self.wizard._ensure_contrast(dark_green, "#000000")
        self.assertGreaterEqual(self.wizard._contrast_ratio(lifted, "#000000"), 4.5)

    def test_readable_on_picks_the_better_side(self):
        self.assertEqual(self.wizard._readable_on("#FFFFFF"), "#000000")
        self.assertEqual(self.wizard._readable_on("#000000"), "#FFFFFF")
        # The case that broke: a pale accent needs dark, not white, text.
        self.assertEqual(self.wizard._readable_on("#81E129"), "#000000")

    def test_malformed_colors_do_not_raise(self):
        """Colours are free-text hex fields; a typo must not break rendering."""
        for bad in ("", None, "not-a-color", "#12345"):
            self.assertEqual(self.wizard._ensure_contrast(bad, "#000000"), bad)
            self.assertIsNone(self.wizard._relative_luminance(bad))


class TestShippedLightPalettesAreReadable(TransactionCase):
    """The light palettes must clear 4.5:1 too, not just the derived dark ones.

    Four of the ten shipped templates used to fall between 3.6:1 and 4.2:1 on
    their navbar and primary button — legible enough to pass a glance, not
    enough to read comfortably all day. Checking every record keeps a new
    template from reintroducing that.
    """

    # (foreground field, background field, what it renders as)
    PAIRS = (
        ("eq_navi_fontcolor", "eq_navi_background", "navbar"),
        ("eq_navi_hover_fontcolor", "eq_navi_hover", "navbar hover"),
        ("eq_btn_primary_fontcolor", "eq_btn_primary_background", "primary button"),
        ("eq_btn_secondary_fontcolor", "eq_btn_secondary_background", "secondary button"),
        ("eq_basic_text_color", "eq_list_primary_background", "text on list"),
        ("eq_basic_secondary_color", "eq_list_primary_background", "muted text"),
        ("eq_link_color", "eq_list_primary_background", "link"),
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["eq.template.colors"].create({})

    def test_shipped_light_palettes_meet_wcag_aa(self):
        templates = self.env["eq.colors"].search([("eq_is_dark", "=", False)])
        self.assertTrue(templates, "no light color templates found")

        for template in templates:
            for fg_field, bg_field, what in self.PAIRS:
                fg, bg = template[fg_field], template[bg_field]
                if not fg or not bg:
                    continue
                with self.subTest(template=template.name, pair=what):
                    contrast = self.wizard._contrast_ratio(fg, bg)
                    self.assertGreaterEqual(
                        contrast,
                        4.5,
                        f"{template.name}: {what} only reaches {contrast:.2f}:1 ({fg} on {bg})",
                    )


class TestDarkPaletteResolution(TransactionCase):
    """Selecting a template fills the dark colours in too."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wizard = cls.env["eq.template.colors"].create({})

    def test_linked_dark_palette_is_applied(self):
        template = self.env.ref("eq_ownerp_ui.eq_itguy_green")
        dark = self.env.ref("eq_ownerp_ui.eq_itguy_green_dark")

        self.wizard.eq_color_template_id = template
        self.wizard.eq_set_colors()

        self.assertEqual(self.wizard.eq_navi_background, template.eq_navi_background)
        self.assertEqual(self.wizard.eq_dark_navi_background, dark.eq_navi_background)
        self.assertEqual(self.wizard.eq_dark_basic_text_color, "#00FF00")
        self.assertEqual(self.wizard.eq_dark_view_background, "#000000")

    def test_template_without_dark_palette_gets_derived_colors(self):
        """Every template stays usable in dark mode, configured or not."""
        template = self.env.ref("eq_ownerp_ui.eq_default_blue")
        self.assertFalse(template.eq_dark_variant_id)

        self.wizard.eq_color_template_id = template
        self.wizard.eq_set_colors()

        for field_name in COLOR_FIELDS:
            self.assertTrue(
                self.wizard[_dark_name(field_name)],
                f"{_dark_name(field_name)} left empty — dark mode would fall back to light colours",
            )
        self.assertEqual(self.wizard.eq_dark_view_background, DEFAULT_DARK[VIEW_BACKGROUND_FIELD])

    def test_dark_palettes_are_not_offered_as_templates(self):
        """A dark palette is a counterpart, never a choice of its own."""
        field = self.env["eq.template.colors"]._fields["eq_color_template_id"]
        self.assertIn(("eq_is_dark", "=", False), field.domain)

    def test_apply_template_via_api_stores_both_sets(self):
        template = self.env.ref("eq_ownerp_ui.eq_itguy_amber")

        self.env["eq.template.colors"].api_apply_template(template.id)

        icp = self.env["ir.config_parameter"].sudo()
        self.assertEqual(icp.get_param("eq_navi_background"), template.eq_navi_background)
        self.assertEqual(icp.get_param(_dark_name("eq_basic_text_color")), "#FFB000")
