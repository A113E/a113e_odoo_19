/** @odoo-module **/
/**
 * Dark mode switch for the user menu.
 *
 * Odoo 19 Community ships the dark-mode plumbing but nothing that operates it:
 * the `color_scheme` cookie decides which stylesheet a request gets, and nobody
 * ever writes that cookie. This service writes it.
 *
 * It stands down when another provider is present. Odoo Enterprise
 * (`web_enterprise`) and OCA `web_dark_mode` both offer their own switch and
 * expose their own field on `res.users.settings`, so the presence of that field
 * is a reliable signal that a switch already exists — without it the user menu
 * would show two.
 */
import {_t} from "@web/core/l10n/translation";
import {browser} from "@web/core/browser/browser";
import {cookie} from "@web/core/browser/cookie";
import {registry} from "@web/core/registry";
import {user} from "@web/core/user";

const COOKIE_NAME = "color_scheme";

/** True when Odoo Enterprise or OCA web_dark_mode already provides a switch. */
export function hasForeignColorSchemeProvider() {
    const settings = user.settings || {};
    return settings.color_scheme !== undefined || settings.dark_mode !== undefined;
}

/** The scheme the operating system asks for. */
export function systemColorScheme() {
    return browser.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
}

/** The scheme the current page was rendered with. */
export function currentColorScheme() {
    return cookie.get(COOKIE_NAME) === "dark" ? "dark" : "light";
}

export function eqDarkModeSwitchItem(env) {
    return {
        type: "switch",
        id: "eq_ownerp_ui.color_scheme",
        description: _t("Dark Mode"),
        callback: () => env.services.eq_color_scheme.toggle(),
        isChecked: currentColorScheme() === "dark",
        sequence: 40,
    };
}

export const eqColorSchemeService = {
    dependencies: ["orm", "ui"],

    async start(env, {orm, ui}) {
        if (hasForeignColorSchemeProvider()) {
            // Another module owns the dark mode; do not add a second switch.
            return {};
        }

        // Resolve what this user should see. "system" follows the OS, which the
        // server cannot know, so the first page load may need one reload to
        // catch up. An explicit light/dark choice is already handled server-side
        // and never reloads here.
        const stored = user.settings.eq_color_scheme;
        const target =
            stored === "light" || stored === "dark" ? stored : systemColorScheme();

        if (target !== currentColorScheme()) {
            cookie.set(COOKIE_NAME, target);
            browser.location.reload();
        }

        registry.category("user_menuitems").add("eq_dark_mode", eqDarkModeSwitchItem);

        return {
            get currentColorScheme() {
                return currentColorScheme();
            },
            async toggle() {
                const scheme = currentColorScheme() === "dark" ? "light" : "dark";
                cookie.set(COOKIE_NAME, scheme);
                // Persist so the choice survives a new browser or device.
                await orm.call(
                    "res.users.settings",
                    "set_res_users_settings",
                    [[user.settings.id]],
                    {
                        new_settings: {eq_color_scheme: scheme},
                    }
                );
                ui.block();
                browser.location.reload();
            },
        };
    },
};

registry.category("services").add("eq_color_scheme", eqColorSchemeService);
