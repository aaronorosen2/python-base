# Generated by Django 2.2.8 on 2020-11-28 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0002_auto_20201128_1005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='course_name',
            new_name='lesson_name',
        ),
    ]
