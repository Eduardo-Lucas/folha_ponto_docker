# Generated by Django 4.2.7 on 2024-08-05 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Refeicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_refeicao', models.DateField()),
                ('consumo', models.BooleanField(default=False)),
                ('observacao', models.TextField(blank=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Refeição',
                'verbose_name_plural': 'Refeições',
                'db_table': 'refeicao',
                'ordering': ['-data_refeicao'],
                'unique_together': {('usuario', 'data_refeicao')},
            },
        ),
    ]
