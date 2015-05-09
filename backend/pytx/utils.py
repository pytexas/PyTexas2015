import re
from string import Template

from django.conf import settings
from django.template.loader import render_to_string

from release import release

def index_generator (conf_slug=settings.DEFAULT_CONF, dev=False):
  template = render_to_string('prebuild-index.html', {})
  
  context = dict(
    base='/{}/app-{}'.format(conf_slug, release()),
    conf=conf_slug,
    api_base='/',
    release=release(),
  )
  
  html = Template(template).safe_substitute(context)
  pattern = '<!--dev-->(.*?)<!--dev-end-->'
  if dev:
    pattern = '<!--prod-->(.*?)<!--prod-end-->'
    
  html = re.sub(pattern, '', html, flags=re.S)
  return html
  