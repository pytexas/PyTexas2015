import os

from pytx.settings import BASE_DIR, INSTALLED_APPS, MIDDLEWARE_CLASSES

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.insert(0, 'devserver')

MIDDLEWARE_CLASSES.insert(0, 'devserver.middleware.DevServerMiddleware')

DEVSERVER_MODULES = (
  #'devserver.modules.sql.SQLRealTimeModule',
  #'devserver.modules.sql.SQLSummaryModule',
  'devserver.modules.profile.ProfileSummaryModule',
  
  # Modules not enabled by default
  #'devserver.modules.ajax.AjaxDumpModule',
  #'devserver.modules.profile.MemoryUseModule',
  #'devserver.modules.cache.CacheSummaryModule',
  #'devserver.modules.profile.LineProfilerModule',
)
