from django.conf import settings

def render_tpl (tpl, context):
  template = settings.TPL_ENV.get_template(tpl)
  return template.render(**context)
  