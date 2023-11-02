from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    situacaoentidade = models.IntegerField()
    contato_id = models.IntegerField()
    bateponto = models.BooleanField()
    cargahoraria = models.TimeField(default="00:00:00")
    departamento = models.IntegerField(default=0)
    semintervaloalmoco = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - Bate ponto: {self.bateponto}, carga horária: {self.cargahoraria}"

    class Meta:
        ordering = ("user",)
        db_table = "userprofiles"
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"
