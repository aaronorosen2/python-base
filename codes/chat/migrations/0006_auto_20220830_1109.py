# Generated by Django 3.1.4 on 2022-08-30 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20220826_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='member',
            name='profile_pic',
        ),
    ]