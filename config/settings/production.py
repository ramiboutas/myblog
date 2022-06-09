import os
from .base import *


DEBUG = os.environ.get('DJANGO_DEBUG') == '1'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


ALLOWED_HOSTS = ['ramiboutas.com', 'www.ramiboutas.com', '207.154.205.99', 'localhost', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
INTERNAL_IPS = ('127.0.0.1')

INSTALLED_APPS += [
    'storages',
]

# Storage

USE_SPACES = os.environ.get('USE_SPACES') == '1'

if USE_SPACES:

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = 'https://spaces.ramiboutas.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', 'ACL': 'public-read'}
    # AWS_LOCATION = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com'

    AWS_DEFAULT_ACL = 'public-read'

    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaRootStorage'
    STATICFILES_STORAGE = 'config.storage_backends.StaticRootStorage'

    AWS_STATIC_LOCATION = 'myblog-static'
    # STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_STATIC_LOCATION}/'
    STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    STATIC_ROOT = f'{AWS_STATIC_LOCATION}/'

    AWS_MEDIA_LOCATION = 'myblog-media'
    # MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com/{AWS_MEDIA_LOCATION}/' # it worked
    # MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_LOCATION}/'
    MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
    MEDIA_ROOT = f'{AWS_MEDIA_LOCATION}/'



else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


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
SECURE_HSTS_SECONDS = 3600 # usual: 31536000 (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
# PREPEND_WWW = True


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
