from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set is_staff=True for a specific user"

    def handle(self, *args, **options):
        username = "bruno"
        User.objects.filter(username=username).update(is_staff=True)
        print(f"User {username} is now staff.")
