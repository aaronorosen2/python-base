# Generated by Django 3.1.4 on 2020-12-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0019_usersessionevent_user_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='usersession',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
