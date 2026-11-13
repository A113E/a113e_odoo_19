{
    "name": "Web Settings",
    "version": "19.0.1.0.0",
    "category": "Hidden",
    "summary": "Global settings for the web environment",
    "author": "Alberto Adrián Mártir González",
    "license": "LGPL-3",
    "depends": [
        "base",
        "eq_ownerp_ui",
        "web_responsive",
    ],
    "data": [
        "views/ir_module_module_views.xml",
        "data/custom_web_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "a113e_web/static/src/css/debug_badge.css",
        ],
    },
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
