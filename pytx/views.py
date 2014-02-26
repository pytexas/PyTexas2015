from django import http
from django.conf import settings

def favicon (request):
  return http.HttpResponseRedirect(settings.STATIC_URL + 'favicon.ico')
  