"""
Django settings for page project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'byj&*)ke@eh$h%yufjisihfp&nuwowqa*%x=a6cp_(tq=4$0by'

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
    'tasks',
    'submit',
    'ksp_login',
    'social.apps.django_app.default',
    'about',
    'django_extensions',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'page.urls'

WSGI_APPLICATION = 'page.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   #'default': {
       #'ENGINE': 'django.db.backends.sqlite3',
       #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   #}
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'liahen-maru',
       'USER': 'maru',
   }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'sk'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_out')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

LOGIN_REDIRECT_URL = '/tasks'
LOGIN_URL = '/account/login/'

AUTHENTICATION_BACKENDS = (
#    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOpenId',
    'social.backends.github.GithubOAuth2',
    'ksp_login.backends.LaunchpadAuth',
    'social.backends.open_id.OpenIdAuth',
    'django.contrib.auth.backends.ModelBackend',
)

AUTHENTICATION_PROVIDERS_BRIEF = 5

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'ksp_login.pipeline.register_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
