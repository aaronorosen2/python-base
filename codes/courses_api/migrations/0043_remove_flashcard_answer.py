# Generated by Django 3.1.4 on 2021-02-26 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_api', '0042_auto_20210226_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='answer',
        ),
    ]
