from pathlib import Path
from datetime import timedelta
import os
import mimetypes
from pickle import TRUE
import environ
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

mimetypes.add_type("application/javascript", ".js", True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = str(env('DEBUG'))=='1'
SECRET_KEY = env('DJANGO_SECRET_KEY') or 'django-insecure-*1(z_n=g0=47qpkkd&t31+@$h$fxlms^%b#1=%o^op2qvkb592'

ENV_ALLOWED_HOST = env('DJANGO_ALLOWED_HOST') or None
ALLOWED_HOSTS =  ['african3.herokuapp.com', 'african3.com',]
if ENV_ALLOWED_HOST is not None:
    ALLOWED_HOSTS = [ ENV_ALLOWED_HOST ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'storages',
    'rest_framework_simplejwt.token_blacklist',

    'users',
    'words',
    'projects',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'build'],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'build/static'
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# ...STATIC and MEDIA settings here...

# The following configs determine if files get served from the server or an S3 storage
S3_ENABLED=str(env('S3_ENABLED'))=='1'
LOCAL_SERVE_MEDIA_FILES=str(env('LOCAL_SERVE_MEDIA_FILES'))=='1'
LOCAL_SERVE_STATIC_FILES=str(env('LOCAL_SERVE_STATIC_FILES'))=='1'

if (not LOCAL_SERVE_MEDIA_FILES or not LOCAL_SERVE_STATIC_FILES) and not S3_ENABLED:
    raise ValueError('S3_ENABLED must be true if either media or static files are not served locally')

if S3_ENABLED:
    AWS_ACCESS_KEY_ID = env('BUCKETEER_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('BUCKETEER_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('BUCKETEER_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('BUCKETEER_AWS_REGION')
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = env('S3_SIGNATURE_VERSION', default='s3v4')
    AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

if not LOCAL_SERVE_STATIC_FILES:
    STATIC_DEFAULT_ACL = 'public-read'
    STATIC_LOCATION = 'static'
    STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'backend.storage_backends.StaticStorage'

if not LOCAL_SERVE_MEDIA_FILES:
    PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
    PUBLIC_MEDIA_LOCATION = 'media/public'

    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'backend.storage_backends.PublicMediaStorage'

    PRIVATE_MEDIA_DEFAULT_ACL = 'private'
    PRIVATE_MEDIA_LOCATION = 'media/private'
    PRIVATE_FILE_STORAGE = 'backend.storage_backends.PrivateMediaStorage'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'game': '2/day'
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer','JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Twitter Authentication details
CONSUMERKEY = env("CONSUMERKEY")
CONSUMERSECRET = env("CONSUMERSECRET")
ACCESSTOKEN = env("ACCESSTOKEN")
ACCESSTOKENSECRET = env("ACCESSTOKENSECRET")


# Telegram
TELEGRAM = {
    'bot_token': env('NEOTRIVIA_BOT'),
    'channel_name': 'NeoTriviaAnnouncements',
}

if not DEBUG:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)
    DATABASES['default']['CONN_MAX_AGE'] = 600
    CORS_ALLOWED_ORIGINS = [
    "https://african3.herokuapp.com",
    "https://african3.com/",
]


django_heroku.settings(locals())

options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)