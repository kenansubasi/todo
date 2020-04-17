from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG is False:
            self.stderr.write(self.style.ERROR("You must enable DEBUG mode to run this command."))
            return

        fixtures = [  # order is important!
            "test_users",
            "test_tasks"
        ]
        for fixture in fixtures:
            self.stdout.write(f"Inserting fixture '{fixture}'...")
            print(f"{settings.FIXTURE_YAML_DIR}/{fixture}")
            call_command('loaddata', f"{settings.FIXTURE_YAML_DIR}/{fixture}", format='yaml')
