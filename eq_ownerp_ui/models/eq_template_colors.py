# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
"""Build the stylesheet that colours the Odoo backend.

The colours are stored as ``ir.config_parameter`` and rendered into the QWeb
view ``eq_ownerp_ui.eq_colors``, which appends a ``<style>`` block to the body of
``web.layout``.

Two colour sets are rendered side by side, a light one and a dark one, wrapped in
a QWeb condition on ``color_scheme``. Odoo swaps its own asset bundle for dark
mode entirely on the server and leaves no marker in the DOM, so a CSS selector
cannot tell the two apart — branching at render time is what makes one
stylesheet able to serve both.

``color_scheme`` is the render value ``web.layout`` itself uses to pick the
asset bundle (see ``ir.http.webclient_rendering_context``), which is the whole
point of reading it rather than the ``color_scheme`` cookie: the cookie lags
behind whenever another provider decides. Odoo Enterprise drops it on logout
and OCA ``web_dark_mode`` only writes it in ``_post_dispatch``, so a
cookie-driven branch would serve the light palette on top of the dark bundle
for one render after every login. Outside the webclient — website, portal,
kiosk pages, all of which go through ``web.layout`` too — the name is simply
not in the render values; QWeb resolves it to ``None`` and the light branch
wins, which is what those pages want.
"""

import colorsys

from odoo import api, fields, models

# The colour fields that make up one complete set. The dark counterpart of each
# is the same name with an "eq_dark_" prefix (see _dark_name), which keeps the
# two sets in step without listing every field twice.
COLOR_FIELDS = (
    "eq_basic_text_color",
    "eq_basic_secondary_color",
    "eq_link_color",
    "eq_apps_color",
    "eq_navi_background",
    "eq_navi_fontcolor",
    "eq_navi_hover",
    "eq_navi_hover_fontcolor",
    "eq_btn_primary_background",
    "eq_btn_primary_fontcolor",
    "eq_btn_secondary_background",
    "eq_btn_secondary_fontcolor",
    "eq_list_primary_background",
    "eq_list_secondary_background",
    "eq_list_hoover_background",
)

# Only meaningful in dark mode: in light mode Odoo's own white surfaces are kept.
VIEW_BACKGROUND_FIELD = "eq_view_background"

DEFAULT_LIGHT = {
    "eq_basic_text_color": "#141414",
    "eq_basic_secondary_color": "#858585",
    "eq_link_color": "#284DA3",
    "eq_apps_color": "#374D8B",
    "eq_navi_background": "#374D8B",
    "eq_navi_fontcolor": "#FFFFFF",
    "eq_navi_hover": "#FFFFFF",
    "eq_navi_hover_fontcolor": "#1E2C52",
    "eq_btn_primary_background": "#374D8B",
    "eq_btn_primary_fontcolor": "#FFFFFF",
    "eq_btn_secondary_background": "#CFCFCF",
    "eq_btn_secondary_fontcolor": "#212529",
    "eq_list_primary_background": "#FFFFFFFF",
    "eq_list_secondary_background": "#00000003",
    "eq_list_hoover_background": "#0000000e",
    VIEW_BACKGROUND_FIELD: "#FFFFFF",
}

# Neutral dark set matching the default blue theme. Used when no dark palette has
# been configured, so switching to dark mode always yields a usable backend.
DEFAULT_DARK = {
    "eq_basic_text_color": "#E4E6EB",
    "eq_basic_secondary_color": "#9BA3B4",
    "eq_link_color": "#8AA1E8",
    "eq_apps_color": "#8AA1E8",
    "eq_navi_background": "#171B24",
    "eq_navi_fontcolor": "#E4E6EB",
    "eq_navi_hover": "#2A3142",
    "eq_navi_hover_fontcolor": "#FFFFFF",
    "eq_btn_primary_background": "#5B76C7",
    "eq_btn_primary_fontcolor": "#FFFFFF",
    "eq_btn_secondary_background": "#2A3142",
    "eq_btn_secondary_fontcolor": "#E4E6EB",
    "eq_list_primary_background": "#1F2430",
    "eq_list_secondary_background": "#232936",
    "eq_list_hoover_background": "#2E3648",
    VIEW_BACKGROUND_FIELD: "#1F2430",
}


def _dark_name(field_name):
    """Return the dark counterpart of a colour field name."""
    return "eq_dark_" + field_name[len("eq_") :]


class EqTemplateColors(models.TransientModel):
    _name = "eq.template.colors"
    _description = "Color Picker"

    # Accent colours. Applied in both light and dark mode; only the values differ.
    CSS_TEMPLATE = """
            /* Scoped to .o_web_client to prevent styles leaking into website/webshop pages */
            .o_web_client {{
                --primary: {eq_btn_primary_background} !important;
                --secondary: {eq_basic_secondary_color} !important;
                --btn-primary: {eq_btn_primary_background} !important;
                --btn-primary-bg: {eq_btn_primary_background} !important;
                --btn-primary-border: {eq_btn_primary_background} !important;
                --btn-primary-color: {eq_btn_primary_fontcolor} !important;
                --link-color: {eq_link_color} !important;

                /* Odoo 19 Enterprise brand overrides */
                --o-enterprise-color: {eq_btn_primary_background} !important;
                --o-brand-primary: {eq_btn_primary_background} !important;
                --o-brand-odoo: {eq_btn_primary_background} !important;
                --o-action-color: {eq_link_color} !important;
                --o-enterprise-action-color: {eq_link_color} !important;

                /* Bootstrap 5 overrides */
                --bs-primary: {eq_btn_primary_background} !important;
                --bs-primary-rgb: auto !important;
                --bs-link-color: {eq_link_color} !important;
                --bs-link-hover-color: {eq_link_color_hover} !important;

                /* Odoo webclient variable overrides */
                --btn-color: {eq_btn_primary_background} !important;
                --o-stat-button-color: {eq_link_color} !important;
                --o-stat-text-color: {eq_link_color} !important;

                --NavBar-background: {eq_navi_background} !important;
                --NavBar-entry-color: {eq_navi_fontcolor} !important;
                --NavBar-entry-backgroundColor: {eq_navi_background} !important;
                --NavBar-entry-backgroundColor--hover: {eq_navi_hover} !important;
                --NavBar-entry-backgroundColor--active: {eq_navi_hover} !important;
            }}

            .o_web_client {{
                color: {eq_basic_text_color};
            }}

            /* Global Links. Menus keep Odoo's own colours: the entries of the
               navbar dropdowns, the apps or home menu with its search results and
               the burger menu are links as well, and painting them in the link
               colour made them unreadable on tinted backgrounds (green on green)
               and took the hover and active colours away from the marked entry. */
            .o_web_client a:not(.dropdown-item, .dropdown-menu *, .o-dropdown-menu *,
                .o_main_navbar *, .o_home_menu *, .o_menu_apps *,
                .dropdown-menu-custom *, .app-menu-container *, .o_burger_menu *),
            .o_web_client .o_form_view .o_form_uri,
            .o_web_client .o_form_view .oe_button_box .oe_stat_button .o_button_icon,
            .o_web_client .o-form-buttonbox .oe_stat_button .o_button_icon,
            .o_web_client .oe_stat_button .o_button_icon {{
                color: {eq_link_color} !important;
            }}

            .o_web_client .o_list_view .text-info {{
                color: {eq_link_color} !important;
            }}

            /* Hover States */
            .o_web_client a:not(.dropdown-item, .dropdown-menu *, .o-dropdown-menu *,
                .o_main_navbar *, .o_home_menu *, .o_menu_apps *,
                .dropdown-menu-custom *, .app-menu-container *, .o_burger_menu *):hover,
            .o_web_client .o_form_view .o_form_uri:hover,
            .o_web_client .o_form_view .oe_button_box .oe_stat_button .o_button_icon:hover,
            .o_web_client .o-form-buttonbox .oe_stat_button .o_button_icon:hover,
            .o_web_client .oe_stat_button .o_button_icon:hover {{
                color: {eq_link_color_hover} !important;
            }}

            /* Smart Button Value (Number) Override */
            .o_web_client .o-form-buttonbox .o_stat_info .o_stat_value,
            .o_web_client .o-form-buttonbox .oe_stat_button .o_stat_info .o_stat_value,
            .o_web_client .o-form-buttonbox .oe_stat_button .o_field_statinfo .o_stat_value {{
                color: {eq_link_color} !important;
            }}

            /* Radio Buttons and Checkboxes Active State */
            .o_web_client .form-check-input:checked,
            .o_web_client .o_radio_input:checked,
            .o_web_client .custom-control-input:checked ~ .custom-control-label::before {{
                background-color: {eq_btn_primary_background} !important;
                border-color: {eq_btn_primary_background} !important;
            }}

            /* Specific Fix for 'Neu' / Create Button in Control Panel */
            .o_web_client .o_control_panel .o_form_button_create,
            .o_web_client .o_control_panel .btn.btn-primary,
            .o_web_client .o_cp_buttons .btn-primary {{
                color: {eq_btn_primary_fontcolor} !important;
                background-color: {eq_btn_primary_background} !important;
                border-color: {eq_btn_primary_background} !important;
            }}

             /* Navbar Styling */
            .o_web_client .o_main_navbar {{
                background: {eq_navi_background} !important;
                border-bottom: 1px solid {eq_navi_background} !important;
            }}

            .o_web_client .o_main_navbar > ul > li > a,
            .o_web_client .o_main_navbar > ul > li > label,
            .o_web_client .o_main_navbar > .o_menu_brand,
            .o_web_client .o_main_navbar .o_menu_brand,
            .o_web_client .o_main_navbar .o_menu_toggle,
            .o_web_client .o_main_navbar .o_menu_sections > * > a,
            .o_web_client .o_main_navbar .o_menu_sections > * > button,
            .o_web_client .o_main_navbar .o_menu_sections .nav-link,
            .o_web_client .o_main_navbar .o_menu_sections .o_nav_entry,
            .o_web_client .o_main_navbar .o_menu_sections .dropdown-toggle,
            .o_web_client .o_main_navbar .o_menu_systray .nav-link,
            .o_web_client .o_main_navbar .o_menu_systray a,
            .o_web_client .o_main_navbar .o_menu_systray button,
            .o_web_client .o_main_navbar .o_menu_systray .o_switch_company_menu,
            .o_web_client .o_main_navbar .o_menu_systray .o_user_menu,
            .o_web_client .o_main_navbar mark {{
                color: {eq_navi_fontcolor} !important;
            }}

            .o_web_client .o_menu_sections,
            .o_web_client .o_main_navbar .o_menu_sections {{
                background: {eq_navi_background} !important;
            }}

            .o_web_client .o_main_navbar .o_menu_sections .o_nav_entry,
            .o_web_client .o_main_navbar .o_menu_sections .dropdown-toggle {{
                background: {eq_navi_background} !important;
                color: {eq_navi_fontcolor} !important;
            }}

            .o_web_client .o_main_navbar > ul > li > a:hover,
            .o_web_client .o_main_navbar > ul > li > label:hover,
            .o_web_client .o_main_navbar > a:hover, .o_web_client .o_main_navbar > a:focus,
            .o_web_client .o_main_navbar > button:hover, .o_web_client .o_main_navbar > button:focus,
            .o_web_client .o_main_navbar > ul > li.o_extra_menu_items.show > ul > li > a.dropdown-toggle,
            .o_web_client .o_main_navbar .show .dropdown-toggle,
            .o_web_client .o_main_navbar .o_menu_sections .nav-link:hover,
            .o_web_client .o_main_navbar .o_menu_sections .nav-link.active,
            .o_web_client .o_main_navbar .o_menu_sections .o_nav_entry:hover,
            .o_web_client .o_main_navbar .o_menu_sections .o_nav_entry.active,
            .o_web_client .o_main_navbar .o_menu_sections .dropdown-toggle:hover,
            .o_web_client .o_main_navbar .o_menu_sections .dropdown-toggle.show,
            .o_web_client .o_main_navbar .o_menu_sections > * > a:hover,
            .o_web_client .o_main_navbar .o_menu_sections > * > button:hover,
            .o_web_client .navbar-default .navbar-nav > .active > a,
            .o_web_client .navbar-default .navbar-nav > .active > a:hover,
            .o_web_client .navbar-default .navbar-nav > .active > a:focus,
            .o_web_client .navbar-default .navbar-nav > .open > a,
            .o_web_client .navbar-default .navbar-nav > .open > a:hover,
            .o_web_client .navbar-default .navbar-nav > .open > a:focus {{
                background: {eq_navi_hover} !important;
                color: {eq_navi_hover_fontcolor} !important;
            }}

            .o_web_client .o_menu_apps .dropdown-menu a.o_app i.o-app-icon,
            .o_web_client #sidebar .eq_new_icons i.o-app-icon {{
                color:{eq_apps_color};
            }}

            .o_web_client .text-muted {{
                color: {eq_basic_secondary_color} !important;
            }}

            .o_web_client .btn-primary {{
                color: {eq_btn_primary_fontcolor} !important;
                background: {eq_btn_primary_background} !important;
                border-color: {eq_btn_primary_background} !important;
            }}

            .o_web_client .btn-primary:hover,
            .o_web_client .btn-primary:focus,
            .o_web_client .btn-primary.focus,
            .o_web_client .btn-primary:not(:disabled):not(.disabled):active,
            .o_web_client .btn-primary:not(:disabled):not(.disabled).active,
            .o_web_client .show > .btn-primary.dropdown-toggle {{
                color: {eq_btn_primary_fontcolor} !important;
                background: {eq_btn_primary_background} !important;
                filter: brightness(90%);
            }}

            .o_web_client .btn-secondary {{
                color: {eq_btn_secondary_fontcolor} !important;
                background: {eq_btn_secondary_background} !important;
            }}

            .o_web_client .btn-secondary:hover,
            .o_web_client .btn-secondary:focus,
            .o_web_client .btn-secondary.focus,
            .o_web_client .btn-secondary:not(:disabled):not(.disabled):active,
            .o_web_client .btn-secondary:not(:disabled):not(.disabled).active,
            .o_web_client .show > .btn-secondary.dropdown-toggle {{
                color: {eq_btn_secondary_fontcolor} !important;
                background: {eq_btn_secondary_background} !important;
                filter: brightness(90%);
            }}

            .o_web_client .o_field_statusbar > .o_statusbar_status > .o_arrow_button.o_arrow_button_current.disabled {{
                background-color: {eq_navi_background} !important;
            }}

            .o_web_client .o_field_statusbar > .o_statusbar_status
                > .o_arrow_button.o_arrow_button_current.disabled:after,
            .o_web_client .o_field_statusbar > .o_statusbar_status
                > .o_arrow_button.o_arrow_button_current.disabled:before {{
                border-left-color: {eq_navi_background} !important;
            }}

            .o_web_client .btn-fill-odoo,
            .o_web_client .btn-odoo {{
                color: {eq_btn_primary_fontcolor};
                background-color: {eq_btn_primary_background};
                border-color: {eq_btn_primary_background};
                box-shadow: 0;
            }}

            .o_web_client .table {{
                --table-accent-bg: {eq_list_primary_background} !important;
                --table-striped-bg: {eq_list_secondary_background} !important;
                --table-hover-bg: {eq_list_hoover_background} !important;
            }}

            {eq_background_img}
    """

    # Surfaces. Only emitted for the dark set: Odoo's own light surfaces are
    # compiled into SCSS ($o-view-background-color and friends) and cannot be
    # reached through a custom property at runtime, so every white area has to be
    # named explicitly. Without this block the backend stays white in dark mode.
    DARK_SURFACE_TEMPLATE = """
            /* --- Dark mode surfaces --- */
            .o_web_client {{
                --bs-body-bg: {eq_view_background} !important;
                --bs-body-color: {eq_basic_text_color} !important;
                --bs-emphasis-color: {eq_basic_text_color} !important;
                --bs-secondary-bg: {eq_list_secondary_background} !important;
                --bs-tertiary-bg: {eq_list_secondary_background} !important;
                --bs-secondary-color: {eq_basic_secondary_color} !important;
                --bs-border-color: {eq_border_color} !important;
                --bs-modal-bg: {eq_view_background} !important;
                --bs-modal-color: {eq_basic_text_color} !important;
                --bs-card-bg: {eq_view_background} !important;
                --bs-card-color: {eq_basic_text_color} !important;
                --bs-list-group-bg: {eq_view_background} !important;
                --bs-list-group-color: {eq_basic_text_color} !important;
                --bs-dropdown-bg: {eq_view_background} !important;
                --bs-dropdown-color: {eq_basic_text_color} !important;
                --bs-dropdown-link-color: {eq_basic_text_color} !important;
                --bs-dropdown-link-hover-bg: {eq_list_hoover_background} !important;
                --bs-dropdown-link-hover-color: {eq_basic_text_color} !important;
                --bs-table-bg: {eq_list_primary_background} !important;
                --bs-table-color: {eq_basic_text_color} !important;
                --bs-popover-bg: {eq_view_background} !important;
                --bs-popover-body-color: {eq_basic_text_color} !important;
                --bs-tooltip-bg: {eq_navi_background} !important;
                --bs-tooltip-color: {eq_navi_fontcolor} !important;
                /* Odoo's own surface variable and the grey scale. Both are SCSS
                   in core, but modules that theme themselves properly read them
                   as CSS variables with a light fallback
                   (`var(--o-view-background-color, #fff)`). Setting them here is
                   what makes such a module follow dark mode without this
                   stylesheet having to know its class names — eq_knowledge is
                   built that way. */
                --o-view-background-color: {eq_view_background} !important;
                --o-webclient-background-color: {eq_view_background} !important;
                --gray-100: {eq_list_secondary_background} !important;
                --gray-200: {eq_list_hoover_background} !important;
                --gray-300: {eq_border_color} !important;
                --gray-400: {eq_basic_secondary_color} !important;
                --gray-500: {eq_basic_secondary_color} !important;
                --gray-600: {eq_basic_secondary_color} !important;
                --gray-700: {eq_basic_text_color} !important;
                --gray-800: {eq_basic_text_color} !important;
                --gray-900: {eq_basic_text_color} !important;

                --bs-breadcrumb-bg: transparent !important;
                --bs-nav-tabs-border-color: {eq_border_color} !important;
                --bs-nav-tabs-link-active-bg: {eq_list_secondary_background} !important;
                --bs-nav-tabs-link-active-color: {eq_link_color} !important;
                --bs-nav-tabs-link-active-border-color: {eq_border_color} !important;
                --bs-nav-tabs-link-hover-border-color: {eq_border_color} !important;
                color-scheme: dark;
            }}

            /* Page and view backgrounds. `body` carries o_web_client in the
               backend (web.layout sets body_classname), so qualifying it costs
               nothing there and keeps the dark backdrop off the website, portal
               and kiosk pages, which render through web.layout as well. */
            body.o_web_client,
            .o_web_client,
            .o_web_client .o_action_manager,
            .o_web_client .o_content,
            .o_web_client .o_view_controller,
            .o_web_client .o_form_view,
            .o_web_client .o_form_sheet_bg,
            .o_web_client .o_list_view,
            .o_web_client .o_list_renderer,
            .o_web_client .o_kanban_renderer,
            .o_web_client .o_kanban_view,
            .o_web_client .o_calendar_view,
            .o_web_client .o_pivot,
            .o_web_client .o_graph_view,
            .o_web_client .o_setting_container,
            .o_web_client .o_home_menu {{
                background-color: {eq_view_background} !important;
                color: {eq_basic_text_color};
            }}

            /* Lifted surfaces: sheets, cards, dialogs, menus */
            .o_web_client .o_form_sheet,
            .o_web_client .o_kanban_record,
            .o_web_client .o_setting_box,
            .o_web_client .card,
            .o_web_client .modal-content,
            .o_web_client .modal-header,
            .o_web_client .modal-footer,
            .o_web_client .dropdown-menu,
            .o_web_client .popover,
            .o_web_client .popover-body,
            .o_web_client .o_notification,
            .o_web_client .list-group-item,
            .o_web_client .o_popover {{
                background-color: {eq_list_secondary_background} !important;
                color: {eq_basic_text_color} !important;
                border-color: {eq_border_color} !important;
            }}

            /* Control panel, search view and side panels */
            .o_web_client .o_control_panel,
            .o_web_client .o_control_panel_main,
            .o_web_client .o_form_statusbar,
            .o_web_client .o_cp_searchview,
            .o_web_client .o_searchview,
            .o_web_client .o_search_panel,
            .o_web_client .o_cp_bottom,
            .o_web_client .o_breadcrumb,
            .o_web_client .o_last_breadcrumb_item {{
                background-color: {eq_view_background} !important;
                color: {eq_basic_text_color} !important;
            }}

            /* Tables */
            .o_web_client .table,
            .o_web_client .o_list_table,
            .o_web_client .o_list_table > thead > tr > th,
            .o_web_client .o_list_table > tbody > tr > td,
            .o_web_client .o_list_table > tfoot > tr > td {{
                background-color: {eq_list_primary_background} !important;
                color: {eq_basic_text_color} !important;
                border-color: {eq_border_color} !important;
            }}

            .o_web_client .o_list_table > tbody > tr:hover > td {{
                background-color: {eq_list_hoover_background} !important;
            }}

            /* Form inputs */
            .o_web_client input:not([type="checkbox"]):not([type="radio"]),
            .o_web_client select,
            .o_web_client textarea,
            .o_web_client .form-control,
            .o_web_client .form-select,
            .o_web_client .o_input,
            .o_web_client .o_field_widget input,
            .o_web_client .o_searchview input {{
                background-color: {eq_list_secondary_background} !important;
                color: {eq_basic_text_color} !important;
                border-color: {eq_border_color} !important;
            }}

            .o_web_client input::placeholder,
            .o_web_client textarea::placeholder {{
                color: {eq_basic_secondary_color} !important;
            }}

            /* Tabs, breadcrumb and separators. Bootstrap paints .nav-tabs and
               .breadcrumb white through its own custom properties, so the
               background has to be named here as well as the colour. */
            .o_web_client .o_notebook .nav-tabs,
            .o_web_client .nav-tabs,
            .o_web_client .breadcrumb,
            .o_web_client .o_notebook .nav-link,
            .o_web_client .o_horizontal_separator,
            .o_web_client hr {{
                background-color: transparent !important;
                color: {eq_basic_text_color} !important;
                border-color: {eq_border_color} !important;
            }}

            .o_web_client .o_notebook .nav-link.active {{
                background-color: {eq_list_secondary_background} !important;
                color: {eq_link_color} !important;
            }}

            /* Chatter and Discuss: mail ships its own *.dark.scss, but those
               build on the dark SCSS variables that Community does not have, so
               every mail surface stays light grey unless it is set here. Matched
               by prefix because the Discuss app alone has a dozen containers. */
            .o_web_client [class*="o-mail-"] {{
                background-color: {eq_list_secondary_background} !important;
            }}

            .o_web_client .o-mail-ChatterContainer,
            .o_web_client .o-mail-Chatter,
            .o_web_client .o-mail-Chatter-top,
            .o_web_client .o-mail-Chatter-content,
            .o_web_client .o-mail-Thread,
            .o_web_client .o-mail-Composer,
            .o_web_client .o-mail-Composer-input,
            .o_web_client .o-mail-Message,
            .o_web_client .o-mail-Message-body,
            .o_web_client .o-mail-DiscussSidebar,
            .o_web_client .o-mail-DiscussContent-core,
            .o_web_client .o-mail-DiscussContent-header,
            .o_web_client .o-mail-DiscussSearch,
            .o_web_client .o-mail-MessagingMenu,
            .o_web_client .o-mail-ActivityList {{
                color: {eq_basic_text_color} !important;
            }}

            /* Status colours stay semantic, but Odoo's values are mixed for a
               white background and drop below readable contrast on a dark one. */
            .o_web_client {{
                --bs-success-text-emphasis: #4ADE80 !important;
                --bs-danger-text-emphasis: #F87171 !important;
                --bs-warning-text-emphasis: #FBBF24 !important;
                --bs-info-text-emphasis: #60A5FA !important;
                --bs-success-bg-subtle: {eq_list_secondary_background} !important;
                --bs-danger-bg-subtle: {eq_list_secondary_background} !important;
                --bs-warning-bg-subtle: {eq_list_secondary_background} !important;
                --bs-info-bg-subtle: {eq_list_secondary_background} !important;
            }}

            .o_web_client .text-success {{ color: #4ADE80 !important; }}
            .o_web_client .text-danger {{ color: #F87171 !important; }}
            .o_web_client .text-warning {{ color: #FBBF24 !important; }}
            .o_web_client .text-info {{ color: #60A5FA !important; }}

            /* Keep icons and headings legible */
            .o_web_client h1, .o_web_client h2, .o_web_client h3,
            .o_web_client h4, .o_web_client h5, .o_web_client h6,
            .o_web_client label,
            .o_web_client .o_form_label,
            .o_web_client .fa {{
                color: {eq_basic_text_color};
            }}

            /* Text that Odoo compiles with Bootstrap's $body-color (#212529).
               Those rules win over --bs-body-color because the value is baked
               into the stylesheet, so each place has to be named. Everything
               below was found by measuring contrast in the running backend, not
               by guessing. */
            .o_web_client .dropdown-item,
            .o_web_client .o-dropdown-item,
            .o_web_client .dropdown-item > span,
            .o_web_client .o_menu_item,
            .o_web_client .o_accordion_toggle,
            .o_web_client .o_stat_text,
            .o_web_client .o-app-menu-item__name,
            .o_web_client .app_name,
            .o_web_client .o-mail-Message-date,
            .o_web_client .o-mail-Message-author,
            .o_web_client .o_list_footer,
            .o_web_client .o_group_name,
            .o_web_client .text-body,
            .o_web_client .text-dark,
            .o_web_client .text-black,
            .o_web_client .btn.border-0,
            .o_web_client .btn-link {{
                color: {eq_basic_text_color} !important;
            }}

            /* Settings screen: its own surfaces, all light in the compiled CSS */
            .o_web_client .settings,
            .o_web_client .settings_tab,
            .o_web_client .o_setting_container,
            .o_web_client .settings .app_settings_block,
            .o_web_client .settings h2 {{
                background-color: {eq_view_background} !important;
                color: {eq_basic_text_color} !important;
            }}

            .o_web_client .settings_tab .tab,
            .o_web_client .settings_tab .tab.selected,
            .o_web_client .o_searchview_dropdown_toggler,
            .o_web_client .o_list_footer,
            .o_web_client tfoot {{
                background-color: {eq_list_secondary_background} !important;
                color: {eq_basic_text_color} !important;
            }}

            .o_web_client .settings_tab .tab.selected {{
                border-color: {eq_btn_primary_background} !important;
            }}

            /* web_responsive: apps menu overlay and its search box */
            .o_web_client .search-input,
            .o_web_client .search-input input,
            .o_web_client .o-app-menu-item,
            .o_web_client .o_grid_apps_menu,
            .o_web_client .dropdown-menu-custom {{
                background-color: {eq_list_secondary_background} !important;
                color: {eq_basic_text_color} !important;
            }}

            /* Alerts: Bootstrap paints them with light *-bg-subtle values */
            .o_web_client .alert {{
                --bs-alert-bg: {eq_list_secondary_background} !important;
                --bs-alert-color: {eq_basic_text_color} !important;
                --bs-alert-border-color: {eq_border_color} !important;
                background-color: {eq_list_secondary_background} !important;
                color: {eq_basic_text_color} !important;
                border-color: {eq_border_color} !important;
            }}
    """

    name = fields.Char(string="Name", default="Template Colors")
    # Dark palettes are the counterpart of a template, never a choice of their own.
    eq_color_template_id = fields.Many2one(
        "eq.colors",
        string="Color Template",
        domain=[("eq_is_dark", "=", False)],
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
    eq_navi_hover_fontcolor = fields.Char(string="Navigation Hover Font Color")
    # Buttons
    eq_btn_primary_background = fields.Char(string="Primary Button Backgroundcolor")
    eq_btn_primary_fontcolor = fields.Char(string="Primary Button Fontcolor")
    eq_btn_secondary_background = fields.Char(string="Secondary Button Backgroundcolor")
    eq_btn_secondary_fontcolor = fields.Char(string="Secondary Button Fontcolor")
    # List View
    eq_list_primary_background = fields.Char(string="Primary Backgroundcolor")
    eq_list_secondary_background = fields.Char(string="Secondary Backgroundcolor")
    eq_list_hoover_background = fields.Char(string="Hover Backgroundcolor")
    # Dark Mode - Basic Colors
    eq_dark_view_background = fields.Char(string="Dark View Background")
    eq_dark_basic_text_color = fields.Char(string="Dark Basic Text Color")
    eq_dark_basic_secondary_color = fields.Char(string="Dark Basic Secondary Color")
    eq_dark_link_color = fields.Char(string="Dark Link Color")
    # Dark Mode - Navigation
    eq_dark_apps_color = fields.Char(string="Dark App-Icon Color")
    eq_dark_navi_background = fields.Char(string="Dark Navigation Background")
    eq_dark_navi_fontcolor = fields.Char(string="Dark Navigation Fontcolor")
    eq_dark_navi_hover = fields.Char(string="Dark Navigation Hover Background")
    eq_dark_navi_hover_fontcolor = fields.Char(string="Dark Navigation Hover Font Color")
    # Dark Mode - Buttons
    eq_dark_btn_primary_background = fields.Char(string="Dark Primary Button Backgroundcolor")
    eq_dark_btn_primary_fontcolor = fields.Char(string="Dark Primary Button Fontcolor")
    eq_dark_btn_secondary_background = fields.Char(string="Dark Secondary Button Backgroundcolor")
    eq_dark_btn_secondary_fontcolor = fields.Char(string="Dark Secondary Button Fontcolor")
    # Dark Mode - List View
    eq_dark_list_primary_background = fields.Char(string="Dark Primary Backgroundcolor")
    eq_dark_list_secondary_background = fields.Char(string="Dark Secondary Backgroundcolor")
    eq_dark_list_hoover_background = fields.Char(string="Dark Hover Backgroundcolor")
    # Background Image
    eq_company_id = fields.Many2one("res.company", string="Company")
    eq_background_image_name = fields.Char(
        string="Background Image Name",
        related="eq_company_id.eq_background_image_name",
        readonly=False,
    )
    eq_background_image = fields.Binary(
        string="Background Image",
        related="eq_company_id.eq_background_image",
        readonly=False,
    )

    @api.onchange("eq_color_template_id")
    def eq_set_colors(self):
        """Copy the selected template's colours onto the wizard.

        The dark values come from the template's linked dark palette. Templates
        without one fall back to colours derived from their light set, so a
        switch to dark mode never lands on an unreadable screen.
        """
        template = self.eq_color_template_id
        if not template:
            return

        for field_name in COLOR_FIELDS:
            self[field_name] = template[field_name]

        dark_palette = template.eq_dark_variant_id
        if dark_palette:
            dark_values = {name: dark_palette[name] for name in COLOR_FIELDS}
            dark_values[VIEW_BACKGROUND_FIELD] = (
                dark_palette.eq_view_background or DEFAULT_DARK[VIEW_BACKGROUND_FIELD]
            )
        else:
            dark_values = self._derive_dark_colors({name: template[name] for name in COLOR_FIELDS})

        for field_name, value in dark_values.items():
            self[_dark_name(field_name)] = value

    def execute(self):
        icp = self.env["ir.config_parameter"]
        for field_name in COLOR_FIELDS:
            icp.set_param(field_name, self[field_name])
            dark_field = _dark_name(field_name)
            icp.set_param(dark_field, self[dark_field])
        icp.set_param(_dark_name(VIEW_BACKGROUND_FIELD), self.eq_dark_view_background)
        if self.eq_color_template_id:
            icp.set_param("eq_color_template_id", self.eq_color_template_id.id)
        self.scss_create_or_update_attachment()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def reset_default(self):
        icp = self.env["ir.config_parameter"]
        for field_name in COLOR_FIELDS:
            icp.set_param(field_name, DEFAULT_LIGHT[field_name])
            self[field_name] = DEFAULT_LIGHT[field_name]
            dark_field = _dark_name(field_name)
            icp.set_param(dark_field, DEFAULT_DARK[field_name])
            self[dark_field] = DEFAULT_DARK[field_name]
        icp.set_param(_dark_name(VIEW_BACKGROUND_FIELD), DEFAULT_DARK[VIEW_BACKGROUND_FIELD])
        self.eq_dark_view_background = DEFAULT_DARK[VIEW_BACKGROUND_FIELD]
        self.scss_create_or_update_attachment()

    @api.model
    def default_get(self, fields):
        icp = self.env["ir.config_parameter"]
        res = {
            "name": "Template Colors",
            "eq_company_id": self.env.company.id,
        }
        for field_name in COLOR_FIELDS:
            res[field_name] = icp.get_param(field_name) or DEFAULT_LIGHT[field_name]
            dark_field = _dark_name(field_name)
            res[dark_field] = icp.get_param(dark_field) or DEFAULT_DARK[field_name]
        dark_view_field = _dark_name(VIEW_BACKGROUND_FIELD)
        res[dark_view_field] = icp.get_param(dark_view_field) or DEFAULT_DARK[VIEW_BACKGROUND_FIELD]

        if icp.get_param("eq_color_template_id"):
            res["eq_color_template_id"] = int(icp.get_param("eq_color_template_id"))
        return res

    def _shift_lightness(self, hex_color, amount):
        """Shift a colour's lightness; positive brightens, negative darkens."""
        if not hex_color or not hex_color.startswith("#"):
            return hex_color
        hex_color = hex_color.lstrip("#")
        try:
            r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            h, lightness, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            lightness = max(0, min(1, lightness + amount))
            r, g, b = colorsys.hls_to_rgb(h, lightness, s)
            return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
        except ValueError:
            return hex_color

    def _darken_color(self, hex_color, amount=0.2):
        return self._shift_lightness(hex_color, -amount)

    def _lighten_color(self, hex_color, amount=0.2):
        return self._shift_lightness(hex_color, amount)

    @staticmethod
    def _relative_luminance(hex_color):
        """WCAG relative luminance of a ``#RRGGBB`` colour, or None if unusable."""
        if not hex_color or not hex_color.startswith("#") or len(hex_color.lstrip("#")) < 6:
            return None
        value = hex_color.lstrip("#")
        try:
            channels = [int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
        except ValueError:
            return None
        adjusted = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * adjusted[0] + 0.7152 * adjusted[1] + 0.0722 * adjusted[2]

    def _contrast_ratio(self, color_a, color_b):
        """WCAG contrast ratio between two colours (1.0 when incomparable)."""
        lum_a = self._relative_luminance(color_a)
        lum_b = self._relative_luminance(color_b)
        if lum_a is None or lum_b is None:
            return 1.0
        lighter, darker = max(lum_a, lum_b), min(lum_a, lum_b)
        return (lighter + 0.05) / (darker + 0.05)

    def _readable_on(self, background, dark_text="#000000", light_text="#FFFFFF"):
        """Pick whichever of two text colours reads better on ``background``."""
        if self._relative_luminance(background) is None:
            return light_text
        return (
            dark_text
            if self._contrast_ratio(dark_text, background)
            >= self._contrast_ratio(light_text, background)
            else light_text
        )

    def _ensure_contrast(self, color, background, minimum=4.5, step=0.05, limit=16):
        """Shift a colour away from ``background`` until it is readable on it.

        A fixed lightness offset is not enough: how far a colour has to move
        depends on where it starts. Odoo's own palettes cover a wide range, and
        several of them land below 2:1 against a dark surface if shifted by a
        constant amount.
        """
        if self._relative_luminance(color) is None or self._relative_luminance(background) is None:
            return color
        # Move towards the opposite end from the background.
        direction = 1 if self._relative_luminance(background) < 0.5 else -1
        current = color
        for _ in range(limit):
            if self._contrast_ratio(current, background) >= minimum:
                return current
            shifted = self._shift_lightness(current, direction * step)
            if shifted == current:  # hit pure black or white
                break
            current = shifted
        return current

    @api.model
    def _derive_dark_colors(self, light_colors):
        """Build a usable dark set from light colours.

        Used for templates that carry no dark palette of their own, and for
        colours a user mixed by hand. Accents are shifted until they are actually
        readable on the dark surface rather than by a fixed amount, and every
        text colour is then chosen to suit the background it sits on — brightening
        a button without revisiting its label is how white-on-pale-green happens.
        Surfaces are replaced outright, because a light background has no
        meaningful dark equivalent to scale towards.
        """
        derived = dict(DEFAULT_DARK)

        # Measure against the lightest surface an accent can land on, not just
        # the page background: cards, list stripes and hover states sit above it,
        # and a colour that only clears the darkest one falls short on those.
        surfaces = [
            derived[VIEW_BACKGROUND_FIELD],
            derived["eq_list_secondary_background"],
            derived["eq_list_hoover_background"],
        ]
        surface = max(surfaces, key=lambda c: self._relative_luminance(c) or 0)

        for accent in ("eq_link_color", "eq_apps_color", "eq_btn_primary_background"):
            if light_colors.get(accent):
                derived[accent] = self._ensure_contrast(light_colors[accent], surface)

        if light_colors.get("eq_navi_background"):
            # Keep the navigation recognisable, just deep enough for dark mode.
            derived["eq_navi_background"] = self._darken_color(
                light_colors["eq_navi_background"], 0.22
            )

        # Text colours follow whatever they end up sitting on.
        derived["eq_btn_primary_fontcolor"] = self._readable_on(
            derived["eq_btn_primary_background"]
        )
        derived["eq_btn_secondary_fontcolor"] = self._readable_on(
            derived["eq_btn_secondary_background"]
        )
        derived["eq_navi_fontcolor"] = self._readable_on(
            derived["eq_navi_background"],
            dark_text="#000000",
            light_text=derived["eq_basic_text_color"],
        )
        derived["eq_navi_hover_fontcolor"] = self._readable_on(
            derived["eq_navi_hover"], dark_text="#000000", light_text=derived["eq_basic_text_color"]
        )
        return derived

    def _css_parameters(self, stored, dark=False):
        """Assemble the placeholder values for one colour set.

        Args:
            stored: Result of ``default_get``, holding both colour sets.
            dark: Whether to build the dark set.

        Returns:
            Dict of placeholders consumed by CSS_TEMPLATE (and, for the dark set,
            DARK_SURFACE_TEMPLATE).
        """
        params = {}
        for field_name in COLOR_FIELDS:
            source = _dark_name(field_name) if dark else field_name
            params[field_name] = (
                stored.get(source) or (DEFAULT_DARK if dark else DEFAULT_LIGHT)[field_name]
            )

        # Link hover: darker on light surfaces, brighter on dark ones.
        link_color = params["eq_link_color"]
        params["eq_link_color_hover"] = (
            self._lighten_color(link_color, 0.15) if dark else self._darken_color(link_color, 0.2)
        )

        if dark:
            params[VIEW_BACKGROUND_FIELD] = (
                stored.get(_dark_name(VIEW_BACKGROUND_FIELD)) or DEFAULT_DARK[VIEW_BACKGROUND_FIELD]
            )
            params["eq_border_color"] = self._lighten_color(params[VIEW_BACKGROUND_FIELD], 0.12)

        params["eq_background_img"] = self._background_image_css(params)
        return params

    def _background_image_css(self, params):
        """Return the CSS for the apps-menu background, if a menu module needs it."""
        modules = self.env["ir.module.module"]
        web_responsive = modules.search(
            [("name", "=", "web_responsive"), ("state", "=", "installed")]
        )
        web_enterprise = modules.search(
            [("name", "=", "web_enterprise"), ("state", "=", "installed")]
        )

        company_image = self.env.company.eq_background_image
        image_url = "url(/web/image/res.company/%s/eq_background_image)" % str(self.env.company.id)

        if web_responsive:
            if not company_image:
                image_url = (
                    "url(/web_responsive/static/src/components/apps_menu/../../img/home-menu-bg-overlay.svg), "
                    "linear-gradient(to bottom,%s,%s)"
                    % (params["eq_navi_background"], params["eq_navi_hover"])
                )
            # Both class names on purpose: web_responsive renamed the apps-menu
            # container from .dropdown-menu-custom to .app-menu-container, and
            # targeting only the old one left the overlay in web_responsive's own
            # pale gradient — a full-screen light panel once dark mode is on.
            return (
                """
                .dropdown-menu-custom,
                .app-menu-container {
                    background:%s !important;
                    background-size: cover !important;
                    }"""
                % image_url
            )
        if web_enterprise:
            if company_image:
                return (
                    """
                .o_web_client.o_home_menu_background {
                    background:%s !important;
                    }"""
                    % image_url
                )
            return """
                .o_web_client.o_home_menu_background {
                    background-color: %s !important;
                    }""" % params["eq_navi_background"]
        return ""

    def scss_create_or_update_attachment(self):
        """Render both colour sets into the QWeb view injected into web.layout."""
        stored = self.sudo().default_get([])
        light_css = self.CSS_TEMPLATE.format(**self._css_parameters(stored, dark=False))
        dark_params = self._css_parameters(stored, dark=True)
        dark_css = self.CSS_TEMPLATE.format(**dark_params) + self.DARK_SURFACE_TEMPLATE.format(
            **dark_params
        )

        # Built by concatenation rather than str.format: the rendered CSS is full
        # of braces, which format() would try to read as placeholders again.
        arch = (
            '<data inherit_id="web.layout">'
            '<xpath expr="//body" position="inside">'
            "<t t-if=\"color_scheme == 'dark'\">"
            "<style>" + dark_css + "</style>"
            "</t>"
            '<t t-else="">'
            "<style>" + light_css + "</style>"
            "</t>"
            "</xpath>"
            "</data>"
        )
        self.env.ref("eq_ownerp_ui.eq_colors").write({"arch": arch})

    @api.model
    def api_apply_template(self, template_id):
        """
        API Helper to apply a color template by ID in one step.
        Useful for XML-RPC / External Scripts.
        """
        template = self.env["eq.colors"].browse(template_id)
        if not template.exists():
            return False

        vals = {"eq_color_template_id": template.id}
        for field_name in COLOR_FIELDS:
            vals[field_name] = template[field_name]

        dark_palette = template.eq_dark_variant_id
        if dark_palette:
            dark_values = {name: dark_palette[name] for name in COLOR_FIELDS}
            dark_values[VIEW_BACKGROUND_FIELD] = (
                dark_palette.eq_view_background or DEFAULT_DARK[VIEW_BACKGROUND_FIELD]
            )
        else:
            dark_values = self._derive_dark_colors({name: template[name] for name in COLOR_FIELDS})
        for field_name, value in dark_values.items():
            vals[_dark_name(field_name)] = value

        wizard = self.create(vals)
        wizard.execute()
        return True
