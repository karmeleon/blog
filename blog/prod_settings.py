import os
from blog.settings import *

# override for settings.py

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['sha.wn.zone']
