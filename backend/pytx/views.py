from string import Template

from django import http
from django.views import static
from django.conf import settings
from django.template.loader import render_to_string

from release import release

def favicon (request):
  return static.serve(request, 'favicon.ico', settings.FRONT_ROOT)
  
def default_conf (request):
  return http.HttpResponseRedirect(settings.DEFAULT_CONF + '/')
  
def index (request, conf_slug):
  conf_slug = conf_slug.split('/')[0]
  template = render_to_string('prebuild-index.html', {})
  
  context = dict(
    base='/{}/app-{}'.format(conf_slug, release()),
    conf=conf_slug,
    api_base='/',
  )
  html = Template(template).safe_substitute(context)
  
  return http.HttpResponse(html)
  