"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from django.conf import settings
from datetime import timedelta
import django_heroku
import cloudinary
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gf5l5bzo29@sn5!81-6mgut+a33m-$z2^-3a2&(6=*@w!s34^x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://www.hagiakinh.xyz",
    "https://www.hagiakinh.me",
    "https://hagiakinh.xyz",
    "https://hagiakinh.me",
    "https://api.hagiakinh.xyz",
    "https://api.hagiakinh.me",
    "https://giakinh-blog.herokuapp.com",
]

CORS_ORIGIN_ALLOW_ALL = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'cloudinary',
    'channels',
    'chatterbot.ext.django_chatterbot',
    'django_celery_results',
    'django_celery_beat',
    'blog',
    'register',
    'chatbot',
]


# chatbot

import logging

def get_most_frequent_response(input_statement, response_list, storage=None):
    """
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement

    :param response_list: A list of statement options to choose a response from.
    :type response_list: list

    :param storage: An instance of a storage adapter to allow the response selection
                    method to access other statements if needed.
    :type storage: StorageAdapter

    :return: The response statement with the greatest number of occurrences.
    :rtype: Statement
    """
    matching_response = None
    occurrence_count = -1

    logger = logging.getLogger(__name__)
    logger.info('Selecting response with greatest number of occurrences.')

    for statement in response_list:
        count = len(list(storage.filter(
            text=statement.text,
            in_response_to=input_statement.text)
        ))

        # Keep the more common statement
        if count >= occurrence_count:
            matching_response = statement
            occurrence_count = count

    # Choose the most commonly occuring matching response
    return matching_response


CHATTERBOT = {
    'name': 'Giakinh',
    'storage_adapter': 'chatterbot.storage.SQLStorageAdapter',
    'logic_adapters': [
        'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
    ],
    'preprocessors': [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    'database_uri': 'sqlite:///db.sqlite3',
    'response_selection_method': get_most_frequent_response,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = "backend.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # "hosts": [('redis', 6379)],
            "hosts": [os.environ.get('REDIS_URL', 'redis://redis:6379')],
            # "hosts": ["redis://:p769ceb4142f3c372a0b6726f6eb50149da7c3326a1b89c025ba486b86c8da704@ec2-54-204-185-228.compute-1.amazonaws.com:25019"],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 500,
    }
}

import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'blog',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'Blog',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': 'mongodb+srv://giakinh0823:Giakinh0823@blog.nahnk.mongodb.net/blog?retryWrites=true&w=majority'
#         }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_FRAMEWORK API
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
}


# JWT


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=5),
}


# cloudinary
CLOUDINARY_URL = "cloudinary://551591186755475:vrlhMJgkLm21pw-qAxyqBf-JfoQ@giakinh0823"

cloudinary.config(
    cloud_name="giakinh0823",
    api_key="551591186755475",
    api_secret="vrlhMJgkLm21pw-qAxyqBf-JfoQ",
    secure=True
)

django_heroku.settings(locals())


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# celery
REDIS_HOST = 'redis'
REDIS_PORT = '6379'

# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0')
CELERY_BACKEND_URL = os.environ.get("REDIS_URL",  'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/1')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"
CELERY_ENABLE_UTC = True

CELERY_REDBEAT_REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/1"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'