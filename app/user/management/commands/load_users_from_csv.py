import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('Usuario.csv', type=str)

    def handle(self, *args, **options):
        with open(options['user/fixtures/Usuario.csv'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not User.objects.filter(username=row['username']).exists():
                    User.objects.create_user(
                        username=row['username'],
                        password=row['password'],
                        email=row['e-mail']
                    )
                    print(f'User {row["username"]} has been created.')
                else:
                    print(f'User {row["username"]} already exists.')
