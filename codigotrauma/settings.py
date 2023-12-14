"""
Django settings for codigotrauma project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# =======================================================
# =============== CONFIGURACION PRINCIPAL ===============
# =======================================================


Configuracion: dict = None

try:
    with open(MAIN_PATH + './root/config.json', 'r') as Configuracion:
        Configuracion = json.load(Configuracion)
except FileNotFoundError:
    print("-> No se ha encontrado el archivo de configuracion")

    exit()

DOMAIN_NAME = Configuracion["DOMAIN_NAME"]
DOMAIN_SHORTNAME = Configuracion["DOMAIN_SHORTNAME"]

DB_IP = Configuracion["backend"]["DB_IP"]
DB_PORT = Configuracion["backend"]["DB_PORT"]

API_CONFIG = Configuracion["API"]


# =======================================================
# ========== FIN DE LA CONFIGURACION PRINCIPAL ==========
# =======================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-eznd3=eh3-xr2u-r-!4n@)i@f#lg-&5ekr1d=ba+=mfo1&fewb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Configuracion["backend"]["modoDebug"]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'codigotrauma',
    'principal',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codigotrauma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [MAIN_PATH + './templates', os.path.join(BASE_DIR, 'templates/html_templates')],
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


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]



WSGI_APPLICATION = 'codigotrauma.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = Configuracion["backend"]["LANGUAGE_CODE"]

TIME_ZONE = Configuracion["backend"]["TIME_ZONE"]

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/img/'

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/templates/assets/'

STATICFILES_DIRS = (
    BASE_DIR / 'templates/assets',
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
