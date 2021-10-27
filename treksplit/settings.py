"""
Django settings for treksplit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, environ
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Setup environ
env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# ADMIN_ENABLED = False
ADMINS = ('Jason', 'treksplit@gmail.com')
MANAGERS = ('Jason', 'treksplit@gmail.com')

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587

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

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
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
        'NAME': env('DATABASE_NAME'),                      # Or path to database file if using sqlite3.
        'USER': env('DATABASE_USER'),                      # Not used with sqlite3.
        'PASSWORD': env('DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': env('DATABASE_HOST'),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CON_MAX_AGE = 60

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = 'media'

# AUTHENTICATION_BACKENDS = ('group_backend')
# LOGIN_URL = '/passcode/'
# AUTH_USER_MODEL = 'splitter.Group'


# BELOW ADDED FROM HEROKU GUIDE
# Parse database configuration from $DATABASE_URL
import dj_database_url
# DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['.treksplit.com', 'localhost']

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
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_DIR, '../templates/')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]
    },
    
}]


