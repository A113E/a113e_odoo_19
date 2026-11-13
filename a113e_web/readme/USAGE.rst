Usage
=====

**Custom "A113e" Filter in Apps**

By default, the Odoo *Apps* menu displays all applications (both core and custom). This module introduces a new search filter called **"A113e"** which automatically filters the list to show only the custom modules developed for this project (those whose technical name starts with ``a113e_``).

When you navigate to the *Apps* menu, the "A113e" filter is applied by default, giving you an immediate view of the project's custom applications.

This behavior is completely non-destructive and reversible:

* The standard Odoo filters (Apps, Extra, Installed, Not Installed, etc.) remain fully functional. You can remove the "A113e" filter or combine it with others using the search bar.
* If this module is uninstalled, the menu reverts to its standard Odoo behavior with no side effects or broken links.

**Fevexpo Color Palette**

This module provides two color palettes for the ``eq_ownerp_ui`` theme:

* **A113e** (light variant): A light theme based on the corporate A113e colors (teal navigation, orange primary buttons, white backgrounds).
* **A113e (Dark)**: A dark variant with a deep blue-green background, designed for low-light environments.

Both palettes are defined as records of the ``eq.colors`` model and are available in the theme color selector. The light variant is linked to its dark counterpart through the ``eq_dark_variant_id`` field, so switching between light and dark modes is seamless.

**Automatic Application on Install**

When the module is installed for the first time, a ``post_init_hook`` automatically applies the **A113e** palette as the active theme. This means you do not need to manually select it from the theme selector after installation.

If the template cannot be applied for any reason (for example, if the ``eq_ownerp_ui`` module is not yet fully initialized), the hook logs a warning and the module installation completes without errors. You can then apply the palette manually from the theme selector.

.. note::

   The ``post_init_hook`` only runs on the **first installation** of the module. If you update the module later (``-u a113e_web``), the hook will not run again. To reapply the palette after an update, use the theme color selector manually.

**Developer Mode Database Badge**

In developer mode, Odoo displays the current database name in the top navigation bar. This module adds a custom style to that badge, making it more visible with the A113e blue background and a light font color. This is purely cosmetic and helps developers quickly identify which database they are working on.
