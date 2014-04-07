"""
WSGI config for pytx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pytx.settings")

base_dir = os.path.dirname(__file__)
ts = os.path.join(base_dir, '..', 'TwoSpaces')
sys.path.append(ts)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
