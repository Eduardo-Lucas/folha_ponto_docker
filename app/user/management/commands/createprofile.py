from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from user.models import UserProfile


class Command(BaseCommand):
    help = "Create a user profile for each user record"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            # create a user profile for each user
            UserProfile.objects.create(user=user)
        print("User Profiles have been successfully created.")
