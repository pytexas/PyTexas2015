from django.conf import settings
from django import http

class WWWMiddleware (object):
  def process_request (self, request):
    if not settings.DEBUG:
      if not request.get_host().startswith('www') or not request.is_secure():
        url = 'https://www.pytexas.org' + request.get_full_path()
        return http.HttpResponseRedirect(url)
        