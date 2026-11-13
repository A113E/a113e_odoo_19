# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Backend UI",
    "license": "LGPL-3",
    "ownerp_packages": ["DACH"],
    # Advertised in the cross-selling block of the Store page, in this
    # order. "package:<name>" links to a package landing page, a bare
    # technical name to a single module.
    "ownerp_cross_selling": [
        "package:DACH",
        "package:Odoo2Fast.Report",
        "eq_chatbot",
    ],
    "version": "19.0.1.4.16",
    "description": "Easy configurable Backend Theme",
    "author": "Equitania Software GmbH",
    "website": "https://www.ownerp.com",
    # mail: the e-mail template colours in the settings live there, and this
    # module restyles them to match the rest of the theme's colour fields
    "depends": ["base_setup", "mail", "web"],
    # Animated Store cover (opt-in, see odoo-appstore-listing "Animated cover"):
    # the Store renders images[0] unchanged as the page header, GIF included.
    "ownerp_animated_cover": True,
    "images": [
        "static/description/eq_ownerp_ui_banner.gif",
        "static/description/eq_ownerp_ui_banner.png",
        "static/description/icon.png",
    ],
    "category": "Extra Tools",
    "summary": "Odoo backend in your corporate colors, with per-user dark mode",
    "eq_package": "ui",
    "data": [
        "data/eq_default_view.xml",
        "data/eq_default_templates.xml",
        "security/ir.model.access.csv",
        "views/eq_template_colors.xml",
        "views/eq_colors.xml",
        "views/eq_res_config_settings.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/eq_ownerp_ui/static/src/js/eq_widgets.js",
            "/eq_ownerp_ui/static/src/js/eq_dark_mode.js",
            "/eq_ownerp_ui/static/src/xml/eq_color_widget.xml",
            "/eq_ownerp_ui/static/src/css/eq_color_widget.css",
        ],
    },
    "installable": True,
    "auto_install": False,
}
