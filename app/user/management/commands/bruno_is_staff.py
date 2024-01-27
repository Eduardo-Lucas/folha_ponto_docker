from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set is_staff=True for a specific user"

    def handle(self, *args, **options):
        username = "bruno"
        user = User.objects.filter(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"User {username} is now staff and superuser.")
