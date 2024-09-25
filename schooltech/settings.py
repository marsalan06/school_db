"""
Django settings for schooltech project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import json
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nlkh$7bp%&*28oq9!l&&4udd-dg+ix-p%7=@0ew-2j119uem6h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
allowed_hosts_file = os.path.join(BASE_DIR, 'allowed_hosts.json')


# Load allowed hosts from JSON file
def load_allowed_hosts():
    with open(allowed_hosts_file) as f:
        data = json.load(f)
    return data.get('allowed_hosts', [])


ALLOWED_HOSTS = load_allowed_hosts()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'colorfield',
    'captcha',
    'school',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'school.middleware.HostRestrictMiddleware',  # Place custom middleware here
    'django.middleware.common.CommonMiddleware',
    'school.middleware.SchoolDomainMiddleware',  # Custom middleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'schooltech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'schooltech.wsgi.application'

SITE_ID = 1  # This is the default site ID

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config(
            "DB_HOST", default="postgres_db_school"
        ),  # Docker Compose service name for PostgreSQL
        "PORT": config("DB_PORT", default="5432"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': config('LOCAL_DB_NAME'),
#             'USER': config('LOCAL_DB_USER'),
#             'PASSWORD': config('LOCAL_DB_PASSWORD'),
#             'HOST': config('LOCAL_DB_HOST'),
#             'PORT': '3306',
#         }
#     }

# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': config('PROD_DB_NAME'),
#             'USER': config('PROD_DB_USER'),
#             'PASSWORD': config('PROD_DB_PASSWORD'),
#             'HOST': config('PROD_DB_HOST'),
#             'PORT': '3306',  # Default MySQL port
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')


AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # Disable default ACL to prevent "Permission Denied" errors


# Static and Media files
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

REMOTE_SERVER = config('REMOTE_SERVER', default=False, cast=bool)

# Common settings for both development and production
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory for static files (CSS, JS, images)
# Only static files, no media
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]

if REMOTE_SERVER:
    # Production (S3)
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    # # Use S3 for static and media files
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'schooltech.boto_conf.StaticStorage'
    DEFAULT_FILE_STORAGE = 'schooltech.boto_conf.MediaStorage'
    # Static files will be stored in the 'static-assets/' folder within your S3 bucket
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static-assets/'

    # Media files will be stored in the 'media-files/' folder within your S3 bucket
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media-files/'

else:
    # Development (local storage)
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    # Directory where Django will collect static files in development
    # Where collected static files go
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # Directory for uploaded media files in development
    # Where media files are uploaded locally
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LMS_SERVER_URL = config('LMS_SERVER_URL')
LMS_EXTERNAL_URL = config('LMS_EXTERNAL_URL')
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
GOOGLE_MAPS_MAP_ID = config('GOOGLE_MAPS_MAP_ID')
