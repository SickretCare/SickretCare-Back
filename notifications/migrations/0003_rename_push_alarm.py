# Generated by Django 5.0.7 on 2024-07-27 09:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Push',
            new_name='Alarm',
        ),
    ]
