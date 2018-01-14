import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bo8m!zop)gqh$5vy8r342bbmoo3b_#znr7pjr3voxlcozc4c7h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'django_rq'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'app', 'templates'),

        ]
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')] +
        # [os.path.join(BASE_DIR, x, 'templates') for x in os.listdir(BASE_DIR)
        #     if os.path.exists(os.path.join(BASE_DIR, x, 'templates'))
        #     and os.path.isdir(os.path.join(BASE_DIR, x, 'templates'))]
        ,
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if 'IS_DOCKER_CONTAINER' in os.environ:
    # Running the Docker image
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_SERVICE'],
            'PORT': os.environ['POSTGRES_PORT']
        }
    }
else:
    # local start

    # DATABASES = {
    #     'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'default_db',
    #     'USER': os.getenv('USER'),
    #     'PASSWORD': 'qwerty',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'data', 'media')
if not os.path.exists(MEDIA_ROOT):
    try:
        os.makedirs(MEDIA_ROOT)
    except:
        print('Cant create MEDIA_ROOT: ', MEDIA_ROOT)

QUEUES = ['high', 'default', 'low']


REDIS_HOST = 'redis' if os.getenv('IS_DOCKER_CONTAINER') else 'localhost'

RQ_QUEUES = {
    'default': {
        'HOST': REDIS_HOST,
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': REDIS_HOST,
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'HOST': REDIS_HOST,
        'PORT': 6379,
        'DB': 0,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "rq_console": {  # stdout
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "rq_console",
        },
        "rq_console_error": {  #stderr
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "rq_console",
        },
    },
    'loggers': {
        "rq.worker": {
            "handlers": ["rq_console", "rq_console_error"],
            "level": "DEBUG"
        },
    }
}
