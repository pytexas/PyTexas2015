from django.conf import settings

def global_vars (request):
  context = {
    'DEV': settings.DEBUG,
    'SITE_INFO': settings.SITE_INFO,
  }
  
  return context
  