
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = #email
EMAIL_HOST_PASSWORD=#pass
EMAIL_USE_TLS = True
EMAIL_PORT = #port

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

AUTH_USER_MODEL = 'accounts.MyUser'



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'accounts',
    'home',
    'profiles',
    'comments',
    'clubs',
    'schedule',
    'teams',
    'team_schedule',
    'frats',
    'frat_schedule',
    'direct_messages',
    'marketplace',
    'course',
    'local',
    'main_schedule',
    'notifications'
    
    
)

MIDDLEWARE_CLASSES = (
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'grounds.urls'


WSGI_APPLICATION = 'grounds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'static', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                ],
            },
        },
    ]


PROTECTED_UPLOADS = os.path.join(BASE_DIR, 'media', 'protected')
STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
    
    
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static-only')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static', 'static'),
)



ACCOUNT_ACTIVATION_DAYS = 7

CRISPY_TEMPLATE_PACK = 'bootstrap3'


