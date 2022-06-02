'''
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'flex',
    'subscribers',
    'blog',
    'menus',
    'contact',
    'wagtail_localize',
    'wagtail_localize.locales',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2',


    'django_extensions',
    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'captcha',
    'wagtailcaptcha',
    'wagtailmarkdown',
    'wagtailcodeblock',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.categories',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# wagtail-localize
WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('de', 'German'),
]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = 'config'

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.search.backends.elasticsearch7',
#         'URLS': ['http://localhost:9200'],
#         'INDEX': 'wagtail',
#         'TIMEOUT': 5,
#         'OPTIONS': {},
#         'INDEX_SETTINGS': {},
#     }
# }


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

# Recaptcha
RECAPTCHA_PUBLIC_KEY = '6LfA4OkfAAAAAESQSzuJcbEPINStI16ILcVTa4fa'
RECAPTCHA_PRIVATE_KEY = '6LfA4OkfAAAAACCEjEIMrbvgjCq5eDNkw4QRchMn'
NOCAPTCHA = True


# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ['ramiboutas', 'elonmusk', 'god']
ACCOUNT_USERNAME_MIN_LENGTH = 3

# wagtailmarkdown

WAGTAILMARKDOWN = {
    # ...
    'extension_configs': {'pymdownx.arithmatex': {'generic': True}}
}

# wagtailcodeblock

# Themes:
# https://github.com/FlipperPA/wagtailcodeblock
# 'default' -> http://prismjs.com/index.html?theme=prism
# 'coy' -> http://prismjs.com/index.html?theme=prism-coy
# 'dark' -> http://prismjs.com/index.html?theme=prism-dark
# 'funky' -> http://prismjs.com/index.html?theme=prism-funky
# 'okaidia' -> http://prismjs.com/index.html?theme=prism-okaidia
# 'solarizedlight' -> http://prismjs.com/index.html?theme=prism-solarizedlight
# 'twilight' -> http://prismjs.com/index.html?theme=prism-twilight
WAGTAIL_CODE_BLOCK_THEME = 'okaidia'

# https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js

WAGTAIL_CODE_BLOCK_LINE_NUMBERS = True
WAGTAIL_CODE_BLOCK_COPY_TO_CLIPBOARD = True

WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('arduino', 'Arduino'),
    ('autoit', 'AutoIt'),
    ('bash', 'Bash + Shell'),
    ('batch', 'Batch'),
    ('css', 'CSS'),
    ('css-extras', 'CSS Extras'),
    ('django', 'Django/Jinja2'),
    ('git', 'Git'),
    ('javascript', 'JavaScript'),
    ('js-extras', 'JS Extras'),
    ('js-templates', 'JS Templates'),
    ('json', 'JSON'),
    ('latex', 'LaTeX'),
    ('lua', 'Lua'),
    ('makefile', 'Makefile'),
    ('markdown', 'Markdown'),
    ('markup', 'Markup + HTML + XML + SVG + MathML'),
    ('markup-templating', 'Markup templating'),
    ('matlab', 'MATLAB'),
    ('nginx', 'nginx'),
    ('powershell', 'PowerShell'),
    ('python', 'Python'),
    ('regex', 'Regex'),
    ('sql', 'SQL'),
    ('textile', 'Textile'),
    ('typescript', 'TypeScript'),
    ('vbnet', 'VB.Net'),
    ('visual-basic', 'Visual Basic'),
    ('wiki', 'Wiki markup'),
    ('wolfram', 'Wolfram Mathematica'),

)
