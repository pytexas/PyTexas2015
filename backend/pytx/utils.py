import re
from string import Template

from django.conf import settings
from django.template.loader import render_to_string

from release import release
from pytx.js import SCRIPTS

def index_generator (conf_slug=settings.DEFAULT_CONF, dev=False):
  template = render_to_string('prebuild-index.html', {})
  
  base = '/{}/app-{}'.format(conf_slug, release())
  
  if dev:
    scripts = ''
    for script in SCRIPTS:
      scripts += '<script src="{}/{}"></script>\n'.format(base, script)
      
  else:
    scripts = '<script src="{}/compressed.js"></script>'.format(base)
    
  context = dict(
    base=base,
    conf=conf_slug,
    api_base='/',
    release=release(),
    app_base='app-{}'.format(release()),
    scripts=scripts,
  )
  
  html = Template(template).safe_substitute(context)
  pattern = '<!--dev-->(.*?)<!--dev-end-->'
  if dev:
    pattern = '<!--prod-->(.*?)<!--prod-end-->'
    
  html = re.sub(pattern, '', html, flags=re.S)
  return html
  