SECRET_KEY = 'super-secret-characters'

DEBUG = True

LOGGING = {
  'version': 1,
  'formatters': {
    'verbose': {
      'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'console': {
      'level': 'INFO',
      'class': 'logging.StreamHandler',
      'formatter': 'simple'
    },
  },
  'loggers': {
    'django': {
      'handlers': ['console'],
      'level': 'INFO',
      'propagate': True,
    },
  }
}

MEDIA_URL = '/uploads/'
MEDIA_ROOT = '../uploads/'

USE_X_FORWARDED_HOST = False
