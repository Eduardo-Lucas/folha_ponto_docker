from apontamento.models import TipoReceita
from django.contrib.auth.models import User
from django.db import models


class Departamento(models.Model):
    """Departamento Model"""

    id = models.AutoField(primary_key=True)
    nome = models.CharField(
        max_length=100, default="", db_index=True, help_text="Nome do Departamento"
    )

    def __str__(self) -> str:
        return f"{self.nome}"

    class Meta:
        """Departamento Meta Class"""

        ordering = ("nome",)
        db_table = "departamentos"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


class UserProfile(models.Model):
    """User Profile Model"""

    sem_intervalo_almoco_choices = (
        ("Não", "Não"),
        ("Sim", "Sim"),
    )
    bate_ponto_choices = (
        ("Não", "Não"),
        ("Sim", "Sim"),
    )
    almoco_choices = (
        ("TODO DIA", "Todo Dia"),
        ("NÃO ALMOÇA", "Não Almoça"),
        ("EVENTUAL", "Eventual"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    situacaoentidade = models.IntegerField(default=0, help_text="Situação Entidade", null=True, blank=True)
    contato_id = models.IntegerField(default=0, help_text="Informe o Contato", null=True, blank=True)
    bateponto = models.CharField(
        bate_ponto_choices,
        default="Sim",
        max_length=3,
        help_text="Marque se bate ponto.",
        null=True,
        blank=True,
    )
    cargahoraria = models.IntegerField(default=8, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1, null=True, blank=True)
    semintervaloalmoco = models.CharField(
        sem_intervalo_almoco_choices,
        default="Sim",
        max_length=10,
        help_text="Marque se não tiver intervalo para almoço.",
        null=True,
        blank=True,
    )
    nome = models.CharField(
        max_length=100, default="", db_index=True, help_text="Informe seu Nome Completo", null=True, blank=True
    )
    email = models.EmailField(
        max_length=100, default="", db_index=True, help_text="Informe seu E-mail", null=True, blank=True
    )
    tipo_receita = models.ForeignKey(
        TipoReceita,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Escolha o Tipo de Receita mais utilizado.",
        null=True,
        blank=True
    )
    almoco = models.CharField(
        almoco_choices,
        max_length=10,
        default="Não Almoça",
        help_text="Informe rotina do almoço",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        """User Meta Class"""

        ordering = ("user",)
        db_table = "user_profiles"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
