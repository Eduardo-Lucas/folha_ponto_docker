# Generated by Django 4.2.7 on 2024-05-20 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banco_de_horas', '0002_rename_saldo_horas_bancodehoras_saldo_inicial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bancodehoras',
            name='saldo_inicial',
        ),
    ]
