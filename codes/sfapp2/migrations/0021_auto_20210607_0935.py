# Generated by Django 2.2.8 on 2021-06-07 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfapp2', '0020_auto_20210607_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membergpsentry',
            name='device_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membersession',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
