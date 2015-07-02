import os
import subprocess

from django import http
from django.views import static
from django.conf import settings

from pytx.utils import index_generator

def favicon (request):
  return static.serve(request, 'favicon.ico', settings.FRONT_ROOT)
  
def default_conf (request):
  return http.HttpResponseRedirect(settings.DEFAULT_CONF + '/')
  
def index (request, conf_slug):
  conf_slug = conf_slug.split('/')[0]
  
  html = index_generator(conf_slug, dev=True)
  return http.HttpResponse(html)
  
def less_view (request):
  less = os.path.join(settings.BASE_DIR, '..', 'frontend', 'css', 'pytx.less')
  pipe = subprocess.Popen(
    "lessc {}".format(less), shell=True, stdout=subprocess.PIPE)
  
  return http.HttpResponse(pipe.stdout, content_type="text/css")
  
def frontend (request, *args, **kwargs):
  return http.HttpResponse(
    "Front-End Should Serve This URL", content_type="text/plain")
    