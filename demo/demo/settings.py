"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hk&0ex(yls%7f%nh^@*^$&a!z3x+1%nw#&h%3@q=mfgn+zoc&c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'formidable',
    'rest_framework',
    'demo',
    'demo.builder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if django.VERSION[:2] == (1, 8):
    engine = 'django18_sqlite3_backend'
else:
    engine = 'django.db.backends.sqlite3',

DATABASES = {
    'default': {
        'ENGINE': engine,
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FORMIDABLE_ACCESS_RIGHTS_LOADER = 'demo.formidable_accesses.get_accesses'
FORMIDABLE_CONTEXT_LOADER = 'demo.formidable_accesses.get_context'
FORMIDABLE_DEFAULT_PERMISSION = ['rest_framework.permissions.AllowAny']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "var"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CORS_ORIGIN_ALLOW_ALL = True


# Formidable call back post-create/update
FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS = 'demo.callback_success_message'
FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS = 'demo.callback_success_message'
FORMIDABLE_POST_CREATE_CALLBACK_FAIL = 'demo.callback_fail_message'
FORMIDABLE_POST_UPDATE_CALLBACK_FAIL = 'demo.callback_fail_message'


# django-perf-rec settings
PERF_REC = {
    'MODE': 'all'
}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, '..', 'formidable', 'locale')
]
