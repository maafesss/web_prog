# main/management/commands/auto_migrate.py
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Automatically apply migrations and create initial data'

    def handle(self, *args, **options):
        # Проверяем, существует ли таблица
        table_exists = "main_car" in connection.introspection.table_names()

        if not table_exists:
            self.stdout.write("Applying migrations...")
            from django.core.management import call_command
            call_command('migrate')

            self.stdout.write("Creating initial data...")
            self.create_initial_data()

    def create_initial_data(self):
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")