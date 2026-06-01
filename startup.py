import os
import sys
import time
import django
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()

def wait_for_db():
    max_retries = 15
    retry_delay = 3

    print(f"🕒 Ожидание подключения к базе данных...")
    print(f"🔧 Конфигурация БД: {connection.settings_dict}")

    for i in range(max_retries):
        try:
            connection.ensure_connection()
            print("✅ Подключение к базе данных установлено")
            return True
        except OperationalError as e:
            print(f"⚠️ Ошибка подключения к БД (попытка {i + 1}/{max_retries}): {str(e)}")
            time.sleep(retry_delay)
    print("❌ Превышено максимальное количество попыток подключения")
    return False


def run_initialization():
    try:
        print("🚀 Запуск инициализации базы данных...")

        # Создаем миграции для приложения main
        print("🔄 Создание миграций...")
        call_command("makemigrations", "main", interactive=False)

        # Применяем миграции
        print("🔄 Применение миграций...")
        call_command("migrate", interactive=False)

        # Создаем начальные данные
        print("✨ Создание начальных данных...")
        from main.models import Car

        car1, created1 = Car.objects.get_or_create(name="KUZANAGI CT-3X")
        car2, created2 = Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print(f"🚗 Машина 1: {'создана' if created1 else 'уже существует'} - {car1.name}")
        print(f"🚗 Машина 2: {'создана' if created2 else 'уже существует'} - {car2.name}")

        print("🎉 Инициализация базы данных завершена успешно!")
        import os
        if os.environ.get('REDIS_URL'):
            import redis
            try:
                r = redis.Redis.from_url(os.environ['REDIS_URL'], socket_connect_timeout=3)
                r.ping()
                print("✅ Redis connection successful")
            except Exception as e:
                print(f"⚠️ Redis connection failed: {str(e)}")

        return True
    except Exception as e:
        print(f"🔥 Критическая ошибка инициализации: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if wait_for_db():
        if run_initialization():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(2)