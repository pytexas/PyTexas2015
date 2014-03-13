from django.conf import settings

def global_vars (request):
  context = {
    'DEV': settings.DEBUG,
  }
  
  return context
  