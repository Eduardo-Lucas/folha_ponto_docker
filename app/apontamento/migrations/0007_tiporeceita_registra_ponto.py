# Generated by Django 4.2.7 on 2024-10-25 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apontamento', '0006_ponto_status_ajuste'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiporeceita',
            name='registra_ponto',
            field=models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Sim', max_length=3),
        ),
    ]
