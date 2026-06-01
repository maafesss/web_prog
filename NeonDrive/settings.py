import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
load_dotenv()

# Сначала пробуем читать .env из корня проекта.
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"ℹ️ {env_path} doesn't exist - using environment variables")

# ДЛЯ DOCKER: если запущено в контейнере, используем переменные окружения
# В контейнере DATABASE_URL должна браться из переменных окружения, а не из жесткой привязки
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    # Для локального запуска без Docker (твой существующий вариант)
    DATABASE_URL = 'postgresql://neondriver_user:qTwJEDfdqYL0xW5WkmnSbq6dQSYD9Bh5@dpg-d11ifqodl3ps73cr2bng-a.frankfurt-postgres.render.com/neondriver'
    print(f"Using default DATABASE_URL: {DATABASE_URL}")

# Для Docker-контейнера переопределяем хост с localhost на db (если используется docker-compose)
# Если DATABASE_URL указывает на localhost и мы в Docker - меняем на 'db'
if 'localhost' in DATABASE_URL and os.environ.get('DOCKER_ENV') == 'true':
    DATABASE_URL = DATABASE_URL.replace('localhost', 'db')
    print(f"🔄 Docker environment detected, changed DATABASE_URL to: {DATABASE_URL}")

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

if not DATABASES['default'].get('PORT'):
    DATABASES['default']['PORT'] = '5432'

# Безопасность: секретный ключ из переменных окружения или значение по умолчанию
SECRET_KEY = os.environ.get('SECRET_KEY', '9dn&kx=fnyu5t0xmvcim*g#_t=&=_5!f2v_o*h$8crim+&1tzf')

# Для Docker: DEBUG по умолчанию True, но можно переопределить
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Разрешенные хосты: добавляем host.docker.internal для доступа из контейнера
ALLOWED_HOSTS = [
    'neondriver.onrender.com', 
    'localhost', 
    '127.0.0.1',
    '0.0.0.0',  # Добавляем для Docker
    'host.docker.internal',  # Для доступа из контейнера к хосту
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

INSTALLED_APPS = [
   #'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'channels',
    #R'channels_postgres',
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

# ДЛЯ DOCKER: настройка Redis для Channel Layers
REDIS_URL = os.environ.get('REDIS_URL')
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
    # В Docker используем in-memory слой (для простоты)
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

# ДЛЯ DOCKER: настройки безопасности для локального запуска
CSRF_TRUSTED_ORIGINS = [
    'https://neondriver.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:8000',
]

# В Docker-контейнере при запуске локально - отключаем HTTPS требования
if os.environ.get('DOCKER_ENV') == 'true':
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    print("Docker mode: disabled HTTPS cookie security")
else:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Инициализация приложения
if 'runserver' not in sys.argv and 'collectstatic' not in sys.argv:
    os.environ.setdefault('RUN_INIT', 'true')