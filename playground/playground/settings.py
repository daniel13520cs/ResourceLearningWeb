"""
Django settings for playground project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from pymongo import MongoClient
import urllib
from mongoengine import connect


username = 'daniel13520cs'
password = 'nlmIVD8svGikrjtG'

# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)
connection_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@playground.lskld.mongodb.net/Playground?retryWrites=true&w=majority"
# Establish a connection to the MongoDB database
connect(host=connection_uri)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*ndgs@-a8n)m^h31s^nk1_zo8=4wi(ud3%5d)%2bsek@ibcnfg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://chihchienhsiao.azurewebsites.net',  # Add your Azure URL with https
    'https://chihchiendjangotodo.azurewebsites.net',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'django_mongoengine.mongo_admin',
    'todos.apps.todosConfig',
    'polls.apps.PollsConfig',
    'event.apps.EventConfig',
    'debug_toolbar',
    'playground',
]


LOGIN_URL = 'login'  # URL to redirect to for login
SESSION_COOKIE_AGE = 3600  # 1 hr

# If you want sessions to expire when the browser is closed, set this to True:
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Keep users logged in after closing the browser
USER_APPS = [
    'todos',
    'polls',
    'event',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'playground.middleware.LogIPMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'playground.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
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

STATICFILES_DIRS = [
    "polls/static",
    "todos/static",
]
WSGI_APPLICATION = 'playground.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'Playground',  # The name of your MongoDB database
    #     'CLIENT': {
    #         'host': f"mongodb+srv://{escaped_username}:{escaped_password}@playground.lskld.mongodb.net/sample_mflix",
    #         'username': escaped_username,
    #         'password': escaped_password,
    #         'authMechanism': 'SCRAM-SHA-1',  # Or SCRAM-SHA-256 depending on your MongoDB setup
    #     }
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
