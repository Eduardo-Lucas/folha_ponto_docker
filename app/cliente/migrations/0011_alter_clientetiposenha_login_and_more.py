# Generated by Django 4.2.7 on 2024-10-12 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0010_alter_cliente_tributacao_estadual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientetiposenha',
            name='login',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clientetiposenha',
            name='senha',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]