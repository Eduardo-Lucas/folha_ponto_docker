# Generated by Django 4.2.3 on 2023-11-11 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
        ('apontamento', '0004_remove_ponto_tiporeceita_id_ponto_tipo_receita'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ponto',
            name='cliente_id',
        ),
        migrations.AddField(
            model_name='ponto',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente'),
        ),
    ]
