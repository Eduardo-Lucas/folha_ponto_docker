# Generated by Django 4.2.7 on 2024-08-14 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_tiposenha_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tiposenha',
            options={'ordering': ('descricao',), 'verbose_name': 'Tipo de Senha', 'verbose_name_plural': 'Tipos de Senha'},
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipo_senha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cliente.tiposenha'),
        ),
    ]