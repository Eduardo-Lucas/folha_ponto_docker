import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """Load Users from CSV file."""
    help = "Loads Users from CSV file."

    def handle(self, *args, **options):
        """Load Users from CSV file."""
        with open("User-current.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not User.objects.filter(username=row["username"]).exists():
                    User.objects.create_user(
                        id=row["id"],
                        username=row["username"],
                        password=row["password"],
                    )
            print("Users have been successfully uploaded.")

        user_bruno = User.objects.get(username="bruno")
        # turn user_bruno into superuser and staff
        user_bruno.is_superuser = True
        user_bruno.is_staff = True
        user_bruno.save()
        print("User bruno is now superuser and staff.")
