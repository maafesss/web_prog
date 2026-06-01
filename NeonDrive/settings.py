import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
load_dotenv()

# Читаем .env если есть
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"ℹ️ {env_path} doesn't exist - using environment variables")

# Настройка базы данных
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if not DATABASE_URL:
    print("Using SQLite database (no DATABASE_URL)")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    print(f"Using PostgreSQL: {DATABASE_URL}")
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }

# Безопасность
SECRET_KEY = os.environ.get('SECRET_KEY', '9dn&kx=fnyu5t0xmvcim*g#_t=&=_5!f2v_o*h$8crim+&1tzf')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Разрешенные хосты
ALLOWED_HOSTS = [
    'neondriver.onrender.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'host.docker.internal',
    '.amvera.ru',
    '.amvera.io',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NeonDrive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'main.context_processors.car_request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Channel Layers (Redis или InMemory)
REDIS_URL = os.environ.get('REDIS_URL', '')
USE_REDIS = os.environ.get('USE_REDIS', 'false') == 'true' and REDIS_URL

if USE_REDIS and REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
                "prefix": "neondrive",
            },
        },
    }
    print(f"Using Redis channel layer: {REDIS_URL}")
else:
    print("Using InMemoryChannelLayer (no Redis)")
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

WSGI_APPLICATION = 'NeonDrive.wsgi.application'
ASGI_APPLICATION = 'NeonDrive.asgi.application'

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
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if (BASE_DIR / 'static').exists() else []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CSRF настройки
CSRF_TRUSTED_ORIGINS = [
    'https://neondriver.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:8000',
    'https://amvera.ru',
    'https://amvera.io',
    'http://amvera.ru',
    'http://amvera.io',
]

# Настройки безопасности
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False