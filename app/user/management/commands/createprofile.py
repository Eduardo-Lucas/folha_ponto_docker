"""
Create a user profile for each user record.
"""

import csv

from apontamento.models import TipoReceita
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from user.models import Departamento, UserProfile


class Command(BaseCommand):
    """Create a user profile for each user record."""

    def handle(self, *args, **options):
        # load user profile from csv file
        with open("UserProfile-2024-05-10.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # ...
                departamento = Departamento.objects.get(id=row["departamento"])
                tipo_receita = TipoReceita.objects.get(id=1)  # default = Contábil

                usuario = User.objects.get(id=row["user"])
                if not UserProfile.objects.filter(user_id=usuario).exists():
                    UserProfile.objects.create(
                        id=row["id"],
                        user_id=usuario.id,
                        situacaoentidade=row["situacaoentidade"],
                        contato_id=row["contato_id"],
                        bateponto=row["bateponto"],
                        cargahoraria=row["cargahoraria"],
                        departamento=departamento,
                        semintervaloalmoco=row["semintervaloalmoco"],
                        nome=row["nome"],
                        email=row["email"],
                        tipo_receita=tipo_receita,
                        almoco=row["almoco"],
                    )
            print("User profiles have been successfully uploaded.")
