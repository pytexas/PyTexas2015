import os

from pytx.settings import BASE_DIR

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
