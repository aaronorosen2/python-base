"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z@g8x(zh990d)ti@6)^a7ng2=t21_)dkwfs4n50d#(v@dy@f=r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SLACK_API_KEY = "xoxb-790630255906-1844871421842-FFFWwP6KQT2eIsjTBHA8fsUR"

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                        'class': 'logging.StreamHandler',
                    },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(os.getcwd(), 'logger.log'),
                'formatter': 'verbose'
            },
            'slack-error': {
                'level': 'ERROR',
                'api_key': SLACK_API_KEY,
                'class': 'slacker_log_handler.SlackerLogHandler',
                'channel': '#debug'
            },
            'slack-info': {
                'level': 'ERROR',
                'api_key': SLACK_API_KEY,
                'class': 'slacker_log_handler.SlackerLogHandler',
                'channel': '#debug'
            },
        },
        'root': {
                'handlers': ['console', 'file',  'slack-error', "slack-info"],
                'level': 'INFO',
            },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',
    'django_rest_passwordreset',
    'sfapp',
    'sfapp2',
    'storages',
    'corsheaders',
    'admin_backend',
    'voip',
    'courses',
    'video',
    'channels',
    'notifications',
    'courses_api',
    'pdf_sign',
    'store',
    'bookbikerescue',
    'form_lead.apps.FormLeadConfig',
    # added by dextersol
    'calendar_app',
    'manifest_app',
    's3_uploader',
    'parking',
    'signature',
    'dreamreader',
    'neighbormade',
    'classroom',
    'vconf',
    'audition',
    'facets',
    'rest_framework_swagger',
    'messaging',
    #stripe
    'store_stripe',
    'bookingstadium.apps.BookingstadiumConfig',
    'bookingsystem.apps.BookingsystemConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Braintree Settings

if DEBUG:
    # test keys
    BT_ENVIRONMENT = 'sandbox'
    BT_MERCHANT_ID = '26343xxtxwwwgfqs'
    BT_PUBLIC_KEY = 'nj723gtbqz2s6229'
    BT_PRIVATE_KEY = '6998bfeb28304c9b97c59460791f84ed'
    # stripe
    # STRIPE_SECRET_KEY = 'sk_test_51ITdUjGOkE0UauzQJwYtyRsqkRYL1M77Fn6QppwqhacQvdLCJOGyc2TdJAhcm8o1tpXgN3Owor4RvAFYGfavG9h6000tqQCYWF'
    # STRIPE_PUBLISHABLE_KEY = 'pk_test_51ITdUjGOkE0UauzQPEu8J9aFw5RmWOVXwkY3NRIXwvnzDMFo3C5pDwfuYmiSLHNhr6o6lzvBF0552ODdE45BbIch00QTrejIEN'
    STRIPE_TEST_PUBLISHABLE_KEY = 'pk_test_x97eNoQQtQDTurBY7lrq1yME005Ntt2hOK'
    STRIPE_TEST_SECRET_KEY = 'sk_test_51GPZU2Gq4mM9DwWGVtsyD1imIC3xNNEfNqYzGuWryfWT8ok25STRDnb4XORmCOv2sqDOYhKRbdowt1SAhjmGyFYT00kNM75J9r'
    STRIPE_LIVE_MODE = False  # Change to True in production
    
else:
    # live keys
    BT_ENVIRONMENT = 'production'
    BT_MERCHANT_ID = '7xyb7rtshbp9q47d'
    BT_PUBLIC_KEY = 'yc3ytr786brjsh9v'
    BT_PRIVATE_KEY = '532eefa88f4f82bce0f12e2ef0adba87'
    # stripe
    STRIPE_SECRET_KEY = ''
    STRIPE_PUBLISHABLE_KEY = ''
    STRIPE_LIVE_MODE = True

ROOT_URLCONF = 'web.urls'

TWILIO = {
    'TWILIO_ACCOUNT_SID': 'AC8c34b4a961b611a3606f55a0e182ad72',
    'TWILIO_AUTH_TOKEN': '7287d6460e997c4c8dfc196fe622fee0',
#    'TWILIO_NUMBER': '(510) 288-5469',
    'TWILIO_NUMBER': '(425) 578-5798',
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAYMPAXPYXGBUSLCO6'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'sfappv2'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  
                    'staticfiles': 'django.templatetags.static',
                    },
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

ASGI_APPLICATION = 'web.routing.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'python-base-restore-dev.cb7bl0nt7fvo.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
        'PASSWORD': 'EhB4bINnDFmzI0Bg'
    }
}
# testing
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'PASSWORD': 'Digitallab'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Make knox’s Token Authentication default
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# KNOX
REST_KNOX = {
  'USER_SERIALIZER': 's3_uploader.serializers.UserSerializer',
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'check_user_connectivity': {
        'task': 'web.celery.check_user_connectivity',
        'schedule': timedelta(minutes=10)
    }
    # 'schedule_member': {
    #     'task': 'web.celery.schedule_member',
    #     'schedule': timedelta(minutes=50)  # execute every minute
    # },
    # 'room_details': {
    #     'task': 'web.celery.room_details',
    #     'schedule': timedelta(minutes=1)  # execute every seconds
    # },
    # 'send_wait_notification_customer': {
    #     'task': 'web.celery.send_wait_notification_customer',
    #     'schedule': timedelta(seconds=1)  # execute every seconds
    # }
}


# CORS
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS=['*']

# Email
EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAIHFAW4CMLKGZJWQQ'
# AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FROM_EMAIL = 'mail-api@dreampotential.org'

# Instead of sending out real emails the console backend just writes the emails that would be sent to the standard
# output. PLEASE REMOVE FOLLOWING LINE TO SEND REAL EMAILS

APPEND_SLASH=False
