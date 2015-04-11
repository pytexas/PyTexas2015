from django.views import static
from django.conf import settings

def favicon (request):
  return static.serve(request, 'favicon.ico', settings.FRONT_ROOT)
  