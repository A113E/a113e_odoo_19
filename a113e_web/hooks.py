import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    try:
        template = env.ref("a113e_web.a113e", raise_if_not_found=True)
        env["eq.template.colors"].api_apply_template(template.id)
        _logger.info("A113E template applied correctly.")
    except Exception as e:
        _logger.warning("The A113E template could not be applied.: %s", e)
