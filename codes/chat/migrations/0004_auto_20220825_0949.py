# Generated by Django 3.1.4 on 2022-08-25 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_member_user_profile'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='channel',
            unique_together={('name', 'org')},
        ),
    ]