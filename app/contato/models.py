from django.db import models


class Contato(models.Model):
    id = models.IntegerField(primary_key=True)
    cpf = models.CharField(null=True, blank=True, verbose_name="CPF")
    nome = models.CharField(max_length=100)
    observation = models.CharField(max_length=100, blank=True, null=True)
    situacaoentidade = models.IntegerField(null=True, blank=True)
    cargo_id = models.IntegerField(null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{str(self.id).zfill(4)}:{self.nome}"

    class Meta:
        ordering = ("nome",)
        db_table = "contatos"
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
