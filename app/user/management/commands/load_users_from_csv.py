from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "This command is used to load fixtures"

    def handle(self, *args, **kwargs):
        fixtures = [
            "Usuario",
        ]

        try:

            for fixture in fixtures:
                self.stdout.write(self.style.MIGRATE_HEADING(fixture + ": "))
                call_command("loaddata", fixture)
            self.stdout.write(self.style.SUCCESS("Finished loading fixtures"))
        except Exception:
            self.stdout.write(self.style.ERROR("An exception occurred while loading fixtures"))
