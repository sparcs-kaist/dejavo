"""
Django settings for dejavo project.

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
SECRET_KEY = 's-v&47@$6*nses7+%o^avcdi2*xo4g^&g2e8=u#cs773+6+kpt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'account.ZaboUser'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'social.apps.django_app.default',
    'sorl.thumbnail',

    'dejavo.apps.account',
    'dejavo.apps.manage',
    'dejavo.apps.zabo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'accept_checker.middleware.ContentNegotiator',
    'jwt_auth.middleware.JWTAuthMiddleware',
)

ROOT_URLCONF = 'dejavo.urls'

WSGI_APPLICATION = 'dejavo.wsgi.application'


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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = BASE_DIR + 'static'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    BASE_DIR + '/template/',
)

ACCEPT_CHECKER = {
    'ACCEPT_FORMAT' : (
        ('application/json', 'json'),
        ('text/html', 'html'),
        ('*/*', 'wildcard'),
    )
}

SITE_ID = 1

LOGIN_URL = '/login/'

# Python Social Auth
SOCIAL_AUTH_FACEBOOK_KEY = '' # facebook app id
SOCIAL_AUTH_FACEBOOK_SECRET = '' # facebook app secret

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'dejavo.apps.account.pipeline.check_fields',
    'social.pipeline.user.create_user',
    'dejavo.apps.account.pipeline.activate_new_user',
    'dejavo.apps.account.pipeline.save_profile_picture',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_USER_FIELDS = ['email']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']

# Django registration
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'


# Thumbnail
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_DB = 1
THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_UPSCALE = False

try:
    from local_settings import *
except ImportError:
    pass
