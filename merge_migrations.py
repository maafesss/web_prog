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
    """Ожидание доступности базы данных."""
    max_retries = 15
    retry_delay = 3

    for i in range(max_retries):
        try:
            connection.ensure_connection()
            print("✅ Database connection established")
            return True
        except OperationalError:
            print(f"⚠️ Database not ready, retrying... ({i + 1}/{max_retries})")
            time.sleep(retry_delay)
    print("❌ Max retries reached. Database still not available.")
    return False

def run_initialization():
    try:
        print("🚀 Starting database initialization...")

        # Всегда применяем миграции
        print("🔄 Applying migrations...")
        call_command("migrate", interactive=False)

        # Создаем начальные данные, если их нет
        print("✨ Creating initial data...")
        from main.models import Car

        # Безопасное создание объектов
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("🎉 Database initialization complete!")
    except Exception as e:
        print(f"🔥 Initialization error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if wait_for_db():
        run_initialization()
    else:
        sys.exit(1)