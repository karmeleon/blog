import os
from blog.settings import *

# override for settings.py

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['sha.wn.zone']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Cache for 24 hours
CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 24
