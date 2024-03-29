# Generated by Django 4.2.7 on 2024-02-26 09:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ferias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.IntegerField(default=2023, validators=[django.core.validators.MinValueValidator(2020)])),
                ('data_inicial', models.DateField()),
                ('data_final', models.DateField()),
                ('cumpriu', models.BooleanField(default=False)),
                ('cadastrado_em', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ferias', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Férias',
                'verbose_name_plural': 'Férias',
            },
        ),
    ]
