# Generated by Django 3.1.4 on 2021-02-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vconf', '0008_auto_20210212_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slack_channel',
            field=models.CharField(max_length=500),
        ),
    ]
