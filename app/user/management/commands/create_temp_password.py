# Create a management command file e.g., create_temp_password.py
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand



User = get_user_model()

class Command(BaseCommand):
    """Management command to create temporary passwords for users."""
    help = 'Create temporary passwords for users'

    def handle(self, *args, **options):
        users = User.objects.filter(username='bruno')

        for user in users:
            temp_password = get_random_string(length=10)  # Generate a random temporary password with length 10

            user.set_password(temp_password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Temporary password set for {user.get_username()}: {temp_password}"))
