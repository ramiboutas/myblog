import os
from .base import *


DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


ALLOWED_HOSTS = ['ramiboutas.com', 'www.ramiboutas.com', '207.154.205.99', 'localhost', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


INTERNAL_IPS = ('127.0.0.1')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'TEST': {
         'NAME': os.environ.get('POSTGRES_TESTS_DB'),
         },
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000 # usual: 31536000 (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
PREPEND_WWW = True


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/home/rami/dev/playing-place/wagtail/config/cache',
#     }
# }

try:
    from .local import *
except ImportError:
    pass
