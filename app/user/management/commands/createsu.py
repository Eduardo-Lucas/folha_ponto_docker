from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates superusers.'



    def handle(self, *args, **options):
        users = ['bruno', 'eduardo']
        for user in users:
            if not User.objects.filter(username=user).exists():
                User.objects.create_superuser(
                    username=user,
                    password='ComplexPassword123#',
                    email='eduardolucas40@gmail.com'  # Add the email argument
                )
            print(f'Superuser {user} has been created.')
