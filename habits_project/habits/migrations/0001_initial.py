# Generated by Django 4.2.4 on 2023-11-06 18:04

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
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('action', models.CharField(max_length=100)),
                ('is_pleasant', models.BooleanField()),
                ('frequency', models.CharField(max_length=20)),
                ('reward', models.CharField(blank=True, max_length=100, null=True)),
                ('time_to_complete', models.IntegerField()),
                ('is_public', models.BooleanField()),
                ('telegram_id', models.CharField(blank=True, max_length=100, null=True)),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
