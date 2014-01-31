"""
Django settings for treksplit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_wv6w-1!j@)se6)r12ygb@x_j=!!$stocd80w&uiq7iz6$e##c'

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
    'splitter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'treksplit.urls'

WSGI_APPLICATION = 'treksplit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # # local server
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    #     'NAME': 'meow',                      # Or path to database file if using sqlite3.
    #     'USER': 'postgres',                      # Not used with sqlite3.
    #     'PASSWORD': 'betterweather',                  # Not used with sqlite3.
    #     'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    #     'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    # }
    # gold database on heroku
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd116sk88i3pfev',                      # Or path to database file if using sqlite3.
        'USER': 'ojxpubpdbnpvhm',                      # Not used with sqlite3.
        'PASSWORD': 'w8qFxXwjVq-6hIC0kyRsaNQulS',                  # Not used with sqlite3.
        'HOST': 'ec2-54-204-43-138.compute-1.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = 'media'


# BELOW ADDED FROM HEROKU GUIDE
# Parse database configuration from $DATABASE_URL
import dj_database_url
# DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
# PROJECT_DIR = os.path.dirname(__file__)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = '/Users/j/Dropbox/treksplit_mac/'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, '/static/'),
# )

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, '../static/'),
)

PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # "/Users/j/Dropbox/treksplit_mac/templates/"
    # "C:/Users/Jason/Dropbox/pyWeather/templates"
    os.path.join(PROJECT_DIR, "../templates/"),
)
