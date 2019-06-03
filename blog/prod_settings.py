import os
from blog.settings import *

# override for settings.py

DEBUG = False

SECRET_KEY = 'who cares I dont use any feautes that need one'

ALLOWED_HOSTS = ['sha.wn.zone', 'localhost', '127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Cache for 24 hours
CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 24
