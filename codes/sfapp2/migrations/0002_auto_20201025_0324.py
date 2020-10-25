# Generated by Django 2.2.8 on 2020-10-25 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='title2',
            new_name='title',
        ),
        migrations.AddField(
            model_name='service',
            name='url',
            field=models.CharField(blank=True, max_length=4096, null=True, unique=True),
        ),
    ]
