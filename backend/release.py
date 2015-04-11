import time

from django.conf import settings

def release ():
  try:
    from release_hash import RELEASE
    return RELEASE
    
  except ImportError:
    if settings.DEBUG:
      return str(time.time())
      
    else:
      raise
      