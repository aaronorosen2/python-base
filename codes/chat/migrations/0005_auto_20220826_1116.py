# Generated by Django 3.1.4 on 2022-08-26 11:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20220825_0949'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='channelmember',
            unique_together={('Channel', 'org', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('user', 'org')},
        ),
    ]
