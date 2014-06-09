"""
Django settings for pytx project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.pytexas.org', 'pytexas.org']


# Application definition

INSTALLED_APPS = [
  'south',
  'grappelli',
  'sorl.thumbnail',
  
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.sites',
  
  #'pulsar.apps.pulse',
  
  'pytx',
  'pizza.kitchen_sink',
  #'pizza.blog',
  #'pizza.calendar',
  
  'twospaces.conference',
  'twospaces.profiles',
  
  'django_markdown',
  'django_gravatar',
]

MIDDLEWARE_CLASSES = [
  'pytx.middleware.WWWMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'pizza.middleware.Siteware',
  'pizza.middleware.RememberAdminQuery',
  'twospaces.conference.middleware.ConferenceMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.core.context_processors.tz",
  "django.contrib.messages.context_processors.messages",
  "django.core.context_processors.request",
  "pytx.context.global_vars",
  "twospaces.conference.context.sponsors",
)

ROOT_URLCONF = 'pytx.urls'

WSGI_APPLICATION = 'pytx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE':'django.db.backends.postgresql_psycopg2',
    'NAME': 'pytexasweb',
    'USER': 'postgres',
    'HOST': 'db.internal',
    'PORT': '5432',
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
SITE_NAME = 'PyTexas'

CSRF_COOKIE_DOMAIN = '.pytexas.org'
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = '.pytexas.org'
SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/var/www/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/var/www/static/uploads/'
MEDIA_URL = '/static/uploads/'

AUTH_USER_MODEL = 'profiles.User'

GRAPPELLI_ADMIN_TITLE = 'PyTexas Admin'

THUMBNAIL_PRESERVE_FORMAT = True

DEFAULT_FROM_EMAIL = 'conference@pytexas.org'

TWOSPACES_SPEAKER_NOTIFY = (
  'conference@pytexas.org',
)

TWOSPACES_SPONSOR_NOTIFY = (
  'conference@pytexas.org',
)

MARKDOWN_EXTENSIONS = ['extra']

PIZZA_CACHE_TIMEOUT = 0

from .templates import *
from .local import *

import sys
import socket

machine = socket.gethostname().split('.')[0]

try:
  istr = 'pytx.settings.' + machine
  tmp = __import__(istr)
  mod = sys.modules[istr]
  
except ImportError:
  print 'No settings module for %s' % machine
  
else:
  print 'Importing settings for %s' % machine
  for setting in dir(mod):
    if setting == setting.upper():
      setattr(sys.modules[__name__], setting, getattr(mod, setting))
      