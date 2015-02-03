"""
Django settings for ctf_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def try_create_personalsettings():
    print("Trying to create personalsettings...")
    if os.path.exists(os.path.join(BASE_DIR, 'ctf_server/personalsettings.py')):
        return
    try:
        f = open(os.path.join(BASE_DIR, 'ctf_server/personalsettings.py'), 'w')
        f.write("# Do not include this file in version control\n\n")
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret = get_random_string(50, chars)
        f.write("SECRET_KEY = '{s}'\n".format(s=secret))
        f.close()
        print("Created")
    except IOError:
        return


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.utils.crypto import get_random_string
try:
    from ctf_server import personalsettings
except ImportError:
    try_create_personalsettings()
    from ctf_server import personalsettings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = personalsettings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'challenges',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ctf_server.urls'

WSGI_APPLICATION = 'ctf_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'


